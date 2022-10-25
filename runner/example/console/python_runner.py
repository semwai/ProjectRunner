from runner.container import Container

code = """
import time
print("hello")
a = 2
b = int(input("b = "))
print(f"({a=})+({b=})")
time.sleep(1)
print(f"({a=})+({b=})={a+b}")
c = int(input("10/c, c ="))
print(10/c)
"""


def main():
    container = Container('python:3.10-alpine')
    container.add_file('app.py', code)
    # Выполняем команду и получаем сокет для ввода-вывода
    command = container.command('python app.py')
    # wait for run
    while (c:=input('command:')) != 'exit':
        match c:
            case 'read':
                print(command.read())
            case 'write':
                command.write(input(':') + '\n')
            case 'status':
                print(command.status())
            case _:
                print('commands: read, write, status, exit')
    del container


if __name__ == '__main__':
    main()
