from threading import Thread
import fastapi
from fastapi import FastAPI, WebSocket, Depends
from starlette.middleware.cors import CORSMiddleware # noqa
from starlette.middleware.sessions import SessionMiddleware # noqa
from starlette.websockets import WebSocketDisconnect # noqa
from starlette.requests import Request # noqa
import asyncio
import uvicorn
import os

from backend.crud import api
from backend.dependencies import verify_auth_websocket
from backend.logger import logger
from backend.runner.container import Container
from backend.runner.page import Page
from backend.schemas import User
from backend.storage.db import Session
from backend.storage import models
from runner.controller import ThreadController

app = FastAPI()

origins = [
    os.environ.get('FRONTEND_URL')
]

app.add_middleware(SessionMiddleware, secret_key=os.environ.get('SECRET_KEY'))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api, prefix='/api', tags=['crud'])


async def websocket_read_timeout(websocket: WebSocket, timeout=0.1):
    try:
        # receive_json - блокирующая операция, поэтому выделяю ей максимум timeout и иду смотреть за контейнером
        data = await asyncio.wait_for(fut=websocket.receive_json(), timeout=timeout)
    except asyncio.exceptions.TimeoutError:
        data = None
    return data


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, project_id: int = 0, user: User = Depends(verify_auth_websocket)):
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
        with Session() as db:
            project: models.Page = db.query(models.Page).get(project_id)
        p = Page(controller, Container(project.container), project.scenario.data)
    except Exception as e:
        logger.error(str(e))
        raise fastapi.HTTPException(404, detail='project not found')
    project.ui.parse(p, ui_data)
    thread = Thread(target=p.run, daemon=True)
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
            p.kill()
            break
        # Читаем все полученные из контейнера данные и передаем пользователю
        while (read := controller.write_websocket()) is not None:
            await websocket.send_json(read)
        if p.stop:
            logger.info("project finished")
            # дочитываю последние данные
            while (read := controller.write_websocket()) is not None:
                await websocket.send_json(read)
            break
    del controller
    del p


if __name__ == '__main__':
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True, log_config=log_config)
