"""Scoate pagini HTML de test pentru vizualizator, ca sa le poti deschide intr-un browser (sau sa faci screenshot).

    python preview.py            # scrie ./_preview/*.html
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from onia import vezi_html  # noqa: E402

DEMO = {
    'suma': ("""
s = 0
for x in [3, 1, 4]:
    s += x   #: adunam elementul curent la suma
print(s)
""", None),
    'alias': ("""
a = [1, 2]
b = a          #: b nu e o copie, e aceeasi lista
b.append(3)
c = a.copy()   #: aici chiar avem o copie
c.append(9)
gresit = [[0] * 3] * 3
gresit[1][1] = 7   #: se schimba pe toate randurile!
bun = [[0] * 3 for _ in range(3)]
bun[1][1] = 7
""", None),
    'factorial': ("""
def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)

print(fact(3))
""", None),
    'eroare': ("""
x = int('5')
y = x + '3'
print(y)
""", None),
    'colectii': ("""
d = {'ana': 9, 'dan': 7}
d['eva'] = 10
s = {3, 1, 2}
s.add(5)
m = [[1, 2, 3], [4, 5, 6]]
t = (1, 'a', 2.5)
nota = d['ana']
""", None),
    'clasa': ("""
class Punct:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def muta(self, dx):
        self.x += dx
p = Punct(1, 2)
q = p
q.muta(5)
""", None),
    'input': ("""
a = int(input('a = '))
b = int(input('b = '))
print('suma:', a + b)
""", ['3', '4']),
}

HEAD = '<!doctype html><html><head><meta charset="utf-8"><title>previzualizare</title></head><body style="margin:14px;background:#fff">'


def main():
    out = os.path.join(os.path.dirname(__file__), '_preview')
    os.makedirs(out, exist_ok=True)
    for nume, (cod, inputs) in DEMO.items():
        with open(os.path.join(out, nume + '.html'), 'w', encoding='utf-8') as f:
            f.write(HEAD + vezi_html(cod, inputs) + '</body></html>')
    print('scris in', out)


if __name__ == '__main__':
    main()
