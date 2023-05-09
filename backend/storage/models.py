from typing import Dict, Any, Literal, TypeVar

from sqlalchemy import Column, String, JSON, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from pydantic import BaseModel, root_validator, validator  # noqa

from backend.storage.db import engine


class Base(DeclarativeBase):
    pass


class ListValue(BaseModel):
    title: str
    value: str


class Input(BaseModel):

    name: str
    description: str
    type: Literal["text", "number", "list", "code", "textarea", "file"]
    values: list[ListValue] = []
    default: str = ""
    destination: Literal["param", "env", "file"]
    file: str = ""
    env: str = ""
    language: str = ""

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        _ignored = kwargs.pop('exclude_none') # noqa
        return super().dict(*args, exclude_none=True, **kwargs)


class UI(BaseModel):

    data: list[Input]

    def parse(self, project, user_input: dict):
        """Для созданного проекта передаем полученные при start данные пользователя и передаем их в контейнер"""
        for d in self.data:
            match d.destination:
                case "param":
                    pass
                case "env":
                    project.add_environment(d.env, user_input[d.name])
                case "file":
                    project.add_file(d.file, user_input[d.name])


class Step(BaseModel):
    """Абстрактная команда"""
    type: str

    @root_validator(pre=True)
    def set_creature_type(cls, values):
        # таким образом получаем имя класса при преобразовании в json, что удобно для фронта
        values['type'] = cls.__name__
        return values


class File(Step):
    """Добавление файла"""

    name: str
    data: str


class Print(Step):
    """Печать в консоль"""

    text: str
    file: Literal["stdout", "stderr"] = "stdout"


class Run(Step):
    """Запуск консольной команды внутри контейнера"""

    command: str
    # Команде нужен ввод?
    stdin: bool
    # Команда выдает в консоль
    stdout: bool
    # Записывать код возврата
    exitCode: bool = True
    # Дублировать команду пользователю для наглядности в stdout
    echo: bool = False


class Condition(BaseModel):
    """Условие для ветвлений"""

    variable: str  # имя переменной
    c: Literal["==", ">", "<", ">=", "<=", "!="]
    value: str


class If(Step):
    """Условное выражение, например если нужно проверить код возврата последней команды и в зависимости от этого
    сделать что-нибудь """
    condition: Condition
    if_branch: Step
    else_branch: Step


Self = TypeVar("Self", bound="Steps")


class Steps(Step):
    """Множество последовательно выполняемых команд"""
    data: list[File | Run | Print | If | Self]


class Page(Base):
    """Модель описания проекта"""
    __tablename__ = "page"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: str = Column(String, default="")
    short_description: str = Column(String, unique=True)
    description: str = Column(String, default="")
    version: str = Column(String, default="1")
    container: Mapped[str]  # имя docker образа
    visible: bool = Column(Boolean, default=False)  # Виден ли проект для обычных пользователей
    _ui = Column("ui", JSON)
    _scenario = Column("scenario", JSON)

    @property
    def ui(self):
        return UI(**self._ui)

    @property
    def scenario(self):
        return Steps(**self._scenario)

    @ui.setter
    def ui(self, ui: UI):
        self._ui = ui.dict()

    @scenario.setter
    def scenario(self, scenario: Steps):
        self._scenario = scenario.dict()

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_description': self.short_description,
            'description': self.description,
            'version': self.version,
            'container': self.container,
            'visible': self.visible,
            'ui': self._ui,
            'scenario': self.scenario.dict()
        }


class User(Base):
    """Модель описания пользователя"""
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: str = Column(String, default="")
    email: str = Column(String, default="")
    access: Literal["user", "admin"] = Column(Enum("user", "admin", name='Access'), default="user")


class Entry(BaseModel):
    id: int
    short_description: str


_Content = TypeVar("_Content", bound="Content")


class Content(BaseModel):
    """Дерево оглавления"""

    description: str = ""  # название главы
    data: list[Entry | _Content]

    def Ids(self) -> set[int]:
        """Все ID страниц"""
        out = set()
        for d in self.data:
            if type(d) == Entry:
                out.add(d.id)
            if type(d) == Content:
                out.union(d.Ids())
        return out


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: str = Column(String, default="")
    description: str = Column(String, default="")
    public: bool = Column(Boolean, default=False)
    _content = Column("content", JSON)

    @property
    def content(self):
        return Content(**self._content)

    @content.setter
    def content(self, content: Content):
        self._content = content.dict()

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'public': self.public,
            'content': self.content.dict()
        }


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
