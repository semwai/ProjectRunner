from abc import ABC
from dataclasses import dataclass
from typing import Literal


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
class Print(Step):
    """Напечатать сообщение в консоль"""
    text: str
    file: Literal["stdout", "stderr"] = "stdout"


@dataclass
class RunCommand(Step):
    """Запуск консольной команды внутри контейнера"""
    command: str
    # Команде нужен ввод?
    stdin: bool
    # Команда выдает в консоль
    stdout: bool
    # Записывать код возврата
    ExitCode: bool = True
    # Дублировать команду пользователю для наглядности в stdout
    echo: bool = False


@dataclass
class Steps(Step):
    """Множество последовательно выполняемых команд"""
    steps: list[Step]


@dataclass
class If(Step):
    """Условное выражение, например если нужно проверить код возврата последней команды и в зависимости от этого
    сделать что-нибудь """
    condition: Step
    _if: Steps
    _else: Steps
