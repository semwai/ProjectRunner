from runner.container import Container


class ProjectController:
    """Контроллер запущенной команды"""
    def __init__(self, text):
        self.runner = Container()
        self.runner.add_file('app.go', text)
        self.runner.add_file('test.txt', '1234')
        self.exec = self.runner.command('go run app.go')
        # print(self.exec.status())

    def write(self, data):
        if self.exec.status()['Running']:
            return self.exec.write(data + "\n")
        else:
            return self.exec.status()['ExitCode']

    def read(self):
        try:
            return self.exec.read()
        except TimeoutError:
            return None

    def status(self):
        return self.exec.status()