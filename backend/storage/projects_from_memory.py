from pydantic import BaseModel  # noqa
import pathlib

from backend.storage.db import Session
from backend.storage.models import Page, Steps, Print, Run, UI, Input, Project, Content, Entry, User


def ex(name: str) -> str:
    file = pathlib.Path(__file__).parent.resolve() / f"progs/{name}"
    return open(file).read()


goScenario = Steps(data=[
    Run(command='ls -la', stdin=False, stdout=True, exitCode=False),
    Run(command='go build main.go', stdin=False, stdout=True, echo=True),
    Run(command='ls -la', stdin=False, stdout=True, exitCode=False),
    Run(command='./main', stdin=True, stdout=True, echo=True)])

javaScenario = Steps(data=[
    Run(command='javac Main.java', stdin=False, stdout=True, echo=True),
    Steps(data=[
        Print(text="1"),
        Print(text="2"),
        Print(text="3"),
    ]),
    Run(command='java Main', stdin=True, stdout=True, echo=True)])

Z3Scenario = Steps(data=[Run(command='/app/main.z3', stdin=True, stdout=True, echo=False)])

pythonScenario = Steps(data=[Run(command='python main.py', stdin=True, stdout=True, echo=False)])

nusmvScenario = Steps(data=[Run(command='nusmv /app/main.smv', stdin=True, stdout=True, echo=False)])

goUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.go', language='go',
          default=ex('main.go')),  # noqa
    Input(name='param', description='example description', destination='env', type='text', env='param',
          default='123321'),  # noqa
])

javaUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='Main.java', language='java',
          default=ex('Main.java')),  # noqa
])

z3UI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.z3', language='z3',
          default=ex('main.z3')),  # noqa
])

pythonUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.py', language='python',
          default=ex('main.py')),  # noqa
    Input(name='data', description='input file', destination='file', type='textarea', file='data.txt', language='txt',
          default="hello world\n!!!"),  # noqa
    Input(name='file_str', description='input file', destination='file', type='file', file='file.txt', language='txt'),
    # noqa
    Input(name='list', description='example list element', destination='file', type='list', file='list.txt',
          values=[{'title': 'One', 'value': '1'}, {'title': 'Two', 'value': '2'}, {'title': 'Three', 'value': '3'}],
          default='1'),  # noqa
])

nusmvUI = UI(data=[
    Input(name='editor', description='code input', destination='file', type='code', file='main.smv', language='nusmv',
          default=ex('main.smv')),  # noqa
])

goMDdesc = """
# Go language
- 1
- 2
- 3
```go
func go() int {
    return 0
}
```
"""
pages = [
    Page(short_description="go example", name="Go", description=goMDdesc, container="golang:alpine", ui=goUI, scenario=goScenario),  # noqa
    Page(short_description="java example",name="Java", description="Java language compiler", container="openjdk:11", ui=javaUI,
         scenario=javaScenario),  # noqa
    Page(short_description="z3 example", name="Z3", description="Z3 language", container="ghcr.io/z3prover/z3:ubuntu-20.04-bare-z3-sha-e3a4425",
         ui=z3UI, scenario=Z3Scenario),  # noqa
    Page(short_description="python example",name="Python", description="Python 3.10", container="python:3.10-alpine", ui=pythonUI,
         scenario=pythonScenario),  # noqa
    Page(short_description="nusmv example",name="nusmv", version="1", description="nusmv",
         container="semwai/nusmv:2.6.0", ui=nusmvUI, scenario=nusmvScenario)  # noqa
]

projects = [
    Project(name="Первый проект", description="Описание первого проекта", content=Content(
        data=[Entry(id=4, short_description="Python 3.10"), Entry(id=5, short_description="nusmw")])),  # noqa
    Project(name="Второй проект со всеми страницами", description="Описание второго проекта",
            content=Content(
                data=[
                    Entry(id=3, short_description="z3"),
                    Content(data=[Entry(id=1, short_description="Go simple goroutines example"),
                                  Entry(id=2, short_description="Java example"),
                                  Content(data=[Entry(id=1, short_description="Уровень"),
                                                Content(
                                                    data=[Entry(id=1, short_description="Вложенности"),
                                                          Content(data=[
                                                              Entry(id=1, short_description="Не"),
                                                              Entry(id=1, short_description="Ограничен")]),
                                                          ]),
                                                ]),
                                  ]),
                    Entry(id=4, short_description="Python 3.10"),
                    Entry(id=5, short_description="nusmw")])),
    Project(name="Go book", description="Интерактивная книга по языку GO",
            content=Content(
                description="Оглавление",
                data=[
                    Entry(id=1, short_description="Введение в Go"),
                    Content(
                        description="Глава 1",
                        data=[Entry(id=1, short_description="Структура программы"),
                              Entry(id=1, short_description="Переменные"),
                              Entry(id=1, short_description="Типы данных"),
                              Entry(id=1, short_description="Константы"),
                              Entry(id=1, short_description="Операторы"),
                              Entry(id=1, short_description="Циклы"),
                              ]),
                    Content(
                        description="Глава 2",
                        data=[Entry(id=1, short_description="Указатели"),
                              Entry(id=1, short_description="Функции и указатели"),
                              ]),
                    Content(
                        description="Горутины",
                        data=[Entry(id=1, short_description="Введение"),
                              Entry(id=1, short_description="Пример"),
                              ]),
                    Entry(id=1, short_description="Вывод")]))
]

if __name__ == "__main__":
    with Session() as db:
        for p in projects:
            db.add(p)
        for p in pages:
            db.add(p)
        db.add(User(name='semwai', email='e14s@mail.ru', access='admin'))
        db.commit()
