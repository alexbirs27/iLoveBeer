"""Genereaza 13-scalare-predare.ipynb si 13-scalare-tema.ipynb (+ variantele cu solutii)."""
from nb import Carnet

FISIERE = ('date/elevi.csv', 'date/case.csv', 'anim_normalizare.py', 'anim_scalare.py')

SETUP = """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.pipeline import make_pipeline

case = pd.read_csv('date/case.csv')
elevi = pd.read_csv('date/elevi.csv').drop_duplicates()

vin = load_wine()                       # 178 vinuri, 13 masuratori chimice, 3 soiuri (clase)
Xv, yv = vin.data, vin.target
Xtr, Xte, ytr, yte = train_test_split(Xv, yv, test_size=0.3, random_state=0, stratify=yv)
"""


def predare():
    c = Carnet('Scalare', 'predare', fisiere=FISIERE)

    c.md("""
## Normalizare, scalare, standardizare

Notebook-ul trecut a adus valorile in `[0, 1]`. Aici facem varianta pe care o vei folosi cel mai des in ML: **standardizarea** (z-score). Fiecare valoare devine "cate abateri standard e departe de medie", deci coloana ajunge cu media 0 si abaterea standard 1. Nu are limite fixe: o valoare poate fi `-3` sau `+8`.

Ce e nou fata de notebook-ul trecut: nu doar formula, ci **efectul** ei. Pe date reale vezi cum se schimba vecinii unui punct si traseul lui gradient descent, apoi vezi ce se strica daca calculezi statisticile pe datele gresite (scurgerea de informatie, *data leakage*).
""")
    c.cod(SETUP)

    c.md("""
## 1. Z-score, de mana

`z = (x - media) / abaterea_standard`

Pentru lista `[2, 4, 4, 4, 5, 5, 7, 9]` media este 5 si abaterea standard este 2 (numere alese sa iasa frumos).

**Prezice:** cat devine `9`? Dar `5`?

<details><summary>Raspuns</summary>

`9` devine `(9 - 5) / 2 = 2.0`, iar `5` devine `0.0`. Media ajunge mereu in 0.
</details>
""")
    c.cod("""
%%vezi
v = [2, 4, 4, 4, 5, 5, 7, 9]
n = len(v)
s = 0
for x in v:
    s = s + x
m = s / n                    #: media: 5.0
var = 0
for x in v:
    var = var + (x - m) ** 2   #: suma patratelor abaterilor
var = var / n                #: dispersia: 4.0
sd = var ** 0.5              #: abaterea standard: 2.0
rez = []
for x in v:
    rez.append((x - m) / sd)   #: cate abateri standard e x fata de medie
""")
    c.md("""
Acum cu animatia. Zona verde este "media plus minus o abatere standard": pe rigla de sus e larga, pe cea de jos devine exact `[-1, 1]`. Din nou, forma norului nu se schimba, doar rigla.
""")
    c.cod("""
def z_de_mana(v):
    m = sum(v) / len(v)
    sd = (sum((x - m) ** 2 for x in v) / len(v)) ** 0.5
    return [(x - m) / sd for x in v]

brut = [2, 4, 4, 4, 5, 5, 7, 9]
scalat = z_de_mana(brut)
print(scalat)
print('media:', round(float(np.mean(scalat)), 10), ' abaterea standard:', round(float(np.std(scalat)), 10))
anim_zscore(brut, scalat, 'z-score: (x - media) / abaterea standard')
""")

    c.md("""
## 2. Abaterea standard: populatie sau esantion?

Sunt doua formule aproape identice: impartim suma patratelor la `n` (*populatie*) sau la `n - 1` (*esantion*). Diferenta conteaza la liste scurte si e o capcana clasica: bibliotecile nu au aceeasi valoare implicita.

| unde | implicit | cum schimbi |
|---|---|---|
| `np.std(x)` | `n` (populatie) | `ddof=1` pentru `n - 1` |
| `pd.Series.std()` | `n - 1` (esantion) | `ddof=0` |
| `StandardScaler` | `n` (populatie) | nu se schimba |

**Prezice:** pentru `[2, 4, 4, 4, 5, 5, 7, 9]`, care e mai mare, abaterea din NumPy sau cea din pandas?

<details><summary>Raspuns</summary>

Cea din pandas: 2.138 fata de 2.0. Impartim la 7 in loc de 8, deci rezultatul creste.
</details>
""")
    c.cod("""
%%vezi
v = [2, 4, 4, 4, 5, 5, 7, 9]
n = len(v)
m = sum(v) / n
suma = 0
for x in v:
    suma = suma + (x - m) ** 2
pop = (suma / n) ** 0.5             #: imparte la n: 2.0
esantion = (suma / (n - 1)) ** 0.5  #: imparte la n - 1: putin mai mare
""")
    c.cod("""
v = [2, 4, 4, 4, 5, 5, 7, 9]
print('numpy      :', np.std(v))
print('pandas     :', pd.Series(v).std())
print('numpy ddof1:', np.std(v, ddof=1))
print('sklearn    :', StandardScaler().fit([[x] for x in v]).scale_[0])
""")
    c.md("""
Cand scrii de mana si vrei sa compari cu `StandardScaler`, foloseste **populatia** (`n`). Pe date mari (mii de randuri) diferenta dispare, dar la teste mici te poate costa puncte.

## 3. Cu NumPy si cu scikit-learn

Aceeasi formula, pe fiecare coloana (`axis=0`), fara bucla:
""")
    c.cod("""
X = np.array([[1, 100], [2, 300], [3, 200], [4, 400]], dtype=float)
Z = (X - X.mean(axis=0)) / X.std(axis=0)
print(Z.round(3))
print('media pe coloane:', Z.mean(axis=0).round(6), ' abaterea:', Z.std(axis=0))
""")
    c.md("""
`StandardScaler` face acelasi lucru in doi pasi: `fit` invata media si abaterea (`mean_`, `scale_`), `transform` le aplica. Nu memora numele, la olimpiada ai documentatia; important e sa stii ce calculeaza.
""")
    c.cod("""
sc = StandardScaler()
Zsk = sc.fit_transform(X)
print('medii invatate:', sc.mean_, ' abateri invatate:', sc.scale_)
verifica_egal('StandardScaler = NumPy', Zsk, Z)
""")

    c.md("""
## 4. Scalare robusta: mediana si IQR

Media si abaterea standard sunt sensibile la valori extreme: un singur outlier le trage dupa el. Alternativa: **mediana** in loc de medie si **IQR** (diferenta dintre cuartila 3 si cuartila 1, adica latimea "mijlocului" datelor) in loc de abatere:

`x' = (x - mediana) / (q3 - q1)`

Intai de mana, pe o lista de 7 valori, cu un outlier:
""")
    c.cod("""
%%vezi
v = [12, 15, 18, 20, 25, 30, 500]
s = sorted(v)                #: mediana si cuartilele se citesc din lista sortata
med = s[3]                   #: elementul din mijloc
q1 = (s[1] + s[2]) / 2       #: un sfert din date sunt sub q1
q3 = (s[4] + s[5]) / 2       #: trei sferturi sunt sub q3
iqr = q3 - q1
rez = []
for x in v:
    rez.append((x - med) / iqr)   #: outlierul iese mare, restul raman apropiati de 0
""")
    c.cod("""
def robust_de_mana(v):
    v = np.array(v, dtype=float)
    q1, med, q3 = np.percentile(v, [25, 50, 75])
    return ((v - med) / (q3 - q1)).tolist()

print([round(x, 2) for x in robust_de_mana([12, 15, 18, 20, 25, 30, 500])])
""")
    c.md("""
**Prezice:** adaugam la `[12, 15, 18, 20, 25, 30]` o valoare tot mai mare (pana la 500). Ce se intampla cu celelalte 6 valori dupa z-score? Dar dupa scalarea robusta?

<details><summary>Raspuns</summary>

Dupa z-score se strang tot mai mult unele langa altele (media si abaterea urmaresc outlierul). Dupa scalarea robusta raman aproape pe loc, pentru ca mediana si IQR aproape nu se misca.
</details>
""")
    c.cod("""
anim_outlier([12, 15, 18, 20, 25, 30], 500, {'z-score': z_de_mana, 'robust': robust_de_mana})
""")
    c.md("""
Pe preturile reale (3 case cu preturi extreme). Uita-te la latimea intervalului ocupat de casele obisnuite:
""")
    c.cod("""
pret = case['pret_eur'].to_numpy()
normale = pret < 500000
z, r = z_de_mana(pret), robust_de_mana(pret)
for nume, val in (('z-score', np.array(z)), ('robust', np.array(r))):
    print(f'{nume:8s} casele obisnuite ocupa [{val[normale].min():.2f}, {val[normale].max():.2f}], latime {np.ptp(val[normale]):.2f}')
sc = RobustScaler()
verifica_egal('RobustScaler = de mana', sc.fit_transform(case[['pret_eur']]).ravel(), np.array(r))
""")

    c.md("""
## 5. Cand conteaza scalarea si cand nu

Scalarea conteaza cand modelul foloseste **distante sau marimea numerelor**:

| model | scalare? | de ce |
|---|---|---|
| KNN, K-means | da | distanta euclidiana e dominata de coloana cu cea mai mare scara |
| SVM, retele neuronale | da | distante / gradient descent |
| regresie liniara sau logistica cu regularizare, PCA | da | penalizarea si varianta depind de unitatea de masura |
| arbori de decizie, random forest, gradient boosting | **nu** | compara o singura coloana cu un prag; conteaza ordinea valorilor, nu scara |

**Prezice:** pe setul `wine` (13 masuratori chimice, 3 soiuri), scalezi datele. Care dintre KNN, SVM, arbore de decizie isi schimba acuratetea?

<details><summary>Raspuns</summary>

KNN si SVM se schimba mult. Arborele deloc (aceleasi predictii). Cifrele sunt mai jos.
</details>
""")
    c.cod("""
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

sc = StandardScaler().fit(Xtr)                    # statisticile vin doar din train
Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)

modele = {'KNN': KNeighborsClassifier(5), 'SVM': SVC(), 'regresie logistica': LogisticRegression(max_iter=5000),
          'arbore': DecisionTreeClassifier(random_state=0), 'random forest': RandomForestClassifier(random_state=0)}
linii = []
for nume, m in modele.items():
    p_brut = m.fit(Xtr, ytr).predict(Xte)
    p_sc = m.fit(Xtr_s, ytr).predict(Xte_s)
    linii.append((nume, round((p_brut == yte).mean(), 3), round((p_sc == yte).mean(), 3), bool((p_brut == p_sc).all())))
print(pd.DataFrame(linii, columns=['model', 'fara scalare', 'cu scalare', 'aceleasi predictii']).to_string(index=False))
""")

    c.md("""
## 6. Efectul asupra KNN, vazut cu ochii

Luam doar doua masuratori, `proline` (sute-mii) si `color_intensity` (1-13). KNN clasifica un punct dupa clasa majoritara a celor `k` vecini cei mai apropiati.

Scalam **cu media si abaterea de pe train**, la fel si punctul de interogat. Scriem si KNN-ul de mana, ca sa vezi ca nu e nicio magie:
""")
    c.cod("""
cols = [vin.feature_names.index('proline'), vin.feature_names.index('color_intensity')]
X2tr, X2te = Xtr[:, cols], Xte[:, cols]
q = X2te[12]                                   # punctul de interogat

mu, sd = X2tr.mean(axis=0), X2tr.std(axis=0)
X2s, qs = (X2tr - mu) / sd, (q - mu) / sd      # scalate cu statisticile din train


def vecini(X, punct, k):
    d = []
    for i, rand in enumerate(X):
        d.append((sum((a - b) ** 2 for a, b in zip(rand, punct)) ** 0.5, i))
    d.sort()
    return [i for _, i in d[:k]]


print('interogare:', q, ' clasa adevarata:', yte[12])
print('vecini brut   :', ytr[vecini(X2tr, q, 5)], ' -> clasele lor')
print('vecini scalat :', ytr[vecini(X2s, qs, 5)], ' -> clasele lor')
""")
    c.md("""
In animatie: steaua este punctul de interogat, cercurile rosii sunt vecinii dupa distanta bruta, cele negre punctate dupa cea scalata. **Elipsa verde** este "ce inseamna aproape" pentru metrica curenta: pe datele brute e o fasie ingusta si inalta (doar `proline` conta, `color_intensity` era ignorat), dupa scalare devine aproape un cerc.
""")
    c.cod("""
anim_knn_scalare(X2tr, ytr, q, k=5, X_scalat=X2s, punct_scalat=qs, nume=('proline', 'color_intensity'))
""")
    c.md("""
Acum acuratetea pe tot setul de test. Mai intai cu cele doua coloane, apoi cu toate 13. `KNeighborsClassifier` face exact ce am scris noi in `vecini`, doar mai rapid.
""")
    c.cod("""
def acuratete_knn(Xa, Xb, k=5):
    return KNeighborsClassifier(k).fit(Xa, ytr).score(Xb, yte)

sc2 = StandardScaler().fit(X2tr)
print('2 coloane  fara scalare:', round(acuratete_knn(X2tr, X2te), 3), '  cu scalare:', round(acuratete_knn(sc2.transform(X2tr), sc2.transform(X2te)), 3))
print('13 coloane fara scalare:', round(acuratete_knn(Xtr, Xte), 3), '  cu scalare:', round(acuratete_knn(Xtr_s, Xte_s), 3))
""")
    c.md("""
Aceeasi metoda, aceleasi date. Singura diferenta: cateva linii de scalare. Asta e cel mai ieftin castig de acuratete pe care il vei avea in ML.

## 7. Efectul asupra gradient descent

Regresie liniara pentru pret: `pret ~ w1 * suprafata + w2 * distanta_centru`. Gradient descent porneste din `w = (0, 0)` si face pasi mici in directia care scade eroarea. Pierderea este media patratelor erorilor. Scriem bucla de mana; fiecare pas salveaza pozitia `w`, ca sa desenam drumul.

Am scos cele 3 preturi extreme si am scazut media din pret si din coloane, ca sa nu avem nevoie de termen liber. Varianta "scalata" mai imparte si la abaterea standard.
""")
    c.cod("""
ieftine = case[case['pret_eur'] < 500000]
X = ieftine[['suprafata_mp', 'distanta_centru_km']].to_numpy()
y = ieftine['pret_eur'].to_numpy() / 1000          # in mii de euro
y = y - y.mean()
Xc = X - X.mean(axis=0)                            # centrat, scarile originale
Xs = Xc / X.std(axis=0)                            # centrat si impartit la abatere = z-score


def pierdere(X, y, w):
    return np.mean((X @ w - y) ** 2)


def gradient_descent(X, y, lr, pasi):
    w = np.zeros(2)
    cai = [w.copy()]
    for _ in range(pasi):
        grad = 2 * X.T @ (X @ w - y) / len(y)      # derivata pierderii in raport cu w
        w = w - lr * grad                          # pas mic in sens invers
        cai.append(w.copy())
    return np.array(cai)


print('scari brute   :', X.std(axis=0).round(1), '   scari dupa scalare:', Xs.std(axis=0).round(1))
""")
    c.md("""
Un detaliu important: cu datele brute pasul `lr` trebuie sa fie **foarte mic** (`0.0015`); peste `0.0016` pasii cresc de la o iteratie la alta si totul explodeaza. Cu datele scalate poti folosi `0.4`.

**Prezice:** dupa cate pasi ajunge fiecare varianta la o pierdere apropiata de minim?

<details><summary>Raspuns</summary>

Fara scalare: aproximativ 70 de pasi. Cu scalare: 3.
</details>
""")
    c.cod("""
cai_brut = gradient_descent(Xc, y, 1.5e-3, 60)
cai_scalat = gradient_descent(Xs, y, 0.4, 60)
anim_gradient(cai_brut, cai_scalat, Xc, Xs, y)
""")
    c.md("""
Stanga: valea pierderii e lunga si ingusta (coloana `suprafata` are scara mult mai mare), deci gradientul arata mai ales "peste vale", iar traseul face zig-zag. Dreapta: contururile sunt aproape cercuri, gradientul arata direct spre minim.

Sa numaram pasii, de mana:
""")
    c.cod("""
def pasi_pana_aproape(X, y, lr, toleranta=0.5):
    opt = pierdere(X, y, np.linalg.lstsq(X, y, rcond=None)[0])     # minimul adevarat
    w = np.zeros(2)
    for k in range(1, 100000):
        w = w - lr * 2 * X.T @ (X @ w - y) / len(y)
        if pierdere(X, y, w) < opt + toleranta:
            return k

print('fara scalare:', pasi_pana_aproape(Xc, y, 1.5e-3), 'pasi   cu scalare:', pasi_pana_aproape(Xs, y, 0.4), 'pasi')
print('brut, lr mai mare (0.0017), pierdere dupa 60 de pasi:', round(pierdere(Xc, y, gradient_descent(Xc, y, 1.7e-3, 60)[-1])))
""")
    c.md("""
De aici vine si legatura cu regularizarea: penalizarea `L1`/`L2` apasa pe coeficienti, iar un coeficient depinde de unitatea de masura a coloanei. Fara scalare, penalizezi coloanele "mici" mai mult doar pentru ca sunt exprimate in unitati mici.

## 8. Scurgerea de informatie (data leakage)

Regula: statisticile (medie, abatere, mediana...) se **invata doar pe train** si se aplica apoi pe test. Testul trebuie sa joace rolul datelor pe care modelul nu le-a vazut niciodata. Daca faci `fit` pe tot setul, informatia din test intra in transformarea datelor de train.

Exemplu concret pe `elevi.csv`, coloana `absente`, care are doua valori extreme (87 si 120). In split-ul de mai jos, valoarea 120 ajunge in test:
""")
    c.cod("""
d = elevi[['nota_info', 'ore_studiu', 'absente', 'calificat']].dropna()
tr, te = train_test_split(d, test_size=0.25, random_state=6)
arata_fuga(tr['absente'], te['absente'], 'absente')
""")
    c.cod("""
sc_train = StandardScaler().fit(tr[['absente']])            # corect: doar train
sc_toate = StandardScaler().fit(d[['absente']])             # scurgere: si test
sc_test = StandardScaler().fit(te[['absente']])             # si mai grav: fit pe test
dupa = pd.DataFrame({'absente': [20]})                      # un elev cu 20 de absente
print('                     media   abaterea   z pentru 20 absente')
for nume, s in (('fit pe train  ', sc_train), ('fit pe toate  ', sc_toate), ('fit pe test   ', sc_test)):
    print(f'{nume}      {s.mean_[0]:6.2f}   {s.scale_[0]:6.2f}   {s.transform(dupa)[0, 0]:8.3f}')
""")
    c.md("""
Aceeasi valoare, `20` de absente, primeste alt numar in fiecare varianta. In cea de a doua, media si abaterea folosite pe **train** au fost trase de o valoare din **test**: modelul a "vazut" ceva ce nu avea voie. In a treia, cel mai grav, datele de test sunt scalate cu alte numere decat cele de train, deci modelul primeste alte valori decat cele pentru care a invatat.

Si un argument practic: cand modelul e folosit pe date noi, un elev la un moment dat, nu ai un "toate datele" din care sa calculezi media.

`fit_transform` pe train, doar `transform` pe test:

| apel | ce face | pe ce set |
|---|---|---|
| `fit(X)` | invata statisticile | doar train |
| `transform(X)` | aplica statisticile invatate | train, test, date noi |
| `fit_transform(X)` | ambele, la o singura trecere | doar train |

Sa vedem cum se vede asta in cod: aceeasi logica, scrisa de mana, cu un dictionar de parametri care circula de la train la test.
""")
    c.cod("""
%%vezi
def fit(v):
    m = sum(v) / len(v)
    s = 0
    for x in v:
        s = s + (x - m) ** 2
    return {'medie': m, 'std': (s / len(v)) ** 0.5}   #: parametrii invatati

def transform(v, p):
    return [(x - p['medie']) / p['std'] for x in v]

train = [2, 4, 4, 4, 5, 5, 7, 9]
test = [5, 9, 1]
p = fit(train)                 #: statisticile vin doar din train
tr = transform(train, p)
te = transform(test, p)        #: aceiasi parametri pe test: 9 -> 2.0, 1 -> -2.0
""")

    c.md("""
### Pipeline: greseala devine imposibila

Cel mai bun mod sa nu gresesti este sa nu scrii singur `fit`/`transform`. Un `Pipeline` leaga scaler-ul de model: cand ii spui `fit(X_train, y_train)`, scaler-ul invata pe train si modelul invata pe datele scalate; cand ii spui `predict(X_test)`, scaler-ul doar aplica.

Mai important, in **validare incrucisata** (`cross_val_score`), pipeline-ul refoloseste procedura corecta pe fiecare fold, cu scaler-ul invatat doar pe partea de antrenare a fold-ului. Daca scalezi tot setul inainte, fiecare fold de validare a contribuit la media si abaterea folosite.
""")
    c.cod("""
knn = KNeighborsClassifier(5)
fara = cross_val_score(knn, Xv, yv, cv=5).mean()                                 # fara scalare
scurgere = cross_val_score(knn, StandardScaler().fit_transform(Xv), yv, cv=5).mean()   # scalat pe TOT inainte de CV
pipe = make_pipeline(StandardScaler(), knn)
corect = cross_val_score(pipe, Xv, yv, cv=5).mean()                              # scaler in pipeline
print(f'fara scalare: {fara:.3f}   scalat pe tot (scurgere): {scurgere:.3f}   pipeline (corect): {corect:.3f}')
""")
    c.md("""
Aici diferenta dintre a doua si a treia cifra e mica, pentru ca scalarea "fura" putin. In alte cazuri (imputare, selectia coloanelor, seturi mici) scurgerea umfla scorul serios. Obiceiul bun: **totul** ce invata ceva din date sta in pipeline.

## 9. Ce nu merita scalat: coloane binare

Coloanele 0/1 (de exemplu `meditatii` da/nu, sau coloanele *one-hot*) au deja scara `[0, 1]`, comparabila cu a celorlalte dupa scalare. Le scalezi si nu castigi informatie, doar pierzi interpretarea ("0 = nu, 1 = da") si, la matrici rare, chiar zerourile.
""")
    c.cod("""
med = elevi['meditatii'].str.strip().str.lower().map({'da': 1, 'nu': 0}).dropna().to_numpy().reshape(-1, 1)
print('valori initiale:', np.unique(med))
print('dupa StandardScaler:', np.unique(StandardScaler().fit_transform(med).round(3)))
""")
    c.md("""
Aceleasi doua valori, doar cu alte etichete.

## 10. Capcane

**Capcana 1: coloana constanta.** `std = 0`, deci imparti la 0. NumPy da `nan`, `StandardScaler` pune `scale_ = 1` si coloana devine 0.
""")
    c.cod("""
col = np.array([[5.0], [5.0], [5.0]])
print((col - col.mean()) / col.std())                          # nan + avertisment
sc = StandardScaler().fit(col)
print('scale_ =', sc.scale_, ' rezultat:', sc.transform(col).ravel())
""")
    c.md("""
**Capcana 2: `NaN`.** `np.mean` da `nan` daca exista un singur `NaN`. `StandardScaler` le ignora la `fit` si le lasa `NaN` la `transform`. Dar KNN si multe alte modele nu accepta `NaN`: tratezi valorile lipsa (cu statistici tot de pe train) inainte de model.
""")
    c.cod("""
nota = elevi[['nota_info']].to_numpy()
sc = StandardScaler().fit(nota)
print('np.mean:', nota.mean(), '  media invatata de scaler:', sc.mean_.round(3))
print('NaN dupa transform:', int(np.isnan(sc.transform(nota)).sum()), '(raman NaN)')
""")
    c.md("""
**Capcana 3: din `DataFrame` iese un `ndarray`.** Numele coloanelor se pierd. Daca vrei un `DataFrame` inapoi: `set_output(transform='pandas')`.
""")
    c.cod("""
print(StandardScaler().fit_transform(d[['nota_info', 'ore_studiu']])[:2])
print(StandardScaler().set_output(transform='pandas').fit_transform(d[['nota_info', 'ore_studiu']]).head(2))
""")
    c.md("""
**Capcana 4: scalezi si tinta `y`.** Rar e necesar (retele neuronale, uneori). Daca o faci, predictiile modelului sunt in unitati scalate, deci le aduci inapoi cu `inverse_transform`, altfel eroarea pare mica pentru ca nu e in euro.
""")
    c.cod("""
scy = StandardScaler().fit(case[['pret_eur']])
prezis_z = np.array([[0.0], [1.0]])                 # ce "prezice" un model antrenat pe pretul scalat
print(scy.inverse_transform(prezis_z).ravel(), '(0 -> pretul mediu, 1 -> media + o abatere)')
""")
    c.md("""
**Capcana 5: scalezi inainte de `train_test_split`.** E aceeasi scurgere din sectiunea 8, doar mai greu de vazut in cod. Ordinea corecta: imparti, `fit` pe train, `transform` pe amandoua. Sau pipeline.

### Cum citesti erorile

- `NotFittedError: This StandardScaler instance is not fitted yet`: ai apelat `transform` inainte de `fit`.
- `ValueError: X has 3 features, but StandardScaler is expecting 2`: ai invatat pe 2 coloane si aplici pe 3.
- `ValueError: Input X contains NaN` (la KNN, SVM, regresie): modelul nu accepta valori lipsa; imputeaza mai intai.
- `RuntimeWarning: invalid value encountered in divide`: `std = 0` sau `NaN` in datele tale.
""")
    c.cod("""
from sklearn.exceptions import NotFittedError
incercari = (lambda: StandardScaler().transform([[1.0]]),
             lambda: StandardScaler().fit([[1.0, 2.0], [3.0, 4.0]]).transform([[1.0, 2.0, 3.0]]),
             lambda: KNeighborsClassifier(1).fit([[1.0], [np.nan]], [0, 1]))
for f in incercari:
    try:
        f()
    except ValueError as e:
        print(type(e).__name__, ':', str(e).splitlines()[0][:110])
""")

    c.md("""
## Exercitii

Toate functiile intorc **liste** daca nu scrie altfel.
""")
    c.md("""
**Exercitiul 1.** `zscore(v)`: standardizeaza o lista (abaterea standard de populatie, cu `n`). Poti presupune ca valorile nu sunt toate egale.
""")
    c.ex("""
def zscore(v):
    pass  # TODO
""", """
def zscore(v):
    m = sum(v) / len(v)
    sd = (sum((x - m) ** 2 for x in v) / len(v)) ** 0.5
    return [(x - m) / sd for x in v]
""")
    c.cod("""
verifica('zscore', zscore, [(([2, 4, 4, 4, 5, 5, 7, 9],), [-1.5, -0.5, -0.5, -0.5, 0, 0, 1, 2]), (([1, 3],), [-1.0, 1.0])],
         referinta=lambda v: list((np.array(v) - np.mean(v)) / np.std(v)),
         generator=lambda: (random.sample(range(-50, 50), random.randint(2, 8)),),
         indiciu='(x - media) / abaterea, iar abaterea = radacina din media patratelor abaterilor')
""")

    c.md("""
**Exercitiul 2.** `abateri(v)`: intoarce perechea `(abatere_populatie, abatere_esantion)`, in aceasta ordine, calculate de mana (fara `np.std`).
""")
    c.ex("""
def abateri(v):
    pass  # TODO
""", """
def abateri(v):
    n = len(v)
    m = sum(v) / n
    suma = sum((x - m) ** 2 for x in v)
    return (suma / n) ** 0.5, (suma / (n - 1)) ** 0.5
""")
    c.cod("""
verifica('abateri', abateri, [(([2, 4, 4, 4, 5, 5, 7, 9],), (2.0, 2.138089935299395)), (([1, 3],), (1.0, 2 ** 0.5))],
         referinta=lambda v: (float(np.std(v)), float(np.std(v, ddof=1))),
         generator=lambda: (random.sample(range(-50, 50), random.randint(2, 8)),),
         indiciu='suma patratelor abaterilor se imparte la n, respectiv la n - 1')
""")

    c.md("""
**Exercitiul 3.** `robust_coloane(X)`: `X` este un `ndarray` 2D. Intoarce `ndarray`-ul scalat robust pe fiecare coloana: `(x - mediana) / (q3 - q1)`. Ai nevoie de `axis=0`. (Poti presupune ca `q3 != q1`.)
""")
    c.ex("""
def robust_coloane(X):
    pass  # TODO
""", """
def robust_coloane(X):
    q1, q3 = np.percentile(X, [25, 75], axis=0)
    return (X - np.median(X, axis=0)) / (q3 - q1)
""")
    c.cod("""
verifica('robust_coloane', robust_coloane,
         [((np.array([[12.], [15.], [18.], [20.], [25.], [30.], [500.]]),), np.array([[-8 / 11], [-5 / 11], [-2 / 11], [0.], [5 / 11], [10 / 11], [480 / 11]]))],
         referinta=lambda X: RobustScaler().fit_transform(X),
         generator=lambda: (np.random.rand(7, 3) * 100,),
         indiciu='np.percentile(X, [25, 75], axis=0) da cele doua cuartile, pe coloane')
""")

    c.md("""
**Exercitiul 4.** Care dintre modelele de mai jos au nevoie de scalare? Completeaza cele doua liste (fiecare model intr-una singura).
""")
    c.ex("""
modele = ['KNN', 'SVM', 'Regresie logistica', 'Arbore de decizie', 'Random Forest', 'K-means',
          'Retea neuronala', 'PCA', 'Gradient Boosting']
cu_scalare = []       # TODO
fara_scalare = []     # TODO
""", """
modele = ['KNN', 'SVM', 'Regresie logistica', 'Arbore de decizie', 'Random Forest', 'K-means',
          'Retea neuronala', 'PCA', 'Gradient Boosting']
cu_scalare = ['KNN', 'SVM', 'Regresie logistica', 'K-means', 'Retea neuronala', 'PCA']
fara_scalare = ['Arbore de decizie', 'Random Forest', 'Gradient Boosting']
""")
    c.cod("""
verifica_egal('modele cu scalare', sorted(cu_scalare), sorted(['KNN', 'SVM', 'Regresie logistica', 'K-means', 'Retea neuronala', 'PCA']),
              indiciu='distante sau gradient descent: da. Arbori (si padurile de arbori): nu')
verifica_egal('modele fara scalare', sorted(fara_scalare), sorted(['Arbore de decizie', 'Random Forest', 'Gradient Boosting']))
""")

    c.md("""
**Exercitiul 5.** `scaleaza_train_test(train, test)`: standardizeaza ambele liste folosind media si abaterea (populatie) **din train**. Intoarce tuplul `(train_scalat, test_scalat)`.
""")
    c.ex("""
def scaleaza_train_test(train, test):
    pass  # TODO
""", """
def scaleaza_train_test(train, test):
    m = sum(train) / len(train)
    sd = (sum((x - m) ** 2 for x in train) / len(train)) ** 0.5
    return [(x - m) / sd for x in train], [(x - m) / sd for x in test]
""")
    c.cod("""
def _ref_st(tr, te):
    m, s = np.mean(tr), np.std(tr)
    return list((np.array(tr) - m) / s), list((np.array(te) - m) / s)

verifica('scaleaza_train_test', scaleaza_train_test,
         [(([2, 4, 4, 4, 5, 5, 7, 9], [5, 9, 1]), ([-1.5, -0.5, -0.5, -0.5, 0, 0, 1, 2], [0, 2, -2]))],
         referinta=_ref_st, generator=lambda: (random.sample(range(0, 40), 6), [random.randint(-20, 60) for _ in range(4)]),
         indiciu='media si abaterea se calculeaza din train si se folosesc si pe test')
""")

    c.md("""
**Exercitiul 6.** `construieste_model()`: intoarce un `Pipeline` cu `StandardScaler` urmat de `KNeighborsClassifier(5)`. Verificarea il antreneaza pe `wine` si cere acuratete peste 0.9.
""")
    c.ex("""
def construieste_model():
    pass  # TODO
""", """
def construieste_model():
    return make_pipeline(StandardScaler(), KNeighborsClassifier(5))
""")
    c.cod("""
def _verif_pipe():
    m = construieste_model()
    primul = type(m.steps[0][1]).__name__
    m.fit(Xtr, ytr)
    return primul, bool(m.score(Xte, yte) > 0.9)

verifica('pipeline', _verif_pipe, [((), ('StandardScaler', True))], indiciu='make_pipeline(scaler, model)')
scor()
""")

    c.md("""
## Recapitulare

- Z-score: `(x - media) / abaterea`. Rezultatul are media 0 si abaterea 1. NumPy: `axis=0` pe tabele. `StandardScaler`: `fit` invata `mean_` si `scale_`, `transform` aplica.
- Abaterea de **populatie** (`n`) o folosesc `np.std` si `StandardScaler`; cea de **esantion** (`n - 1`) o foloseste implicit `pandas`.
- Scalare robusta: `(x - mediana) / IQR`. Rezista la outlieri, spre deosebire de media si abaterea standard.
- Conteaza pentru KNN, K-means, SVM, retele neuronale, modele cu regularizare, PCA, gradient descent. Nu conteaza pentru arbori si paduri de arbori. Coloanele 0/1 nu se scaleaza.
- Efectul: vecinii se schimba (acuratetea KNN pe `wine` creste de la circa 0.72 la circa 0.96), iar gradient descent ajunge la minim in cativa pasi in loc de zeci.
- `fit` **doar pe train**, `transform` pe train si pe test. Pipeline face asta fara sa mai poti gresi, inclusiv in validarea incrucisata.
- Capcane: `std = 0`, `NaN`, `DataFrame` devine `ndarray`, `y` scalat trebuie adus inapoi, scalare inainte de split.

In ML: scalarea, imputarea si modelul intra impreuna intr-un pipeline. La mini-olimpiada de la final vei face exact asta.
""")
    c.salveaza('13-scalare-predare')


def tema():
    c = Carnet('Scalare', 'tema', fisiere=FISIERE)
    c.md("""
Exercitiile de acasa. Testele ascunse verifica si cazurile limita (liste constante, valori extreme, coloane cu `std = 0`). Functiile intorc **liste** daca nu scrie altfel.
""")
    c.cod(SETUP)

    c.md("""
### 1. Z-score cu `ddof`

`standardizeaza(v, ddof)`: standardizeaza lista `v`. Abaterea standard se calculeaza impartind suma patratelor la `n - ddof` (`ddof=0` populatie, `ddof=1` esantion). Daca abaterea e 0, intoarce zerouri.
""")
    c.ex("""
def standardizeaza(v, ddof):
    pass  # TODO
""", """
def standardizeaza(v, ddof):
    n = len(v)
    m = sum(v) / n
    sd = (sum((x - m) ** 2 for x in v) / (n - ddof)) ** 0.5
    if sd == 0:
        return [0.0] * n
    return [(x - m) / sd for x in v]
""")
    c.cod("""
def _ref_z(v, ddof):
    a = np.array(v, dtype=float)
    s = a.std(ddof=ddof)
    return [0.0] * len(v) if s == 0 else list((a - a.mean()) / s)

verifica('standardizeaza', standardizeaza,
         [(([2, 4, 4, 4, 5, 5, 7, 9], 0), [-1.5, -0.5, -0.5, -0.5, 0, 0, 1, 2]), (([1, 3], 1), [-(0.5 ** 0.5), 0.5 ** 0.5])],
         ascunse=[(([5, 5, 5], 0), [0.0, 0.0, 0.0]), (([7, 7], 1), [0.0, 0.0])],
         referinta=_ref_z, generator=lambda: (random.sample(range(-30, 30), random.randint(3, 7)), random.randint(0, 1)),
         indiciu='ddof spune cu cat scazi n la impartire; verifica si std == 0', puncte=2)
""")

    c.md("""
### 2. Scalare robusta

`robust_scaleaza(v)`: `(x - mediana) / (q3 - q1)`, cu cuartilele din `np.percentile` (interpolare liniara, cea implicita). Daca IQR este 0, imparte la 1 (asa face si `RobustScaler`).
""")
    c.ex("""
def robust_scaleaza(v):
    pass  # TODO
""", """
def robust_scaleaza(v):
    a = np.array(v, dtype=float)
    q1, med, q3 = np.percentile(a, [25, 50, 75])
    iqr = q3 - q1 if q3 != q1 else 1.0
    return list((a - med) / iqr)
""")
    c.cod("""
def _ref_rob(v):
    return [float(x) for x in RobustScaler().fit_transform(np.array(v, dtype=float).reshape(-1, 1)).ravel()]

verifica('robust_scaleaza', robust_scaleaza,
         [(([12, 15, 18, 20, 25, 30, 500],), [-8 / 11, -5 / 11, -2 / 11, 0, 5 / 11, 10 / 11, 480 / 11])],
         ascunse=[(([5, 5, 5, 5],), [0.0, 0.0, 0.0, 0.0]), (([1, 1, 1, 1, 9],), [0.0, 0.0, 0.0, 0.0, 8.0])],
         referinta=_ref_rob, generator=lambda: ([random.randint(-40, 40) for _ in range(random.randint(4, 9))],),
         indiciu='np.percentile(a, [25, 50, 75]) da q1, mediana, q3 dintr-o singura chemare', puncte=2)
""")

    c.md("""
### 3. Outlieri dupa z-score

`outlieri_z(v, prag)`: intoarce lista **indicilor** valorilor pentru care `|z| > prag` (z-score cu abatere de populatie), in ordine crescatoare. Cu asta poti gasi valorile ciudate inainte sa scalezi.
""")
    c.ex("""
def outlieri_z(v, prag):
    pass  # TODO
""", """
def outlieri_z(v, prag):
    a = np.array(v, dtype=float)
    z = (a - a.mean()) / a.std()
    return [i for i in range(len(v)) if abs(z[i]) > prag]
""")
    c.cod("""
def _ref_out(v, prag):
    a = np.array(v, dtype=float)
    return [int(i) for i in np.where(np.abs((a - a.mean()) / a.std()) > prag)[0]]

verifica('outlieri_z', outlieri_z,
         [(([10] * 9 + [100], 2), [9]), (([1, 2, 3, 4, 5], 2), []), (([1, 2, 3, 4, 5], 1), [0, 4])],
         referinta=_ref_out, generator=lambda: ([random.randint(0, 10) for _ in range(12)] + [random.choice([-60, 80])], 2),
         indiciu='calculeaza z pentru fiecare valoare, apoi pastreaza indicii cu |z| > prag', puncte=2)
""")

    c.md("""
### 4. Cat de mult "fuge" informatia

`diferenta_fuga(train, test)`: calculeaza z-score-ul **primei valori din test** in doua feluri: cu media si abaterea (populatie) de pe `train`, si cu cele de pe `train + test` la un loc (varianta cu scurgere). Intoarce valoarea absoluta a diferentei dintre cele doua.
""")
    c.ex("""
def diferenta_fuga(train, test):
    pass  # TODO
""", """
def diferenta_fuga(train, test):
    def z(x, date):
        return (x - np.mean(date)) / np.std(date)
    return abs(z(test[0], train) - z(test[0], train + test))
""")
    c.cod("""
def _ref_fuga(tr, te):
    tot = tr + te
    return abs((te[0] - np.mean(tr)) / np.std(tr) - (te[0] - np.mean(tot)) / np.std(tot))

verifica('diferenta_fuga', diferenta_fuga,
         [(([0, 10], [20]), 3 - 10 / (200 / 3) ** 0.5), (([1, 2, 3], [2]), 0.0)],
         referinta=_ref_fuga, generator=lambda: (random.sample(range(0, 30), 6), random.sample(range(-40, 80), 3)),
         indiciu='calculeaza z de doua ori: o data cu statisticile din train, o data cu cele din train + test', puncte=2)
""")

    c.md("""
### 5. KNN cu si fara scalare

`acuratete_knn(scalat)`: antreneaza `KNeighborsClassifier(5)` pe `Xtr, ytr` (setul `wine` din prima celula) si intoarce acuratetea pe `Xte, yte`. Daca `scalat=True`, scaleaza intai cu `StandardScaler`, **cu statisticile din train**. Ar trebui sa vezi circa `0.72` si circa `0.96`.
""")
    c.ex("""
def acuratete_knn(scalat):
    pass  # TODO
""", """
def acuratete_knn(scalat):
    A, B = Xtr, Xte
    if scalat:
        sc = StandardScaler().fit(Xtr)
        A, B = sc.transform(Xtr), sc.transform(Xte)
    return KNeighborsClassifier(5).fit(A, ytr).score(B, yte)
""")
    c.cod("""
verifica('acuratete_knn', acuratete_knn, [((False,), 39 / 54), ((True,), 52 / 54)],
         indiciu='fit pe Xtr, transform pe Xtr si pe Xte', puncte=2)
""")

    c.md("""
### 6. Un pipeline pentru regresia logistica

`construieste_pipeline()`: intoarce un `Pipeline` cu doi pasi, `StandardScaler` si `LogisticRegression(max_iter=1000)`, in aceasta ordine. Verificarea il evalueaza cu validare incrucisata pe `wine`.
""")
    c.ex("""
def construieste_pipeline():
    pass  # TODO
""", """
def construieste_pipeline():
    from sklearn.linear_model import LogisticRegression
    return make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
""")
    c.cod("""
def _verif_pipeline():
    p = construieste_pipeline()
    nume = [type(s[1]).__name__ for s in p.steps]
    return nume, bool(cross_val_score(p, Xv, yv, cv=5).mean() > 0.95)

verifica('construieste_pipeline', _verif_pipeline, [((), (['StandardScaler', 'LogisticRegression'], True))],
         indiciu='make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))', puncte=2)
""")

    c.md("""
### 7. Program: z-score

Pe prima linie este `n`, pe a doua `n` numere. Afiseaza, **cate unul pe linie**, z-score-ul fiecaruia (abaterea standard de populatie), cu **3 zecimale**. Daca toate numerele sunt egale, afiseaza `0.000` pentru fiecare.
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    n = int(input())
    v = list(map(float, input().split()))
    m = sum(v) / n
    sd = (sum((x - m) ** 2 for x in v) / n) ** 0.5
    for x in v:
        print(f'{(x - m) / sd if sd else 0.0:.3f}')
""")
    c.cod("""
verifica_program('program z-score', main,
                 [(['8', '2 4 4 4 5 5 7 9'], '-1.500\\n-0.500\\n-0.500\\n-0.500\\n0.000\\n0.000\\n1.000\\n2.000'),
                  (['3', '7 7 7'], '0.000\\n0.000\\n0.000'),
                  (['2', '-4 4'], '-1.000\\n1.000')],
                 ascunse=[(['3', '1 2 3'], '-1.225\\n0.000\\n1.225'), (['1', '5'], '0.000'),
                          (['4', '10 20 30 40'], '-1.342\\n-0.447\\n0.447\\n1.342')], puncte=2)
""")

    c.md("""
### 8. Repara codul: scaler-ul invatat pe tot

Functia trebuie sa scaleze `train` si `test` cu statisticile din `train`. Pare corecta, dar cu `train = [2, 4, 4, 4, 5, 5, 7, 9]` si `test = [5, 9]` nu iese `[0, 2]` pentru test. Uita-te in animatie de unde vin media si abaterea, apoi repar-o.
""")
    c.cod("""
%%vezi
train = [2, 4]
test = [6, 100]
toate = train + test
m = sum(toate) / len(toate)
s = 0
for x in toate:
    s = s + (x - m) ** 2
sd = (s / len(toate)) ** 0.5
rez_test = [(x - m) / sd for x in test]
""")
    c.ex("""
def scaleaza(train, test):
    toate = train + test
    m = sum(toate) / len(toate)
    sd = (sum((x - m) ** 2 for x in toate) / len(toate)) ** 0.5
    return [(x - m) / sd for x in train], [(x - m) / sd for x in test]
""", """
def scaleaza(train, test):
    m = sum(train) / len(train)
    sd = (sum((x - m) ** 2 for x in train) / len(train)) ** 0.5
    return [(x - m) / sd for x in train], [(x - m) / sd for x in test]
""")
    c.cod("""
verifica('scaleaza', scaleaza,
         [(([2, 4, 4, 4, 5, 5, 7, 9], [5, 9]), ([-1.5, -0.5, -0.5, -0.5, 0, 0, 1, 2], [0, 2])), (([0, 10], [20]), ([-1, 1], [3]))],
         ascunse=[(([1, 3], [3, 5, 1]), ([-1, 1], [1, 3, -1]))],
         indiciu='media si abaterea trebuie sa vina numai din train', puncte=2)
""")

    c.md("""
### 9. Repara codul: `fit_transform` pe test

Aceasta functie foloseste `StandardScaler` si are aceeasi greseala, ascunsa intr-un singur rand. Cauta-l.
""")
    c.ex("""
def pregateste(Xtr, Xte):
    sc = StandardScaler()
    A = sc.fit_transform(Xtr)
    B = sc.fit_transform(Xte)
    return A, B
""", """
def pregateste(Xtr, Xte):
    sc = StandardScaler()
    A = sc.fit_transform(Xtr)
    B = sc.transform(Xte)
    return A, B
""")
    c.cod("""
verifica('pregateste', pregateste,
         [((np.array([[0.0], [10.0]]), np.array([[20.0]])), (np.array([[-1.0], [1.0]]), np.array([[3.0]])))],
         ascunse=[((np.array([[1.0, 5.0], [3.0, 9.0]]), np.array([[5.0, 5.0], [1.0, 1.0]])),
                   (np.array([[-1.0, -1.0], [1.0, 1.0]]), np.array([[3.0, -1.0], [-1.0, -3.0]])))],
         indiciu='pe test nu mai inveti nimic, doar aplici', puncte=1)
""")

    c.md("""
### 10. Provocare: propriul tau `StandardScaler`

Fara NumPy si fara `sklearn`, pe liste de liste (fiecare sublista e un rand, coloanele sunt caracteristicile).

- `fit(X)` intoarce dictionarul `{'medie': [...], 'std': [...]}` cu media si abaterea standard (populatie) **pe fiecare coloana**. Daca o coloana are `std == 0`, pune `1.0` in loc (ca `sklearn`).
- `transform(X, params)` intoarce lista de liste standardizata cu parametrii dati. Astfel `transform(test, fit(train))` foloseste statisticile din train.
""")
    c.ex("""
def fit(X):
    pass  # TODO


def transform(X, params):
    pass  # TODO
""", """
def fit(X):
    n = len(X)
    medie, std = [], []
    for j in range(len(X[0])):
        col = [rand[j] for rand in X]
        m = sum(col) / n
        s = (sum((x - m) ** 2 for x in col) / n) ** 0.5
        medie.append(m)
        std.append(s if s != 0 else 1.0)
    return {'medie': medie, 'std': std}


def transform(X, params):
    return [[(x - m) / s for x, m, s in zip(rand, params['medie'], params['std'])] for rand in X]
""")
    c.cod("""
verifica('fit', fit, [(([[1, 10], [3, 30], [5, 20]],), {'medie': [3.0, 20.0], 'std': [(8 / 3) ** 0.5, (200 / 3) ** 0.5]})],
         ascunse=[(([[4, 1], [4, 3]],), {'medie': [4.0, 2.0], 'std': [1.0, 1.0]})], puncte=1,
         indiciu='pentru fiecare coloana j: scoate coloana intr-o lista, apoi medie si abatere; std 0 devine 1.0')


def _fit_apoi_transform(train, test):
    return transform(test, fit(train))


def _ref_sk(train, test):
    return StandardScaler().fit(train).transform(test).tolist()

verifica('transform', _fit_apoi_transform,
         [(([[1, 10], [3, 30], [5, 20]], [[3, 20], [5, 10]]), _ref_sk([[1, 10], [3, 30], [5, 20]], [[3, 20], [5, 10]]))],
         ascunse=[(([[4, 1], [4, 3]], [[9, 5]]), [[5.0, 3.0]])],
         referinta=_ref_sk,
         generator=lambda: ([[random.randint(0, 9), random.randint(0, 99), 7] for _ in range(5)],
                            [[random.randint(-5, 15), random.randint(0, 99), random.randint(0, 9)] for _ in range(3)]),
         indiciu='transform(test, fit(train)): statisticile din train, aplicate pe test', puncte=2)
scor()
""")
    c.salveaza('13-scalare-tema')


if __name__ == '__main__':
    predare()
    tema()
