"""Animatii pentru notebook-ul despre scalare (matplotlib, to_jshtml). Foloseste si anim_normalizare.py."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Ellipse
from anim_normalizare import anim_transformare, _html, _ease, _f, BRUT, NOU, GRI, ROSU, VERDE, DPI

__all__ = ['anim_zscore', 'anim_knn_scalare', 'anim_gradient', 'arata_fuga']

CLASE = ['#2b6cb0', '#d9730d', '#2f9e44', '#7048e8']


def anim_zscore(brut, scalat, titlu='z-score'):
    """Ca anim_transformare, dar cu zona media +/- o abatere standard (verde) pe ambele drepte."""
    b = np.asarray(brut, float)
    m, s = b.mean(), b.std()
    return anim_transformare(b, scalat, titlu, zone_brut=[(m - s, m + s)], zone_transf=[(-1, 1)])


def anim_knn_scalare(X, y, punct, k=5, X_scalat=None, punct_scalat=None, nume=('x', 'y')):
    """X: (n, 2) brut, y: clase, punct: interogarea (2 valori). Arata cei k vecini ai lui 'punct' dupa distanta
    bruta si dupa cea pe date scalate. Elipsa verde = 'ce inseamna aproape' pentru metrica curenta.
    Daca nu dai X_scalat / punct_scalat, se folosesc media si abaterea standard ale lui X."""
    X, y, punct = np.asarray(X, float), np.asarray(y), np.asarray(punct, float)
    if X_scalat is None:
        mu, sd = X.mean(0), X.std(0)
        X_scalat, punct_scalat = (X - mu) / sd, (punct - mu) / sd
    Xs, ps = np.asarray(X_scalat, float), np.asarray(punct_scalat, float)
    d0, d1 = np.linalg.norm(X - punct, axis=1), np.linalg.norm(Xs - ps, axis=1)
    v0, v1 = np.argsort(d0, kind='stable')[:k], np.argsort(d1, kind='stable')[:k]
    r0, r1 = d0[v0[-1]], d1[v1[-1]]
    lo, sp0, sp1 = X.min(0), np.ptp(X, axis=0), np.ptp(Xs, axis=0)
    U = (X - lo) / sp0                      # aceleasi coordonate de ecran pentru brut si scalat
    q = (punct - lo) / sp0
    sem0 = np.array([r0 / sp0[0], r0 / sp0[1]])   # semiaxele elipsei, in coordonate de ecran
    sem1 = np.array([r1 / sp1[0], r1 / sp1[1]])
    clase = list(np.unique(y))
    cul = [CLASE[clase.index(c) % len(CLASE)] for c in y]

    def vot(v):
        vals, cnt = np.unique(y[v], return_counts=True)
        return f'prezice clasa {vals[np.argmax(cnt)]}  (voturi: ' + ', '.join(f'{a}:{b}' for a, b in zip(vals, cnt)) + ')'

    fig, ax = plt.subplots(figsize=(6.2, 5.0), dpi=DPI)
    ax.set_xlim(-0.08, 1.08)
    ax.set_ylim(-0.08, 1.08)
    ax.axis('off')
    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color='#d0d5db', lw=0.8)
    ax.scatter(U[:, 0], U[:, 1], s=18, c=cul, alpha=0.75, zorder=2, edgecolor='white', linewidth=0.4)
    elipsa = Ellipse(q, 2 * sem0[0], 2 * sem0[1], fill=True, fc=VERDE, alpha=0.12, ec=VERDE, lw=1.3, zorder=1)
    elipsa.set_clip_path(ax.patch)
    ax.add_patch(elipsa)
    ring0 = ax.scatter(U[v0, 0], U[v0, 1], s=140, facecolor='none', edgecolor=ROSU, linewidth=1.8, zorder=4)
    ring1 = ax.scatter(U[v1, 0], U[v1, 1], s=140, facecolor='none', edgecolor='#111', linewidth=1.8, zorder=4, linestyle='--')
    ax.scatter([q[0]], [q[1]], s=150, marker='*', color='#111', zorder=5)
    tit = ax.text(0.5, 1.09, '', ha='center', fontsize=10, fontweight='bold', color='#333')
    sub = ax.text(0.5, -0.085, '', ha='center', va='top', fontsize=9, color='#333')
    ex = ax.text(0.5, -0.02, '', ha='center', va='top', fontsize=7.5, color=GRI)
    ey = ax.text(-0.01, 0.5, '', ha='right', va='center', fontsize=7.5, color=GRI, rotation=90)
    N_A, N_M, N_C = 10, 22, 12

    def update(f):
        p = _ease((f - N_A) / N_M)
        sem = (1 - p) * sem0 + p * sem1
        elipsa.set_width(2 * sem[0])
        elipsa.set_height(2 * sem[1])
        ring0.set_alpha(1.0 - 0.7 * p)
        ring1.set_alpha(min(1.0, max(0.0, (p - 0.3) / 0.5)))
        A = p < 0.5
        M, V = (X, v0) if A else (Xs, v1)
        tit.set_text('BRUT: vecinii dupa distanta pe datele originale' if A else 'SCALAT: vecinii dupa distanta pe date scalate')
        sub.set_text(vot(V))
        ex.set_text(f'{nume[0]}: {_f(M[:, 0].min())} .. {_f(M[:, 0].max())}')
        ey.set_text(f'{nume[1]}: {_f(M[:, 1].min())} .. {_f(M[:, 1].max())}')
        return []

    ani = animation.FuncAnimation(fig, update, frames=N_A + N_M + N_C, interval=100, blit=False)
    return _html(fig, ani)


def _pierdere(X, y, w):
    return float(np.mean((X @ w - y) ** 2))


def anim_gradient(cai_brut, cai_scalat, X_brut, X_scalat, y, pasi=40, titluri=('fara scalare', 'cu scalare')):
    """Doua trasee de gradient descent (liste de [w1, w2], calculate de tine) pe curbele de nivel ale pierderii
    medii patratice mean((X @ w - y)^2). Stanga: datele brute, dreapta: datele scalate."""
    cai = [np.asarray(cai_brut, float), np.asarray(cai_scalat, float)]
    Xs = [np.asarray(X_brut, float), np.asarray(X_scalat, float)]
    y = np.asarray(y, float)
    pasi = min(pasi, min(len(c) for c in cai) - 1)
    fig, axe = plt.subplots(1, 2, figsize=(9.6, 4.2), dpi=DPI)
    linii, puncte, texte = [], [], []
    for ax, c, X, t in zip(axe, cai, Xs, titluri):
        wo = np.linalg.lstsq(X, y, rcond=None)[0]
        toate = np.vstack([c[:pasi + 1], wo])
        lo, hi = toate.min(0), toate.max(0)
        marja = (hi - lo) * 0.12 + 1e-9
        g1 = np.linspace(lo[0] - marja[0], hi[0] + marja[0], 120)
        g2 = np.linspace(lo[1] - marja[1], hi[1] + marja[1], 120)
        L = np.array([[_pierdere(X, y, np.array([a, b])) for a in g1] for b in g2])
        opt, start = _pierdere(X, y, wo), _pierdere(X, y, c[0])
        niv = opt + (start - opt) * np.geomspace(2e-3, 1, 9)
        ax.contour(g1, g2, L, levels=niv, colors=GRI, linewidths=0.8)
        ax.plot(*wo, marker='*', color=VERDE, ms=13, zorder=5, linestyle='')
        ax.set_title(t, fontsize=10, fontweight='bold', color='#333')
        ax.set_xlabel('w1', fontsize=8)
        ax.set_ylabel('w2', fontsize=8)
        ax.tick_params(labelsize=7)
        ax.spines[['top', 'right']].set_visible(False)
        linii.append(ax.plot([], [], '-', color=BRUT, lw=1.2, alpha=0.8)[0])
        puncte.append(ax.plot([], [], 'o', color=ROSU, ms=6, zorder=6)[0])
        texte.append(ax.text(0.03, 0.03, '', transform=ax.transAxes, fontsize=8.5, color='#333',
                             bbox=dict(fc='white', ec='none', alpha=0.8)))
    plt.tight_layout()

    def update(f):
        k = min(f, pasi)
        for i in range(2):
            linii[i].set_data(cai[i][:k + 1, 0], cai[i][:k + 1, 1])
            puncte[i].set_data([cai[i][k, 0]], [cai[i][k, 1]])
            texte[i].set_text(f'pasul {k}, pierdere {_pierdere(Xs[i], y, cai[i][k]):.1f}')
        return []

    ani = animation.FuncAnimation(fig, update, frames=pasi + 6, interval=150, blit=False)
    return _html(fig, ani, fps=7)


def arata_fuga(train, test, nume='valoare'):
    """Grafic static: media pe train (albastru) vs media pe toate datele (rosu). Diferenta e informatia care 'fuge'
    din test in scaler."""
    train, test = np.asarray(train, float), np.asarray(test, float)
    toate = np.concatenate([train, test])
    fig, ax = plt.subplots(figsize=(8, 2.6), dpi=DPI)
    ax.scatter(train, np.zeros(len(train)), s=22, color=NOU, label='train', zorder=3)
    ax.scatter(test, np.zeros(len(test)), s=40, color=BRUT, marker='D', label='test', zorder=4)
    ax.axvline(train.mean(), color=NOU, ls='--', lw=1.5)
    ax.axvline(toate.mean(), color=ROSU, ls='--', lw=1.5)
    ax.annotate(f'media pe train = {train.mean():.2f}', (train.mean(), 0.6), xytext=(-6, 0), textcoords='offset points',
                ha='right', fontsize=8.5, color=NOU)
    ax.annotate(f'media pe toate = {toate.mean():.2f}', (toate.mean(), 0.6), xytext=(6, 0), textcoords='offset points',
                ha='left', fontsize=8.5, color=ROSU)
    ax.set_ylim(-0.5, 1.0)
    ax.set_yticks([])
    ax.set_xlabel(nume, fontsize=9)
    ax.spines[['top', 'right', 'left']].set_visible(False)
    ax.legend(loc='upper center', ncol=2, fontsize=8, frameon=False)
    plt.tight_layout()
    plt.show()
