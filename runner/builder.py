from runner.container import Container
from runner.controller import Controller
from runner.project import Project
from runner.step import AddFile, RunCommand


def GoProject(controller: Controller, code) -> Project:
    project = Project(
        controller,
        Container('golang:alpine'),
        AddFile('main.go', code),
        RunCommand('echo "Hello user, v0.2.0"', stdin=False, stdout=True, ExitCode=False),
        RunCommand('ls -la', stdin=False, stdout=True, ExitCode=False),
        RunCommand('go build main.go', stdin=False, stdout=True, echo=True),
        RunCommand('ls -la', stdin=False, stdout=True, ExitCode=False),
        RunCommand('./main', stdin=True, stdout=True, echo=True)
    )
    return project

