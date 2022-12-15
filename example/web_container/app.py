from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect # noqa
import asyncio
import uvicorn

from backend.runner.container import Container
from backend.runner.controller import ProjectController

app = FastAPI()


@app.get("/")
async def get():
    return HTMLResponse(open("index.html").read())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    run_model = None

    while True:

        # Жду сообщение от клиента, если не придет сообщение, то иду дальше проверять сообщения от контейнера
        try:
            # receive_json - блокирующая операция, поэтому выделяю ей максимум timeout и иду смотреть за контейнером
            data = await asyncio.wait_for(fut=websocket.receive_json(), timeout=0.1)
        except asyncio.exceptions.TimeoutError:
            data = None
        # Клиент может отключиться
        except WebSocketDisconnect:
            print("client disconnect")
            break
        # Если придет сообщение от клиента, то проверяю его
        if data is not None:
            match data['type']:
                case "program":
                    run_model = ProjectController(data['data'], Container('golang:alpine'))
                case "stdio":
                    if run_model is not None:
                        run_model.write(data['data'])
        # Если код еще не был запущен
        if run_model is None:
            continue
        # Пытаюсь получить данные из контейнера
        if (ret := run_model.read()) != (None, None):
            # decode byte to str if not empty
            stdout, stderr = ret
            stdout = stdout if stdout is None else stdout.replace('\n', '<br>')
            stderr = stderr if stderr is None else stderr.replace('\n', '<br>')
            await websocket.send_json({'stdout': stdout, 'stderr': stderr})
        # Если выполнение завершено, то вывести код результата
        status = run_model.status()
        if not status['Running']:
            await websocket.send_json({'exit': f"Process finished with exit code {status['ExitCode']}"})
            run_model = None


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8001, reload=True)
