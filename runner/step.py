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
    # читать из stdout/stderr запущенной команды
    read: bool
    # писать в stdin
    write: bool


@dataclass
class If(Step):
    """Условное выражение, например если нужно проверить код возврата последней команды и в зависимости от этого
    сделать что-нибудь """
    condition: Step
    _if: Step
    _else: Step
