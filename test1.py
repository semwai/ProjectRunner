import yaml

document = """
version: 1 # Версия описания документа

project:
    name: gcc 5.15 # Отображаемое имя проекта
    version: 2 # Версия проекта
    description: С language compiler # Краткая информация
    full-description: С language compiler v5.15 # Подробная информация
    url: 
      github: github.com/gcc/gcc
      telegram: tg.me/...
    authors: [John, Alex, Dog]
    
    input:
        params:
            - optimization:
                name: optimization
                description: optimization level
                type: list # выбор одного из множества параметров
                values:
                    - O0: zero optimization
                    - O1: light optimization
                    - O2: standard optimization
            - env_example:
                name: env
                description: переменная среды 
                type: text
                destination: env # env или params
                # set env=$text
                
            - code: # окно ввода кода
                name: code editor
                type: editor
                lang: c
                width: 80
                file: 
                    name: main.c # в конечном итоге содержимое отправляется под видом файла 
    
"""

scenario = """
print("hello from gcc example project")
run(gcc $) # $ - вставляет все параметры
if code == 0: # если ошибок не было, то вывести результата работы компилятора
    print(stdout)
    run(./a.out)
    if code == 0:
        print(stdout)
    else:
        print(code)
        print(stderr)
else: # ошибка компиляции, выводим в консоль данные
    print(code)
    print(stderr)
    number = parse(stderr) # набросок того, как будет происходить поиск номера ошибочной строки
    code.select(number) # code - id поля ввода файла. Поле ввода указано в паспорте проекта
    
"""


if __name__ == '__main__':
    config = yaml.load(document, Loader=yaml.Loader)
    print(config)
