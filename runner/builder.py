from runner.container import Container
from runner.controller import Controller
from runner.project import Project
from runner.step import Run, Print, Steps


def GoProject(controller: Controller) -> Project:
    project = Project(
        controller,
        Container('golang:alpine'),
        program=Steps([
            Print("Hello user, v0.5.0"),
            Run('ls -la', stdin=False, stdout=True, ExitCode=False),
            Run('go build main.go', stdin=False, stdout=True, echo=True),
            Run('ls -la', stdin=False, stdout=True, ExitCode=False),
            Run('./main', stdin=True, stdout=True, echo=True)
        ])
    )
    return project


def JavaProject(controller: Controller) -> Project:
    project = Project(
        controller,
        Container('openjdk:11'),
        program=Steps([
            Print("Hello user, v0.5.0"),
            Run('javac Main.java', stdin=False, stdout=True, echo=True),
            Steps([
                Print("1"),
                Print("2"),
                Print("3"),
            ]),
            Run('java Main', stdin=True, stdout=True, echo=True)
        ])
    )
    return project


def Z3Project(controller: Controller) -> Project:
    project = Project(
        controller,
        Container('ghcr.io/z3prover/z3:ubuntu-20.04-bare-z3-sha-e3a4425'),
        program=Steps([
            Print("Hello user, v0.5.0", file='stderr'),
            Run('/app/main.z3', stdin=True, stdout=True, echo=False)
        ])
    )
    return project


def PythonProject(controller: Controller) -> Project:
    project = Project(
        controller,
        Container('python:3.10-alpine'),
        program=Steps([
            Print("Hello user, v0.5.0", file='stderr'),
            Run('python main.py', stdin=True, stdout=True, echo=False)
        ])
    )
    return project


def NuSMVproject(controller: Controller) -> Project:
    project = Project(
        controller,
        Container('semwai/nusmv:2.6.0'),
        program=Steps([
            Print("Hello user, v0.5.0", file='stderr'),
            Run('nusmv /app/main.smv', stdin=True, stdout=True, echo=False)
        ])
    )
    return project
