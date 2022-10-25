
class Step:

    def __init__(self, command: str):
        self.command = command


class Project:

    def __init__(self, steps: Step, image):
        self.steps = steps

