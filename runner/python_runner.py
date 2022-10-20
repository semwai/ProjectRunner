from runner import Runner


code = """
a = 2
b = input()
print(f"({a=})+({b=})={a+b}")
"""


if __name__ == '__main__':
    r = Runner()
    r.add_file('app.py', code)
    print(r.exec('python app.py'))
    print(r.exec('ls'))
    print(r.folder.name)
