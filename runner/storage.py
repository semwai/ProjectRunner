from pydantic import BaseModel  # noqa
import pathlib

from runner.input import UI, Input


class Project(BaseModel):
    """Web модель описания проекта"""
    id: int
    name: str
    description: str
    lang: str
    example: str
    ui: UI


class Projects(BaseModel):
    data: list[Project]


def ex(name: str) -> str:
    file = pathlib.Path(__file__).parent.resolve() / f"example/progs/{name}"
    return open(file).read()


emptyUI = UI(data=[])

goUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.go', language='go')
])

projects = Projects(
    data=[
        Project(id=1, name="Go", description="Golang language compiler", lang="go", example=ex('main.go'), ui=goUI),
        Project(id=2, name="Java", description="Java language compiler", lang="java", example=ex('Main.java'), ui=emptyUI),
        Project(id=3, name="Z3", description="Z3 language", lang="Z3", example=ex('main.z3'), ui=emptyUI),
        Project(id=4, name="Python", description="Python 3.10", lang="python", example=ex('main.smv'), ui=emptyUI),
        Project(id=5, name="nusmv", description="nusmv", lang="nusmv", example=ex('main.smv'), ui=emptyUI)
    ]
)
