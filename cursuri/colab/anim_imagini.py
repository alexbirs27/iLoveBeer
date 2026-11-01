"""Animatii pentru notebook-ul 09 (imagini): pixelii ca numere si pragul alb/negru."""
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML
from matplotlib import animation
from matplotlib.patches import Rectangle

__all__ = ['anim_pixeli', 'anim_prag']


def anim_pixeli(img, r0, c0, n=8):
    """Zoom de la imaginea intreaga pana la un patrat n x n de la (r0, c0), cu valoarea fiecarui pixel scrisa in celula."""
    img = np.asarray(img)
    H, W = img.shape[:2]
    if not (0 <= r0 and r0 + n <= H and 0 <= c0 and c0 + n <= W):
        raise ValueError(f'patratul {n}x{n} de la ({r0}, {c0}) iese din imagine ({H}x{W})')
    color = img.ndim == 3

    fig, ax = plt.subplots(figsize=(5, 5.3), layout='tight')
    if color:
        ax.imshow(img, interpolation='nearest')
    else:
        ax.imshow(img, cmap='gray', vmin=0, vmax=255, interpolation='nearest')
    ax.set_xlabel('coloana')
    ax.set_ylabel('rand')
    caseta = Rectangle((c0 - 0.5, r0 - 0.5), n, n, fill=False, ec='#e03131', lw=2)
    ax.add_patch(caseta)

    cel = 5 * 72 * 0.85 / n                   # marimea unei celule pe ecran, in puncte
    texte, linii = [], []
    for r in range(r0, r0 + n):
        for c in range(c0, c0 + n):
            v = img[r, c]
            if color:
                lum = 0.299 * v[0] + 0.587 * v[1] + 0.114 * v[2]
                txt = f'{int(v[0])}\n{int(v[1])}\n{int(v[2])}'
                fs = min(11, cel / 4.2)
            else:
                lum = float(v)
                txt = str(int(v))
                fs = min(12, cel / 3.0)
            t = ax.text(c, r, txt, ha='center', va='center', fontsize=fs, visible=False,
                        color='white' if lum < 128 else 'black', linespacing=1.0)
            texte.append(t)
    for k in range(n + 1):
        linii.append(ax.axhline(r0 - 0.5 + k, xmin=0, xmax=1, color='#adb5bd', lw=0.6, visible=False))
        linii.append(ax.axvline(c0 - 0.5 + k, ymin=0, ymax=1, color='#adb5bd', lw=0.6, visible=False))

    z = 12                                    # cadre de zoom
    cadre = z + 5

    def limite(t):
        # interpolare geometrica intre imaginea intreaga si patrat
        f = lambda a, b: a * (b / a) ** t
        wi, wf = W, n
        hi, hf = H, n
        w, h = f(wi, wf), f(hi, hf)
        # centrul se muta liniar de la centrul imaginii la centrul patratului
        cx = (W / 2 - 0.5) * (1 - t) + (c0 + n / 2 - 0.5) * t
        cy = (H / 2 - 0.5) * (1 - t) + (r0 + n / 2 - 0.5) * t
        return (cx - w / 2, cx + w / 2), (cy + h / 2, cy - h / 2)

    def update(k):
        t = min(1.0, k / z)
        t = t * t * (3 - 2 * t)               # start si oprire lina
        (x0, x1), (y0, y1) = limite(t)
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        arata = k >= z
        for o in texte + linii:
            o.set_visible(arata)
        if k == 0:
            ax.set_title(f'imaginea intreaga: {H} x {W}' + (' x 3' if color else '') + ' numere')
        elif k < z:
            ax.set_title('zoom pe patratul rosu...')
        else:
            ax.set_title(f'patrat {n} x {n}: celula = pixel = ' + ('3 numere R,G,B' if color else 'un numar'))

    ani = animation.FuncAnimation(fig, update, frames=cadre, interval=350)
    html = ani.to_jshtml()
    plt.close(fig)
    return HTML(html)


def anim_prag(img_gri):
    """Mareste pragul de la 0 la 255 si arata imaginea alb/negru (pixel > prag = alb) plus histograma."""
    a = np.asarray(img_gri)
    if a.ndim != 2:
        raise ValueError('da-mi imaginea in tonuri de gri (matrice 2D), nu una color')
    pas = max(1, max(a.shape) // 160)         # imaginile mari se subesantioneaza, ca animatia sa ramana usoara
    a = a[::pas, ::pas].astype(int)
    hist = np.bincount(a.ravel(), minlength=256)[:256]
    total = a.size
    praguri = list(range(0, 256, 8)) + [255]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 3.4), layout='tight', dpi=72,
                                        gridspec_kw={'width_ratios': [1, 1, 1.3]})
    ax1.imshow(a, cmap='gray', vmin=0, vmax=255)
    ax1.set_title('tonuri de gri')
    im2 = ax2.imshow(a > 0, cmap='gray', vmin=0, vmax=1)
    for ax in (ax1, ax2):
        ax.axis('off')
    bare = ax3.bar(range(256), hist, width=1.0, color='#adb5bd')
    linie = ax3.axvline(0, color='#e03131', lw=2)
    ax3.set_xlim(0, 255)
    ax3.set_xlabel('valoarea pixelului')
    ax3.set_ylabel('cati pixeli')
    ax3.set_title('histograma')

    def update(k):
        t = praguri[k]
        alb = a > t
        im2.set_data(alb)
        ax2.set_title(f'prag = {t}: {int(alb.sum())} pixeli albi ({100 * alb.sum() / total:.0f}%)')
        linie.set_xdata([t, t])
        for i, b in enumerate(bare):
            b.set_color('#495057' if i <= t else '#dee2e6')

    ani = animation.FuncAnimation(fig, update, frames=len(praguri), interval=300)
    html = ani.to_jshtml()
    plt.close(fig)
    return HTML(html)
