from runner.container import Container
from runner.controller import Controller, ConsoleController
from runner.step import AddFile, RunCommand
import time


class Project:
    """Проект принимает последовательность команд, которые выполняет согласно сценарию. Данные получаются и
    отправляются на контроллер """
    def __init__(self, controller: Controller, container: Container, *steps):
        self.controller = controller
        self.steps = steps
        self.current = 0
        self.container = container
        self.last_status = None  # код возврата из последней запущенной команды

    def step(self):
        if self.current == len(self.steps):
            raise IndexError
        inst = self.steps[self.current]
        match inst:
            case AddFile(name, data):
                self.container.add_file(name, data)
                self.last_status = None
            case RunCommand(command, read, write):
                c = self.container.command(command)
                print(inst, c.status())
                while c.status()['Running']:
                    time.sleep(0.5)
                    if write:
                        self.controller.write(c.read())
                    if read:
                        c.write(self.controller.read())
                if write:
                    time.sleep(0.5)
                    self.controller.write(c.read())
                self.last_status = c.status()['ExitCode']
        self.current += 1

    def __del__(self):
        del self.container


def main():
    text = """
print(123 + 321)
print(input('str:')*10)
        """
    p = Project(
        ConsoleController(),
        Container('python:3.10-alpine'),
        AddFile('app.py', text),  # Вместо text будет описание источника ввода файла
        # RunCommand('python app.py', read=True, write=True),
        RunCommand('ls', read=True, write=True)
    )
    p.step()
    p.step()
    # p.step()
    del p


if __name__ == '__main__':
    main()
