from threading import Thread

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect # noqa
import asyncio
import uvicorn

from runner.container import Container
from runner.controller import ThreadController
from runner.project import Project
from runner.step import AddFile, RunCommand

app = FastAPI()


@app.get("/")
async def get():
    return HTMLResponse(open("index.html").read())


async def websocket_read_timeout(websocket: WebSocket, timeout=0.1):
    try:
        # receive_json - блокирующая операция, поэтому выделяю ей максимум timeout и иду смотреть за контейнером
        data = await asyncio.wait_for(fut=websocket.receive_json(), timeout=timeout)
    except asyncio.exceptions.TimeoutError:
        data = None
    return data


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # жду программу
    while True:
        try:
            message = await websocket_read_timeout(websocket)
        except WebSocketDisconnect:
            return
        if message is not None and message.get('type') == 'program':
            code = message.get('data')
            break
    controller = ThreadController()
    project = Project(
        controller,
        Container('golang:alpine'),
        AddFile('main.go', code),  # Вместо text будет описание источника ввода файла
        RunCommand('go build main.go', stdin=False, stdout=True),
        RunCommand('ls -la', stdin=False, stdout=True),
        RunCommand('./main', stdin=True, stdout=True)
    )
    thread = Thread(target=project.run, daemon=True)
    thread.start()
    while True:
        # Жду сообщение от клиента, если не придет сообщение, то иду дальше проверять сообщения от контейнера
        try:
            # receive_json - блокирующая операция, поэтому выделяю ей максимум timeout и иду смотреть за контейнером
            message = await asyncio.wait_for(fut=websocket.receive_json(), timeout=0.5)
            controller.read_websocket(message['data'])
        except asyncio.exceptions.TimeoutError:
            pass
        # Клиент может отключиться
        except WebSocketDisconnect:
            print("client disconnect")
            project.kill()
            break

        if (read := controller.write_websocket()) is not None:
            await websocket.send_json(read)
        if project.stop:
            print("project finished")
            break
    del controller
    del project

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)
