"""Constructor de notebook-uri pentru colab-urile cursului.

Scrii celulele ca text Python, iese un .ipynb pentru elevi (cu exercitiile goale) si unul cu solutii.

    from nb import Carnet
    c = Carnet('Structuri liniare', 'predare')
    c.md('## Titlu\\n\\ntext')
    c.cod('print(1)')
    c.ex('def f(x):\\n    pass  # TODO', 'def f(x):\\n    return x')   # stub pentru elevi / solutie
    c.salveaza('01-structuri-liniare-predare')
"""
import os
import nbformat as nbf

AICI = os.path.dirname(os.path.abspath(__file__))
COLAB = os.path.normpath(os.path.join(AICI, '..'))
URL = 'https://raw.githubusercontent.com/alexbirs27/iLoveBeer/main/cursuri/colab/'


def _ascii(text, unde):
    for n, ch in enumerate(text):
        if not ch.isascii():
            ctx = text[max(0, n - 25):n + 25].replace('\n', ' ')
            raise ValueError(f'caracter non-ASCII {ch!r} (diacritice, cratima lunga, emoji nu sunt permise) in {unde}: ...{ctx}...')


class Carnet:
    def __init__(self, titlu, tip, fisiere=()):
        """tip: 'predare' sau 'tema'. fisiere: fisiere de adus la pornire, ex ('date/elevi.csv', 'anim_liste.py')."""
        assert tip in ('predare', 'tema')
        self.titlu, self.tip, self.celule = titlu, tip, []
        self._pornire(fisiere)

    def _pornire(self, fisiere):
        extra = ''.join(f"descarca({', '.join(repr(f) for f in fisiere)})\n" for _ in [0] if fisiere)
        anim = [f for f in fisiere if f.endswith('.py')]
        imp = ''.join(f'from {f[:-3]} import *\n' for f in anim)
        cod = ("import os, urllib.request\n"
               "if not os.path.exists('onia.py'):\n"
               f"    urllib.request.urlretrieve('{URL}onia.py', 'onia.py')\n"
               "from onia import *\n" + extra + imp).rstrip()
        banner = (f"# {self.titlu} ({'predare' if self.tip == 'predare' else 'tema'})\n\n"
                  "Apasa **Copy to Drive** (sus, in stanga) inainte sa scrii ceva aici, altfel tot ce faci "
                  "dispare cand inchizi tab-ul.\n\n"
                  "Ruleaza prima celula de mai jos, o singura data, ca sa aduci utilitarele cursului.")
        self.md(banner)
        self.cod(cod)

    def md(self, text):
        text = text.strip('\n')
        _ascii(text, 'markdown')
        self.celule.append(('md', text, None))

    def cod(self, src):
        src = src.strip('\n')
        _ascii(src, 'cod')
        self.celule.append(('cod', src, None))

    def ex(self, stub, solutie):
        """Celula pe care o completeaza elevul. In notebook-ul cu solutii apare solutia."""
        stub, solutie = stub.strip('\n'), solutie.strip('\n')
        _ascii(stub, 'ex stub')
        _ascii(solutie, 'ex solutie')
        self.celule.append(('ex', stub, solutie))

    def _construieste(self, cu_solutii):
        nb = nbf.v4.new_notebook()
        nb.metadata['kernelspec'] = {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}
        nb.metadata['language_info'] = {'name': 'python'}
        cells = []
        for tip, src, sol in self.celule:
            if tip == 'md':
                cells.append(nbf.v4.new_markdown_cell(src))
            else:
                cells.append(nbf.v4.new_code_cell(sol if (tip == 'ex' and cu_solutii) else src))
        if cu_solutii:
            cells.append(nbf.v4.new_code_cell('asigura_toate()'))
        nb.cells = cells
        return nb

    def salveaza(self, nume):
        """Scrie ../<nume>.ipynb (elevi) si ../solutii/<nume>-solutii.ipynb."""
        os.makedirs(os.path.join(COLAB, 'solutii'), exist_ok=True)
        nbf.write(self._construieste(False), os.path.join(COLAB, nume + '.ipynb'))
        nbf.write(self._construieste(True), os.path.join(COLAB, 'solutii', nume + '-solutii.ipynb'))
        print('scris', nume)
