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
        <title>Chat</title>
    </head>
    <body>
        <h1>Python online</h1>
        <form action="" onsubmit="sendMessage(event)">
            <textarea id="messageText" autocomplete="off" rows=25 cols=80>
import time
print("Hello world")
time.sleep(2)
print("Message after 2 seconds")
            </textarea>
            <p><button>Send</button></p>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8001/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    r = Runner()
    data = await websocket.receive_text()
    r.add_file('app.py', data)
    exec = r.exec('python app.py')
    pool = read_pool(exec)
    while exec.status()['Running']:
        # data = await websocket.receive_text()

        # await write_pool(exec, data)

        # await websocket.send_text(await read_pool(exec))
        for text in pool:
            await websocket.send_text(text)
    print("CLOSE")


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8001, reload=True)
