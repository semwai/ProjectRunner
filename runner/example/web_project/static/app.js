var ws = null

function start(event) {
    document.getElementById("messages").innerHTML = ""
    start_button.innerHTML = "Restart"
    run_button.disabled = false
    ws = new WebSocket("ws://localhost:8000/ws");
    ws.onmessage = function(event) {
        var messages = document.getElementById('messages')
        msg = JSON.parse(event.data)
        if (msg.stdout) {
            messages.innerHTML += `<span>${msg.stdout}</span>`
        }
        if (msg.stderr) {
            messages.innerHTML += `<span style="color:red;">${msg.stderr}</span>`
        }
        if (msg.ExitCode) {
            messages.innerHTML += `<span style="color:white;">${msg.ExitCode}</span>`
        }
        messages.scrollTop += 1000
    };
}

function run(event) {
    if (ws == null) {
        return
    }
    run_button.disabled = true
    document.getElementById("messages").innerHTML = ""
    //var input = document.getElementById("messageText")
    ws.send(JSON.stringify({type: 'program', data: editor.getValue()}))
    event.preventDefault()
}

function newstdIO(event) {
    if (ws == null) {
        return
    }
    var input = document.getElementById("stdIOText")
    messages.innerHTML += `<span style="color:green;">${input.value}<br><span>`
    ws.send(JSON.stringify({type: 'stdio', data: input.value}))
    event.preventDefault()
}

function decorate(start, end){
var decorations = editor.deltaDecorations(
	[],
	[
		{
			range: new monaco.Range(start, 1, end, 1),
			options: {
			    className: 'myContentClass',
				glyphMarginClassName: 'myGlyphMarginClass',
			    isWholeLine: true,
			}
		}
	]
);
}

code = `package main

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
}`