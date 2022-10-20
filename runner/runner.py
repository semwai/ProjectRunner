import tempfile
import shutil
from pathlib import Path
import docker


client = docker.from_env()


class Runner:

    def __init__(self):
        self.folder = tempfile.TemporaryDirectory()
        self.container = client.containers.run(
            'python:3.10-alpine',
            command=f"sleep infinity",
            working_dir='/app',
            volumes=[f'{Path(self.folder.name)}:/app'],
            tty=True,
            detach=True,
            network_disabled=True,
        )

    def add_file(self, filename: str, data: str):
        name = Path(self.folder.name) / filename
        with open(name, 'w') as file:
            file.write(data)

    def exec(self, command):
        return self.container.exec_run(command)

    def __del__(self):
        self.container.remove(force=True)
        shutil.rmtree(self.folder.name, ignore_errors=True)
