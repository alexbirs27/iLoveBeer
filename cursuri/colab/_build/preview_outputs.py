"""Ruleaza un notebook si strange rezultatele HTML (verifica, scor, animatii) intr-o singura pagina, ca sa o vezi in browser.

    python preview_outputs.py 01-structuri-liniare-tema.ipynb [filtru]
filtru: ruleaza doar celulele al caror cod contine textul (implicit: verifica / scor)
"""
import os
import sys
import warnings

import nbformat
from nbclient import NotebookClient

warnings.filterwarnings('ignore')
AICI = os.path.dirname(os.path.abspath(__file__))
COLAB = os.path.normpath(os.path.join(AICI, '..'))


def main():
    os.environ['ONIA_BAZA'] = COLAB + os.sep
    cale = os.path.join(COLAB, sys.argv[1])
    filtru = sys.argv[2] if len(sys.argv) > 2 else None
    nb = nbformat.read(cale, as_version=4)
    NotebookClient(nb, timeout=240, kernel_name='python3', resources={'metadata': {'path': COLAB}}).execute()
    out = ['<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:14px;font-family:system-ui;background:#fff">']
    for c in nb.cells:
        if c.cell_type != 'code':
            continue
        potrivit = (filtru in c.source) if filtru else ('verifica' in c.source or 'scor()' in c.source)
        if not potrivit:
            continue
        out.append('<pre style="background:#f4f4f4;padding:6px;margin:14px 0 4px;font-size:12px;white-space:pre-wrap">'
                   + c.source.replace('<', '&lt;') + '</pre>')
        for o in c.get('outputs', []):
            if o.output_type == 'display_data' and 'text/html' in o.data:
                out.append(o.data['text/html'])
            elif o.output_type == 'stream':
                out.append('<pre>' + o.text.replace('<', '&lt;') + '</pre>')
    out.append('</body></html>')
    dest = os.path.join(AICI, '_preview')
    os.makedirs(dest, exist_ok=True)
    fisier = os.path.join(dest, 'iesiri.html')
    with open(fisier, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print('scris', fisier)


if __name__ == '__main__':
    main()
