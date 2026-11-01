"""Genereaza 12-normalizare-predare.ipynb si 12-normalizare-tema.ipynb (+ variantele cu solutii)."""
from nb import Carnet

FISIERE = ('date/case.csv', 'anim_normalizare.py')


def predare():
    c = Carnet('Normalizare', 'predare', fisiere=FISIERE)

    c.md("""
## De ce normalizam

Un model nu stie ce e un euro, un metru patrat sau o camera. Vede doar numere. Daca o coloana are valori de ordinul sutelor de mii si alta de ordinul unitatilor, prima decide singura tot.

Normalizarea aduce coloanele pe aceeasi scara, fara sa schimbe forma datelor. E pe lista oficiala ONIA (impreuna cu scalarea, din notebook-ul urmator). Facem intai de mana, cu bucle pe liste mici, pe care le poti urmari in `%%vezi`, apoi cu NumPy, apoi cu `scikit-learn`.
""")

    c.cod("""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

case = pd.read_csv('date/case.csv')
print(case[['suprafata_mp', 'camere', 'pret_eur']].describe().loc[['min', 'max']])
""")

    c.md("""
Uita-te la `pret_eur`: ordinul zecilor de mii. `suprafata_mp`: zeci. `camere`: unitati.

**Prezice inainte sa rulezi:** avem trei case, descrise prin `[suprafata_mp, camere, pret_eur]`:

- A = `[50, 2, 60000]`
- B = `[100, 4, 61000]` (dublu ca suprafata, dublu ca numar de camere, dar acelasi pret aproape)
- C = `[52, 2, 90000]` (aproape identica cu A, doar cu pretul mai mare)

Care e mai aproape de A dupa distanta euclidiana, B sau C?

<details><summary>Raspuns</summary>

B. Distanta A-B este circa 1001, iar A-C este 30000. Pretul a "mancat" toata distanta: diferenta de 50 mp si de 2 camere aproape nu conteaza.
</details>
""")
    c.cod("""
%%vezi
A = [50, 2, 60000]
B = [100, 4, 61000]
C = [52, 2, 90000]
dAB = ((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2 + (A[2] - B[2]) ** 2) ** 0.5   #: 1000 de la pret, 50 si 2 de la rest
dAC = ((A[0] - C[0]) ** 2 + (A[1] - C[1]) ** 2 + (A[2] - C[2]) ** 2) ** 0.5   #: aici pretul e 30000, restul aproape zero
print(dAB > dAC)     #: False: B pare mai aproape de A decat C
""")
    c.md("""
Asta se intampla in orice metoda bazata pe distante (KNN, K-means) si in gradient descent (o vezi la scalare). Solutia: aduci toate coloanele pe aceeasi scara *inainte* sa le dai modelului.

## 1. Min-max: totul intre 0 si 1

Cea mai simpla idee: cea mai mica valoare devine 0, cea mai mare devine 1, iar restul se aseaza proportional intre ele.

`x' = (x - min) / (max - min)`

**Prezice:** pentru lista `[10, 20, 30, 50]`, cat devine `30`?

<details><summary>Raspuns</summary>

`0.5`. `min = 10`, `max = 50`, deci `(30 - 10) / (50 - 10) = 20 / 40 = 0.5`.
</details>
""")
    c.cod("""
%%vezi
v = [10, 20, 30, 50]
mn = min(v)            #: minim si maxim sunt doua parcurgeri ale listei (O(n) fiecare)
mx = max(v)
rez = []
for x in v:
    rez.append((x - mn) / (mx - mn))     #: (x - 10) / 40
""")
    c.md("""
Il punem intr-o functie (o s-o mai folosim) si il rulam pe o lista mai lunga. In animatie, valorile aluneca de pe rigla "brut" pe rigla "transformat". Uita-te ca **forma nu se schimba**: cea mai apropiata pereche ramane cea mai apropiata. Se schimba doar rigla.
""")
    c.cod("""
def norm01(v):
    mn, mx = min(v), max(v)
    return [(x - mn) / (mx - mn) for x in v]

brut = [12, 15, 21, 30, 44, 60]
scalat = norm01(brut)
print([round(x, 3) for x in scalat])
anim_transformare(brut, scalat, 'min-max: (x - min) / (max - min)', zone_transf=[(0, 1)])
""")

    c.md("""
## 2. Min-max in alt interval [a, b]

Uneori vrei `[-1, 1]` (de exemplu pentru anumite retele neuronale) sau `[0, 255]`. Aduci intai totul in `[0, 1]`, apoi intinzi cu `(b - a)` si muti cu `a`:

`x' = a + (x - min) * (b - a) / (max - min)`
""")
    c.cod("""
%%vezi
v = [10, 20, 30, 50]
a, b = -1, 1
mn = min(v)
mx = max(v)
rez = []
for x in v:
    z = (x - mn) / (mx - mn)      #: mai intai in [0, 1]
    rez.append(a + z * (b - a))   #: apoi intins pe (b - a) si mutat cu a
""")

    c.md("""
## 3. Max-abs: impartim la cea mai mare valoare in modul

`x' = x / max(|x|)`. Rezultatul ajunge in `[-1, 1]`, **zero ramane zero** si semnul se pastreaza. De asta se foloseste la date cu multe zerouri (matrici rare): min-max ar muta zerourile.
""")
    c.cod("""
%%vezi
v = [-4, 2, 8, -8, 0]
m = 0
for x in v:
    if abs(x) > m:
        m = abs(x)       #: cea mai mare valoare in modul
rez = []
for x in v:
    rez.append(x / m)    #: 0 ramane 0, -8 devine -1
""")

    c.md("""
## 4. Scalare zecimala

Impartim la cea mai mica putere a lui 10 care aduce toate valorile strict sub 1 in modul: `x' = x / 10^j`. E varianta din carti vechi si din programa oficiala. In practica rar o vei folosi, dar e buna ca exercitiu cu `while`.
""")
    c.cod("""
%%vezi
v = [120, -45, 803, 7]
m = max(max(v), -min(v))       #: cea mai mare valoare in modul
j = 0
while m / 10 ** j >= 1:        #: cat timp nu e sub 1, mai impartim o data la 10
    j = j + 1
rez = []
for x in v:
    rez.append(x / 10 ** j)
""")

    c.md("""
## 5. Normalizarea unui RAND: lungime 1

Pana acum am lucrat pe **coloane** (o caracteristica, mai multe exemple). Aici lucram pe **rand** (un singur exemplu, cu toate caracteristicile lui): il impartim la lungimea lui, ca sa aiba lungime 1.

- norma L2: `||x|| = sqrt(x1^2 + x2^2 + ...)` (lungimea obisnuita)
- norma L1: `|x1| + |x2| + ...` (suma modulelor)

**Prezice:** ce iese daca normalizezi L2 randul `[3, 4]`? Dar `[6, 8]`?

<details><summary>Raspuns</summary>

Amandoua dau `[0.6, 0.8]`. `[6, 8]` e `[3, 4]` de doua ori mai lung, dar pe aceeasi directie. Normalizarea pe rand pastreaza doar directia.
</details>
""")
    c.cod("""
%%vezi
r = [3, 4]
s = 0
for x in r:
    s = s + x * x        #: suma patratelor
lung = s ** 0.5          #: lungimea vectorului: 5.0
rez = []
for x in r:
    rez.append(x / lung) #: [0.6, 0.8]
""")
    c.md("""
In animatie, vectorii aluneca pe cercul de raza 1. **Directia ramane aceeasi**, doar lungimea devine 1.
""")
    c.cod("""
randuri = [[3, 4], [6, 2], [1, 5], [-4, 3]]
unit = []
for r in randuri:
    lung = sum(x * x for x in r) ** 0.5
    unit.append([x / lung for x in r])
anim_linii(randuri, unit, 'normalizare L2 pe randuri')
""")
    c.md("""
**Legatura cu similaritatea cosinus.** Cosinusul unghiului dintre doi vectori este produsul scalar al vectorilor *normalizati*. La texte (cuvinte numarate) un document lung si unul scurt despre acelasi subiect au aceeasi directie, deci cosinus 1, oricat de diferite ar fi lungimile.
""")
    c.cod("""
def unitar(r):
    lung = sum(x * x for x in r) ** 0.5
    return [x / lung for x in r]

u, w = unitar([3, 4]), unitar([6, 8])
print('cosinus dintre [3,4] si [6,8]:', sum(a * b for a, b in zip(u, w)))
print('cosinus dintre [3,4] si [4,-3]:', sum(a * b for a, b in zip(unitar([3, 4]), unitar([4, -3]))))
""")

    c.md("""
## 6. Logaritm pentru date asimetrice

Preturi, populatii, numar de vizite: cateva valori uriase si multe mici. Logaritmul strange valorile mari si le desface pe cele mici: fiecare inmultire cu 10 devine o adunare cu 1. Merge doar pentru valori **pozitive** (`log(0)` nu exista; pentru zerouri se foloseste `log(1 + x)`, adica `np.log1p`).
""")
    c.cod("""
%%vezi
import math
v = [1, 10, 100, 1000, 10000]
rez = []
for x in v:
    rez.append(math.log10(x))     #: fiecare x10 devine +1
""")
    c.cod("""
v = [1, 10, 100, 1000, 10000]
anim_transformare(v, [np.log10(x) for x in v], 'logaritm: x10 devine +1')
""")
    c.md("""
Pe preturile reale: histograma din stanga are un varf lipit de zero si o coada lunga, cea din dreapta seamana cu un clopot.
""")
    c.cod("""
pret = case['pret_eur']
compara_hist(pret, np.log(pret), ('pret_eur', 'log(pret_eur)'))
""")

    c.md("""
## 7. Cu NumPy: aceeasi formula, fara bucla

Operatiile pe un `ndarray` se aplica pe toate elementele deodata (bucla ruleaza in C, pe memorie contigua, fara obiecte Python pe fiecare numar). Formula ramane aceeasi.
""")
    c.cod("""
v = np.array([12, 15, 21, 30, 44, 60])
mm = (v - v.min()) / (v.max() - v.min())
verifica_egal('numpy = de mana', mm, np.array(norm01([12, 15, 21, 30, 44, 60])))
""")
    c.md("""
**De ce e mai rapida?** Ambele sunt O(n), dar constanta difera: in bucla Python fiecare element e un obiect, fiecare operatie trece prin interpretor. Sa masuram pe un milion de numere:
""")
    c.cod("""
import time
mare = np.random.default_rng(0).random(1_000_000) * 100

t0 = time.perf_counter()
mn, mx = min(mare), max(mare)
de_mana = [(x - mn) / (mx - mn) for x in mare]
t1 = time.perf_counter()
vect = (mare - mare.min()) / (mare.max() - mare.min())
t2 = time.perf_counter()

print(f'bucla Python: {t1 - t0:.3f} s   NumPy: {t2 - t1:.4f} s   (de ~{(t1 - t0) / (t2 - t1):.0f} ori mai rapid)')
print('acelasi rezultat:', np.allclose(de_mana, vect))
""")

    c.md("""
## 8. Pe coloane: matrici si `axis`

Un tabel are mai multe coloane si vrem **fiecare coloana** cu minimul si maximul ei. `axis=0` inseamna "de sus in jos", deci un rezultat pentru fiecare coloana. NumPy apoi scade vectorul de minime din fiecare rand (se numeste *broadcasting*).
""")
    c.cod("""
%%vezi
import numpy as np
X = np.array([[1, 100], [2, 300], [3, 200]])
mn = X.min(axis=0)         #: cate un minim PE COLOANA: [1, 100]
mx = X.max(axis=0)         #: [3, 300]
Z = (X - mn) / (mx - mn)   #: mn si mx se aplica pe fiecare rand
""")
    c.md("""
Acum pe case. Am scos cele 3 preturi extreme (le discutam la capcane). In animatie vezi norul de puncte cu **aceeasi scara pe ambele axe**: brut, `pret_eur` intinde totul intr-o linie verticala si suprafata abia se vede; dupa min-max, ambele axe conteaza la fel.
""")
    c.cod("""
ieftine = case[case['pret_eur'] < 500000]
X = ieftine[['suprafata_mp', 'pret_eur']].to_numpy()
Xn = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
anim_scatter_transformare(X, Xn, ('suprafata', 'pret'), 'min-max pe fiecare coloana')
""")

    c.md("""
## 9. Cu scikit-learn

Aceleasi lucruri, ambalate: `MinMaxScaler`, `MaxAbsScaler` (pe coloane) si `Normalizer` (pe randuri). Au mereu doi pasi:

- `fit(X)` **invata** statisticile (minimul si maximul fiecarei coloane) si le tine in `data_min_`, `data_max_`
- `transform(X)` **aplica** formula cu ce a invatat
- `fit_transform(X)` le face pe amandoua

De ce doi pasi? Ca sa poti invata pe datele de antrenare si sa aplici apoi *aceleasi* numere pe datele de test. Vezi asta la capcane.

Nu memora numele: la olimpiada ai documentatia. Trebuie doar sa stii ce face fiecare.
""")
    c.cod("""
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, Normalizer

sc = MinMaxScaler()
Xsk = sc.fit_transform(X)
print('min invatat:', sc.data_min_, ' max invatat:', sc.data_max_)
verifica_egal('MinMaxScaler = de mana', Xsk, Xn)

print(MinMaxScaler(feature_range=(-1, 1)).fit_transform([[10], [20], [30], [50]]).ravel())
print(MaxAbsScaler().fit_transform([[-4], [2], [8], [-8], [0]]).ravel())
print(Normalizer(norm='l2').fit_transform([[3, 4], [6, 8]]))      # pe RANDURI
print(Normalizer(norm='l1').fit_transform([[3, 4], [6, 8]]))
""")

    c.md("""
## 10. Capcane

**Capcana 1: coloana constanta.** Daca `max == min`, formula imparte la 0. In Python pur crapa, in NumPy da `nan` (cu avertisment), iar `MinMaxScaler` pune 0. Cand scrii tu functia, decide ce faci.
""")
    c.cod("""
%%vezi
v = [5, 5, 5]
mn = min(v)
mx = max(v)
rez = [(x - mn) / (mx - mn) for x in v]
""")
    c.cod("""
col = np.array([5.0, 5.0, 5.0])
print((col - col.min()) / (col.max() - col.min()))                     # nan + avertisment
print(MinMaxScaler().fit_transform(col.reshape(-1, 1)).ravel())        # [0. 0. 0.]
""")
    c.md("""
**Capcana 2: o singura valoare extrema turteste restul.** Min-max depinde de minim si de maxim, deci de *cele mai ciudate* doua valori. Un singur punct departe si toate celelalte se strang langa 0.

**Prezice:** valorile normale sunt `[12, 15, 18, 20, 25, 30]`. Cat de mare e intervalul pe care ajung ele dupa min-max daca mai adaugam o valoare de 500?

<details><summary>Raspuns</summary>

De la `[0, 1]` la un interval de latime 0.037: `(30 - 12) / (500 - 12)`. Toate cele 6 valori stau in primul 4% din interval. Animatia de mai jos creste valoarea extrema pas cu pas.
</details>
""")
    c.cod("""
anim_outlier([12, 15, 18, 20, 25, 30], 500, {'min-max': norm01})
""")
    c.md("""
Ce faci: cauti si tratezi outlierii inainte (notebook-ul de EDA), sau folosesti scalari robuste (notebook-ul urmator), sau logaritm.

**Capcana 3: NaN in NumPy.** In `case.csv` coloana `an_constructie` are valori lipsa. `pandas` le sare, NumPy nu:
""")
    c.cod("""
an = case['an_constructie'].to_numpy()
print(an.min(), an.max())                  # nan nan: un singur NaN otraveste tot
print(np.nanmin(an), np.nanmax(an))        # variantele care sar peste NaN
print(case['an_constructie'].min())        # pandas sare singur
""")
    c.md("""
**Capcana 4: rezultatul modelului e in unitati normalizate.** Daca ai normalizat pretul si modelul prezice `0.25`, asta nu e in euro. Te intorci cu formula inversa: `x = z * (max - min) + min`. In `scikit-learn`: `inverse_transform`.
""")
    c.cod("""
pret = case[['pret_eur']].to_numpy()
sc = MinMaxScaler().fit(pret)
z = np.array([[0.0], [0.25], [1.0]])          # ce ar "prezice" un model
print('de mana:', z * (sc.data_max_ - sc.data_min_) + sc.data_min_)
print('sklearn:', sc.inverse_transform(z))
""")
    c.md("""
**Capcana 5: `fit` pe datele de test.** Statisticile (min si max) se invata **doar pe train** si se aplica apoi pe test. Uneori un exemplu de test iese din `[0, 1]` (are o valoare mai mare decat maximul de la train). E normal si trebuie lasat asa: nu il tai, nu refaci scaler-ul.

Daca faci `fit` separat pe test, aceeasi casa primeste alta valoare in train si alta in test, iar modelul invatat nu mai are legatura cu datele pe care le vede.
""")
    c.cod("""
idx = np.random.default_rng(0).permutation(len(case))
train, test = case.iloc[idx[:240]], case.iloc[idx[240:]]
mp_tr, mp_te = train[['suprafata_mp']].to_numpy(), test[['suprafata_mp']].to_numpy()

corect = MinMaxScaler().fit(mp_tr)                    # invata pe train
print('train: min', corect.data_min_[0], ' max', corect.data_max_[0])
print('test:  min', mp_te.min(), ' max', mp_te.max())
arata_train_test(corect.transform(mp_tr), corect.transform(mp_te), 'suprafata: fit pe train, transform pe test')

gresit = MinMaxScaler().fit(mp_te)                    # GRESIT: invata pe test
a = 100
print('casa de 100 mp -> corect:', corect.transform([[a]])[0, 0].round(3), ' gresit (fit pe test):', gresit.transform([[a]])[0, 0].round(3))
""")
    c.md("""
**Capcana 6: randuri sau coloane?** `MinMaxScaler` lucreaza pe **coloane**, `Normalizer` pe **randuri**. Numele seamana, dar fac lucruri diferite. Si daca uiti `axis=0` in NumPy, iei un singur minim si un singur maxim pentru tot tabelul, deci coloanele raman pe scari diferite.
""")
    c.cod("""
M = np.array([[1, 100], [2, 300], [3, 200]])
print('MinMaxScaler (coloane):'); print(MinMaxScaler().fit_transform(M))
print('Normalizer (randuri):'); print(Normalizer().fit_transform(M).round(3))
print('fara axis (un singur min/max):'); print((M - M.min()) / (M.max() - M.min()))
""")
    c.md("""
**Capcana 7: tipul intreg.** Un `ndarray` de intregi ramane de intregi. Daca pui rezultatele inapoi in el, zecimalele se taie in tacere. La fel, `//` in loc de `/`.

**Prezice:** ce afiseaza celula de mai jos?

<details><summary>Raspuns</summary>

`[0 0 0 1]`. Rezultatele `0, 0.25, 0.5, 1.0` sunt puse inapoi intr-un array de intregi si se taie la parte intreaga. Nicio eroare, doar date stricate.
</details>
""")
    c.cod("""
a = np.array([10, 20, 30, 50])
a[:] = (a - a.min()) / (a.max() - a.min())
print(a)

b = np.array([10, 20, 30, 50], dtype=float)      # solutia: array de float
b[:] = (b - b.min()) / (b.max() - b.min())
print(b)
print([(x - 10) // 40 for x in [10, 20, 30, 50]])   # si // strica la fel
""")

    c.md("""
### Cum citesti erorile

- `ZeroDivisionError: division by zero`: `max - min` este 0 (coloana constanta) sau lungimea unui rand e 0 (`[0, 0]`).
- `ValueError: Expected 2D array, got 1D array instead`: scaler-ele din `sklearn` vor tabel (`X.reshape(-1, 1)` pentru o coloana).
- `ValueError: X has 3 features, but MinMaxScaler is expecting 2 features`: ai invatat pe 2 coloane si aplici pe 3.
- `RuntimeWarning: invalid value encountered in divide`: ai `nan` in rezultat (coloana constanta sau `0/0`).
""")
    c.cod("""
for f in (lambda: MinMaxScaler().fit_transform([1, 2, 3]),
          lambda: MinMaxScaler().fit([[1, 2], [3, 4]]).transform([[1, 2, 3]])):
    try:
        f()
    except ValueError as e:
        print(str(e).splitlines()[0])
""")

    c.md("""
## Exercitii

Le rezolvi tu. Toate functiile intorc **liste** (nu array-uri) daca nu scrie altfel.
""")

    c.md("""
**Exercitiul 1.** `min_max(v)`: normalizarea min-max a unei liste in `[0, 1]`. (Poti presupune ca `max != min`.)
""")
    c.ex("""
def min_max(v):
    pass  # TODO
""", """
def min_max(v):
    mn, mx = min(v), max(v)
    return [(x - mn) / (mx - mn) for x in v]
""")
    c.cod("""
import random
verifica('min_max', min_max, [(([10, 20, 30, 50],), [0, 0.25, 0.5, 1.0]), (([-5, 0, 5],), [0, 0.5, 1.0])],
         ascunse=[(([3, 1],), [1.0, 0.0])],
         referinta=lambda v: [(x - min(v)) / (max(v) - min(v)) for x in v],
         generator=lambda: (random.sample(range(-50, 50), random.randint(2, 8)),),
         indiciu='(x - min) / (max - min), pentru fiecare x')
""")

    c.md("""
**Exercitiul 2.** `min_max_ab(v, a, b)`: normalizare in intervalul `[a, b]`.
""")
    c.ex("""
def min_max_ab(v, a, b):
    pass  # TODO
""", """
def min_max_ab(v, a, b):
    mn, mx = min(v), max(v)
    return [a + (x - mn) * (b - a) / (mx - mn) for x in v]
""")
    c.cod("""
verifica('min_max_ab', min_max_ab, [(([10, 20, 30, 50], -1, 1), [-1, -0.5, 0, 1.0]), (([0, 5, 10], 10, 20), [10, 15, 20])],
         referinta=lambda v, a, b: [a + (x - min(v)) / (max(v) - min(v)) * (b - a) for x in v],
         generator=lambda: (random.sample(range(-50, 50), random.randint(2, 8)), random.randint(-5, 0), random.randint(1, 9)),
         indiciu='mai intai in [0, 1], apoi inmultesti cu (b - a) si adaugi a')
""")

    c.md("""
**Exercitiul 3.** `max_abs(v)`: imparte fiecare valoare la cea mai mare valoare in modul.
""")
    c.ex("""
def max_abs(v):
    pass  # TODO
""", """
def max_abs(v):
    m = max(abs(x) for x in v)
    return [x / m for x in v]
""")
    c.cod("""
verifica('max_abs', max_abs, [(([-4, 2, 8, -8, 0],), [-0.5, 0.25, 1.0, -1.0, 0.0]), (([1, 2, 4],), [0.25, 0.5, 1.0])],
         referinta=lambda v: [x / max(abs(y) for y in v) for x in v],
         generator=lambda: ([random.randint(-30, 30) for _ in range(6)] + [31],),
         indiciu='ai nevoie de max(abs(x) ...), nu de max(v)')
""")

    c.md("""
**Exercitiul 4.** `l2_rand(r)`: normalizeaza un rand (o lista de numere) ca sa aiba lungimea 1 (norma L2).
""")
    c.ex("""
def l2_rand(r):
    pass  # TODO
""", """
def l2_rand(r):
    lung = sum(x * x for x in r) ** 0.5
    return [x / lung for x in r]
""")
    c.cod("""
verifica('l2_rand', l2_rand, [(([3, 4],), [0.6, 0.8]), (([0, 5],), [0.0, 1.0]), (([6, 8],), [0.6, 0.8])],
         ascunse=[(([-1, 1],), [-(0.5 ** 0.5), 0.5 ** 0.5])],
         referinta=lambda r: [x / sum(y * y for y in r) ** 0.5 for x in r],
         generator=lambda: ([random.randint(-9, 9) for _ in range(4)] + [10],),
         indiciu='lungimea este radacina sumei patratelor: sum(x * x) ** 0.5')
""")

    c.md("""
**Exercitiul 5.** `log_transform(v)`: intoarce `log(1 + x)` (logaritm natural) pentru fiecare valoare, ca sa mearga si cu 0. Foloseste `math.log1p`.
""")
    c.ex("""
import math


def log_transform(v):
    pass  # TODO
""", """
import math


def log_transform(v):
    return [math.log1p(x) for x in v]
""")
    c.cod("""
import math
verifica('log_transform', log_transform, [(([0, 9, 99],), [0.0, math.log(10), math.log(100)]), (([1000000],), [math.log(1000001)])],
         referinta=lambda v: [math.log(1 + x) for x in v],
         generator=lambda: ([random.randint(0, 10 ** random.randint(1, 6)) for _ in range(5)],))
""")

    c.md("""
**Exercitiul 6.** `min_max_coloane(X)`: `X` este un `ndarray` 2D, intoarce tot un `ndarray` 2D cu fiecare coloana normalizata min-max. Fara bucle, cu `axis=0`. Rezultatul trebuie sa fie identic cu `MinMaxScaler`.
""")
    c.ex("""
def min_max_coloane(X):
    pass  # TODO
""", """
def min_max_coloane(X):
    return (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
""")
    c.cod("""
verifica('min_max_coloane', min_max_coloane,
         [((np.array([[1, 100], [2, 300], [3, 200]]),), np.array([[0, 0], [0.5, 1], [1, 0.5]]))],
         referinta=lambda X: MinMaxScaler().fit_transform(X),
         generator=lambda: (np.random.randint(0, 100, (6, 3)).astype(float),),
         indiciu='X.min(axis=0) si X.max(axis=0) dau cate un numar pe coloana')
""")

    c.md("""
**Exercitiul 7.** `revenire(z, mn, mx)`: ai valori normalizate min-max `z` (o lista) si stii minimul `mn` si maximul `mx` initial. Intoarce valorile originale.
""")
    c.ex("""
def revenire(z, mn, mx):
    pass  # TODO
""", """
def revenire(z, mn, mx):
    return [x * (mx - mn) + mn for x in z]
""")
    c.cod("""
verifica('revenire', revenire, [(([0, 0.25, 1], 10, 50), [10, 20, 50]), (([0.5], 20800, 2600000), [1310400.0])],
         referinta=lambda z, mn, mx: [mn + x * (mx - mn) for x in z],
         generator=lambda: ([random.random() for _ in range(4)], random.randint(0, 9), random.randint(10, 99)))
scor()
""")

    c.md("""
## Recapitulare

- Normalizezi ca sa aduci coloanele pe aceeasi scara: distantele si gradient descent nu mai sunt dominate de o singura coloana.
- Min-max: `(x - min) / (max - min)` in `[0, 1]`; in `[a, b]`: `a + z * (b - a)`. Max-abs: `x / max|x|`, pastreaza zerourile. Zecimala: `x / 10^j`.
- Pe **rand**: L2 (`x / sqrt(suma patratelor)`) si L1 (`x / suma modulelor`), pastreaza directia (legatura cu cosinusul). Pe **coloana**: cele de mai sus.
- Logaritm (`log1p` daca ai zerouri) pentru valori pozitive foarte asimetrice.
- NumPy: aceeasi formula, cu `axis=0` pe tabele, de zeci de ori mai rapid decat bucla. `sklearn`: `fit` invata, `transform` aplica, `inverse_transform` te intoarce.
- Capcane: coloana constanta, un outlier care turteste restul, `nan` in NumPy, `fit` doar pe train (test poate iesi din `[0, 1]`), `axis`, dtype intreg.

In ML: normalizarea e primul pas inainte de KNN, K-means, SVM sau retele neuronale. In notebook-ul urmator vezi *standardizarea* si de ce conteaza in practica.
""")
    c.salveaza('12-normalizare-predare')


def tema():
    c = Carnet('Normalizare', 'tema', fisiere=FISIERE)
    c.md("""
Exercitiile de acasa. Testele ascunse verifica si cazurile limita (liste constante, numere negative, tabele cu `nan`). Functiile intorc **liste** daca nu scrie altfel. Poti rula celulele de verificare de cate ori vrei.
""")
    c.cod("""
import numpy as np
import pandas as pd
import random

case = pd.read_csv('date/case.csv')
""")

    c.md("""
### 1. Min-max sigur

Ca `min_max`, dar daca toate valorile sunt egale (`max == min`) intoarce o lista de zerouri, fara sa imparta la 0.
""")
    c.ex("""
def min_max_sigur(v):
    pass  # TODO
""", """
def min_max_sigur(v):
    mn, mx = min(v), max(v)
    if mx == mn:
        return [0.0] * len(v)
    return [(x - mn) / (mx - mn) for x in v]
""")
    c.cod("""
verifica('min_max_sigur', min_max_sigur, [(([10, 20, 30, 50],), [0, 0.25, 0.5, 1.0]), (([7, 7, 7],), [0.0, 0.0, 0.0])],
         ascunse=[(([5],), [0.0]), (([-2, -2],), [0.0, 0.0]), (([3, 1],), [1.0, 0.0])],
         referinta=lambda v: [(x - min(v)) / (max(v) - min(v)) if max(v) != min(v) else 0.0 for x in v],
         generator=lambda: ([random.randint(-5, 5) for _ in range(random.randint(1, 6))],),
         indiciu='verifica intai daca max == min', puncte=1)
""")

    c.md("""
### 2. Scalare zecimala

Imparte toate valorile la `10 ** j`, unde `j` este cel mai mic intreg `>= 0` pentru care toate valorile ajung **strict** sub 1 in modul. De exemplu `[120, -45, 803, 7]` devine `[0.12, -0.045, 0.803, 0.007]`, iar `[10, 5]` devine `[0.1, 0.05]` (nu `[1.0, 0.5]`).
""")
    c.ex("""
def scala_decimala(v):
    pass  # TODO
""", """
def scala_decimala(v):
    m = max(abs(x) for x in v)
    j = 0
    while m / 10 ** j >= 1:
        j += 1
    return [x / 10 ** j for x in v]
""")
    c.cod("""
def _sd(v):
    m = max(abs(x) for x in v)
    j = 0
    while m / 10 ** j >= 1:
        j += 1
    return [x / 10 ** j for x in v]

verifica('scala_decimala', scala_decimala,
         [(([120, -45, 803, 7],), [0.12, -0.045, 0.803, 0.007]), (([1, 5, 9],), [0.1, 0.5, 0.9]), (([10, 5],), [0.1, 0.05])],
         ascunse=[(([0],), [0.0]), (([1000, -1],), [0.1, -0.0001])],
         referinta=_sd, generator=lambda: ([random.randint(-9999, 9999) for _ in range(5)],),
         indiciu='cat timp max_abs / 10 ** j >= 1, creste j', puncte=2)
""")

    c.md("""
### 3. Normalizare L1 pe randuri

`X` este un `ndarray` 2D. Intoarce un `ndarray` in care fiecare **rand** este impartit la suma modulelor lui (norma L1). Fara bucle. Atentie la `axis` si la `keepdims`.
""")
    c.ex("""
import numpy as np


def l1_randuri(X):
    pass  # TODO
""", """
import numpy as np


def l1_randuri(X):
    return X / np.abs(X).sum(axis=1, keepdims=True)
""")
    c.cod("""
from sklearn.preprocessing import Normalizer


def _gen_l1():
    X = np.random.randint(-9, 10, (5, 3)).astype(float)
    X[:, 0] = np.random.randint(10, 20, 5)      # sa nu avem randuri cu suma 0
    return X


verifica('l1_randuri', l1_randuri,
         [((np.array([[1.0, 3.0], [2.0, 2.0]]),), np.array([[0.25, 0.75], [0.5, 0.5]])),
          ((np.array([[-1.0, 1.0, 2.0]]),), np.array([[-0.25, 0.25, 0.5]]))],
         referinta=lambda X: Normalizer(norm='l1').fit_transform(X),
         generator=lambda: (_gen_l1(),),
         indiciu='X.sum(axis=1) da un numar pe rand; keepdims=True pastreaza forma (n, 1) ca sa mearga impartirea', puncte=2)
""")

    c.md("""
### 4. Test cu statisticile din train

Ai `train` si `test` (liste de numere). Normalizeaza **test** min-max, folosind minimul si maximul din **train**. Valorile din test pot iesi din `[0, 1]`, e in regula. De exemplu `train = [10, 20, 30]`, `test = [0, 15, 40]` da `[-0.5, 0.25, 1.5]`.
""")
    c.ex("""
def aplica_pe_test(train, test):
    pass  # TODO
""", """
def aplica_pe_test(train, test):
    mn, mx = min(train), max(train)
    return [(x - mn) / (mx - mn) for x in test]
""")
    c.cod("""
verifica('aplica_pe_test', aplica_pe_test, [(([10, 20, 30], [0, 15, 40]), [-0.5, 0.25, 1.5]), (([0, 10], [5]), [0.5])],
         referinta=lambda tr, te: [(x - min(tr)) / (max(tr) - min(tr)) for x in te],
         generator=lambda: (random.sample(range(0, 50), 6), [random.randint(-20, 70) for _ in range(4)]),
         indiciu='minimul si maximul se calculeaza din train, nu din test', puncte=2)
""")

    c.md("""
### 5. Cine e cel mai apropiat?

`X` este un `ndarray` cu case (un rand = o casa, coloane: suprafata, camere, pret). Intoarce **indexul** casei cel mai apropiate de casa `i` (distanta euclidiana, fara `i` insasi). Daca `normalizat=True`, intai normalizezi fiecare coloana min-max; daca e `False`, folosesti valorile brute. Vei vedea cu ochii tai cum se schimba raspunsul.
""")
    c.ex("""
import numpy as np


def cel_mai_apropiat(X, i, normalizat):
    pass  # TODO
""", """
import numpy as np


def cel_mai_apropiat(X, i, normalizat):
    X = np.asarray(X, dtype=float)
    if normalizat:
        X = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
    d = np.sqrt(((X - X[i]) ** 2).sum(axis=1))
    d[i] = np.inf
    return int(np.argmin(d))
""")
    c.cod("""
casele = np.array([[50, 2, 60000], [100, 4, 61000], [52, 2, 90000], [70, 3, 75000]])
verifica('cel_mai_apropiat', cel_mai_apropiat,
         [((casele, 0, False), 1), ((casele, 0, True), 3)],
         indiciu='cu normalizare fiecare coloana conteaza la fel; fara ea, decide pretul', puncte=2)
""")
    c.md("""
Acelasi lucru, pe date reale: pentru prima casa din `case.csv` (fara cele 3 preturi extreme), care e cea mai apropiata casa brut si care normalizat? Rezultatul e doar de citit, nu se noteaza.
""")
    c.cod("""
ieftine = case[case['pret_eur'] < 500000]
M = ieftine[['suprafata_mp', 'camere', 'pret_eur']].to_numpy()
print('brut:', cel_mai_apropiat(M, 0, False), '  normalizat:', cel_mai_apropiat(M, 0, True))
""")

    c.md("""
### 6. Tabel cu sklearn

Scrie `normalizeaza_df(df, coloane)`: intoarce o **copie** a lui `df` in care coloanele din lista `coloane` sunt normalizate min-max cu `MinMaxScaler`, iar restul raman neatinse. Valorile lipsa (`NaN`) trebuie sa ramana `NaN`. Nu modifica `df`-ul primit.
""")
    c.ex("""
from sklearn.preprocessing import MinMaxScaler


def normalizeaza_df(df, coloane):
    return df  # TODO
""", """
from sklearn.preprocessing import MinMaxScaler


def normalizeaza_df(df, coloane):
    rez = df.copy()
    rez[coloane] = MinMaxScaler().fit_transform(df[coloane])
    return rez
""")
    c.cod("""
def _ref(df, coloane):
    rez = df.copy()
    for col in coloane:
        rez[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    return rez

mic = pd.DataFrame({'a': [10.0, 20.0, 30.0], 'b': [1.0, np.nan, 3.0], 'nume': ['x', 'y', 'z']})
verifica('normalizeaza_df', normalizeaza_df,
         [((mic, ['a']), _ref(mic, ['a'])), ((mic, ['a', 'b']), _ref(mic, ['a', 'b']))],
         ascunse=[((case, ['suprafata_mp', 'an_constructie']), _ref(case, ['suprafata_mp', 'an_constructie'])),
                  ((case, ['etaj', 'pret_eur', 'camere']), _ref(case, ['etaj', 'pret_eur', 'camere']))],
         indiciu='rez = df.copy(); rez[coloane] = scaler.fit_transform(df[coloane])', puncte=2)
""")

    c.md("""
### 7. Program: normalizeaza numerele

Pe prima linie este `n`, pe a doua linie `n` numere (intregi sau cu zecimale), separate prin spatiu. Afiseaza, pe **o singura linie**, numerele normalizate min-max, fiecare cu **3 zecimale**, separate prin spatiu. Daca toate numerele sunt egale, afiseaza `0.000` pentru fiecare.
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    n = int(input())
    v = list(map(float, input().split()))
    mn, mx = min(v), max(v)
    if mx == mn:
        rez = [0.0] * n
    else:
        rez = [(x - mn) / (mx - mn) for x in v]
    print(' '.join(f'{x:.3f}' for x in rez))
""")
    c.cod("""
verifica_program('program normalizare', main,
                 [(['5', '10 20 30 40 50'], '0.000 0.250 0.500 0.750 1.000'),
                  (['3', '7 7 7'], '0.000 0.000 0.000'),
                  (['4', '1.5 3 0 6'], '0.250 0.500 0.000 1.000')],
                 ascunse=[(['2', '-4 4'], '0.000 1.000'), (['1', '9'], '0.000'),
                          (['6', '100 200 -100 0 50 300'], '0.500 0.750 0.000 0.250 0.375 1.000')], puncte=2)
""")

    c.md("""
### 8. Repara codul: datele gresite

Functia trebuie sa normalizeze `test` folosind minimul si maximul din `train`. Dar da rezultate ciudate: pe `train = [10, 20, 30]` si `test = [15, 25]` ar trebui sa iasa `[0.25, 0.75]`. Uita-te in animatie ce se intampla, apoi repar-o.
""")
    c.cod("""
%%vezi
train = [10, 20, 30]
test = [15, 25]
mn = min(test)
mx = max(test)
rez = [(x - mn) / (mx - mn) for x in test]
""")
    c.ex("""
def normalizeaza_test(train, test):
    mn = min(test)
    mx = max(test)
    return [(x - mn) / (mx - mn) for x in test]
""", """
def normalizeaza_test(train, test):
    mn = min(train)
    mx = max(train)
    return [(x - mn) / (mx - mn) for x in test]
""")
    c.cod("""
verifica('normalizeaza_test', normalizeaza_test, [(([10, 20, 30], [15, 25]), [0.25, 0.75]), (([0, 100], [50, 150]), [0.5, 1.5])],
         ascunse=[(([5, 10], [5]), [0.0]), (([-10, 10], [0, 20]), [0.5, 1.5])],
         indiciu='cine trebuie sa dea minimul si maximul: train sau test?', puncte=1)
""")

    c.md("""
### 9. Repara codul: zecimalele dispar

Functia normalizeaza un array de intregi, dar iese `[0 0 0 1]` in loc de `[0, 0.25, 0.5, 1]`. Cauta problema (capcana 7 din predare).
""")
    c.ex("""
import numpy as np


def normalizeaza_int(a):
    a = np.array(a)
    a[:] = (a - a.min()) / (a.max() - a.min())
    return a
""", """
import numpy as np


def normalizeaza_int(a):
    a = np.array(a, dtype=float)
    a[:] = (a - a.min()) / (a.max() - a.min())
    return a
""")
    c.cod("""
verifica('normalizeaza_int', normalizeaza_int,
         [(([10, 20, 30, 50],), np.array([0, 0.25, 0.5, 1.0])), (([3, 6, 9],), np.array([0, 0.5, 1.0]))],
         ascunse=[(([-4, 0, 4],), np.array([0, 0.5, 1.0]))],
         indiciu='un array de intregi taie zecimalele cand ii pui inapoi rezultate cu virgula', puncte=1)
""")

    c.md("""
### 10. Provocare: normalizeaza fiecare coloana, fara NumPy

`M` este o lista de liste (un tabel, fiecare sublista e un rand, toate au aceeasi lungime). Intoarce tot o lista de liste, cu **fiecare coloana** normalizata min-max. Daca o coloana e constanta, ea devine numai zerouri. Fara NumPy si fara pandas.
""")
    c.ex("""
def normalizeaza_coloane(M):
    pass  # TODO
""", """
def normalizeaza_coloane(M):
    n_col = len(M[0])
    rez = [[0.0] * n_col for _ in M]
    for j in range(n_col):
        col = [rand[j] for rand in M]
        mn, mx = min(col), max(col)
        if mx != mn:
            for i in range(len(M)):
                rez[i][j] = (M[i][j] - mn) / (mx - mn)
    return rez
""")
    c.cod("""
def _nc(M):
    rez = [[0.0] * len(M[0]) for _ in M]
    for j in range(len(M[0])):
        col = [r[j] for r in M]
        for i in range(len(M)):
            if max(col) != min(col):
                rez[i][j] = (M[i][j] - min(col)) / (max(col) - min(col))
    return rez

verifica('normalizeaza_coloane', normalizeaza_coloane,
         [(([[1, 100], [2, 300], [3, 200]],), [[0, 0], [0.5, 1], [1, 0.5]]),
          (([[5, 1], [5, 2]],), [[0, 0], [0, 1]])],
         ascunse=[(([[7]],), [[0.0]])],
         referinta=_nc, generator=lambda: ([[random.randint(0, 9) for _ in range(3)] for _ in range(random.randint(1, 5))],),
         indiciu='mai intai scoate coloana j intr-o lista, apoi calculeaza min si max pentru ea', puncte=3)
scor()
""")
    c.salveaza('12-normalizare-tema')


if __name__ == '__main__':
    predare()
    tema()
