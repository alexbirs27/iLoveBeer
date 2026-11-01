"""Animatii pentru notebook-urile despre normalizare / scalare (matplotlib, se afiseaza cu to_jshtml)."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Rectangle
from matplotlib.ticker import MaxNLocator
from IPython.display import HTML

__all__ = ['anim_transformare', 'anim_scatter_transformare', 'anim_outlier', 'anim_linii',
           'compara_hist', 'arata_train_test']

BRUT = '#d9730d'     # portocaliu: valorile initiale
NOU = '#2b6cb0'      # albastru: valorile transformate
GRI = '#8a94a0'
ROSU = '#c92a2a'
VERDE = '#2f9e44'
DPI = 75


def _mix(t):
    a, b = np.array(matplotlib_rgb(BRUT)), np.array(matplotlib_rgb(NOU))
    return tuple((1 - t) * a + t * b)


def matplotlib_rgb(c):
    return tuple(int(c[i:i + 2], 16) / 255 for i in (1, 3, 5))


def _ease(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def _f(v):
    v = float(v)
    if abs(v) >= 1000:
        return f'{v:.0f}'
    return f'{v:.3g}'


def _html(fig, ani, fps=10):
    h = ani.to_jshtml(fps=fps)
    plt.close(fig)
    return HTML(h)


def _limite(v, extra=None, pad=0.08):
    lo, hi = float(np.min(v)), float(np.max(v))
    if extra:
        lo, hi = min(lo, min(extra)), max(hi, max(extra))
    if hi == lo:
        lo, hi = lo - 1, hi + 1
    d = (hi - lo) * pad
    return lo - d, hi + d


def _bara(ax, y, lo, hi, culoare, nume):
    """Deseneaza o dreapta numerica orizontala (bara) la inaltimea y, cu gradatii rotunde."""
    ax.plot([0.04, 0.96], [y, y], color=GRI, lw=1.2, zorder=1)
    for g in MaxNLocator(5, steps=[1, 2, 5, 10]).tick_values(lo, hi):
        if lo <= g <= hi:
            x = 0.04 + 0.92 * (g - lo) / (hi - lo)
            ax.plot([x, x], [y - 0.015, y + 0.015], color=GRI, lw=1, zorder=1)
            ax.text(x, y - 0.06, _f(g), ha='center', va='top', fontsize=7.5, color=GRI)
    ax.text(-0.14, y, nume, ha='left', va='center', fontsize=9, color=culoare, fontweight='bold')


def _poz(v, lo, hi):
    return 0.04 + 0.92 * (np.asarray(v, float) - lo) / (hi - lo)


def anim_transformare(brut, transformat, titlu='', zone_brut=None, zone_transf=None):
    """Valorile 'brut' aluneca de pe dreapta de sus pe cea de jos, unde au valorile 'transformat'.
    zone_brut / zone_transf: lista de intervale (lo, hi) umbrite pe dreapta respectiva."""
    brut, transformat = np.asarray(brut, float), np.asarray(transformat, float)
    n = len(brut)
    assert n == len(transformat), 'brut si transformat trebuie sa aiba aceeasi lungime'
    zb, zt = list(zone_brut or []), list(zone_transf or [])
    lo_b, hi_b = _limite(brut, [x for z in zb for x in z])
    lo_t, hi_t = _limite(transformat, [x for z in zt for x in z])
    x0, x1 = _poz(brut, lo_b, hi_b), _poz(transformat, lo_t, hi_t)
    yt, yb = 0.7, 0.2
    rng = np.random.default_rng(0)
    jit = rng.uniform(-0.035, 0.035, n) if n > 12 else np.zeros(n)
    rang = np.argsort(np.argsort(brut))
    intarziere = 0.4 * rang / max(1, n - 1)
    fig, ax = plt.subplots(figsize=(7, 2.9), dpi=DPI)
    ax.set_xlim(-0.15, 1.02)
    ax.set_ylim(0.02, 1.0)
    ax.axis('off')
    for (a, b), y, lo, hi in [(z, yt, lo_b, hi_b) for z in zb] + [(z, yb, lo_t, hi_t) for z in zt]:
        ax.add_patch(Rectangle((_poz(a, lo, hi), y - 0.05), _poz(b, lo, hi) - _poz(a, lo, hi), 0.1,
                               color=VERDE, alpha=0.18, lw=0, zorder=0))
    _bara(ax, yt, lo_b, hi_b, BRUT, 'brut')
    _bara(ax, yb, lo_t, hi_t, NOU, 'transformat')
    if n <= 40:
        for i in range(n):
            ax.plot([x0[i], x1[i]], [yt + jit[i], yb + jit[i]], color=GRI, lw=0.5, alpha=0.35, zorder=1)
    pct = ax.scatter(x0, yt + jit, s=70 if n <= 12 else 22, color=BRUT, zorder=3, edgecolor='white', linewidth=0.8)
    etic = [ax.text(x0[i], yt + 0.06, '', ha='center', fontsize=8, color='#333') for i in range(n)] if n <= 12 else []
    tt = ax.text(0.5, 0.97, titlu, ha='center', fontsize=10, fontweight='bold', color='#333')
    N_START, N_MISCARE, N_FINAL = 6, 26, 8
    total = N_START + N_MISCARE + N_FINAL

    def update(f):
        t = min(1.0, max(0.0, (f - N_START) / N_MISCARE))
        p = np.array([_ease((t - intarziere[i]) / 0.6) for i in range(n)])
        x = (1 - p) * x0 + p * x1
        y = (1 - p) * (yt + jit) + p * (yb + jit)
        pct.set_offsets(np.c_[x, y])
        pct.set_color([_mix(v) for v in p])
        for i, e in enumerate(etic):
            v = (1 - p[i]) * brut[i] + p[i] * transformat[i]
            e.set_position((x[i], y[i] + (0.06 if rang[i] % 2 == 0 else 0.14)))
            e.set_text(_f(v))
        return []

    ani = animation.FuncAnimation(fig, update, frames=total, interval=100, blit=False)
    return _html(fig, ani)


def anim_scatter_transformare(brut, transformat, nume=('x', 'y'), titlu=''):
    """Doua coloane (n, 2): norul de puncte brut (cu aceeasi scara pe ambele axe) devine cel transformat."""
    brut, transformat = np.asarray(brut, float), np.asarray(transformat, float)

    def norm(a):
        lo, hi = a.min(0), a.max(0)
        c = (lo + hi) / 2
        span = max((hi - lo).max(), 1e-12)
        return (a - c) / span, (lo - c) / span, (hi - c) / span

    s0, lo0, hi0 = norm(brut)
    s1, lo1, hi1 = norm(transformat)
    fig, ax = plt.subplots(figsize=(5.6, 4.4), dpi=DPI)
    ax.set_xlim(-0.62, 0.62)
    ax.set_ylim(-0.62, 0.62)
    ax.set_aspect('equal')
    ax.axis('off')
    cutie = Rectangle((lo0[0], lo0[1]), hi0[0] - lo0[0], hi0[1] - lo0[1], fill=False, ec=GRI, ls='--', lw=1)
    ax.add_patch(cutie)
    pct = ax.scatter(s0[:, 0], s0[:, 1], s=14, color=BRUT, alpha=0.75, zorder=3)
    txt = ax.text(0, -0.6, '', ha='center', va='top', fontsize=8.5, color='#333')
    ax.text(0, 0.6, titlu, ha='center', va='bottom', fontsize=10, fontweight='bold', color='#333')
    N_START, N_MISCARE, N_FINAL = 8, 24, 10

    def dom(a):
        return f'{nume[0]}: {_f(a[:, 0].min())} .. {_f(a[:, 0].max())}   {nume[1]}: {_f(a[:, 1].min())} .. {_f(a[:, 1].max())}'

    def update(f):
        p = _ease((f - N_START) / N_MISCARE)
        pct.set_offsets((1 - p) * s0 + p * s1)
        pct.set_color(_mix(p))
        lo, hi = (1 - p) * lo0 + p * lo1, (1 - p) * hi0 + p * hi1
        cutie.set_xy((lo[0], lo[1]))
        cutie.set_width(hi[0] - lo[0])
        cutie.set_height(hi[1] - lo[1])
        txt.set_text(dom(brut if p < 0.5 else transformat))
        return []

    ani = animation.FuncAnimation(fig, update, frames=N_START + N_MISCARE + N_FINAL, interval=100, blit=False)
    return _html(fig, ani)


def _minmax_implicit(v):
    lo, hi = min(v), max(v)
    return [(x - lo) / (hi - lo) for x in v]


def anim_outlier(valori, extrem_final, norma=None, pasi=36):
    """Adauga o valoare care creste pana la 'extrem_final'. norma = functia ta (lista -> lista) sau
    un dict {nume: functie}. Vezi ce se intampla cu celelalte valori dupa transformare."""
    valori = [float(v) for v in valori]
    if norma is None:
        norma = {'min-max': _minmax_implicit}
    elif callable(norma):
        norma = {getattr(norma, '__name__', 'norma'): norma}
    nume = list(norma)
    start = max(valori)
    ov = np.geomspace(start, extrem_final, pasi) if start > 0 else np.linspace(start, extrem_final, pasi)
    ov = np.concatenate([[ov[0]] * 4, ov, [ov[-1]] * 6])
    rez = {k: [np.array(norma[k](valori + [float(o)]), float) for o in ov] for k in nume}
    lim = {}
    for k in nume:
        nuc = np.concatenate([r[:-1] for r in rez[k]] + [rez[k][0]])
        lo, hi = float(nuc.min()), float(nuc.max())
        d = (hi - lo) * 0.12 or 0.1
        lim[k] = (lo - d, hi + d)
    lo_b, hi_b = _limite(valori + [extrem_final])
    r = 1 + len(nume)
    fig, ax = plt.subplots(figsize=(7, 0.3 + 0.95 * r), dpi=DPI)
    ax.set_xlim(-0.15, 1.02)
    ax.set_ylim(0.3, r + 0.3)
    ax.axis('off')
    ys = [r - i - 0.05 for i in range(r)]
    _bara(ax, ys[0] - 0.25, lo_b, hi_b, BRUT, 'brut')
    for i, k in enumerate(nume):
        _bara(ax, ys[i + 1] - 0.25, lim[k][0], lim[k][1], NOU, k)
    xb = _poz(valori, lo_b, hi_b)
    ax.scatter(xb, [ys[0] - 0.25] * len(valori), s=40, color=BRUT, zorder=3, edgecolor='white')
    ob = ax.scatter([0], [ys[0] - 0.25], s=70, color=ROSU, zorder=4, edgecolor='white')
    nuclee, oute, tx = [], [], []
    for i, k in enumerate(nume):
        nuclee.append(ax.scatter([0] * len(valori), [ys[i + 1] - 0.25] * len(valori), s=40, color=NOU, zorder=3, edgecolor='white'))
        oute.append(ax.scatter([0], [ys[i + 1] - 0.25], s=70, color=ROSU, zorder=4, edgecolor='white'))
        tx.append(ax.text(1.0, ys[i + 1] + 0.05, '', ha='right', va='bottom', fontsize=8.5, color='#333'))
    tval = ax.text(1.0, ys[0] + 0.05, '', ha='right', va='bottom', fontsize=8.5, color=ROSU)

    def update(f):
        o = ov[f]
        ob.set_offsets([[_poz(o, lo_b, hi_b), ys[0] - 0.25]])
        tval.set_text(f'valoare extrema: {_f(o)}')
        for i, k in enumerate(nume):
            r_ = rez[k][f]
            lo, hi = lim[k]
            xs = _poz(r_[:-1], lo, hi)
            yy = ys[i + 1] - 0.25
            nuclee[i].set_offsets(np.c_[np.clip(xs, 0.0, 1.0), [yy] * len(xs)])
            xo = float(_poz(r_[-1], lo, hi))
            oute[i].set_offsets([[min(max(xo, 0.0), 1.0), yy]])
            oute[i].set_alpha(1.0 if 0 <= xo <= 1 else 0.5)
            a, b = r_[:-1].min(), r_[:-1].max()
            tx[i].set_text(f'valorile normale sunt acum in [{a:.3f}, {b:.3f}]  (latime {b - a:.3f})')
        return []

    ani = animation.FuncAnimation(fig, update, frames=len(ov), interval=100, blit=False)
    return _html(fig, ani)


def anim_linii(brut, normalizat, titlu='', norma='l2'):
    """Randurile (vectori 2D) 'brut' devin 'normalizat' (lungime 1). Directia ramane aceeasi."""
    brut, normalizat = np.asarray(brut, float), np.asarray(normalizat, float)
    n = len(brut)
    L0 = float(np.abs(brut).max()) * 1.25
    L1 = float(np.abs(normalizat).max()) * 1.35
    fig, ax = plt.subplots(figsize=(4.8, 4.8), dpi=DPI)
    ax.set_aspect('equal')
    ax.set_xlim(-L0, L0)
    ax.set_ylim(-L0, L0)
    ax.axhline(0, color=GRI, lw=0.8)
    ax.axvline(0, color=GRI, lw=0.8)
    if norma == 'l1':
        ax.plot([1, 0, -1, 0, 1], [0, 1, 0, -1, 0], color=VERDE, lw=1.4)
    else:
        u = np.linspace(0, 2 * np.pi, 200)
        ax.plot(np.cos(u), np.sin(u), color=VERDE, lw=1.4)
    lin = [ax.plot([0, brut[i, 0]], [0, brut[i, 1]], color=BRUT, lw=1.6)[0] for i in range(n)]
    cap = ax.scatter(brut[:, 0], brut[:, 1], s=40, color=BRUT, zorder=3)
    et = [ax.text(0, 0, '', fontsize=8, color='#333') for _ in range(n)]
    ax.set_title(titlu, fontsize=10, fontweight='bold', color='#333')
    N_START, N_MISCARE, N_FINAL = 6, 24, 8

    def update(f):
        p = _ease((f - N_START) / N_MISCARE)
        v = (1 - p) * brut + p * normalizat
        L = L0 ** (1 - p) * L1 ** p
        ax.set_xlim(-L, L)
        ax.set_ylim(-L, L)
        cap.set_offsets(v)
        cap.set_color(_mix(p))
        for i in range(n):
            lin[i].set_data([0, v[i, 0]], [0, v[i, 1]])
            lin[i].set_color(_mix(p))
            lung = float(np.hypot(*v[i])) if norma != 'l1' else float(np.abs(v[i]).sum())
            et[i].set_position((0.55 * v[i, 0] + 0.03 * L, 0.55 * v[i, 1] - 0.05 * L))
            et[i].set_text(f'lungime {lung:.2f}')
        return []

    ani = animation.FuncAnimation(fig, update, frames=N_START + N_MISCARE + N_FINAL, interval=100, blit=False)
    return _html(fig, ani)


def compara_hist(brut, transformat, titluri=('brut', 'transformat'), bins=25):
    """Doua histograme una langa alta (grafic static)."""
    fig, ax = plt.subplots(1, 2, figsize=(9, 3), dpi=DPI)
    for a, d, t, c in zip(ax, (brut, transformat), titluri, (BRUT, NOU)):
        a.hist(np.asarray(d, float), bins=bins, color=c, edgecolor='white')
        a.set_title(t, fontsize=10, fontweight='bold')
        a.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    plt.show()


def arata_train_test(train_sc, test_sc, titlu=''):
    """Valorile scalate (o coloana): train albastru, test portocaliu, iesirile din [0, 1] cu rosu (grafic static)."""
    train_sc, test_sc = np.asarray(train_sc, float).ravel(), np.asarray(test_sc, float).ravel()
    fig, ax = plt.subplots(figsize=(8, 2.4), dpi=DPI)
    ax.axvspan(0, 1, color=VERDE, alpha=0.15, lw=0)
    ax.scatter(train_sc, np.full(len(train_sc), 0.0), s=30, color=NOU, label='train', zorder=3)
    afara = (test_sc < 0) | (test_sc > 1)
    ax.scatter(test_sc[~afara], np.full((~afara).sum(), 0.0), s=30, color=BRUT, label='test', zorder=3, marker='D')
    ax.scatter(test_sc[afara], np.full(afara.sum(), 0.0), s=50, color=ROSU, label='test, in afara lui [0, 1]', zorder=4, marker='D')
    for v in test_sc[afara]:
        ax.annotate(f'{v:.2f}', (v, 0), xytext=(0, 12), textcoords='offset points', ha='center', fontsize=8, color=ROSU)
    ax.set_yticks([])
    ax.set_ylim(-0.5, 0.9)
    ax.spines[['top', 'right', 'left']].set_visible(False)
    ax.set_title(titlu, fontsize=10, fontweight='bold')
    ax.legend(loc='upper right', fontsize=8, frameon=False, ncol=3)
    plt.tight_layout()
    plt.show()
