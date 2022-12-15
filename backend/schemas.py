from pydantic import BaseModel  # noqa

from runner.input import UI


class GetProjects(BaseModel):
    class Inner(BaseModel):
        id: str
        name: str
        description: str

    data: list[Inner]


class GetProject(BaseModel):
    id: str
    name: str
    description: str
    lang: str
    ui: UI
