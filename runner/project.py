from runner.container import Container
from abc import ABC
from dataclasses import dataclass


@dataclass
class Step(ABC):
    """Абстрактная команда"""
    pass


@dataclass
class AddFile(Step):
    """Добавление файла"""
    name: str
    data: str | bytes


@dataclass
class RunCommand(Step):
    """Запуск консольной команды внутри контейнера"""
    command: str
    # читать из stdout/stderr
    read: bool
    # писать в stdin
    write: bool


class Project:
    """Проект руководит командами и обеспечивает их правильное выполнение"""
    def __init__(self, container: Container, *steps):
        self.steps = steps
        self.container = container


if __name__ == '__main__':
    text = """
    print(123 + 321)
    """
    p = Project(
        Container('python:3.10-alpine'),
        AddFile('app.py', text),
        RunCommand('python app.py', read=True, write=True)
    )
