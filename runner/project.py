import time

from runner.container import Container
from runner.controller import Controller, ConsoleController, ThreadConsoleController
from runner.step import AddFile, RunCommand


class Project:
    """Проект принимает последовательность команд, которые выполняет согласно сценарию. Данные получаются и
    отправляются на контроллер """
    def __init__(self, controller: Controller, container: Container, *steps):
        self.controller = controller
        self.steps = steps
        self.current = 0
        self.container = container
        self.last_status = None  # код возврата из последней запущенной команды

    def step(self):
        if self.current == len(self.steps):
            raise IndexError
        inst = self.steps[self.current]
        match inst:
            case AddFile(name, data):
                self.container.add_file(name, data)
                self.last_status = None
            case RunCommand(command, read, write):
                c = self.container.command(command)
                while c.status()['Running']:
                    # небольшая задержка чтобы проект не спрашивал постоянно у контейнера и пользователя данные
                    time.sleep(0.1)
                    if write:
                        data = c.read()
                        if data != (None, None):
                            self.controller.write(data)
                    if read and c.status()['Running']:
                        data = self.controller.read()
                        if data is not None:
                            # print(f"project load {data}")
                            c.write(data)
                # чтение оставшихся данных
                if write:
                    while True:
                        read = c.read()
                        if read == ('', ''):
                            break
                        self.controller.write(read)
                self.last_status = c.status()['ExitCode']
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
    for i := 0; i < 3; i++ {
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
    time.Sleep(time.Second * 4)
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
    project.run()
    controller.stop()
    del controller
    del project


if __name__ == '__main__':
    main()
