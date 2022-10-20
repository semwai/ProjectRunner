from runner import Runner
import time

code = """
import time
print("hello")
a = 2
b = int(input())
print(f"({a=})+({b=})")
time.sleep(1)
print(f"({a=})+({b=})={a+b}")
c = input()
print(c*10)
"""


if __name__ == '__main__':
    r = Runner()
    r.add_file('app.py', code)
    # Выполняем команду и получаем сокет для ввода-вывода
    res, socket = r.exec('python app.py')
    # Посылаем сокету сообщение
    socket._sock.send("142\n".encode('utf-8'))
    # Читаем ответ
    time.sleep(2)
    print(socket._sock.recv(1024).decode())
    print(r.exec('ls'))
    print(r.folder.name)
