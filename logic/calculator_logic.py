import math
import re

def change_eval_symbols(text):
    if '√' in text:
        text = re.sub(r"sqrt\((\d+)", r"sqrt(\1)", text)
    if '÷' in text:
        text = text.replace("÷", '/')
    if '×' in text:
        text = text.replace('×', '*')
    return text

def calculate(text):
    text = change_eval_symbols(text)
    result = eval(text, {"__builtins__": None}, {'sqrt': math.sqrt})
    result = str(round(result, 10))
    return result