from runner.container import Container
from runner.controller import ThreadConsoleController
from runner.project import Project
from runner.step import AddFile, RunCommand


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
    fmt.Print("enter value:")
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
