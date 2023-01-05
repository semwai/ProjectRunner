print(f"selected element = {open('list.txt').read()}")

while (y := input()) != 'exit':
    match y:
        case 'file':
            print(open('data.txt').read())
        case _:
            print(y)
