import time
from runner.container import Container
from runner.controller import Controller
from runner.step import AddFile, RunCommand, Print, Steps


class Project:
    """Проект принимает последовательность команд, которые выполняет согласно сценарию. Данные получаются и
    отправляются на контроллер """
    def __init__(self, controller: Controller, container: Container, program: Steps):
        self.controller = controller
        self.steps = program.steps
        self.container = container
        self.last_ExitCode = None  # код возврата из последней запущенной команды
        self.stop = False  # завершен ли проект
        self._kill = False  # завершен ли проект с внешней стороны (пользователь закрыл вкладку браузера)
        self.queue = []  # очередь команд

    def step(self) -> None:
        inst = self.queue.pop(0)
        self.last_ExitCode = None
        match inst:
            case Print(text, file):
                self.controller.write({file: text})
            case AddFile(name, data):
                self.container.add_file(name, data)
            case RunCommand(command, read, write, ExitCode, echo):
                if echo:
                    self.controller.write({'stdout': command + '\n'})
                c = self.container.command(command)
                while c.status()['Running']:
                    if self._kill:
                        return
                    if write:
                        while (data := c.read()) != (None, None):
                            self.controller.write({'stdout': data[0], 'stderr': data[1]})
                    if read and c.status()['Running']:
                        data = self.controller.read()
                        if data is not None:
                            c.write(data)
                    # небольшая задержка чтобы проект не спрашивал постоянно у контейнера и пользователя данные
                    time.sleep(0.25)
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
            case Steps(steps):
                self.queue = [*steps, *self.queue]

    def run(self):
        self.queue.extend(self.steps)
        while len(self.queue):
            print(self.queue)
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
