import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('alt="Trans Ontario Express"')
print(text[idx1-20:idx1+400])
