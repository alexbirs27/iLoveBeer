"""Genereaza cursuri/colab/README.md din notebook-urile care exista (tabel cu badge-uri Colab).

    python gen_readme.py
"""
import glob
import os
import re

import nbformat

AICI = os.path.dirname(os.path.abspath(__file__))
COLAB = os.path.normpath(os.path.join(AICI, '..'))
REPO = 'alexbirs27/iLoveBeer'
CALE = 'cursuri/colab/'


def badge(nume):
    url = f'https://colab.research.google.com/github/{REPO}/blob/main/{CALE}{nume}'
    return f'[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url})'


def titlu(nume):
    nb = nbformat.read(os.path.join(COLAB, nume), as_version=4)
    m = re.match(r'#\s+(.*?)\s+\((predare|tema)\)', nb.cells[0].source)
    return m.group(1) if m else nume


def main():
    seturi = {}
    for cale in sorted(glob.glob(os.path.join(COLAB, '[0-9][0-9]-*.ipynb'))):
        nume = os.path.basename(cale)
        m = re.match(r'(\d\d)-(.*?)(?:-(predare|tema))?\.ipynb$', nume)
        if not m:
            continue
        nr, slug, tip = m.groups()
        tip = tip or 'tema'
        seturi.setdefault((nr, slug), {})[tip] = nume
    linii = []
    for (nr, slug), fis in seturi.items():
        ref = fis.get('predare') or fis['tema']
        linii.append(f"| {nr} | {titlu(ref)} | {badge(fis['predare']) if 'predare' in fis else ''} | "
                     f"{badge(fis['tema']) if 'tema' in fis else ''} |")
    text = f"""# Colab-uri pentru cursul ONIA

Deschizi un notebook cu un click, apesi **Copy to Drive** si lucrezi pe copia ta. Nu poti strica originalul.

Fiecare topic are doua notebook-uri:

- **predare** - cel pe care il parcurgem la curs: concept, animatie, varianta de mana, scurtatura, capcane, exercitii cu verificare pe loc.
- **tema** - exercitiile de acasa, cu teste ascunse ca la concurs si punctaj la final.

Celulele care incep cu `%%vezi` iti arata codul rulat pas cu pas (linia curenta, memoria, ce afiseaza programul).
Prima celula din fiecare notebook aduce utilitarele (`onia.py`); ruleaz-o o singura data.

| # | topic | predare | tema |
|---|---|---|---|
{chr(10).join(linii)}

## Pentru profesor

- La curs: deschizi notebook-ul de predare pe proiector, rulezi celulele pe rand, cei din clasa raspund la blocurile "Prezice" inainte sa dai Run.
- Dupa curs: trimiti linkul de la tema. Solutiile sunt in `solutii/` (folder ignorat local de git; le publici tu, cand vrei, cu `git add -f`).
- Randarea o poti verifica local: `python _build/test_colab.py all` ruleaza toate notebook-urile (elevi si solutii).
- Ghidul pentru scris notebook-uri noi: `_build/GHID.md`. Exemplul de referinta: `_build/gen_01_liniare.py`.
"""
    with open(os.path.join(COLAB, 'README.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print('scris README.md cu', len(linii), 'seturi')


if __name__ == '__main__':
    main()
