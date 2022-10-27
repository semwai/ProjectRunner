from abc import ABC, abstractmethod
from runner.container import Container


class Controller(ABC):
    """У контроллера проект получает файлы и данные для ввода. Контроллеру проект отдает данные и коды состояний"""
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, data):
        pass


class ConsoleController(Controller):
    """Чтение и запись из консоли"""
    def read(self):
        return input() + '\n'

    def write(self, data):
        stdout, stderr = data
        if stdout:
            print(stdout, end='')
        if stderr:
            print(stderr, end='')


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
