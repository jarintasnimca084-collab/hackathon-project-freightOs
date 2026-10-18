import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s_idx = text.find('sidebar-brand')
print("Index:", s_idx)
print(text[s_idx-30:s_idx+400])
