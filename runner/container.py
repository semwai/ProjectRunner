import docker
import tarfile
import io
from uuid import uuid4 as uuid

client = docker.from_env()


class Command:
    """Одна команда, которая имеет сокет для ввода и вывода"""
    def __init__(self, container):
        self.container = container
        self.container.start()
        self.stdin = client.api.attach_socket(container.id, params={'stdin': 1, 'stdout': 0, 'stderr': 0, 'stream': 1})
        self.stdout = client.api.attach_socket(container.id, params={'stdin': 0, 'stdout': 1, 'stderr': 0, 'stream': 1})
        self.stderr = client.api.attach_socket(container.id, params={'stdin': 0, 'stdout': 0, 'stderr': 1, 'stream': 1})
        # Сокет перестаёт блокировать при чтении, если сокет пуст, то вместо байта будет None
        self.stdin._sock.setblocking(0) # noqa
        # Разрешаю запись в сокет
        self.stdin._writing = True # noqa
        self.stdout._sock.setblocking(0) # noqa
        self.stderr._sock.setblocking(0) # noqa

    def write(self, data: str):
        """write data to stdin"""
        return self.stdin.write(data.encode('utf-8'))

    def read(self):
        """read from (stdout, stderr)"""
        # Первым делом получаю заголовок 8 байт, первый байт всегда содержит 0x01
        # В последних байтах записана длина сообщения
        header = self.stderr.read(8)
        if header is not None:
            size = int.from_bytes(header[1:8], 'big')
            stderr = self.stderr.read(size).decode()
        else:
            stderr = None

        header = self.stdout.read(8)
        if header is not None:
            size = int.from_bytes(header[1:8], 'big')
            stdout = self.stdout.read(size).decode()
        else:
            stdout = None
        return stdout, stderr

    def status(self):
        """Позволяет узнать завершила ли работу команда и узнать код возврата"""
        self.container.reload()
        return self.container.attrs['State']


class Container:
    """Открытый проект, в рамках которого исполняется несколько команд"""
    def __init__(self, image: str):
        """Запускаю контейнер и увожу его в вечный сон (контейнер использую для загрузки файлов)"""
        self.image = image
        unique_id = uuid()
        self.volume = client.volumes.create(name=f"volume_{unique_id}")
        self.container = client.containers.run(
            self.image,
            command='sleep infinity',
            working_dir='/app',
            volumes=[f'{self.volume.id}:/app'],
            tty=False,
            detach=True,
            network_disabled=True,
            name=f"container_{unique_id}"
        )
        # Созданные контейнеры
        self.containers = [self.container]

    @staticmethod
    def _make_archive(filename: str, data: bytes):
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
        container = client.containers.create(
            self.image,
            command=command,
            working_dir='/app',
            volumes=[f'{self.volume.id}:/app'],
            tty=False,
            detach=True,
            network_disabled=True,
            stdin_open=True,
            name=f"command_{uuid()}"
        )
        self.containers.append(container)
        return Command(container)

    def __del__(self):
        """После завершения работы контейнера его нужно удалить"""
        for c in self.containers:
            c.remove(force=True)
        self.volume.remove(force=True)
