var ws = null

function start(event) {
    document.getElementById("messages").innerHTML = ""
    start_button.innerHTML = "Restart"
    run_button.disabled = false
    ws = new WebSocket("ws://localhost:8000/ws");
    ws.onmessage = function(event) {
        var messages = document.getElementById('messages')
        msg = JSON.parse(event.data)
        console.log(msg)
        if (msg.stdout) {
            messages.innerHTML += `<span>${msg.stdout}<span>`
        }
        if (msg.stderr) {
            messages.innerHTML += `<span style="color:red;">${msg.stderr}<span>`
        }
        if (msg.ExitCode) {
            messages.innerHTML += `<span style="color:blue;">${msg.ExitCode}<span>`
        }
    };
}

function run(event) {
    if (ws == null) {
        return
    }
    run_button.disabled = true
    document.getElementById("messages").innerHTML = ""
    var input = document.getElementById("messageText")
    ws.send(JSON.stringify({type: 'program', data: input.value}))
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