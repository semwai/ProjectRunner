from runner.container import Container


def main():
    container = Container('python:3.10-alpine')
    container.add_file('app.py', open('example/console/code.py').read())
    command = container.command('python app.py')
    while (c := input('command:')) != 'exit':
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
