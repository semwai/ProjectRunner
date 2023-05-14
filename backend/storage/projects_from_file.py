from pydantic import BaseModel  # noqa

from backend.storage.db import Session
from backend.storage.models import Project, Content, Entry, User

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
        db.add(User(name='semwai', email='e14s@mail.ru', access='admin'))
        db.commit()
