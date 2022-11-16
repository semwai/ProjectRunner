from pydantic import BaseModel  # noqa


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
    example: str