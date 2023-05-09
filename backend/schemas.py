from typing import Literal

from pydantic import BaseModel, Field  # noqa

from backend.storage.models import UI, Steps, Content


class GetPage(BaseModel):
    """Получить один проект с подробным описанием"""
    id: int
    name: str = Field(min_length=1)
    description: str = ""
    short_description: str = Field(min_length=1)
    version: str = ""
    visible: bool = False
    container: str = Field(min_length=1)
    ui: UI
    scenario: Steps


class GetPages(BaseModel):
    """Получить множество страниц"""
    data: list[GetPage]


class User(BaseModel):
    email: str
    name: str
    access: Literal["user", "admin"]


class GetProject(BaseModel):
    id: int
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    public: bool
    content: Content


class GetFullProject(BaseModel):
    id: int
    name: str = ""
    description: str = ""
    public: bool
    content: Content
    pages: list[GetPage]
