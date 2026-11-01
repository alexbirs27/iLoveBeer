"""Animatii pentru notebook-ul 08 (clase): cautarea unei metode pe lantul de mostenire."""
import types

import matplotlib.pyplot as plt
from IPython.display import HTML
from matplotlib import animation
from matplotlib.patches import FancyBboxPatch

__all__ = ['anim_mro']


def _metode(cls):
    nume = [n for n, v in vars(cls).items() if isinstance(v, (types.FunctionType, property))]
    return ', '.join(nume) if nume else '(nimic)'


def anim_mro(clasa, metoda):
    """Arata cum cauta Python metoda `metoda` pe lantul de mostenire al clasei `clasa`."""
    lant = list(clasa.__mro__)
    gasit = next((i for i, k in enumerate(lant) if metoda in vars(k)), None)
    ultim = gasit if gasit is not None else len(lant) - 1
    n = len(lant)

    fig, ax = plt.subplots(figsize=(7, 0.9 + 1.0 * n), layout='tight')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.15 * n + 0.8)
    ax.axis('off')

    # clasa copil jos, parintii mai sus; object e ultima
    ys = [0.3 + 1.15 * i for i in range(n)]
    casete, texte = [], []
    for i, k in enumerate(lant):
        p = FancyBboxPatch((1, ys[i]), 8, 0.8, boxstyle='round,pad=0.02', fc='#f8fafc', ec='#9aa5b1', lw=1.5)
        ax.add_patch(p)
        ax.text(1.25, ys[i] + 0.55, k.__name__, fontsize=11, fontweight='bold', va='center')
        ax.text(1.25, ys[i] + 0.22, _metode(k) if k is not object else '(metodele de baza ale lui Python)',
                fontsize=9, va='center', color='#52606d')
        casete.append(p)
        texte.append(k)
        if i:
            ax.annotate('', xy=(5, ys[i]), xytext=(5, ys[i - 1] + 0.8),
                        arrowprops=dict(arrowstyle='->', color='#7b8794'))
    titlu = ax.text(0.2, ys[-1] + 1.0, '', fontsize=11, va='center')

    def update(k):
        for i, p in enumerate(casete):
            p.set_facecolor('#f8fafc')
            p.set_edgecolor('#9aa5b1')
        if k == 0:
            titlu.set_text(f'obiect.{metoda}(...): Python cauta "{metoda}" incepand de jos')
            return
        i = k - 1
        if i == gasit:
            casete[i].set_facecolor('#d3f9d8')
            casete[i].set_edgecolor('#2b8a3e')
            titlu.set_text(f'gasit in {lant[i].__name__}: se executa {lant[i].__name__}.{metoda}')
        elif i == len(lant) - 1 and gasit is None:
            casete[i].set_facecolor('#ffe3e3')
            casete[i].set_edgecolor('#e03131')
            titlu.set_text(f'nu exista nicaieri: AttributeError ({metoda})')
        else:
            casete[i].set_facecolor('#fff3bf')
            casete[i].set_edgecolor('#f59f00')
            titlu.set_text(f'in {lant[i].__name__} nu e "{metoda}", urcam la parinte')

    ani = animation.FuncAnimation(fig, update, frames=ultim + 2, interval=1300)
    html = ani.to_jshtml()
    plt.close(fig)
    return HTML(html)
