from threading import Thread

import fastapi
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware # noqa
from starlette.websockets import WebSocketDisconnect # noqa
import asyncio
import uvicorn

import runner.builder
from runner.controller import ThreadController
import runner.storage
from runner.example.web_project.schemas import GetProjects, GetProject

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://v1442641.hosted-by-vdsina.ru"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# async def get():
#     return HTMLResponse(open("index.html").read())


@app.get("/project/{project_id}")
async def get(project_id: int):
    return HTMLResponse(open(f"project{project_id}.html").read())


@app.get("/api/projects", response_model=GetProjects, tags=["api"])
async def get():
    return runner.storage.projects


@app.get("/api/project/{project_id}", response_model=GetProject, tags=["api"])
async def get(project_id: int):
    try:
        return [project for project in runner.storage.projects.data if project.id == project_id][0]
    except IndexError:
        raise fastapi.HTTPException(status_code=404, detail="project not found")


async def websocket_read_timeout(websocket: WebSocket, timeout=0.1):
    try:
        # receive_json - блокирующая операция, поэтому выделяю ей максимум timeout и иду смотреть за контейнером
        data = await asyncio.wait_for(fut=websocket.receive_json(), timeout=timeout)
    except asyncio.exceptions.TimeoutError:
        data = None
    return data


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, project_id: int = 0):
    await websocket.accept()
    print(f"{project_id=}")
    # жду программу
    while True:
        try:
            message = await websocket_read_timeout(websocket)
        except WebSocketDisconnect:
            return
        if message is not None and message.get('type') == 'program':
            code = message.get('data')
            break
    # сообщение пользователю, что нужно подождать загрузку
    await websocket.send_json({"wait": True})
    controller = ThreadController()
    match project_id:
        case 1:
            project = runner.builder.GoProject(controller, code)
        case 2:
            project = runner.builder.JavaProject(controller, code)
        case 3:
            project = runner.builder.Z3Project(controller, code)
        case 4:
            project = runner.builder.PythonProject(controller, code)
        case 5:
            project = runner.builder.NuSMVroject(controller, code)
        case _:
            raise fastapi.HTTPException(404, detail='project not found')

    thread = Thread(target=project.run, daemon=True)
    thread.start()
    await websocket.send_json({"wait": False})
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
            # дочитываю последние данные
            while (read := controller.write_websocket()) is not None:
                await websocket.send_json(read)
            break
    del controller
    del project

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)
