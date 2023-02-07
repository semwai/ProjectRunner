from typing import Literal

from pydantic import BaseModel  # noqa

from backend.storage.models import UI


class GetProjects(BaseModel):
    """Получить множество проектов"""
    class GetProjectsProject(BaseModel):
        """При получении множества проектов каждый проект будет представлен в кратком формате"""
        id: str
        name: str = ""
        description: str = ""
        short_description: str = ""
        version: str = ""
        visible: bool = False

    data: list[GetProjectsProject]


class GetProject(BaseModel):
    """Получить один проект с подробным описанием"""
    id: str
    name: str
    description: str
    short_description: str
    version: str
    visible: bool
    ui: UI


class User(BaseModel):
    email: str
    name: str
    access: Literal["user", "admin"]
