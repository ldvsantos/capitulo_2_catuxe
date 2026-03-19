import re
from collections import Counter

with open('artigo2-elsevier_V1.tex', 'r', encoding='utf-8') as f:
    txt = f.read()

pattern = re.compile(r'\\cite[tp]?\{([^}]+)\}')
keys = []
for m in pattern.finditer(txt):
    for k in m.group(1).split(','):
        keys.append(k.strip())

print(f'Total citation keys: {len(keys)}')
print(f'Unique keys: {len(set(keys))}')
print()
print('Keys appearing 2+ times:')
for k, v in Counter(keys).most_common():
    if v >= 2:
        print(f'  {v}x  {k}')
