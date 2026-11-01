"""Animatii pentru recursivitate: arborele de apeluri al lui fib naiv si umplerea memoriei (memoizare)."""
import math

from IPython.display import HTML
from matplotlib import animation
import matplotlib.pyplot as plt

__all__ = ['anim_arbore_fib', 'anim_memo_fib']

_VERDE, _ROSU, _GALBEN, _ALBASTRU, _GRI, _PORTOCALIU = '#b2f2bb', '#ffa8a8', '#ffe066', '#a5d8ff', '#ced4da', '#ff922b'


def _arbore_naiv(n):
    """Nodurile apelurilor lui fib(n) naiv, in ordinea in care sunt apelate: (arg, parinte, adancime)."""
    noduri = []

    def fib(m, parinte, adanc):
        i = len(noduri)
        noduri.append({'arg': m, 'p': parinte, 'd': adanc, 'copii': []})
        if parinte is not None:
            noduri[parinte]['copii'].append(i)
        if m >= 2:
            fib(m - 1, i, adanc + 1)
            fib(m - 2, i, adanc + 1)

    fib(n, None, 0)
    return noduri


def _pozitii(noduri):
    """x = media copiilor, frunzele pe pozitii consecutive; y = -adancime."""
    frunza = [0]
    x = [0.0] * len(noduri)

    def pune(i):
        if not noduri[i]['copii']:
            x[i] = frunza[0]
            frunza[0] += 1
        else:
            for c in noduri[i]['copii']:
                pune(c)
            x[i] = sum(x[c] for c in noduri[i]['copii']) / len(noduri[i]['copii'])

    pune(0)
    return x, [-nod['d'] for nod in noduri]


def _subarbore(noduri, i):
    ies = {i}
    for c in noduri[i]['copii']:
        ies |= _subarbore(noduri, c)
    return ies


def _deseneaza_arbore(ax, noduri, x, y, dim):
    linii, texte = [], []
    for i, nod in enumerate(noduri):
        if nod['p'] is None:
            linii.append(None)
        else:
            p = nod['p']
            (l,) = ax.plot([x[p], x[i]], [y[p], y[i]], color='#868e96', lw=1, zorder=1, visible=False)
            linii.append(l)
        t = ax.text(x[i], y[i], str(nod['arg']), ha='center', va='center', fontsize=dim, zorder=2, visible=False,
                    bbox=dict(boxstyle='circle,pad=0.25', fc=_VERDE, ec='#495057', lw=1))
        texte.append(t)
    return linii, texte


def anim_arbore_fib(n, apeluri=None):
    """Arborele de apeluri al lui fib(n) naiv, apel cu apel. apeluri = numarul numarat de tine (apare la final)."""
    n = max(2, min(int(n), 8))
    noduri = _arbore_naiv(n)
    total = len(noduri)
    x, y = _pozitii(noduri)
    aparut = {}
    for i, nod in enumerate(noduri):
        aparut[i] = nod['arg'] in [noduri[j]['arg'] for j in range(i)]     # a mai fost apelat inainte?
    repetate = [a for a in range(n - 1, 1, -1) if sum(1 for nod in noduri if nod['arg'] == a) >= 2]
    h = repetate[0] if repetate else None
    radacini = [i for i, nod in enumerate(noduri) if h is not None and nod['arg'] == h]
    izolate = set().union(*[_subarbore(noduri, r) for r in radacini]) if radacini else set()

    pas = max(1, math.ceil(total / 45))
    cadre = list(range(0, total, pas)) + [total - 1]
    cadre = [('apel', k) for k in cadre]
    if h is not None:
        cadre += [('repetat', 0)] * 2
    cadre += [('final', 0)] * 3

    fig, ax = plt.subplots(figsize=(7 if total <= 45 else 8.5, 4.6), dpi=70)
    fig.subplots_adjust(bottom=0.14)
    dim = 11 if total <= 30 else (9 if total <= 50 else 8)
    linii, texte = _deseneaza_arbore(ax, noduri, x, y, dim)
    ax.set_xlim(-0.8, max(x) + 0.8)
    ax.set_ylim(min(y) - 0.7, 0.8)
    ax.axis('off')
    titlu = ax.set_title('', fontsize=12)
    jos = ax.text(0.5, -0.03, '', transform=ax.transAxes, ha='center', va='top', fontsize=11)
    ax.text(0.01, 0.99, 'verde = apel nou\nrosu = apel repetat', transform=ax.transAxes, va='top', fontsize=9, color='#495057')

    def update(k):
        tip, ind = cadre[k]
        ultim = ind if tip == 'apel' else total - 1
        for i in range(total):
            vazut = i <= ultim
            texte[i].set_visible(vazut)
            if linii[i] is not None:
                linii[i].set_visible(vazut)
            if not vazut:
                continue
            fc = _ROSU if aparut[i] else _VERDE
            lw, alpha = 1, 1.0
            if tip == 'repetat':
                fc = _PORTOCALIU if i in izolate else _GRI
                alpha = 1.0 if i in izolate else 0.45
            elif tip == 'apel' and i == ind:
                fc, lw = _GALBEN, 2.5
            texte[i].get_bbox_patch().set(fc=fc, lw=lw, alpha=alpha)
            texte[i].set_alpha(alpha)
        if tip == 'apel':
            titlu.set_text(f'fib({n}): apelul #{ind + 1} este fib({noduri[ind]["arg"]})')
            jos.set_text(f'apeluri pana acum: {ind + 1}')
        elif tip == 'repetat':
            nr = len(radacini)
            titlu.set_text(f'fib({h}) e calculat de {nr} ori, de fiecare data de la zero')
            jos.set_text('portocaliu = munca repetata degeaba')
        else:
            txt = f'fib({n}) a facut {total} apeluri, dar sunt doar {n + 1} valori diferite (fib(0)..fib({n}))'
            if apeluri is not None:
                txt += f'\ntu ai numarat: {apeluri}' + ('  (corect)' if apeluri == total else f'  (ai gresit ceva, trebuie {total})')
            titlu.set_text(f'gata: {total} apeluri')
            jos.set_text(txt)
        return []

    ani = animation.FuncAnimation(fig, update, frames=len(cadre), interval=450, blit=False)
    html = ani.to_jshtml()
    plt.close(fig)
    return HTML(html)


def _arbore_memo(n):
    """Apelurile lui fib(n) cu memoizare: noduri + lista de evenimente ('apel', i) / ('gata', i, valoare)."""
    noduri, evenimente, memo = [], [], {}

    def fib(m, parinte, adanc):
        i = len(noduri)
        hit = m in memo
        noduri.append({'arg': m, 'p': parinte, 'd': adanc, 'copii': [], 'hit': hit})
        if parinte is not None:
            noduri[parinte]['copii'].append(i)
        evenimente.append(('apel', i, None))
        if hit:
            return memo[m]
        r = m if m < 2 else fib(m - 1, i, adanc + 1) + fib(m - 2, i, adanc + 1)
        memo[m] = r
        evenimente.append(('gata', i, r))
        return r

    fib(n, None, 0)
    return noduri, evenimente


def anim_memo_fib(n):
    """fib(n) cu memoizare: arborele de apeluri (gri = valoare luata din memorie) si tabelul memo care se umple."""
    n = max(2, min(int(n), 12))
    noduri, ev = _arbore_memo(n)
    total = len(noduri)
    x, y = _pozitii(noduri)
    fig, (ax, at) = plt.subplots(2, 1, figsize=(7, 4.6), dpi=70, gridspec_kw={'height_ratios': [4, 1]})
    linii, texte = _deseneaza_arbore(ax, noduri, x, y, 10)
    ax.set_xlim(-0.8, max(x) + 0.8)
    ax.set_ylim(min(y) - 0.7, 0.8)
    ax.axis('off')
    titlu = ax.set_title('', fontsize=12)
    ax.text(0.01, 0.99, 'albastru = ruleaza\nverde = calculat\ngri = luat din memo', transform=ax.transAxes, va='top',
            fontsize=9, color='#495057')
    at.set_xlim(-1.6, n + 0.5)
    at.set_ylim(-0.6, 1.5)
    at.axis('off')
    celule = []
    for m in range(n + 1):
        at.text(m, 1.15, str(m), ha='center', va='center', fontsize=9, color='#868e96')
        celule.append(at.text(m, 0.3, '', ha='center', va='center', fontsize=10,
                              bbox=dict(boxstyle='square,pad=0.35', fc='white', ec='#adb5bd')))
    at.text(-0.6, 0.3, 'memo', fontsize=10, ha='right', va='center', color='#495057')

    def update(k):
        stare = {}                 # nod -> 'ruleaza' / 'gata' / 'hit'
        plin = {}
        for j in range(k + 1):
            tip, i, val = ev[j]
            if tip == 'apel':
                stare[i] = 'hit' if noduri[i]['hit'] else 'ruleaza'
            else:
                stare[i] = 'gata'
                plin[noduri[i]['arg']] = val
        tip, i, _ = ev[k]
        for j in range(total):
            vazut = j in stare
            texte[j].set_visible(vazut)
            if linii[j] is not None:
                linii[j].set_visible(vazut)
            if vazut:
                fc = {'ruleaza': _ALBASTRU, 'gata': _VERDE, 'hit': _GRI}[stare[j]]
                if j == i:
                    fc = _GALBEN
                texte[j].get_bbox_patch().set(fc=fc, lw=2.5 if j == i else 1)
        for m in range(n + 1):
            celule[m].set_text(str(plin[m]) if m in plin else '  ')
            celule[m].get_bbox_patch().set(fc=_GALBEN if (tip == 'gata' and noduri[i]['arg'] == m) else 'white')
        nr_apeluri = sum(1 for e in ev[:k + 1] if e[0] == 'apel')
        if k == len(ev) - 1:
            titlu.set_text(f'gata: fib({n}) = {plin[n]} din doar {total} apeluri')
        elif tip == 'apel':
            titlu.set_text(f'apel fib({noduri[i]["arg"]})' + ('  -> gasit in memo, fara calcul' if noduri[i]['hit'] else ''))
        else:
            titlu.set_text(f'fib({noduri[i]["arg"]}) = {val}  -> il scriem in memo (apeluri: {nr_apeluri})')
        return []

    cadre = list(range(len(ev))) + [len(ev) - 1] * 3
    ani = animation.FuncAnimation(fig, lambda k: update(min(k, len(ev) - 1)), frames=len(cadre), interval=550, blit=False)
    html = ani.to_jshtml()
    plt.close(fig)
    return HTML(html)
