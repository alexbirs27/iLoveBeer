"""Animatii pentru notebook-urile despre valori lipsa: mecanisme, umplerea golurilor, imputare pe grafic.

Toate primesc array-urile calculate de TINE in notebook si intorc o animatie gata de afisat.
masca = array bool, True unde valoarea LIPSEA.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML

__all__ = ['anim_mecanisme', 'anim_imputare', 'anim_scatter_imputare']

ALBASTRU, PORTOCALIU, ROSU, GRI, VERDE = '#2563eb', '#ea580c', '#dc2626', '#cbd5e1', '#15803d'


def _html(fig, update, n, interval):
    ani = animation.FuncAnimation(fig, update, frames=n, interval=interval)
    html = ani.to_jshtml()
    plt.close(fig)
    return HTML(html)


def anim_mecanisme(valori, masti, eticheta='valoare'):
    """valori = datele complete (adevarul), masti = {'MCAR': masca1, 'MAR': masca2, ...}. Compara media reala cu media a ce a ramas."""
    v = np.asarray(valori, dtype=float)
    nume = ['adevarul'] + list(masti)
    bins = np.linspace(v.min(), v.max(), 26)
    ymax = np.histogram(v, bins=bins)[0].max() * 1.15
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=80)

    def update(i):
        ax.clear()
        ax.hist(v, bins=bins, color=GRI, edgecolor='white', label='toate valorile (adevarul)')
        ax.axvline(v.mean(), color='#475569', ls='--', lw=2, label=f'media reala = {v.mean():.2f}')
        if i > 0:
            ramas = v[~np.asarray(masti[nume[i]], dtype=bool)]
            ax.hist(ramas, bins=bins, color=ALBASTRU, edgecolor='white', label=f'ce a ramas ({len(ramas)} valori)')
            ax.axvline(ramas.mean(), color=PORTOCALIU, lw=2.5, label=f'media ramasa = {ramas.mean():.2f}')
        ax.set_ylim(0, ymax)
        ax.set_xlabel(eticheta)
        ax.set_title(nume[i] if i == 0 else f'lipsesc valori: {nume[i]}', fontsize=11)
        ax.legend(fontsize=8, loc='upper right', framealpha=0.9)
        ax.spines[['top', 'right']].set_visible(False)

    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.18, top=0.88)
    return _html(fig, update, len(nume), 1800)


def anim_imputare(valori, masca, strategii, eticheta='valoare'):
    """Histograma in care golurile se umplu pe rand cu fiecare strategie: albastru = valori reale, portocaliu = imputate.
    strategii = {'media': array_completat, 'mediana': array_completat, ...} (fiecare cu aceeasi lungime ca valori)."""
    v = np.asarray(valori, dtype=float)
    masca = np.asarray(masca, dtype=bool)
    real = v[~masca]
    nume = ['fara umplere'] + list(strategii)
    umplute = {n: np.asarray(a, dtype=float) for n, a in strategii.items()}
    lo = min([real.min()] + [a.min() for a in umplute.values()])
    hi = max([real.max()] + [a.max() for a in umplute.values()])
    bins = np.linspace(lo, hi, 31)
    ymax = max(np.histogram(a, bins=bins)[0].max() for a in umplute.values()) * 1.1
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=80)

    def update(i):
        ax.clear()
        if i == 0:
            ax.hist(real, bins=bins, color=ALBASTRU, edgecolor='white')
            ax.set_title(f'{masca.sum()} goluri din {len(v)}  |  std = {real.std(ddof=1):.2f}', fontsize=10)
        else:
            a = umplute[nume[i]]
            ax.hist([a[~masca], a[masca]], bins=bins, stacked=True, color=[ALBASTRU, PORTOCALIU],
                    edgecolor='white', label=['reale', 'imputate'])
            ax.legend(fontsize=8, loc='upper right')
            ax.set_title(f'{nume[i]}  |  std = {a.std(ddof=1):.2f}  (reale: {real.std(ddof=1):.2f})', fontsize=10)
        ax.set_ylim(0, ymax)
        ax.set_xlabel(eticheta)
        ax.set_ylabel('cate valori')
        ax.spines[['top', 'right']].set_visible(False)

    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.18, top=0.88)
    return _html(fig, update, len(nume), 1700)


def anim_scatter_imputare(x, y, masca, strategii, adevar=None, eticheta_x='x', eticheta_y='y'):
    """Nor de puncte (x, y) unde y are goluri. Pe rand, fiecare strategie pune punctele imputate (portocaliu).
    Daca dai adevar (valorile reale de la goluri), vezi si erorile ca linii rosii si RMSE-ul in titlu."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    masca = np.asarray(masca, dtype=bool)
    nume = list(strategii)
    umplute = {n: np.asarray(a, dtype=float) for n, a in strategii.items()}
    fig, ax = plt.subplots(figsize=(6.2, 4), dpi=80)
    piese = [y[~masca]] + [a[masca] for a in umplute.values()]
    if adevar is not None:
        piese.append(np.asarray(adevar, dtype=float))
    toate = np.concatenate(piese)
    yl = (toate.min() - 0.3, toate.max() + 0.3)

    def update(i):
        ax.clear()
        a = umplute[nume[i]]
        ax.scatter(x[~masca], y[~masca], s=14, color=ALBASTRU, alpha=0.5, label='reale')
        titlu = nume[i]
        if adevar is not None:
            ad = np.asarray(adevar, dtype=float)
            ax.scatter(x[masca], ad, s=26, facecolors='none', edgecolors=VERDE, label='adevarul ascuns')
            ax.plot([x[masca], x[masca]], [a[masca], ad], color=ROSU, lw=0.8, alpha=0.7)
            titlu += f'  |  RMSE = {np.sqrt(np.mean((a[masca] - ad) ** 2)):.2f}'
        ax.scatter(x[masca], a[masca], s=26, color=PORTOCALIU, label='imputate', zorder=5)
        ax.set_ylim(*yl)
        ax.set_xlabel(eticheta_x)
        ax.set_ylabel(eticheta_y)
        ax.set_title(titlu, fontsize=10)
        ax.legend(fontsize=8, loc='upper left')
        ax.spines[['top', 'right']].set_visible(False)

    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.18, top=0.88)
    return _html(fig, update, len(nume), 1700)
