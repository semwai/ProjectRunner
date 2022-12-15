import time
from .container import Container
from .controller import Controller
from .step import File, Run, Print, Steps, If, Condition


class Project:
    """Проект принимает последовательность команд, которые выполняет согласно сценарию. Данные получаются и
    отправляются на контроллер """
    def __init__(self, controller: Controller, container: Container, program: Steps):
        self.controller = controller
        self.steps = program.steps
        self.container = container
        # переменные проекта хранятся тут - код возврата и различные другие параметры
        self.dict = {'stdout': '', 'stderr': ''}
        self.stop = False  # завершен ли проект
        self._kill = False  # завершен ли проект с внешней стороны (пользователь закрыл вкладку браузера)
        self.queue = []  # очередь команд

    def append(self, data):
        """Добавить данные в переменные ввода"""
        if data[0]:
            self.dict['stdout'] += data[0]
        if data[1]:
            self.dict['stderr'] += data[0]

    def step(self) -> None:
        inst = self.queue.pop(0)
        # print(self.dict)
        match inst:
            case Print(text, file):
                self.controller.write({file: text + '\n'})
                self.dict['ExitCode'] = None
                self.dict['stdout'] = ''
                self.dict['stderr'] = ''
            case File(name, data):
                self.container.add_file(name, data)
                self.dict['ExitCode'] = None
            case Run(command, read, write, ExitCode, echo):
                if echo:
                    self.controller.write({'stdout': command + '\n'})
                c = self.container.command(command)
                while c.status()['Running']:
                    # если проект завершен извне
                    if self._kill:
                        return
                    if write:
                        while (data := c.read()) != (None, None):
                            self.controller.write({'stdout': data[0], 'stderr': data[1]})
                            self.append(data)
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
                        self.append(read)
                if ExitCode:
                    self.dict['ExitCode'] = c.status()['ExitCode']
                else:
                    self.dict['ExitCode'] = None
            case Steps(steps):
                self.queue = [*steps, *self.queue]
                self.dict['ExitCode'] = None
            case If(Condition(variable, c, value), if_branch, else_branch):
                flag = None
                match c:
                    case '!=':
                        flag = self.dict[variable] != value
                    case '==':
                        flag = self.dict[variable] == value
                if flag is None:
                    raise Exception("Condition problem")
                if flag:
                    self.queue = [*if_branch.steps, *self.queue]
                else:
                    self.queue = [*else_branch.steps, *self.queue]

                self.dict['ExitCode'] = None

    def add_file(self, filename: str, data: str):
        self.container.add_file(filename, data)

    def run(self):
        self.queue.extend(self.steps)
        while len(self.queue):
            self.step()
            if self.dict['ExitCode'] is not None:
                self.controller.write({'ExitCode': f"Process finished with exit code {self.dict['ExitCode']}\n"})

    def kill(self):
        """Закончить выполнение проекта если пользователь закрыл выполнение на своей стороне"""
        self._kill = True

    def __del__(self):
        del self.container
