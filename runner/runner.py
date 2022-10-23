import tempfile
import shutil
from pathlib import Path
import docker
import tarfile
import io
import asyncio

client = docker.from_env()


class Execution:
    """Одна команда, которая имеет сокет для ввода и вывода"""
    def __init__(self, container):
        self.container = container
        self.container.start()
        #self.reader = client.api.attach(container.id, stream=True, demux=True)
        self.stdin = client.api.attach_socket(container.id, params={'stdin': 1, 'stdout': 0, 'stderr': 0, 'stream': 1})
        self.stdout = client.api.attach_socket(container.id, params={'stdin': 0, 'stdout': 1, 'stderr': 0, 'stream': 1})
        self.stderr = client.api.attach_socket(container.id, params={'stdin': 0, 'stdout': 0, 'stderr': 1, 'stream': 1})
        # Сокет перестаёт блокировать при чтении, но если сокет пуст, то будет вылетать BlockingIOError
        self.stdin._sock.setblocking(0)
        self.stdout._sock.setblocking(0)
        self.stderr._sock.setblocking(0)
        print()

    def write(self, data: str):
        """write data to stdin"""
        return self.stdin._sock.send(data.encode('utf-8'))

    def read(self):
        """read from (stdout, stderr)""" # only 1024!!
        try:
            stderr = self.stderr._sock.recv(1024)
        except BlockingIOError:
            stderr = None
        try:
            stdout = self.stdout._sock.recv(1024)
        except BlockingIOError:
            stdout = None
        return stdout, stderr

    def status(self):
        """Позвлоляет узнать завершила ли работу команда и узнать код возврата"""
        self.container.reload()
        return self.container.attrs['State']

    def __del__(self):
        self.container.remove(force=True)


class Runner:
    """Открытый контейнер, в рамках которого исполняется несколько команд"""
    def __init__(self):
        """Запускаю контейнер и увожу его в вечный сон и ожидание команд"""
        self.folder = tempfile.TemporaryDirectory()
        self.volume = client.volumes.create()
        self.container = client.containers.run(
            'python:3.10',
            command='sleep infinity',
            working_dir='/app',
            volumes=[f'{self.volume.id}:/app'],
            tty=False,
            detach=True,
            network_disabled=True,
        )

    def _make_archive(self, filename: str, data: bytes):
        """Делаю архив с одним файлом из данных"""
        tarstream = io.BytesIO()
        tar = tarfile.open(fileobj=tarstream, mode='w')
        tarinfo = tarfile.TarInfo(name=filename)
        tarinfo.size = len(data)
        tar.addfile(tarinfo=tarinfo, fileobj=io.BytesIO(data))
        tar.close()
        tarstream.seek(0)
        return tarstream

    def add_file(self, filename: str, data: str):
        """Загрузка файла в контейнер"""
        tarstream = self._make_archive(filename, data.encode('utf-8'))
        client.api.put_archive(self.container.id, '/app', tarstream)

    def command(self, command):
        """Выполнить команду, аналог docker exec"""
        return Execution(client.containers.create(
            'python:3.10',
            command=command,
            working_dir='/app',
            volumes=[f'{self.volume.id}:/app'],
            tty=True,
            detach=True,
            network_disabled=True,
            stdin_open=True,
        ))

    def __del__(self):
        """После завершени работы контейнера его нужно удалить"""
        self.container.remove(force=True)
        self.volume.remove()
        shutil.rmtree(self.folder.name, ignore_errors=True)
