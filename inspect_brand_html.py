import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('<div class="sidebar-brand">')
idx2 = text.find('</aside>')
print(text[idx1:idx1+700])
