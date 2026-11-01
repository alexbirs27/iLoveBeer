"""Executa notebook-urile din colab/ local, ca sa vedem ca nu crapa nimic.

    python test_colab.py 01          # notebook-urile care incep cu 01 (elevi + solutii)
    python test_colab.py all

Notebook-urile pentru elevi trebuie sa ruleze fara erori chiar si cu exercitiile necompletate.
Notebook-urile cu solutii trebuie sa treaca toate exercitiile (asigura_toate() la final).
"""
import glob
import os
import sys
import warnings

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

warnings.filterwarnings('ignore')
AICI = os.path.dirname(os.path.abspath(__file__))
COLAB = os.path.normpath(os.path.join(AICI, '..'))


def ruleaza(cale):
    nb = nbformat.read(cale, as_version=4)
    client = NotebookClient(nb, timeout=240, kernel_name='python3', resources={'metadata': {'path': COLAB}})
    try:
        client.execute()
    except CellExecutionError as e:
        return False, str(e)[-1800:]
    nr_vezi = sum(1 for c in nb.cells if c.cell_type == 'code' and c.source.lstrip().startswith('%%vezi'))
    return True, f'ok ({len(nb.cells)} celule, {nr_vezi} animatii %%vezi)'


def main():
    os.environ['ONIA_BAZA'] = COLAB + os.sep
    prefix = sys.argv[1] if len(sys.argv) > 1 else 'all'
    cai = sorted(glob.glob(os.path.join(COLAB, '[0-9]*.ipynb')) + glob.glob(os.path.join(COLAB, 'solutii', '[0-9]*.ipynb')))
    if prefix != 'all':
        cai = [c for c in cai if os.path.basename(c).startswith(prefix)]
    esuat = 0
    for c in cai:
        ok, msg = ruleaza(c)
        print(('OK    ' if ok else 'ESEC  ') + os.path.relpath(c, COLAB) + ' - ' + msg)
        esuat += not ok
    print(f'\n{len(cai) - esuat}/{len(cai)} notebook-uri ruleaza curat')
    sys.exit(1 if esuat else 0)


if __name__ == '__main__':
    main()
