"""Animatii pentru notebook-urile despre liste si matrici: parcurgeri de tablouri si sortari."""
import matplotlib.pyplot as plt
from IPython.display import HTML
from matplotlib import animation
from matplotlib.patches import Rectangle

__all__ = ['anim_parcurgere', 'anim_sortare']

MODURI = ('linii', 'coloane', 'sarpe', 'diagonale', 'diagonale_principale', 'spirala')


def _ordine(n, m, mod):
    """Lista de celule (i, j) in ordinea vizitarii, pentru un mod din MODURI sau o lista data de elev."""
    if not isinstance(mod, str):
        ordine = [tuple(p) for p in mod]
        for i, j in ordine:
            if not (0 <= i < n and 0 <= j < m):
                raise ValueError(f'celula ({i}, {j}) nu exista intr-o matrice cu {n} linii si {m} coloane')
        return ordine
    if mod == 'linii':
        return [(i, j) for i in range(n) for j in range(m)]
    if mod == 'coloane':
        return [(i, j) for j in range(m) for i in range(n)]
    if mod == 'sarpe':
        return [(i, j) for i in range(n) for j in (range(m) if i % 2 == 0 else range(m - 1, -1, -1))]
    if mod == 'diagonale':          # cele cu i + j constant, de sus-dreapta spre stanga-jos
        return [(i, s - i) for s in range(n + m - 1) for i in range(max(0, s - m + 1), min(n - 1, s) + 1)]
    if mod == 'diagonale_principale':   # cele cu j - i constant
        return [(i, i + d) for d in range(-(n - 1), m) for i in range(n) if 0 <= i + d < m]
    if mod == 'spirala':
        out = []
        sus, jos, st, dr = 0, n - 1, 0, m - 1
        while sus <= jos and st <= dr:
            out += [(sus, j) for j in range(st, dr + 1)]
            out += [(i, dr) for i in range(sus + 1, jos + 1)]
            if sus < jos:
                out += [(jos, j) for j in range(dr - 1, st - 1, -1)]
            if st < dr:
                out += [(i, st) for i in range(jos - 1, sus, -1)]
            sus, jos, st, dr = sus + 1, jos - 1, st + 1, dr - 1
        return out
    raise ValueError(f'mod necunoscut: {mod!r}. Alege dintre {MODURI} sau da o lista de perechi (i, j)')


def anim_parcurgere(n, m, mod='linii', interval=450):
    """Arata ORDINEA in care se viziteaza o matrice n x m. mod = 'linii', 'coloane', 'sarpe', 'diagonale',
    'diagonale_principale', 'spirala' sau o lista de perechi (i, j) facuta de tine."""
    ordine = _ordine(n, m, mod)
    total = len(ordine)
    nume = mod if isinstance(mod, str) else 'ordinea ta'
    pas = max(1, -(-total // 45))
    cadre = sorted(set(list(range(0, total + 1, pas)) + [total]))

    fig, ax = plt.subplots(figsize=(min(7, 0.75 * m + 1.4), min(6, 0.75 * n + 1.6)), dpi=80)
    marime = max(7, 15 - max(n, m))
    casute, texte = {}, {}
    for i in range(n):
        for j in range(m):
            r = Rectangle((j - 0.45, i - 0.45), 0.9, 0.9, facecolor='#f1f3f5', edgecolor='#adb5bd')
            ax.add_patch(r)
            casute[i, j] = r
            texte[i, j] = ax.text(j, i, '', ha='center', va='center', fontsize=marime, color='#212529', zorder=3)
    linie, = ax.plot([], [], color='#1c7ed6', alpha=0.45, lw=2, zorder=2)
    ax.set_xlim(-0.6, m - 0.4)
    ax.set_ylim(n - 0.4, -0.6)
    ax.set_aspect('equal')
    ax.set_xticks(range(m))
    ax.set_yticks(range(n))
    ax.xaxis.tick_top()
    ax.tick_params(length=0, labelsize=9)
    for s in ax.spines.values():
        s.set_visible(False)
    titlu = ax.set_title('', fontsize=11, pad=22)

    def update(k):
        for p in casute:
            casute[p].set_facecolor('#f1f3f5')
            texte[p].set_text('')
        vazute = {}
        for idx, p in enumerate(ordine[:k]):
            vazute.setdefault(p, []).append(idx + 1)
        for idx, p in enumerate(ordine[:k]):
            casute[p].set_facecolor(plt.cm.Blues(0.15 + 0.45 * idx / max(1, total)))
            texte[p].set_text(','.join(map(str, vazute[p][-2:])) if len(vazute[p]) > 1 else str(idx + 1))
        if k > 0:
            casute[ordine[k - 1]].set_facecolor('#ffa94d')
            i, j = ordine[k - 1]
            titlu.set_text(f'{nume}: pasul {k} din {total}, celula ({i}, {j})')
        else:
            titlu.set_text(f'{nume}: {total} celule de vizitat')
        linie.set_data([p[1] for p in ordine[:k]], [p[0] for p in ordine[:k]])
        return []

    ani = animation.FuncAnimation(fig, update, frames=cadre, interval=interval, repeat=False, blit=False)
    html = ani.to_jshtml()
    plt.close(fig)
    return HTML(html)


def anim_sortare(stari, interval=500):
    """Animeaza o sortare ca bare. stari = lista de liste (instantanee v.copy() facute de tine la fiecare schimbare)."""
    stari = [list(s) for s in stari]
    if not stari:
        raise ValueError('stari e goala: adauga v.copy() in lista la fiecare schimbare din sortarea ta')
    n = len(stari[0])
    if any(len(s) != n for s in stari):
        raise ValueError('toate instantaneele trebuie sa aiba aceeasi lungime')
    total = len(stari)
    if total > 60:
        cadre = sorted(set(round(x * (total - 1) / 59) for x in range(60)))
    else:
        cadre = list(range(total))
    toate = [x for s in stari for x in s]
    jos, sus = min(0, min(toate)), max(toate)
    final_sortat = stari[-1] == sorted(stari[-1])

    fig, ax = plt.subplots(figsize=(min(7, 0.55 * n + 2.5), 3.6), dpi=80)
    bare = ax.bar(range(n), stari[0], color='#74c0fc', edgecolor='#1c7ed6')
    etichete = [ax.text(i, 0, '', ha='center', va='bottom', fontsize=max(7, 12 - n // 3)) for i in range(n)]
    ax.set_xlim(-0.7, n - 0.3)
    ax.set_ylim(jos * 1.15, sus * 1.18 + 0.5)
    ax.set_xticks(range(n))
    ax.tick_params(labelsize=9)
    ax.set_xlabel('pozitia in lista')
    ax.spines[['top', 'right']].set_visible(False)
    titlu = ax.set_title('', fontsize=11)
    fig.tight_layout()

    def update(k):
        s, ant = stari[k], (stari[k - 1] if k > 0 else stari[0])
        schimbate = [i for i in range(n) if s[i] != ant[i]]
        for i in range(n):
            bare[i].set_height(s[i])
            if k == total - 1 and final_sortat:
                bare[i].set_facecolor('#8ce99a')
                bare[i].set_edgecolor('#2f9e44')
            elif i in schimbate:
                bare[i].set_facecolor('#ffa94d')
                bare[i].set_edgecolor('#e8590c')
            else:
                bare[i].set_facecolor('#74c0fc')
                bare[i].set_edgecolor('#1c7ed6')
            etichete[i].set_position((i, max(s[i], 0)))
            etichete[i].set_text(str(s[i]) if n <= 16 else '')
        if k == 0:
            titlu.set_text(f'la inceput ({total - 1} schimbari in total)')
        elif schimbate:
            titlu.set_text(f'schimbarea {k} din {total - 1}: pozitiile {", ".join(map(str, schimbate))}')
        else:
            titlu.set_text(f'schimbarea {k} din {total - 1}')
        return []

    ani = animation.FuncAnimation(fig, update, frames=cadre, interval=interval, repeat=False, blit=False)
    html = ani.to_jshtml()
    plt.close(fig)
    return HTML(html)
