from runner.container import Container, Command


class Step:

    def __init__(self, command: Command):
        self.command = command


class Project:

    def __init__(self, steps: Step, container: Container):
        self.steps = steps

