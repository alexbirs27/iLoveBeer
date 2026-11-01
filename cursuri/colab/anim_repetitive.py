"""Animatii pentru notebook-ul 03 (structuri repetitive): cresterea numarului de pasi si parcurgerea perechilor (i, j)."""
import math

import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, ScalarFormatter
from IPython.display import HTML
from matplotlib import animation

__all__ = ['anim_crestere_pasi', 'anim_perechi']

_CULORI = ['#1f77b4', '#d95f02', '#2a9d8f', '#7b3fb0', '#c2255c', '#5c6773']


def anim_crestere_pasi(ns, serii, titlu='Cati pasi face bucla ta cand n creste'):
    """Animatie: pentru fiecare n din ns, numarul de pasi (dict nume -> lista) pe scara normala si pe scara log-log."""
    nume = list(serii)
    y_max = max(max(v) for v in serii.values())
    fig, (st, dr) = plt.subplots(1, 2, figsize=(9.5, 3.8), dpi=75)
    fig.suptitle(titlu, fontsize=11)

    st.set_xlim(0, max(ns) * 1.05)
    st.set_xlabel('n')
    st.set_ylabel('pasi')
    st.set_title('scara normala', fontsize=10)
    dr.set_xscale('log')
    dr.set_yscale('log')
    dr.set_xlim(min(ns) * 0.8, max(ns) * 1.25)
    dr.set_ylim(0.8, y_max * 2)
    dr.set_xlabel('n')
    dr.set_xticks([n for n in ns if n in (ns[0], ns[len(ns) // 2], ns[-1])])
    dr.xaxis.set_major_formatter(ScalarFormatter())
    dr.xaxis.set_minor_formatter(NullFormatter())
    dr.set_title('scara log-log (panta = ordinul lui n)', fontsize=10)

    linii_st, linii_dr, puncte = [], [], []
    for k, nm in enumerate(nume):
        col = _CULORI[k % len(_CULORI)]
        linii_st.append(st.plot([], [], color=col, lw=2, label=nm)[0])
        linii_dr.append(dr.plot([], [], color=col, lw=2, label=nm)[0])
        puncte.append(st.plot([], [], 'o', color=col, ms=6)[0])
    dr.legend(fontsize=8, loc='upper left')
    text = st.text(0.02, 0.95, '', transform=st.transAxes, va='top', fontsize=9, family='monospace')
    fig.tight_layout(rect=(0, 0, 1, 0.94))

    def update(k):
        for i, nm in enumerate(nume):
            y = [max(v, 1) for v in serii[nm][:k + 1]]
            linii_st[i].set_data(ns[:k + 1], serii[nm][:k + 1])
            linii_dr[i].set_data(ns[:k + 1], y)
            puncte[i].set_data([ns[k]], [serii[nm][k]])
        st.set_ylim(-0.03 * max(1, max(serii[nm][k] for nm in nume)),
                    max(1, max(serii[nm][k] for nm in nume)) * 1.08)
        text.set_text(f'n = {ns[k]}\n' + '\n'.join(f'{nm}: {serii[nm][k]}' for nm in nume))
        return linii_st + linii_dr + puncte + [text]

    ani = animation.FuncAnimation(fig, update, frames=len(ns), interval=600, blit=False)
    html = ani.to_jshtml()
    plt.close(fig)
    return HTML(html)


def anim_perechi(perechi, titlu='Ordinea in care bucla parcurge perechile (i, j)'):
    """Animatie: lista de perechi (i, j) produse de doua bucle imbricate, aprinse pe rand intr-o grila."""
    pas = max(1, math.ceil(len(perechi) / 50))
    cadre = list(range(0, len(perechi), pas))
    if cadre[-1] != len(perechi) - 1:
        cadre.append(len(perechi) - 1)
    li = max(p[0] for p in perechi) + 1
    co = max(p[1] for p in perechi) + 1
    fig, ax = plt.subplots(figsize=(max(4.2, co * 0.7 + 1.5), max(3.4, li * 0.6 + 1.5)), dpi=75)
    ax.set_xlim(-0.6, co - 0.4)
    ax.set_ylim(li - 0.4, -0.6)
    ax.set_xticks(range(co))
    ax.set_yticks(range(li))
    ax.set_xlabel('j')
    ax.set_ylabel('i')
    ax.set_aspect('equal')
    ax.grid(True, color='#e2e8f0')
    vechi = ax.scatter([], [], s=260, color='#74a7ff', edgecolor='#1c5fb5')
    curent = ax.scatter([], [], s=380, color='#f59f00', edgecolor='#a65f00', zorder=3)
    ax.set_title(titlu + '\npasul 99 din 99: i=9, j=9', fontsize=9)
    fig.tight_layout()

    def update(k):
        i = cadre[k]
        trecut = perechi[:i]
        vechi.set_offsets([(j, r) for r, j in trecut] if trecut else [(-9, -9)])
        curent.set_offsets([(perechi[i][1], perechi[i][0])])
        ax.set_title(f'{titlu}\npasul {i + 1} din {len(perechi)}: i={perechi[i][0]}, j={perechi[i][1]}', fontsize=9)
        return vechi, curent

    ani = animation.FuncAnimation(fig, update, frames=len(cadre), interval=350, blit=False)
    html = ani.to_jshtml()
    plt.close(fig)
    return HTML(html)
