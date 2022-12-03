from dataclasses import dataclass, field
import dataclasses
from typing import Literal


@dataclass
class Params:

    name: str
    # Описание для пользователя
    description: str
    # Тип параметра, это влияет на отображение элемента в браузере
    type: Literal["text", "number", "list"]
    # Возможные значения для type=list
    values: list[str] | None = None
    # Значение по умолчанию
    default: str = None
    # Куда направлять параметр, можно создать таким образом окно ввода текста в дополнительный файл
    destination: Literal["param", "env", "file"] = "param"
    # если destination=file, то нужно передать название файла
    file: str = None
    # если destination=env, то нужно передать значение имени
    env: str = None

    def dict(self) -> dict:
        return {key: value for key, value in dataclasses.asdict(self).items() if value is not None}


@dataclass
class Input:
    data: list[Params] = field(default_factory=list)
