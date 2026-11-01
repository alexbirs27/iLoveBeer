"""Genereaza imaginile sintetice pentru notebook-ul 09 (deterministe, seed fix): date/09_forme.png si date/09_mic.png.

    python date_09_fisiere.py

09_forme.png: 64x64 RGB - fond crem, patrat rosu, cerc verde, bara albastra, putin zgomot.
09_mic.png:   24x24 tonuri de gri - gradient orizontal, disc intunecat, putin zgomot (pentru anim_pixeli).
"""
import os

import numpy as np
from PIL import Image

AICI = os.path.dirname(os.path.abspath(__file__))
DATE = os.path.normpath(os.path.join(AICI, '..', 'date'))


def forme():
    rng = np.random.default_rng(9)
    img = np.empty((64, 64, 3), dtype=np.int16)
    img[:] = (235, 232, 215)
    img[8:28, 8:28] = (205, 40, 40)                       # patrat rosu
    rr, cc = np.ogrid[:64, :64]
    disc = (rr - 42) ** 2 + (cc - 44) ** 2 <= 13 ** 2
    img[disc] = (35, 155, 65)                             # cerc verde
    img[52:60, 6:58] = (45, 75, 200)                      # bara albastra
    img += rng.integers(-6, 7, img.shape)
    return np.clip(img, 0, 255).astype(np.uint8)


def mic():
    rng = np.random.default_rng(24)
    rr, cc = np.ogrid[:24, :24]
    img = 170 + cc * 3 + 0 * rr                           # gradient: 170 ... 239
    img = np.broadcast_to(img, (24, 24)).astype(np.int16).copy()
    disc = (rr - 11) ** 2 + (cc - 10) ** 2 <= 7 ** 2
    img[disc] = 35
    img += rng.integers(-8, 9, img.shape)
    return np.clip(img, 0, 255).astype(np.uint8)


def main():
    os.makedirs(DATE, exist_ok=True)
    Image.fromarray(forme()).save(os.path.join(DATE, '09_forme.png'), optimize=True)
    Image.fromarray(mic()).save(os.path.join(DATE, '09_mic.png'), optimize=True)
    for f in ('09_forme.png', '09_mic.png'):
        p = os.path.join(DATE, f)
        im = Image.open(p)
        print(f, im.size, im.mode, os.path.getsize(p), 'bytes')


if __name__ == '__main__':
    main()
