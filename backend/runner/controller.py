from abc import ABC, abstractmethod
from typing import Literal
from .container import Container
from threading import Thread, Lock
from queue import Queue
import select
import sys

from .utils import colored


class Controller(ABC):
    """У контроллера проект получает файлы и данные для ввода. Контроллеру проект отдает данные и коды состояний"""
    @abstractmethod
    def read(self) -> str | None:
        pass

    @abstractmethod
    def write(self, data: dict[Literal["stdout", "stderr", "ExitCode"]]):
        pass


class ConsoleController(Controller):
    """Чтение и запись из консоли"""
    def read(self) -> str | None:
        return input() + '\n'

    def write(self, data: dict[Literal["stdout", "stderr", "ExitCode"]]):
        if (stdout := data.get('stdout')) is not None:
            print(stdout, end='')
        if (stderr := data.get('stderr')) is not None:
            print(stderr, end='')
        if (ExitCode := data.get('ExitCode')) is not None:
            print(ExitCode, end='')


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
            return data

    def write(self, data: dict[Literal["stdout", "stderr", "ExitCode"]]):
        if (stdout := data.get('stdout')) is not None:
            print(stdout, end='')
        if (stderr := data.get('stderr')) is not None:
            print(colored(stderr, "FAIL"), end='')
        if (ExitCode := data.get('ExitCode')) is not None:
            print(colored(ExitCode, "OKBLUE"), end='')

    @staticmethod
    def input_with_timeout(timeout) -> str | None:
        """Чтение в течении timeout секунд, иначе возвращает None
        https://stackoverflow.com/a/15533404/17676574
        """
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if ready:
            return sys.stdin.readline().rstrip('\n')  # expect stdin to be line-buffered
        else:
            return None

    def _console_reader(self):
        while True:
            # чтение из консоли пока объект существует
            with self._lock:
                if self._stop:
                    break
            # если использовать обычный input, то в случае закрытия приложения останется незавершенным поток,
            # ждущий input()
            data = self.input_with_timeout(1)
            if data is not None:
                self.q.put(data + '\n')

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


class ThreadController(Controller):
    """Контроллер для работы между потоками"""
    def __init__(self):
        self._stop: bool = False
        self._lock: Lock = Lock()
        self.container_queue = Queue()
        self.user_queue = Queue()

    def read_websocket(self, data: str):
        self.container_queue.put(data + '\n')

    def read(self) -> str | None:
        if self.container_queue.qsize() == 0:
            return None
        else:
            data = self.container_queue.get_nowait()
            return data

    def write(self, data: dict[Literal["stdout", "stderr", "ExitCode"]]):
        self.user_queue.put(data)

    def write_websocket(self):
        if self.user_queue.qsize() > 0:
            return self.user_queue.get_nowait()
        else:
            return None


# old, (web_container)
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
