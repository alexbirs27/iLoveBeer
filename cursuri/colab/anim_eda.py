"""Animatii pentru notebook-urile de EDA: histograma, medie vs mediana, corelatie si outlier.

Toate primesc valorile TALE (calculate in notebook) si intorc o animatie gata de afisat.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML

__all__ = ['anim_histograma', 'anim_medie_mediana', 'anim_corelatie']

ALBASTRU, PORTOCALIU, ROSU, VERDE = '#2563eb', '#ea580c', '#dc2626', '#15803d'


def _curat(v):
    v = np.asarray(v, dtype=float)
    return v[~np.isnan(v)]


def _html(fig, update, cadre, interval):
    ani = animation.FuncAnimation(fig, update, frames=cadre, interval=interval)
    html = ani.to_jshtml()
    plt.close(fig)
    return HTML(html)


def anim_histograma(valori, nmin=2, nmax=40, eticheta='valoare'):
    """Histograma cu numarul de bare de la nmin la nmax: vezi cand forma apare si cand se pierde in zgomot."""
    v = _curat(valori)
    lo, hi = v.min(), v.max()
    ideal = np.sqrt(len(v))
    ks = list(range(nmin, min(nmax, 12) + 1)) + list(range(14, nmax + 1, 2))
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=80)

    def update(i):
        k = ks[i]
        ax.clear()
        ax.hist(v, bins=k, range=(lo, hi), color=ALBASTRU, edgecolor='white')
        if k < 0.5 * ideal:
            verdict, cul = 'prea putine bare: forma se pierde', ROSU
        elif k > 2 * ideal:
            verdict, cul = 'prea multe bare: zgomot', ROSU
        else:
            verdict, cul = 'in jur de radical din n: de obicei bine', VERDE
        ax.set_title(f'{k} bare (n = {len(v)}, radical din n = {ideal:.0f})\n{verdict}', fontsize=10, color=cul)
        ax.set_xlabel(eticheta)
        ax.set_ylabel('cate valori')
        ax.spines[['top', 'right']].set_visible(False)

    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.18, top=0.84)
    return _html(fig, update, len(ks), 500)


def anim_medie_mediana(valori, n_cadre=30, eticheta='valoare'):
    """Adauga o valoare extrema care urca pas cu pas. Media o urmareste, mediana abia se misca.
    (Cu multe valori, un singur outlier misca media putin: de aceea urca mai sus cand ai multe date.)"""
    v = _curat(valori)
    sd = v.std() or 1.0
    start, stop = v.max(), v.max() + max(12.0, len(v) / 4) * sd
    poz = np.linspace(start, stop, n_cadre)
    y = np.random.default_rng(0).uniform(0.1, 0.9, len(v))
    fig, ax = plt.subplots(figsize=(6.4, 3.3), dpi=80)
    xmin, xmax = v.min() - 0.5 * sd, stop + 1.0 * sd

    def update(i):
        ax.clear()
        tot = np.append(v, poz[i])
        media, mediana = tot.mean(), np.median(tot)
        ax.scatter(v, y, s=14, color=ALBASTRU, alpha=0.6, label='datele tale')
        ax.scatter([poz[i]], [0.5], s=90, color=ROSU, marker='D', label='outlier', zorder=5)
        ax.axvline(media, color=PORTOCALIU, lw=2.5, label=f'media = {media:.2f}')
        ax.axvline(mediana, color=VERDE, lw=2.5, ls='--', label=f'mediana = {mediana:.2f}')
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_xlabel(eticheta)
        ax.set_title(f'outlier = {poz[i]:.1f}', fontsize=10)
        ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
        ax.spines[['top', 'right', 'left']].set_visible(False)

    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.18, top=0.88)
    return _html(fig, update, n_cadre, 250)


def anim_corelatie(x, y, n_cadre=25, eticheta_x='x', eticheta_y='y'):
    """Un singur punct extrem se muta pe grafic si schimba corelatia (si dreapta) mult mai mult decat te astepti."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    bun = ~(np.isnan(x) | np.isnan(y))
    x, y = x[bun], y[bun]
    sx, sy = x.std() or 1.0, y.std() or 1.0
    x0, y0 = x.mean(), y.mean()
    x1, y1 = x.max() + 3 * sx, y.min() - 4 * sy
    t = np.linspace(0, 1, n_cadre)
    fig, ax = plt.subplots(figsize=(6, 3.8), dpi=80)
    xl = (x.min() - sx, x1 + sx)
    yl = (y1 - sy, y.max() + sy)

    def update(i):
        ax.clear()
        px, py = x0 + t[i] * (x1 - x0), y0 + t[i] * (y1 - y0)
        xx, yy = np.append(x, px), np.append(y, py)
        r = np.corrcoef(xx, yy)[0, 1]
        a, b = np.polyfit(xx, yy, 1)
        dr = np.array(xl)
        ax.scatter(x, y, s=14, color=ALBASTRU, alpha=0.6)
        ax.scatter([px], [py], s=90, color=ROSU, marker='D', zorder=5)
        ax.plot(dr, a * dr + b, color=PORTOCALIU, lw=2)
        ax.set_xlim(*xl)
        ax.set_ylim(*yl)
        ax.set_xlabel(eticheta_x)
        ax.set_ylabel(eticheta_y)
        ax.set_title(f'corelatia (r) = {r:.2f}', fontsize=10)
        ax.spines[['top', 'right']].set_visible(False)

    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.18, top=0.88)
    return _html(fig, update, n_cadre, 250)
