import time
from runner.container import Container
from runner.controller import Controller
from runner.step import AddFile, RunCommand


class Project:
    """Проект принимает последовательность команд, которые выполняет согласно сценарию. Данные получаются и
    отправляются на контроллер """
    def __init__(self, controller: Controller, container: Container, *steps):
        self.controller = controller
        self.steps = steps
        self.current = 0
        self.container = container
        self.last_ExitCode = None  # код возврата из последней запущенной команды
        self.stop = False  # завершен ли проект
        self._kill = False  # завершен ли проект с внешней стороны (пользователь закрыл вкладку браузера)

    def step(self):
        if self.current == len(self.steps):
            self.stop = True
            self.current += 1
            return
        if self.last_ExitCode is not None and self.last_ExitCode != 0:
            self.stop = True
            return
        inst = self.steps[self.current]
        match inst:
            case AddFile(name, data):
                self.container.add_file(name, data)
                self.last_ExitCode = None
            case RunCommand(command, read, write, ExitCode, echo):
                if echo:
                    self.controller.write({'stdout': command + '\n'})
                c = self.container.command(command)
                while c.status()['Running']:
                    if self._kill:
                        return
                    if write:
                        data = c.read()
                        if data != (None, None):
                            self.controller.write({'stdout': data[0], 'stderr': data[1]})
                    if read and c.status()['Running']:
                        data = self.controller.read()
                        if data is not None:
                            c.write(data)
                    # небольшая задержка чтобы проект не спрашивал постоянно у контейнера и пользователя данные
                    time.sleep(0.5)
                # чтение оставшихся данных
                if write:
                    while True:
                        read = c.read()
                        if read == ('', ''):
                            break
                        self.controller.write({'stdout': read[0], 'stderr': read[1]})
                if ExitCode:
                    self.last_ExitCode = c.status()['ExitCode']
                else:
                    self.last_ExitCode = None
        self.current += 1

    def run(self):
        while self.current < len(self.steps) and not self._kill:
            self.step()
            if self.last_ExitCode is not None:
                self.controller.write({'ExitCode': f"Process finished with exit code {self.last_ExitCode}\n"})
                if self.last_ExitCode != 0:
                    break

    def kill(self):
        """Закончить выполнение проекта если пользователь закрыл выполнение на своей стороне"""
        self._kill = True

    def __del__(self):
        del self.container
