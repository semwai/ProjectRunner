import time

from runner import Runner
import asyncio

code = """
import time
print("hello")
a = 2
b = int(input())
print(f"({a=})+({b=})")
time.sleep(1)
print(f"({a=})+({b=})={a+b}")
c = input()
print("HaHa", c*10)
"""


async def read_pool(exec):
    while exec.status()['Running']:
        try:
            print('***read***')
            print(exec.read())
        except TimeoutError:
            pass
        await asyncio.sleep(1)


async def write_pool(exec):
    while exec.status()['Running']:
        exec.write(input("***data to programm:***") + '\n')
        await asyncio.sleep(1)


async def main():
    r = Runner()
    r.add_file('app.py', code)
    # Выполняем команду и получаем сокет для ввода-вывода
    exec = r.exec('python app.py')
    print(exec.status())
    await asyncio.gather(
        write_pool(exec), read_pool(exec)
    )


if __name__ == '__main__':
    asyncio.run(main())
