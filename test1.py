import yaml

document = """
version: 1 # Версия описания документа

project:
    name: gcc 5.15 # Отображаемое имя проекта
    version: 2 # Версия проекта
    description: gcc language compiler # Краткая информация
    full-description: gcc language compiler v5.15 # Подробная информация
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
            - code: # окно ввода кода
                name: code redactor
                type: redactor
                lang: wotlin
                width: 80
                file: 
                    name: main.c
    
    output: > # как обрабатывает выход компилятора 
        run (gcc $) # $ - вставляет все параметры
        if code == 0: # если ошибок не было, то вывести результата работы компилятора
            print(stdout)
            run(./a.out)
            if code == 0:
                print(stdout)
            else:
                print(code)
                print(stderr)
        else: 
            print(code)
            print(stderr)
"""

if __name__ == '__main__':
    config = yaml.load(document, Loader=yaml.Loader)
    print(config)
