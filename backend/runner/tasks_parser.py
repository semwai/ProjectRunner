"""
Модуль преобразует описание сценария в паспорте в объекты
"""
import yaml
from backend.storage.models import Steps, Print, File, Run, If, Condition


def str_to_yaml(text: str) -> dict:
    doc = yaml.load(text, Loader=yaml.Loader)
    return doc


def parse(config: dict):

    program = Steps(data=[])

    for step in config:
        match (step['type']):
            case 'Print':
                program.data.append(Print(text=step.get('text'), file=step.get('file')))
            case 'File':
                program.data.append(File(text=step.get('name'), file=step.get('data')))
            case 'Run':
                program.data.append(Run(
                    step.get('command'), step.get('stdin'), step.get('stdout'), step.get('exitCode'), step.get('echo')))
            case 'If':
                cond = step.get('condition')
                _if = step.get('if_branch')
                if _if:
                    _if = _if['tasks']
                _else = step.get('else_branch')
                if _else:
                    _else = _else['tasks']
                s = If(Condition(cond.get('variable'), cond.get('c'), cond.get('value')),
                       parse(_if), parse(_else))
                program.steps.append(s)
    return program


if __name__ == '__main__':
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
        variable: exitCode
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
    print(parse(str_to_yaml(document)['tasks']))
