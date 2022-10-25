from runner.container import Container
from runner.controller import Controller
from runner.step import AddFile, RunCommand


class Project:
    """Проект принимает последовательность команд, которые выполняет согласно сценарию. Данные получаются и
    отправляются на контроллер """
    def __init__(self, controller: Controller, container: Container, *steps):
        self.controller = controller
        self.steps = steps
        self.container = container


if __name__ == '__main__':
    text = """
    print(123 + 321)
    """
    p = Project(
        Controller(),
        Container('python:3.10-alpine'),
        AddFile('app.py', text),  # Вместо text будет описание источника ввода файла
        RunCommand('python app.py', read=True, write=True)
    )
