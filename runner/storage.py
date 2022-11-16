from pydantic import BaseModel  # noqa


class Project(BaseModel):
    """Web модель описания проекта"""
    id: int
    name: str
    description: str
    lang: str
    example: str


class Projects(BaseModel):
    data: list[Project]


projects = Projects(
    data=[
        Project(id=1, name="Go", description="Golang language compiler", lang="go",
                example="""package main

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
    fmt.Print("enter value:")
    fmt.Scan(&text)
    f(text)

    go f("goroutine1")
    go f("goroutine2")

    time.Sleep(time.Second * 4)
    fmt.Println("done")
}               
                """),
        Project(id=2, name="Java", description="Java language compiler", lang="java",
                example="""public class Main {
  public static void main(String[] args) {
    int x = 5;
    int y = 2;
    System.out.println(x % y);
  }
}"""),
        Project(id=3, name="Z3", description="Z3 language", lang="Z3",
                example="""; Getting values or models
(set-option :print-success false)
(set-option :produce-models true)
(set-logic QF_LIA)
(declare-const x Int)
(declare-const y Int)
(assert (= (+ x (* 2 y)) 20))
(assert (= (- x y) 2))
(check-sat)
; sat
(get-value (x y))
; ((x 8) (y 6))
(get-model)
; ((define-fun x () Int 8)
;  (define-fun y () Int 6)
; )
(exit)"""),
        Project(id=4, name="Python", description="Python 3.10", lang="python", example="""while (y:=input())!='exit':
    print(y)
        """)
    ]
)
