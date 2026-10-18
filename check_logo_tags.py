import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s_idx = text.find('alt="Trans Ontario Express"')
print(text[s_idx-20:s_idx+350])
