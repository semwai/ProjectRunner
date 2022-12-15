from backend.runner.container import Container
from backend.runner.controller import ThreadConsoleController
from backend.runner.project import Project
from backend.runner.step import File, Run, Steps, If, Condition, Print


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
    fmt.Sc an(&text)
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
        program=Steps([
            File('main.go', text),  # Вместо text будет описание источника ввода файла
            Run('go build main.go', stdin=False, stdout=True),
            If(Condition("ExitCode", "==", 0),
               if_branch=Steps([
                   Run('ls -la', stdin=False, stdout=True),
                   Run('./main', stdin=True, stdout=True)
               ]),
               else_branch=Steps([
                   Print("Build error")
               ])
               ),
        ])
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
