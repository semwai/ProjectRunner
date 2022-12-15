from threading import Thread
import fastapi
from fastapi import FastAPI, WebSocket
from starlette.middleware.cors import CORSMiddleware # noqa
from starlette.websockets import WebSocketDisconnect # noqa
import asyncio
import uvicorn

from backend import storage
from runner.controller import ThreadController

from schemas import GetProjects, GetProject

logger = uvicorn.config.logger

app = FastAPI()

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


@app.get("/api/projects", response_model=GetProjects, tags=["api"])
async def get_projects():
    return storage.projects


@app.get("/api/project/{project_id}", response_model=GetProject, tags=["api"])
async def get_project(project_id: int):
    try:
        project = [project for project in storage.projects.data if project.id == project_id][0]
        return project.dict(exclude_none=True)
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
    logger.info(f"{project_id=}")
    # жду программу
    while True:
        try:
            message = await websocket_read_timeout(websocket)
        except WebSocketDisconnect:
            return

        if message is not None and message.get('type') == 'start':
            logger.info(message)
            try:
                ui_data = message.get('data')
            except KeyError as e:
                await websocket.send_json({"wait": False})
                await websocket.send_json({"stderr": f"{e} not found"})
                logger.error(e)
                return
            break
    # сообщение пользователю, что нужно подождать загрузку
    await websocket.send_json({"wait": True})
    controller = ThreadController()
    try:
        project = storage.projectById(project_id)
        builder = project.builder(controller)
    except Exception as e:
        logger.error(str(e))
        raise fastapi.HTTPException(404, detail='project not found')
    # UI
    project.ui.parse(builder, ui_data)
    # builder.add_file('main.go', ui_data['editor'])
    #
    thread = Thread(target=builder.run, daemon=True)
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
            logger.info("client disconnect")
            builder.kill()
            break

        if (read := controller.write_websocket()) is not None:
            await websocket.send_json(read)
        if builder.stop:
            logger.info("project finished")
            # дочитываю последние данные
            while (read := controller.write_websocket()) is not None:
                await websocket.send_json(read)
            break
    del controller
    del builder


if __name__ == '__main__':
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True, log_config=log_config)
