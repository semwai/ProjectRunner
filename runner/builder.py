from runner.container import Container
from runner.controller import Controller
from runner.project import Project
from runner.step import AddFile, RunCommand


def GoProject(controller: Controller, code) -> Project:
    project = Project(
        controller,
        Container('golang:alpine'),
        AddFile('main.go', code),
        RunCommand('echo "Hello user, v0.4.0"', stdin=False, stdout=True, ExitCode=False),
        RunCommand('ls -la', stdin=False, stdout=True, ExitCode=False),
        RunCommand('go build main.go', stdin=False, stdout=True, echo=True),
        RunCommand('ls -la', stdin=False, stdout=True, ExitCode=False),
        RunCommand('./main', stdin=True, stdout=True, echo=True)
    )
    return project


def JavaProject(controller: Controller, code) -> Project:
    project = Project(
        controller,
        Container('openjdk:11'),
        AddFile('Main.java', code),
        RunCommand('echo "Hello user, v0.4.0"', stdin=False, stdout=True, ExitCode=False),
        #  RunCommand('ls -la', stdin=False, stdout=True, ExitCode=False),
        RunCommand('javac Main.java', stdin=False, stdout=True, echo=True),
        #  RunCommand('ls', stdin=False, stdout=True, ExitCode=False),
        RunCommand('java Main', stdin=True, stdout=True, echo=True)
    )
    return project


def Z3Project(controller: Controller, code) -> Project:
    project = Project(
        controller,
        Container('ghcr.io/z3prover/z3:ubuntu-20.04-bare-z3-sha-e3a4425'),
        AddFile('main.z3', code),
        # RunCommand('echo "Hello user, v0.4.0"', stdin=False, stdout=True, ExitCode=False),
        RunCommand('/app/main.z3', stdin=True, stdout=True, echo=False)
    )
    return project
