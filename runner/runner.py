import tempfile
import shutil
from pathlib import Path
import docker


client = docker.from_env()


class Execution:
    """Одна команда, которая имеет сокет для ввода и вывода"""
    def __init__(self, exec):
        self.exec = exec
        self.socket = client.api.exec_start(self.exec['Id'], socket=True, tty=True, demux=True)
        self.socket._sock.settimeout(0.2)

    def write(self, data: str):
        """write data to stdin"""
        return self.socket._sock.send(data.encode('utf-8'))

    def read(self):
        """read from stdout/stderr""" # only 1024!!
        return self.socket._sock.recv(1024).decode()

    def status(self):
        """Позвлоляет узнать завершила ли работу команда и узнать код возврата"""
        return client.api.exec_inspect(self.exec['Id'])


class Runner:
    """Открытый контейнер, в рамках которого исполняется несколько команд"""
    def __init__(self):
        """Запускаю контейнер и увожу его в вечный сон и ожидание команд"""
        self.folder = tempfile.TemporaryDirectory()
        self.container = client.containers.run(
            'python:3.10',
            command=f"sleep infinity",
            working_dir='/app',
            volumes=[f'{Path(self.folder.name)}:/app'],
            tty=True,
            detach=True,
            network_disabled=True,
        )

    def add_file(self, filename: str, data: str):
        """Загрузка файла в контейнер"""
        name = Path(self.folder.name) / filename
        with open(name, 'w') as file:
            file.write(data)

    def exec(self, command):
        """Выполнить команду, аналог docker exec"""
        return Execution(client.api.exec_create(self.container.id, command, tty=True, stdin=True))

    def __del__(self):
        """После завершени работы контейнера его нужно удалить"""
        self.container.remove(force=True)
        shutil.rmtree(self.folder.name, ignore_errors=True)
