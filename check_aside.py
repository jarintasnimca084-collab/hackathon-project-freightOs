import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s_idx = text.find('<aside class="sidebar"')
print(text[s_idx:s_idx+400])
