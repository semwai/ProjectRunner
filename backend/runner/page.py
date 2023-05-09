import time
from .container import Container
from .controller import Controller
from backend.storage.models import File, Run, Print, Steps, If


class Page:
    """Проект принимает последовательность команд, которые выполняет согласно сценарию. Данные получаются и
    отправляются на контроллер """
    def __init__(self, controller: Controller, container: Container, program: Steps):
        self.controller = controller
        self.steps = program
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
            case Print():
                text, file = inst.text, inst.file
                self.controller.write({file: text + '\n'})
                self.dict['exitCode'] = None
                self.dict['stdout'] = ''
                self.dict['stderr'] = ''
            case File():
                name, data = inst.name, inst.data
                self.container.add_file(name, data)
                self.dict['exitCode'] = None
            case Run():
                raw_command, stdin, stdout, exitCode, echo = inst.command, inst.stdin, inst.stdout, inst.exitCode, inst.echo
                format_command = self.container.format_command(raw_command)
                if echo:
                    self.controller.write({'stdout': format_command + '\n'})
                c = self.container.command(format_command)
                while c.status()['Running']:
                    # если проект завершен извне
                    if self._kill:
                        return
                    if stdout:
                        while (data := c.read()) != (None, None):
                            self.controller.write({'stdout': data[0], 'stderr': data[1]})
                            self.append(data)
                    if stdin and c.status()['Running']:
                        data = self.controller.read()
                        if data is not None:
                            c.write(data)
                    # небольшая задержка чтобы проект не спрашивал постоянно у контейнера и пользователя данные
                    time.sleep(0.25)
                # чтение оставшихся данных
                if stdout:
                    while True:
                        stdin = c.read()
                        if stdin == ('', ''):
                            break
                        self.controller.write({'stdout': stdin[0], 'stderr': stdin[1]})
                        self.append(stdin)
                if exitCode:
                    self.dict['exitCode'] = c.status()['ExitCode']
                else:
                    self.dict['exitCode'] = None
            case Steps():
                data = inst.data
                self.queue = [*data, *self.queue]
                self.dict['exitCode'] = None
            case If():
                variable, c, value, if_branch, else_branch = inst.condition.variable, inst.condition.c, inst.condition.value, inst.if_branch, inst.else_branch # noqa
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

                self.dict['exitCode'] = None

    def add_file(self, filename: str, data: str):
        self.container.add_file(filename, data)

    def add_environment(self, name: str, value: str):
        self.container.add_environment(name, value)

    def add_variable(self, name: str, value: str):
        self.container.add_variable(name, value)

    def run(self):
        print(self.steps)
        self.queue.extend(self.steps)
        while len(self.queue):
            self.step()
            if self.dict.get('exitCode') is not None:
                self.controller.write({'exitCode': f"Process finished with exit code {self.dict['exitCode']}\n"})

    def kill(self):
        """Закончить выполнение проекта если пользователь закрыл выполнение на своей стороне"""
        self._kill = True

    def __del__(self):
        del self.container
