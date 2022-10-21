from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
import uvicorn
import time
from runner import Runner

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Example</title>
    </head>
    <body>
        <h1>Python online</h1>
        <div>
            <textarea id="messageText" autocomplete="off" rows=25 cols=80>
import time
print("Hello world")
a = int(input("value:"))
time.sleep(2)
print(f"Message after 2 seconds, value^2={a**2}")
            </textarea>
            <p><button onclick="newProgramm(event)">Run</button></p>
        </div>
        <p>stdin:</p>
        <p><input type=text id="stdIOText"/><button onclick="newstdIO(event)">send</button></p>
        <p>stdout:</p>
        <pre id='messages' style='font-family:Monospace;'>
        </pre>
        <script>
            var ws = new WebSocket("ws://localhost:8001/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                //var message = document.createElement('am')
                //var content = document.createTextNode(event.data)
                //message.appendChild(content)
                //messages.appendChild(message)
                messages.innerHTML += event.data
            };
            function newProgramm(event) {
                document.getElementById("messages").innerHTML = ""
                var input = document.getElementById("messageText")
                ws.send(JSON.stringify({type: 'programm', data: input.value}))
                //input.value = ''
                event.preventDefault()
            }
            function newstdIO(event) {
                var input = document.getElementById("stdIOText")
                ws.send(JSON.stringify({type: 'stdio', data: input.value}))
                //input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


def read_pool(exec):
    while exec.status()['Running']:
        try:
            yield exec.read()
        except TimeoutError:
            pass
        time.sleep(1)


async def write_pool(exec, data):
    while exec.status()['Running']:
        exec.write(data)
        await asyncio.sleep(1)


class RunModel:

    def __init__(self, text):
        self.runner = Runner()
        self.runner.add_file('app.py', text)
        self.exec = self.runner.exec('python app.py')
        print(self.exec.status())

    def write(self, data):
        if self.exec.status()['Running']:
            return self.exec.write(data + "\n")
        else:
            return self.exec.status()['ExitCode']

    def read(self):
        try:
            return self.exec.read()
        except TimeoutError:
            return None

    def status(self):
        return self.exec.status()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    run_model = None

    while True:

        try:
            data = await asyncio.wait_for(fut=websocket.receive_json(), timeout=1)
        except asyncio.exceptions.TimeoutError:
            data = None

        if data is not None:
            match data['type']:
                case "programm":
                    run_model = RunModel(data['data'])
                case "stdio":
                    if run_model is not None:
                        run_model.write(data['data'])

        if run_model is None:
            continue

        if (ret := run_model.read()) is not None:
            await websocket.send_text(ret)

        status = run_model.status()
        if not status['Running']:
            await websocket.send_text(f"Process finished with exit code {status['ExitCode']}")
            run_model = None


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8001, reload=True)
