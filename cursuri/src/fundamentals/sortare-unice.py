import numpy as np

v = np.array([5, 2, 8, 2, 5, 1, 9])

np.sort(v)     # array([1, 2, 2, 5, 5, 8, 9])
np.unique(v)   # array([1, 2, 5, 8, 9]), sortat si fara duplicate
np.argmax(v)   # 6, pozitia lui 9 in v, nu valoarea lui
