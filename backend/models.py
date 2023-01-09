from pydantic import BaseModel # noqa

from backend.runner.step import Steps
from runner.input import UI


class ProjectStorage(BaseModel):
    """Модель описания проекта"""
    id: int
    name: str
    short_description: str = ""
    description: str = ""
    lang: str
    container: str  # имя docker образа
    ui: UI
    steps: Steps


class ProjectsStorage(BaseModel):
    data: list[ProjectStorage]
