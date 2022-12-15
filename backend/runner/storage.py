from typing import Callable

from pydantic import BaseModel  # noqa
import pathlib

from .input import UI, Input
from .builder import *
from .project import Project
from .controller import Controller


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


def ex(name: str) -> str:
    file = pathlib.Path(__file__).parent.resolve() / f"progs/{name}"
    return open(file).read()


emptyUI = UI(data=[])

goUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.go', language='go', default=ex('main.go')), # noqa
    Input(name='param', description='example description', destination='env', type='text', env='param', default='123321'), # noqa
])

javaUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='Main.java', language='java', default=ex('Main.java')), # noqa
])

z3UI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.z3', language='z3', default=ex('main.z3')), # noqa
])

pythonUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.py', language='python', default=ex('main.py')), # noqa
])

nusmvUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.smv', language='nusmv', default=ex('main.smv')), # noqa
])


projects = ProjectsStorage(
    data=[
        ProjectStorage(id=1, name="Go", description="Golang language compiler", lang="go", ui=goUI, builder=GoProject), # noqa
        ProjectStorage(id=2, name="Java", description="Java language compiler", lang="java", ui=javaUI, builder=JavaProject), # noqa
        ProjectStorage(id=3, name="Z3", description="Z3 language", lang="Z3", ui=z3UI, builder=Z3Project), # noqa
        ProjectStorage(id=4, name="Python", description="Python 3.10", lang="python", ui=pythonUI, builder=PythonProject), # noqa
        ProjectStorage(id=5, name="nusmv", description="nusmv", lang="nusmv", ui=nusmvUI, builder=NuSMVproject) # noqa
    ]
)


def projectById(project_id: int) -> ProjectStorage:
    return [p for p in projects.data if p.id == project_id][0]
