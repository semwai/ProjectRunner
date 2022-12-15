from typing import Callable
from pydantic import BaseModel # noqa

from runner.input import UI
from runner.project import Project
from runner.controller import Controller


class ProjectStorage(BaseModel):
    """Модель описания проекта"""
    id: int
    name: str
    description: str
    lang: str
    ui: UI
    builder: Callable[[Controller], Project]


class ProjectsStorage(BaseModel):
    data: list[ProjectStorage]
