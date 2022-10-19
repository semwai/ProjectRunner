import logging
import tempfile
from pathlib import Path

import docker
from docker.errors import ContainerError


def build():
    client = docker.from_env()
    client.images.build(path='.', tag='kotlin1720')


def run(code: str, filename: str):
    # Создаю временную папку, которая удалится после выполнения функции
    with tempfile.TemporaryDirectory() as dir:
        print(dir)
        # Имя исходного файла
        name = Path(dir) / filename
        # Записываю код
        with open(name, 'w') as file:
            file.write(code)

        client = docker.from_env()

        result = client.containers.run(
            'python:3.10-alpine',
            command=f"python {filename}",
            working_dir='/app',
            volumes=[f'{Path(dir)}:/app'],
            stdin_open=True,
            remove=True
        )
        return result
