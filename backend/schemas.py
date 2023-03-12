from typing import Literal

from pydantic import BaseModel  # noqa

from backend.storage.models import UI, Steps, Content


class GetPages(BaseModel):
    """Получить множество проектов"""
    class GetShortPages(BaseModel):
        """При получении множества проектов каждый проект будет представлен в кратком формате"""
        id: int
        name: str = ""
        description: str = ""
        short_description: str = ""
        version: str = ""
        visible: bool = False

    data: list[GetShortPages]


class GetPage(BaseModel):
    """Получить один проект с подробным описанием"""
    id: int
    name: str = ""
    description: str = ""
    short_description: str = ""
    version: str = ""
    visible: bool = False
    ui: UI
    scenario: Steps


class User(BaseModel):
    email: str
    name: str
    access: Literal["user", "admin"]


class GetProject(BaseModel):
    id: int
    name: str = ""
    description: str = ""
    content: Content
