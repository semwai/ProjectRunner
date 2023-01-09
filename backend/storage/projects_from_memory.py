from pydantic import BaseModel  # noqa
import pathlib

from backend.models import ProjectsStorage, ProjectStorage
from backend.runner.step import Steps, Print, Run
from backend.runner.input import UI, Input


def ex(name: str) -> str:
    file = pathlib.Path(__file__).parent.resolve() / f"progs/{name}"
    return open(file).read()


goScenario = Steps([
    Run('ls -la', stdin=False, stdout=True, ExitCode=False),
    Run('go build main.go', stdin=False, stdout=True, echo=True),
    Run('ls -la', stdin=False, stdout=True, ExitCode=False),
    Run('./main', stdin=True, stdout=True, echo=True)])


javaScenario = Steps([
    Run('javac Main.java', stdin=False, stdout=True, echo=True),
    Steps([
        Print("1"),
        Print("2"),
        Print("3"),
    ]),
    Run('java Main', stdin=True, stdout=True, echo=True)])

Z3Scenario = Steps([Run('/app/main.z3', stdin=True, stdout=True, echo=False)])

pythonScenario = Steps(
    [Run('python main.py', stdin=True, stdout=True, echo=False)])


nusmvScenario = Steps(
    [Run('nusmv /app/main.smv', stdin=True, stdout=True, echo=False)])


emptyUI = UI(data=[])

goUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.go', language='go', default=ex('main.go')),  # noqa
    Input(name='param', description='example description', destination='env', type='text', env='param', default='123321'),  # noqa
])

javaUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='Main.java', language='java', default=ex('Main.java')),  # noqa
])

z3UI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.z3', language='z3', default=ex('main.z3')),  # noqa
])

pythonUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.py', language='python', default=ex('main.py')),  # noqa
    Input(name='data', description='input file', destination='file', type='textarea', file='data.txt', language='txt', default="hello world\n!!!"),  # noqa
    Input(name='list', description='example list element', destination='file', type='list', file='list.txt',
          values=[{'title': 'One', 'value': '1'}, {'title': 'Two', 'value': '2'}, {'title': 'Three', 'value': '3'}], default='1'),  # noqa
])

nusmvUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.smv', language='nusmv', default=ex('main.smv')),  # noqa
])


projects = ProjectsStorage(
    data=[
        ProjectStorage(id=1, name="Go", description="Golang language compiler", lang="go", container="golang:alpine", ui=goUI, steps=goScenario),  # noqa
        ProjectStorage(id=2, name="Java", description="Java language compiler", lang="java", container="openjdk:11", ui=javaUI, steps=javaScenario),  # noqa
        ProjectStorage(id=3, name="Z3", description="Z3 language", lang="Z3", container="ghcr.io/z3prover/z3:ubuntu-20.04-bare-z3-sha-e3a4425", ui=z3UI, steps=Z3Scenario),  # noqa
        ProjectStorage(id=4, name="Python", description="Python 3.10", lang="python", container="python:3.10-alpine", ui=pythonUI, steps=pythonScenario),  # noqa
        ProjectStorage(id=5, name="nusmv", description="nusmv", lang="nusmv", container="semwai/nusmv:2.6.0", ui=nusmvUI, steps=nusmvScenario)  # noqa
    ]
)


def projectById(project_id: int) -> ProjectStorage:
    return [p for p in projects.data if p.id == project_id][0]
