import yaml

document = """
version: 1 # Версия описания документа

project:
    name: wotlin language 1.15 # Отображаемое имя проекта
    version: 2 # Версия проекта
    description: wotlin language compiler # Краткая информация
    full-description: wotlin language compiler v1.15 # Подробная информация
    url: 
      github: github.com/wotlin/wotlin
      telegram: tg.me/...
    authors: [John, Alex, Dog]
    
    start:
        command: ./wotlin -a 123 -i # часть параметров передаются при любом запуске
    input:
        params:
            - optimization:
                name: optimization
                description: optimization level
                type: list # выбор одного из множества параметров
                values:
                    - O0: zero optimization
                    - 01: light optimization
                    - 02: standard optimization
            - code: # окно ввода кода
                name: code redactor
                type: redactor
                lang: wotlin
                width: 80
                file: 
                    name: main.wt
    
    output: # как обрабатывает выход компилятора 
        - if code == 0: # если ошибок не было, то вывести результа работы компилятора
            - print stdout
        - else: 
            - print code
            - print stderr
"""

if __name__ == '__main__':
    config = yaml.load(document, Loader=yaml.Loader)
    print(config)
