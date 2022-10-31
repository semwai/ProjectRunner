from abc import ABC, abstractmethod
from runner.container import Container
from threading import Thread, Lock
from queue import Queue


class Controller(ABC):
    """У контроллера проект получает файлы и данные для ввода. Контроллеру проект отдает данные и коды состояний"""
    @abstractmethod
    def read(self) -> str | None:
        pass

    @abstractmethod
    def write(self, data):
        pass


class ConsoleController(Controller):
    """Чтение и запись из консоли"""
    def read(self) -> str | None:
        return input() + '\n'

    def write(self, data):
        stdout, stderr = data
        if stdout:
            print(stdout, end='')
        if stderr:
            print(stderr, end='')


class ThreadConsoleController(Controller):
    """Контроллер с конкурентным чтением и записью в контроллер"""
    def __init__(self):
        self.q: Queue | None = None  # queue
        self.reader: Thread | None = None  # поток чтения из консоли
        self._stop: bool = False
        self._lock: Lock = Lock()

    def read(self) -> str | None:
        if self.q is None:
            raise RuntimeError("Run the controller first")
        if self.q.qsize() == 0:
            return None
        else:
            data = self.q.get_nowait()
            # print(f"get from queue {data}")
            return data

    def write(self, data):
        stdout, stderr = data
        if stdout:
            print(stdout, end='')
        if stderr:
            print(stderr, end='')

    def _console_reader(self):
        while True:
            # чтение из консоли пока объект существует
            with self._lock:
                if self._stop:
                    break
            data = input() + '\n'
            # print(f":{data}")
            self.q.put(data)

    def run(self) -> None:
        self.q = Queue()
        # запуск потока бесконечного чтения пользовательского ввода в консоль
        self.reader = Thread(target=self._console_reader, daemon=False)
        self.reader.start()

    def stop(self):
        with self._lock:
            self._stop = True

    def __del__(self):
        with self._lock:
            self._stop = True


# old, remove
class ProjectController:
    """Контроллер запущенного проекта"""
    def __init__(self, code, container: Container):
        self.container = container
        self.container.add_file('app.go', code)  # must be step
        self.container.add_file('test.txt', '1234')
        self.exec = self.container.command('go run app.go')

    def write(self, data):
        if self.exec.status()['Running']:
            return self.exec.write(data + "\n")
        else:
            return self.exec.status()['ExitCode']

    def read(self):
        try:
            return self.exec.read()
        except TimeoutError:
            return None

    def status(self):
        return self.exec.status()

    def __del__(self):
        # Внимательно следим за удалением контейнера, поскольку GC сам удаляет объекты не сразу
        # и они остаются пока не накопится достаточное количество кандидатов на удаление
        del self.container
