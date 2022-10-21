from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect
import asyncio
import uvicorn

from runner import Runner

app = FastAPI()


@app.get("/")
async def get():
    return HTMLResponse(open("index.html").read())


class RunModel:
    """Контроллер запущенной команды"""
    def __init__(self, text):
        self.runner = Runner()
        self.runner.add_file('app.py', text)
        self.exec = self.runner.exec('python app.py')
        # print(self.exec.status())

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

        # Жду сообщение от клиента, если не придет сообщение, то иду дальше проверять сообщения от контейнера
        try:
            # receive_json - блокирующая операция, поэтому выделяю ей максимум timeout и иду смотреть за контейнером
            data = await asyncio.wait_for(fut=websocket.receive_json(), timeout=0.1)
        except asyncio.exceptions.TimeoutError:
            data = None
        # Клиент может отлючиться
        except WebSocketDisconnect:
            print("client disconnect")
            break
        # Если придет сообщение от клиента, то проверяю его
        if data is not None:
            match data['type']:
                case "programm":
                    run_model = RunModel(data['data'])
                case "stdio":
                    if run_model is not None:
                        run_model.write(data['data'])
        # Если код еще не был запущен
        if run_model is None:
            continue
        # Пытаюсь получить данные из контейнера
        if (ret := run_model.read()) is not None:
            await websocket.send_text(ret)
        # Если выполнение завершено, то вывести код результата
        status = run_model.status()
        if not status['Running']:
            await websocket.send_text(f"Process finished with exit code {status['ExitCode']}")
            run_model = None


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8001, reload=True)
