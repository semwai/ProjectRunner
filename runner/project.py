import time

from runner.container import Container
from runner.controller import Controller, ThreadConsoleController
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

    def step(self):
        if self.current == len(self.steps):
            raise IndexError
        if self.last_ExitCode is not None and self.last_ExitCode != 0:
            raise Exception(f"ExitCode {self.last_ExitCode}")
        inst = self.steps[self.current]
        match inst:
            case AddFile(name, data):
                self.container.add_file(name, data)
                self.last_ExitCode = None
            case RunCommand(command, read, write):
                c = self.container.command(command)
                while c.status()['Running']:
                    # небольшая задержка чтобы проект не спрашивал постоянно у контейнера и пользователя данные
                    time.sleep(0.1)
                    if write:
                        data = c.read()
                        if data != (None, None):
                            self.controller.write({'stdout': data[0], 'stderr': data[1]})
                    if read and c.status()['Running']:
                        data = self.controller.read()
                        if data is not None:
                            c.write(data)
                # чтение оставшихся данных
                if write:
                    while True:
                        read = c.read()
                        if read == ('', ''):
                            break
                        self.controller.write({'stdout': read[0], 'stderr': read[1]})
                self.last_ExitCode = c.status()['ExitCode']
                self.controller.write({'ExitCode': f"Process finished with exit code {self.last_ExitCode}\n"})
        self.current += 1

    def run(self):
        while self.current < len(self.steps):
            self.step()

    def __del__(self):
        del self.container


def main():
    text = """
package main
import (
    "fmt"
    "time"
)
func f(from string) {
    for i := 0; i < 2; i++ {
        fmt.Println(from, ":", i)
        time.Sleep(time.Second)
    }
}
func main() {
    var text string
    fmt.Println("enter value:")
    fmt.Scan(&text)
    f(text)
    go f("goroutine1")
    go f("goroutine2")
    time.Sleep(time.Second * 3)
    fmt.Println("done")
}
        """
    controller = ThreadConsoleController()
    project = Project(
        controller,
        Container('golang:alpine'),
        AddFile('main.go', text),  # Вместо text будет описание источника ввода файла
        RunCommand('go build main.go', stdin=False, stdout=True),
        RunCommand('ls -la', stdin=False, stdout=True),
        RunCommand('./main', stdin=True, stdout=True)
    )
    controller.run()
    try:
        project.run()
    except Exception as e:
        print(e)
    controller.stop()
    del controller
    del project


if __name__ == '__main__':
    main()
