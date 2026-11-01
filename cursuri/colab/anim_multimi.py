"""Animatii pentru notebook-urile despre multimi: tabela de dispersie (hash) si diagrame Venn."""
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML
from matplotlib import animation
from matplotlib.patches import Circle, FancyBboxPatch

__all__ = ['hash_simplu', 'anim_hash', 'anim_venn']


def hash_simplu(x):
    """Hash didactic: numarul insusi pentru int, suma codurilor caracterelor pentru text."""
    if isinstance(x, str):
        return sum(ord(c) for c in x)
    return int(x)


def _cadre_hash(valori, buckete, cauta):
    """Pregateste cadrele (starea desenului la fiecare pas) pentru anim_hash."""
    b = [[] for _ in range(buckete)]
    cadre = [dict(b=[list(x) for x in b], val=None, k=None, msg='bucketele sunt goale, incepem sa adaugam', col=False)]
    for v in valori:
        h = hash_simplu(v)
        k = h % buckete
        col = v not in b[k] and len(b[k]) > 0
        if v in b[k]:
            msg = f'hash({v!r}) = {h}, {h} % {buckete} = {k}. Bucketul {k} il contine deja pe {v!r}: dublura, nu se adauga'
        else:
            msg = f'hash({v!r}) = {h}, {h} % {buckete} = {k}, deci merge in bucketul {k}'
        cadre.append(dict(b=[list(x) for x in b], val=v, k=k, msg=msg, col=False, sageata=True))
        adaugat = v not in b[k]
        if adaugat:
            b[k].append(v)
        if col:
            msg = f'COLIZIUNE: in bucketul {k} era deja {b[k][:-1]}, {v!r} se pune langa'
        elif not adaugat:
            msg = f'{v!r} era deja in bucketul {k}, setul nu are dubluri'
        elif len(b[k]) == 1:
            msg = f'{v!r} sta singur in bucketul {k}'
        else:
            msg = f'{v!r} este in bucketul {k}'
        cadre.append(dict(b=[list(x) for x in b], val=None, k=k, msg=msg, col=col, nou=v if adaugat else None))
    if cauta is not None:
        h = hash_simplu(cauta)
        k = h % buckete
        cadre.append(dict(b=[list(x) for x in b], val=cauta, k=k, sageata=True, cautare=True, col=False,
                          msg=f'cautam {cauta!r}: hash = {h}, {h} % {buckete} = {k}. Ne uitam DOAR in bucketul {k}'))
        gasit = False
        for idx, e in enumerate(b[k]):
            gasit = e == cauta
            cadre.append(dict(b=[list(x) for x in b], val=cauta, k=k, cautare=True, col=False, comp=(k, idx, gasit),
                              msg=f'comparam {cauta!r} cu {e!r}: ' + ('gasit!' if gasit else 'nu e el')))
            if gasit:
                break
        total = len(valori)
        if gasit:
            fin = f'{cauta!r} exista. Am comparat cu cel mult {len(b[k])} elemente, nu cu toate cele {total}'
        else:
            fin = f'{cauta!r} nu exista. Am verificat doar {len(b[k])} elemente, nu toate cele {total}'
        cadre.append(dict(b=[list(x) for x in b], val=None, k=k, col=False, cautare=True, msg=fin))
    return cadre


def anim_hash(valori, buckete=8, cauta=None):
    """Arata cum ajung valorile in bucketele unei tabele hash (hash % buckete), cu coliziuni. Optional: cauta o valoare."""
    valori = list(valori)
    if len(valori) > 22:
        raise ValueError('maxim 22 de valori, altfel animatia devine prea lunga')
    cadre = _cadre_hash(valori, buckete, cauta)
    stiva = max(3, max(len(x) for c in cadre for x in c['b']))
    inalt = 1.0 + 0.72 * stiva
    fig, ax = plt.subplots(figsize=(min(9, 0.95 * buckete + 1), 4.4), dpi=80)

    def deseneaza(k):
        c = cadre[k]
        ax.clear()
        ax.set_xlim(-0.2, buckete + 0.2)
        ax.set_ylim(-0.3, inalt + 2.2)
        ax.axis('off')
        for i in range(buckete):
            hi = c['k'] == i
            ax.add_patch(FancyBboxPatch((i + 0.08, 0.0), 0.84, 0.6, boxstyle='round,pad=0.02',
                                        fc='#ffe066' if hi else '#dee2e6', ec='#868e96'))
            ax.text(i + 0.5, 0.3, str(i), ha='center', va='center', fontsize=12, fontweight='bold')
            for lvl, e in enumerate(c['b'][i]):
                nou = c.get('nou') is not None and hi and lvl == len(c['b'][i]) - 1 and e == c['nou']
                rosu = nou and c['col']
                verde = c.get('comp') == (i, lvl, True)
                ax.add_patch(FancyBboxPatch((i + 0.1, 0.8 + 0.72 * lvl), 0.8, 0.58, boxstyle='round,pad=0.02',
                                            fc='#8ce99a' if verde else ('#ffc9c9' if rosu else ('#d0ebff' if not nou else '#ffd8a8')),
                                            ec='#e03131' if rosu else '#1c7ed6', lw=2 if rosu else 1))
                ax.text(i + 0.5, 0.8 + 0.72 * lvl + 0.29, str(e), ha='center', va='center', fontsize=10)
        if c.get('val') is not None:
            xv = buckete / 2
            ax.add_patch(FancyBboxPatch((xv - 0.6, inalt + 0.55), 1.2, 0.6, boxstyle='round,pad=0.02',
                                        fc='#ffd8a8' if not c.get('cautare') else '#e5dbff', ec='#e8590c'))
            ax.text(xv, inalt + 0.85, str(c['val']), ha='center', va='center', fontsize=12, fontweight='bold')
            if c.get('sageata'):
                cap = 0.8 + 0.72 * len(c['b'][c['k']]) + 0.05
                ax.annotate('', xy=(c['k'] + 0.5, cap), xytext=(xv, inalt + 0.5),
                            arrowprops=dict(arrowstyle='->', color='#e8590c', lw=2))
        ax.text(buckete / 2, inalt + 1.75, c['msg'], ha='center', va='center', fontsize=10,
                color='#c92a2a' if c['col'] else '#212529', wrap=True)

    ani = animation.FuncAnimation(fig, deseneaza, frames=len(cadre), interval=1100, repeat=False, blit=False)
    html = ani.to_jshtml()
    plt.close(fig)
    return HTML(html)


# ---------------------------------------------------------------------------
# Venn
# ---------------------------------------------------------------------------

_OPERATII = {
    '|': 'reuniune', 'reuniune': 'reuniune', 'union': 'reuniune',
    '&': 'intersectie', 'intersectie': 'intersectie', 'intersection': 'intersectie',
    '-': 'diferenta', 'diferenta': 'diferenta', 'difference': 'diferenta',
    'b-a': 'diferenta_inv', 'diferenta_inv': 'diferenta_inv',
    '^': 'simetrica', 'simetrica': 'simetrica', 'symmetric_difference': 'simetrica',
}
_TITLURI = {'reuniune': 'A | B  (reuniune)', 'intersectie': 'A & B  (intersectie)', 'diferenta': 'A - B  (diferenta)',
            'diferenta_inv': 'B - A  (diferenta)', 'simetrica': 'A ^ B  (diferenta simetrica)'}
_RA, _RB, _R = (-0.65, 0.0), (0.65, 0.0), 1.25


def _sortat(elem):
    try:
        return sorted(elem)
    except TypeError:
        return sorted(elem, key=repr)


def _pozitii(k, region):
    """k puncte bine imprastiate intr-o regiune a diagramei: 'A', 'B' sau 'AB'."""
    if k == 0:
        return []
    cand = []
    for x in np.arange(-2.2, 2.21, 0.2):
        for y in np.arange(-1.15, 1.16, 0.2):
            da = np.hypot(x - _RA[0], y - _RA[1])
            db = np.hypot(x - _RB[0], y - _RB[1])
            m = 0.3
            if region == 'AB' and da < _R - m and db < _R - m:
                cand.append((x, y))
            elif region == 'A' and da < _R - m and db > _R + 0.12:
                cand.append((x, y))
            elif region == 'B' and db < _R - m and da > _R + 0.12:
                cand.append((x, y))
    cand = np.array(cand)
    centru = cand.mean(axis=0)
    alese = [cand[np.argmin(np.hypot(*(cand - centru).T))]]
    while len(alese) < k:
        d = np.min([np.hypot(*(cand - p).T) for p in alese], axis=0)
        if d.max() < 0.05:            # nu mai e loc: refolosim pozitii usor decalate
            alese.append(alese[len(alese) % len(cand)] + np.array([0.0, 0.11]))
        else:
            alese.append(cand[np.argmax(d)])
    return [tuple(p) for p in alese]


def anim_venn(A, B, operatie='|'):
    """Diagrama Venn cu elementele ca puncte; coloreaza rezultatul unei operatii: | & - ^ (sau b-a)."""
    op = _OPERATII.get(str(operatie).lower())
    if op is None:
        raise ValueError(f'operatie necunoscuta: {operatie!r}. Foloseste una dintre: | & - ^ b-a')
    A, B = set(A), set(B)
    rez = {'reuniune': A | B, 'intersectie': A & B, 'diferenta': A - B, 'diferenta_inv': B - A, 'simetrica': A ^ B}[op]
    doar_a, doar_b, comune = _sortat(A - B), _sortat(B - A), _sortat(A & B)
    poz = {}
    for elem, reg in ((doar_a, 'A'), (doar_b, 'B'), (comune, 'AB')):
        for e, p in zip(elem, _pozitii(len(elem), reg)):
            poz[e] = p
    ordine = _sortat(A | B)

    xs, ys = np.meshgrid(np.linspace(-2.3, 2.3, 460), np.linspace(-1.5, 1.5, 300))
    in_a = np.hypot(xs - _RA[0], ys - _RA[1]) < _R
    in_b = np.hypot(xs - _RB[0], ys - _RB[1]) < _R
    masca = {'reuniune': in_a | in_b, 'intersectie': in_a & in_b, 'diferenta': in_a & ~in_b,
             'diferenta_inv': in_b & ~in_a, 'simetrica': in_a ^ in_b}[op]

    fig, ax = plt.subplots(figsize=(6.2, 4.3), dpi=80)
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    zona = ax.imshow(np.where(masca, 1.0, np.nan), extent=(-2.3, 2.3, -1.5, 1.5), origin='lower',
                     cmap='Greens', vmin=0, vmax=2, alpha=0.0, zorder=0)
    for c, nume, col in ((_RA, 'A', '#1c7ed6'), (_RB, 'B', '#e8590c')):
        ax.add_patch(Circle(c, _R, fill=False, ec=col, lw=2.5, zorder=2))
        ax.text(c[0] + (-1 if nume == 'A' else 1) * 0.95, 1.22, nume, color=col, fontsize=15, fontweight='bold', ha='center')
    puncte, texte = {}, {}
    for e in ordine:
        x, y = poz[e]
        puncte[e], = ax.plot([x], [y], 'o', color='#495057', ms=5, zorder=3)
        texte[e] = ax.text(x, y + 0.09, str(e), ha='center', va='bottom', fontsize=11, color='#212529', zorder=4)
    titlu = ax.set_title(_TITLURI[op], fontsize=13)
    jos = ax.text(0, -1.42, '', ha='center', va='center', fontsize=11, zorder=5)
    cadre = list(range(len(ordine) + 2))

    def update(k):
        zona.set_alpha(0.0 if k == 0 else 0.55)
        vazute = ordine[:max(0, k - 1)]
        for e in ordine:
            if k <= 1:
                puncte[e].set_color('#495057')
                texte[e].set_color('#212529')
                texte[e].set_fontweight('normal')
            elif e in vazute:
                da = e in rez
                puncte[e].set_color('#2b8a3e' if da else '#adb5bd')
                texte[e].set_color('#2b8a3e' if da else '#adb5bd')
                texte[e].set_fontweight('bold' if da else 'normal')
            else:
                puncte[e].set_color('#495057')
                texte[e].set_color('#212529')
                texte[e].set_fontweight('normal')
        if k == 0:
            jos.set_text(f'A = {set(_sortat(A))}   B = {set(_sortat(B))}'.replace('set()', '{}'))
        elif k == 1:
            jos.set_text('zona colorata = ce intra in rezultat')
        else:
            gata = [e for e in vazute if e in rez]
            jos.set_text('rezultat: {' + ', '.join(map(repr, gata)) + '}')
        return []

    ani = animation.FuncAnimation(fig, update, frames=cadre, interval=650, repeat=False, blit=False)
    html = ani.to_jshtml()
    plt.close(fig)
    return HTML(html)
