from pydantic import BaseModel  # noqa

from backend.storage.models import UI


class GetProjects(BaseModel):
    """Получить множество проектов"""
    class GetProjectsProject(BaseModel):
        """При получении множества проектов каждый проект будет представлен в кратком формате"""
        id: str
        name: str
        description: str

    data: list[GetProjectsProject]


class GetProject(BaseModel):
    """Получить один проект с подробным описанием"""
    id: str
    name: str
    description: str
    lang: str
    ui: UI
    scenario: dict


class User(BaseModel):
    email: str
