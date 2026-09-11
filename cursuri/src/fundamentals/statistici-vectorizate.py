import numpy as np

v = np.random.rand(1_000_000)

# varianta cu bucla - asta calculeaza de fapt v.mean()
def medie_bucla(v):
    s = 0.0
    for x in v:
        s += x
    return s / len(v)

# varianta vectorizata, acelasi rezultat, de zeci de ori mai rapid
v.mean()

# normalizare (z-score): aducem datele la medie 0, deviatie 1
z = (v - v.mean()) / v.std()
