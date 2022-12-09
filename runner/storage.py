from pydantic import BaseModel  # noqa
import pathlib

from runner.input import UI, Input


class Project(BaseModel):
    """Модель описания проекта"""
    id: int
    name: str
    description: str
    lang: str
    ui: UI


class Projects(BaseModel):
    data: list[Project]


def ex(name: str) -> str:
    file = pathlib.Path(__file__).parent.resolve() / f"example/progs/{name}"
    return open(file).read()


emptyUI = UI(data=[])

goUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.go', language='go', default=ex('main.go')),
    Input(name='param', description='example description', destination='env', type='text', env='param', default='123321'),
])

javaUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='Main.java', language='java', default=ex('Main.java')),
])

z3UI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.z3', language='z3', default=ex('main.z3')),
])

pythonUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.py', language='python', default=ex('main.py')),
])

projects = Projects(
    data=[
        Project(id=1, name="Go", description="Golang language compiler", lang="go", ui=goUI),
        Project(id=2, name="Java", description="Java language compiler", lang="java", ui=javaUI),
        Project(id=3, name="Z3", description="Z3 language", lang="Z3", ui=z3UI),
        Project(id=4, name="Python", description="Python 3.10", lang="python", ui=pythonUI),
        Project(id=5, name="nusmv", description="nusmv", lang="nusmv", ui=emptyUI)
    ]
)
