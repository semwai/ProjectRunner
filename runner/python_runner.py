from runner import build, run
from docker.errors import ContainerError
code = """
a = 2
b = input("b=")
print(f"({a=})+({b=})={a+b}")
"""

if __name__ == '__main__':
    build()
    try:
        result = run(code, 'app.py')
        print()
    except ContainerError as e:
        print(f"status = {e.exit_status}\n")
        print(e.stderr.decode("utf-8"))
        print()
