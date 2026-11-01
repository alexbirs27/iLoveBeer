"""Teste rapide pentru vizualizator: fragmente de cod variate trebuie sa se execute fara sa crape tracerul.

    python test_vezi.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from onia import _colecteaza  # noqa: E402

CAZURI = {
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
""", []),
    'comprehension': ("""
v = [x * x for x in range(4)]
d = {x: x + 1 for x in range(3)}
s = sorted(['bb', 'a', 'ccc'], key=lambda t: len(t))
g = (x for x in range(3))
t = sum(g)
""", []),
    'try': ("""
try:
    x = int('a')
except ValueError:
    x = -1
finally:
    y = 2
""", []),
    'closure': ("""
def fabrica(k):
    def inm(x):
        return x * k
    return inm
dublu = fabrica(2)
r = dublu(5)
""", []),
    'global': ("""
total = 0
def adauga(x):
    global total
    total += x
adauga(3)
adauga(4)
""", []),
    'while': ("""
i = 0
while True:
    i += 1
    if i % 2 == 0:
        continue
    if i > 5:
        break
""", []),
    'for_else': ("""
for n in range(2, 6):
    for d in range(2, n):
        if n % d == 0:
            break
    else:
        print(n)
""", []),
    'numpy': ("""
import numpy as np
a = np.array([1, 2, 3])
b = a * 2
m = np.zeros((2, 3))
z = float(b.sum())
""", []),
    'lung': ("""
s = 0
for i in range(1000):
    s += i
""", []),
    'input_epuizat': ("""
a = int(input())
b = int(input())
""", ['5']),
    'recursie': ("""
def perm(pref, rest):
    if not rest:
        print(pref)
        return
    for i in range(len(rest)):
        perm(pref + [rest[i]], rest[:i] + rest[i + 1:])
perm([], [1, 2, 3])
""", []),
    'structuri': ("""
d = {'a': [1, 2], 'b': {'x': (1, 2)}}
s = {(1, 2), (3, 4)}
big = 10 ** 30
f = 0.1 + 0.2
txt = 'a' * 100
n = None
""", []),
    'args': ("""
def f(a, b=2, *args, **kw):
    return a + b + sum(args) + sum(kw.values())
r = f(1, 2, 3, 4, x=5)
""", []),
    'sintaxa': ("""
x = (1 +
""", []),
    'generator': ("""
def numara(n):
    i = 0
    while i < n:
        yield i
        i += 1
for x in numara(3):
    print(x)
""", []),
}


def main():
    esuat = 0
    for nume, (cod, inputs) in CAZURI.items():
        try:
            pasi, out = _colecteaza(cod.strip('\n'), list(inputs), 250)
            ok = len(pasi) > 0
            info = f'{len(pasi)} pasi' + (', eroare: ' + pasi[-1]['err'] if 'err' in pasi[-1] else '') + \
                   (', oprit' if pasi[-1].get('oprit') else '')
        except Exception as e:  # noqa: BLE001
            ok, info = False, f'CRAPA: {type(e).__name__}: {e}'
        esuat += not ok
        print(('OK    ' if ok else 'ESEC  ') + nume + ' - ' + info)
    sys.exit(1 if esuat else 0)


if __name__ == '__main__':
    main()
