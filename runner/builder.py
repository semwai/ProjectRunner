from runner.container import Container
from runner.controller import Controller
from runner.project import Project
from runner.step import AddFile, RunCommand, Print, Steps


def GoProject(controller: Controller, code) -> Project:
    project = Project(
        controller,
        Container('golang:alpine'),
        program=Steps([
            Print("Hello user, v0.4.1"),
            AddFile('main.go', code),
            RunCommand('ls -la', stdin=False, stdout=True, ExitCode=False),
            RunCommand('go build main.go', stdin=False, stdout=True, echo=True),
            RunCommand('ls -la', stdin=False, stdout=True, ExitCode=False),
            RunCommand('./main', stdin=True, stdout=True, echo=True)
        ])
    )
    return project


def JavaProject(controller: Controller, code) -> Project:
    project = Project(
        controller,
        Container('openjdk:11'),
        program=Steps([
            Print("Hello user, v0.4.1"),
            AddFile('Main.java', code),
            RunCommand('javac Main.java', stdin=False, stdout=True, echo=True),
            Steps([
                Print("1"),
                Print("2"),
                Print("3"),
            ]),
            RunCommand('java Main', stdin=True, stdout=True, echo=True)
        ])
    )
    return project


def Z3Project(controller: Controller, code) -> Project:
    project = Project(
        controller,
        Container('ghcr.io/z3prover/z3:ubuntu-20.04-bare-z3-sha-e3a4425'),
        program=Steps([
            Print("Hello user, v0.4.1", file='stderr'),
            AddFile('main.z3', code),
            RunCommand('/app/main.z3', stdin=True, stdout=True, echo=False)
        ])
    )
    return project


def PythonProject(controller: Controller, code) -> Project:
    project = Project(
        controller,
        Container('python:3.10-alpine'),
        program=Steps([
            Print("Hello user, v0.4.1", file='stderr'),
            AddFile('main.py', code),
            RunCommand('python main.py', stdin=True, stdout=True, echo=False)
        ])
    )
    return project
