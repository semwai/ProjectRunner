import pytest # noqa

from backend.runner.step import Steps, Print, File, Run, If, Condition
from backend.runner.tasks_parser import parse, str_to_yaml


def test_main():
    document = """
tasks:
    - type: Print
      text: Hello world
    - type: File
      name: app.py
      data: print(123)
    - type: Run
      command: python main.py
      stdin: true
      stdout: true
    - type: If
      condition:
        variable: ExitCode
        c: '!='
        value: 0
      if_branch:
        tasks:
          - type: Print
            text: Error
      else_branch:
        tasks:
          - type: Print
            text: Ok
    """
    steps = [
        Print(text="Hello world"),
        File(name="app.py", data="print(123)"),
        Run(command="python main.py", stdin=True, stdout=True),
        If(condition=Condition(variable="ExitCode", c="!=", value=0),
           if_branch=Steps([
               Print(text="Error"),
           ]),
           else_branch=Steps([
               Print(text="Ok"),
           ])),
    ]
    assert parse(str_to_yaml(document)['tasks']).steps == steps
