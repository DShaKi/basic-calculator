import re

def change_symbols(text):
  if '√' in text:
    text = re.sub(r"sqrt\((\d+)", r"sqrt(\1)", text)
  if '÷' in text:
    text = text.replace("÷", '/')
  if '×' in text:
    text.replace('×', '*')
  return text