"""
Модуль преобразует описание сценария в паспорте в объекты
"""
import yaml
from .step import Steps, Print, File, Run, If, Condition


def str_to_yaml(text: str) -> dict:
    doc = yaml.load(text, Loader=yaml.Loader)
    return doc


def parse(config: dict):

    program = Steps([])

    for step in config:
        match (step['type']):
            case 'Print':
                program.steps.append(Print(step.get('text'), step.get('file')))
            case 'File':
                program.steps.append(File(step.get('name'), step.get('data')))
            case 'Run':
                program.steps.append(Run(
                    step.get('command'), step.get('stdin'), step.get('stdout'), step.get('ExitCode'), step.get('echo')))
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
    print(parse(str_to_yaml(document)['tasks']))
