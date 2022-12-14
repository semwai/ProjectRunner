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
    fmt.Print("enter value:")
    fmt.Scan(&text)
    f(text)

    go f("goroutine1")
    go f("goroutine2")

    time.Sleep(time.Second * 4)
    fmt.Println("done")
}