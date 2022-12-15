from typing import Literal, Dict, Any
from pydantic import BaseModel

from runner.project import Project


class Input(BaseModel):
    """Описание графических элементов, которые будут передаваться в запущенный контейнер"""
    name: str
    # Описание для пользователя
    description: str
    # Тип параметра, это влияет на отображение элемента в браузере
    type: Literal["text", "number", "list", "code"]
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
    # язык ввода для редактора
    language: str = None

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        _ignored = kwargs.pop('exclude_none') # noqa
        return super().dict(*args, exclude_none=True, **kwargs)


class UI(BaseModel):
    data: list[Input]

    def parse(self, project: Project, user_input: dict):
        """Для созданного проекта передаем полученные при start данные пользователя и передаем их в контейнер"""
        for d in self.data:
            match d.destination:
                case "param":
                    pass
                case "env":
                    pass
                case "file":
                    project.add_file(d.file, user_input[d.name])
            # print(f"{d.name}={user_input[d.name]}")


if __name__ == '__main__':
    i = UI(data=[
        Input(name='optimization', description='level of optimization', type='text'),
        Input(name='var', description='example', type='text'),
        Input(name='code', description='app', type='code', language='python', destination='file', file='app.py'),
    ])

    print(i.dict())
