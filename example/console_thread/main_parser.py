from backend.runner.container import Container
from backend.runner.controller import ThreadConsoleController
from backend.runner.tasks_parser import parse, str_to_yaml
from backend.runner.project import Project


def main():
    text = """package main
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
    text = '\n        '.join(text.split('\n'))
    document = f"""
tasks:
    - type: File
      name: main.go
      data: |
        {text}
    - type: Run
      command: go build main.go
      stdin: false
      stdout: true
    - type: If
      condition:
        variable: exitCode
        c: '!='
        value: 0
      if_branch:
        tasks:
          - type: Print
            text: Error!!!!
      else_branch:
        tasks:
          - type: Print
            text: 'Compile: OK'
          - type: Run
            command: ./main
            stdin: true
            stdout: true
    """
    controller = ThreadConsoleController()
    project = Project(
        controller,
        Container('golang:alpine'),
        program=parse(str_to_yaml(document)['tasks'])
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
