"""Genereaza 10-eda-predare.ipynb si 10-eda-tema.ipynb (+ variantele cu solutii).

Valorile asteptate din teste (inclusiv cele ascunse) sunt calculate aici, de solutiile de referinta, si scrise ca numere in notebook.
"""
import os
import random

import numpy as np
import pandas as pd

from nb import Carnet, COLAB

ELEVI = pd.read_csv(os.path.join(COLAB, 'date', 'elevi.csv'))
CASE = pd.read_csv(os.path.join(COLAB, 'date', 'case.csv'))
MAGAZIN = pd.read_csv(os.path.join(COLAB, 'date', '10_magazin.csv'))
NS = {'np': np, 'pd': pd, 'elevi': ELEVI, 'case': CASE, 'magazin': MAGAZIN}


def py(x):
    """Numere/colectii numpy -> tipuri Python simple, ca sa le scriem ca text in notebook."""
    if isinstance(x, dict):
        return {py(k): py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return type(x)(py(v) for v in x)
    if isinstance(x, np.generic):
        return x.item()
    return x


def R(x):
    return repr(py(x))


def T(nume, f, vis, asc=(), pre='', extra=''):
    """Celula de verificare. vis/asc = liste de argumente ca text sursa ('elevi, "nota_info"'); asteptatul se calculeaza cu solutia din NS."""
    if pre:
        exec(pre, NS)

    def cazuri(lst):
        return '[' + ', '.join('((%s,), %s)' % (a, R(eval('%s(%s)' % (f, a), NS))) for a in lst) + ']'

    cod = (pre.strip() + '\n\n' if pre else '') + "verifica('%s', %s, %s" % (nume, f, cazuri(vis))
    if asc:
        cod += ',\n         ascunse=%s' % cazuri(asc)
    if extra:
        cod += ',\n         ' + extra
    return cod + ')'


def E(nume, var, expr, extra=''):
    """verifica_egal cu valoarea asteptata calculata in NS."""
    cod = "verifica_egal('%s', %s, %s" % (nume, var, R(eval(expr, NS)))
    return cod + (', ' + extra if extra else '') + ')'


# ---------------------------------------------------------------------------
# PREDARE
# ---------------------------------------------------------------------------

def predare():
    c = Carnet('EDA: modelarea si explorarea datelor', 'predare',
               fisiere=('date/elevi.csv', 'date/case.csv', 'anim_eda.py'))

    c.md("""
## Ce e EDA si de ce o faci inaintea oricarui model

EDA (Exploratory Data Analysis) inseamna sa te uiti la date **inainte** sa le dai unui model. Nu e o formalitate: majoritatea greselilor de la concurs nu sunt in model, sunt in date. O varsta de 150 de ani, o coloana citita ca text, acelasi raspuns scris in trei feluri, cateva randuri copiate de doua ori.

Modelul nu se plange de nimic din toate astea. Iti da doar un scor mai prost, iar tu crezi ca ai ales algoritmul gresit.

In acest notebook:

1. ce inseamna fiecare coloana (tipuri de feature-uri);
2. statistici de baza **de mana** (medie, mediana, varianta, cuantile, IQR), apoi cu pandas, apoi de ce pandas e mai rapid;
3. selectii, sortari, grupari;
4. grafice: distributii, outlieri, relatii;
5. o lista de intrebari (checklist) pe care o pui oricarui set de date. O aplicam pe `date/elevi.csv`, care e murdar intentionat, si apoi pe `date/case.csv`.

Pandas il invatam pe parcurs, doar cat ai nevoie. **Nu memora biblioteca**: la olimpiada ai documentatia. Trebuie sa stii ce *intrebare* pui datelor si sa poti scrie de mana ce face functia.

**Cum lucram.** Celulele `%%vezi` executa cod Python simplu pas cu pas (liste, bucle, dictionare). Nu pot afisa tabele pandas, asa ca partea "de mana" o vezi acolo, iar partea cu tabele o vezi in grafice si in animatii facute pe datele tale.
""")

    c.md("""
## 1. Ce e o coloana: tipurile de feature-uri

Inainte de orice calcul te intrebi: ce fel de coloana am in fata? Asta decide ce ai voie sa faci cu ea (nu are sens media la `oras`).

| tip | exemplu in `elevi.csv` | ce faci cu el |
|---|---|---|
| numeric continuu | `nota_mate`, `ore_studiu` | medie, histograma, corelatie |
| numeric discret (numarat) | `absente` | la fel, dar valori intregi |
| categoric (nominal) | `meditatii` (da / nu) | `value_counts`, `groupby` |
| ordinal (are ordine) | `clasa` (9 < 10 < 11 < 12) | il poti trata ca numar sau ca categorie |
| **tinta** (target) | `calificat` (0 / 1) | ce vrem sa prezicem |
| identificator | `id` | **nu e feature**: nu-l dai modelului |

Un identificator nu spune nimic despre elev, dar daca randurile sunt ordonate dupa ceva, modelul poate "invata" ordinea. Il scoti.

Incarcam datele. Fiecare rand e un elev, iar `calificat` spune daca a trecut mai departe.
""")
    c.cod("""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

elevi = pd.read_csv('date/elevi.csv')
elevi.head()
""")

    c.md("""
## 2. Media si mediana, de mana

**Media** = suma / cate sunt. **Mediana** = valoarea din mijloc, dupa ce sortezi lista. Uite-le pas cu pas:
""")
    c.cod("""
%%vezi
note = [7, 9, 5, 8, 6]
suma = 0
for x in note:
    suma = suma + x       #: adunam pe rand
media = suma / len(note)  #: suma impartita la cate sunt
""")
    c.md("""
**Prezice:** ai lista `[3, 4, 5, 5, 6, 100]`. Care e mai mare, media sau mediana, si aproximativ cu cat?

<details><summary>Raspuns</summary>

Media e `123 / 6 = 20.5`, mediana e `5`. O singura valoare uriasa trage media dupa ea, iar mediana nici nu observa: ea se uita doar la ce e in mijloc. De aici regula: **la date cu valori extreme sau asimetrice, mediana e mai de incredere**.
</details>
""")
    c.cod("""
%%vezi
v = [3, 9, 4, 100, 5, 5]
s = sorted(v)                              #: mediana cere lista sortata
n = len(s)
mij = n // 2
if n % 2 == 1:
    mediana = s[mij]                       #: numar impar: elementul din mijloc
else:
    mediana = (s[mij - 1] + s[mij]) / 2    #: numar par: media celor doua din mijloc
media = sum(v) / n
""")

    c.md("""
## 3. Varianta si deviatia standard, de mana

Media spune *unde* e centrul. Varianta spune *cat de imprastiate* sunt valorile in jurul lui: media patratelor distantelor la medie. Deviatia standard e radacina ei, ca sa revina la aceeasi unitate ca datele.

Doua formule, si aici se incurca toata lumea:

- **populatie** (ai TOATE datele): imparti la `n`
- **esantion** (ai doar o parte din date, cazul obisnuit): imparti la `n - 1`. Se numeste `ddof=1` ("delta degrees of freedom"). Motivul pe scurt: distantele se masoara fata de media *esantionului*, care e mai aproape de puncte decat media adevarata, deci `n` ar da un rezultat mereu prea mic.
""")
    c.cod("""
%%vezi
x = [2, 4, 4, 4, 5, 5, 7, 9]
n = len(x)
m = sum(x) / n                    #: media este 5
patrate = 0
for v in x:
    patrate += (v - m) ** 2       #: cat de departe e fiecare de medie, la patrat
var_pop = patrate / n             #: impartit la n: populatie
var_esantion = patrate / (n - 1)  #: impartit la n-1: esantion
std_pop = var_pop ** 0.5
""")
    c.md("""
**Prezice:** pentru aceeasi lista, ce iti dau `np.std(x)` si `pd.Series(x).std()`? Sunt egale?

<details><summary>Raspuns</summary>

Nu. `np.std` are implicit `ddof=0` (formula de populatie), iar pandas are implicit `ddof=1` (esantion). Aceeasi lista, doua rezultate. Cand compari cu un rezultat asteptat la concurs, uita-te ce formula cere enuntul.
</details>
""")
    c.cod("""
x = [2, 4, 4, 4, 5, 5, 7, 9]
print('numpy :', np.std(x))
print('pandas:', pd.Series(x).std())
print('numpy cu ddof=1:', np.std(x, ddof=1))
print('pandas cu ddof=0:', pd.Series(x).std(ddof=0))
""")

    c.md("""
## 4. Cuantile si IQR, de mana

Cuantila `q` (de ex. 0.25) e valoarea sub care se afla o fractiune `q` din date. Cele trei importante: `Q1` (0.25), mediana (0.5), `Q3` (0.75). **IQR = Q3 - Q1** e "latimea mijlocului" datelor.

Cum o calculezi: sortezi, iei pozitia `q * (n - 1)`, iar daca pozitia cade intre doua elemente, interpolezi liniar intre ele.

Regula pentru outlieri (Tukey): o valoare e suspecta daca iese din **garduri**:

`gard_jos = Q1 - 1.5 * IQR`, `gard_sus = Q3 + 1.5 * IQR`
""")
    c.cod("""
%%vezi
def cuantila(s, q):
    poz = q * (len(s) - 1)     #: pozitia in lista sortata, poate cu virgula
    jos = int(poz)
    frac = poz - jos
    if jos + 1 < len(s):
        return s[jos] + frac * (s[jos + 1] - s[jos])   #: interpolam intre vecini
    return s[jos]

s = sorted([2, 3, 4, 6, 8, 9, 10, 40])
q1 = cuantila(s, 0.25)
q3 = cuantila(s, 0.75)
iqr = q3 - q1
gard_jos = q1 - 1.5 * iqr
gard_sus = q3 + 1.5 * iqr
outlieri = [x for x in s if x < gard_jos or x > gard_sus]   #: ce iese din garduri
""")
    c.md("""
NumPy face exact asta (`np.percentile`, interpolare liniara), la fel `Series.quantile`. Atentie: exista mai multe definitii de cuantila (manualele nu se pun de acord la `Q1`). Pandas si NumPy o folosesc pe cea de mai sus, deci rezultatele lor sunt cele "oficiale" pentru noi.
""")
    c.cod("""
s = [2, 3, 4, 6, 8, 9, 10, 40]
print(np.percentile(s, [25, 75]))
print(pd.Series(s).quantile([0.25, 0.75]).tolist())
""")

    c.md("""
## 5. De ce pandas / NumPy e mai rapid

Ai scris de mana media cu o bucla. Functia din librarie face acelasi lucru, dar:

- valorile stau intr-un **bloc continuu de memorie**, cate 8 octeti fiecare, nu ca obiecte Python separate;
- bucla ruleaza in **C**, nu in interpretorul Python (care verifica tipul fiecarui `+`);
- procesorul poate aduna mai multe numere deodata.

Masoara:
""")
    c.cod("""
import time

mare = np.random.default_rng(0).random(2_000_000)
lista = mare.tolist()

t = time.perf_counter()
suma = 0.0
for x in lista:
    suma += x
t_bucla = time.perf_counter() - t

t = time.perf_counter()
suma_np = mare.sum()
t_np = time.perf_counter() - t

print(f'bucla Python: {t_bucla * 1000:.0f} ms | NumPy: {t_np * 1000:.1f} ms | de ~{t_bucla / t_np:.0f} ori mai rapid')
print(abs(suma - suma_np) < 1e-6)
""")
    c.md("""
Un `Series` din pandas e un array NumPy cu etichete deasupra, deci mosteneste viteza aceasta. La date mici nu simti diferenta. La un milion de randuri, o bucla scrisa de mana devine problema.
""")

    c.md("""
## 6. Prima privire: `shape`, `info`, `describe`

Trei comenzi pe care le rulezi mereu, in ordinea asta:

- `shape` = (randuri, coloane)
- `info()` = tipul fiecarei coloane si cate valori **nenule** are
- `describe()` = numar, medie, deviatie (cu `ddof=1`), minim, cuartile, maxim, pentru coloanele numerice
""")
    c.cod("""
print(elevi.shape)
elevi.info()
""")
    c.md("""
**Prezice:** uita-te la `describe()` de mai jos. Ce numere ti se par suspecte? (Cauta minimul, maximul, si `count` fata de 245 de randuri.)

<details><summary>Raspuns</summary>

- `varsta`: minim 2, maxim 150. Un elev de liceu nu are 2 sau 150 de ani.
- `absente`: maxim 120, dar 75% dintre elevi au cel mult 8. Ceva nu se leaga.
- `nota_info`, `ore_studiu`: `count` mai mic decat 245 inseamna valori lipsa.
- `id`: maxim 240, dar sunt 245 de randuri. Cineva apare de doua ori.
</details>
""")
    c.cod("""
elevi.describe()
""")

    c.md("""
## 7. Selectii: coloane, randuri, masti

```python
elevi['nota_info']                 # o coloana -> Series
elevi[['nota_info', 'absente']]    # mai multe coloane -> DataFrame (lista in interiorul parantezelor!)
elevi.loc[5, 'nota_info']          # dupa ETICHETA: randul 5, coloana nota_info
elevi.iloc[0:3, 0:2]               # dupa POZITIE, ca la liste (capatul din dreapta nu intra)
```
Diferenta care musca: `.loc[0:3]` **include** capatul 3, `.iloc[0:3]` **nu**.

Partea cea mai folosita e filtrarea cu o **masca**: un sir de `True`/`False`, cate unul pe rand. Intai o faci de mana, pe liste:
""")
    c.cod("""
%%vezi
nota = [4.5, 8.2, 9.1, 6.0, 8.8]
absente = [2, 9, 1, 3, 2]
masca = []
for n, a in zip(nota, absente):
    masca.append(n >= 8 and a <= 3)             #: True doar daca ambele conditii sunt adevarate
bune = [n for n, m in zip(nota, masca) if m]    #: pastram doar pozitiile unde masca e True
""")
    c.md("""
In pandas masca se construieste dintr-o singura expresie, pe toata coloana deodata, si se pune in paranteze drepte. Aici nu mai poti scrie `and` / `or` / `not`: pentru mastile pandas si NumPy ai `&`, `|`, `~`, **iar fiecare conditie trebuie pusa in paranteze**. Uite de ce.
""")
    c.cod("""
%%vezi
import numpy as np
n = np.array([4.5, 8.2, 9.1, 6.0])
a = np.array([2, 9, 1, 3])
m1 = n >= 8            #: o masca: True / False pe fiecare pozitie
m2 = a <= 3
m = m1 & m2            #: & compara element cu element: merge
m = m1 and m2          #: and vrea UN singur adevarat/fals pentru tot array-ul: eroare
""")
    c.cod("""
%%vezi
import numpy as np
n = np.array([4.5, 8.2, 9.1, 6.0])
a = np.array([2, 9, 1, 3])
gresit = n >= 8 & a <= 3      #: & are prioritate mai mare decat >= si <=, deci se calculeaza intai 8 & a
""")
    c.md("""
Ordinea operatiilor e cauza: `n >= 8 & a <= 3` se citeste `n >= (8 & a) <= 3`, fara paranteze. Eroarea ("truth value ... is ambiguous") vorbeste despre `and`, dar vinovatul adevarat e lipsa parantezelor. Varianta corecta:
""")
    c.cod("""
buni = elevi[(elevi['nota_info'] >= 7) & (elevi['absente'] <= 5)]
print(len(buni), 'elevi cu nota_info >= 7 si cel mult 5 absente')

# sau, cu | : clasa a 9-a SAU a 12-a
print(len(elevi[(elevi['clasa'] == 9) | (elevi['clasa'] == 12)]))
# isin face la fel de scurt
print(elevi['clasa'].isin([9, 12]).sum())
""")

    c.md("""
## 8. Sortare, frecvente, grupari

`sort_values` ordoneaza. `value_counts` numara cate ori apare fiecare valoare. Numaratul de mana e un dictionar:
""")
    c.cod("""
%%vezi
raspunsuri = ['da', 'nu', 'Da', 'nu', 'da', 'DA ', 'nu']
frecv = {}
for r in raspunsuri:
    if r in frecv:
        frecv[r] = frecv[r] + 1     #: cheia exista deja: crestem contorul
    else:
        frecv[r] = 1                #: prima aparitie
""")
    c.md("""
Observa ca `'da'`, `'Da'` si `'DA '` sunt **trei chei diferite**. Pentru calculator nu sunt acelasi raspuns. Exact asta e problema din coloana `meditatii`:
""")
    c.cod("""
print(elevi['meditatii'].value_counts(dropna=False))
elevi.sort_values('absente', ascending=False).head(4)
""")
    c.md("""
**`groupby`** = imparte randurile in grupuri dupa o coloana, calculeaza ceva pe fiecare grup, aduna rezultatele (split / apply / combine). De mana, cu un dictionar de liste:
""")
    c.cod("""
%%vezi
clasa = [9, 10, 9, 11, 10, 9]
nota = [6.0, 8.0, 7.0, 5.0, 9.0, 8.0]
grupuri = {}
for cl, n in zip(clasa, nota):
    if cl not in grupuri:
        grupuri[cl] = []
    grupuri[cl].append(n)                  #: fiecare nota intra in lista clasei ei
medii = {}
for cl in grupuri:
    medii[cl] = sum(grupuri[cl]) / len(grupuri[cl])   #: apoi facem media pe fiecare grup
""")
    c.cod("""
print(elevi.groupby('clasa')['nota_info'].mean())
elevi.groupby('clasa').agg(elevi=('id', 'count'), nota_medie=('nota_info', 'mean'), ore_mediana=('ore_studiu', 'median'))
""")

    c.md("""
## 9. Distributii: histograma

O histograma imparte valorile in "cosuri" (bare) si numara cate cad in fiecare. Un singur parametru conteaza mult: **numarul de bare**. Uita-te cum se schimba imaginea pentru `nota_info`, de la 2 la 40 de bare:
""")
    c.cod("""
anim_histograma(elevi['nota_info'], eticheta='nota_info')
""")
    c.md("""
Prea putine bare ascund forma, prea multe o umplu de zgomot. Punct de plecare: aproximativ radical din `n` bare (formula lui Sturges, `log2(n) + 1`, da un numar apropiat).

Doua lucruri de citit dintr-o histograma: **forma** (un varf? doua?) si **asimetria** (coada mai lunga intr-o parte). Daca coada e in dreapta, media > mediana. `ore_studiu` e asa:
""")
    c.cod("""
fig, ax = plt.subplots(1, 2, figsize=(10, 3.2))
for a, col in zip(ax, ['nota_info', 'ore_studiu']):
    x = elevi[col].dropna()
    a.hist(x, bins=20, color='#2563eb', edgecolor='white')
    a.axvline(x.mean(), color='#ea580c', lw=2, label=f'media {x.mean():.2f}')
    a.axvline(x.median(), color='#15803d', lw=2, ls='--', label=f'mediana {x.median():.2f}')
    a.set_title(f'{col}: asimetrie (skew) = {x.skew():.2f}')
    a.legend()
plt.tight_layout()
plt.show()
""")
    c.md("""
`skew()` aproape de 0 = simetric, pozitiv = coada in dreapta, negativ = coada in stanga. `ore_studiu` (skew ~0.9) are coada in dreapta: cativa elevi invata mult mai mult decat restul.
""")

    c.md("""
## 10. Outlieri

Un outlier e o valoare care iese din tiparul restului. Prima intrebare nu e "cum il sterg", ci **"de ce e acolo?"**: greseala de tastare (varsta 150), sau caz real rar (o casa de 2,6 milioane)?

Ai regula IQR de mana (sectiunea 4). Aplic-o pe `absente` cu pandas si uita-te si la o **boxplot**: cutia e intre `Q1` si `Q3`, linia e mediana, mustatile ajung la ultimele valori din garduri, iar punctele sunt outlierii.
""")
    c.cod("""
a = elevi['absente']
q1, q3 = a.quantile(0.25), a.quantile(0.75)
iqr = q3 - q1
jos, sus = q1 - 1.5 * iqr, q3 + 1.5 * iqr
print(f'Q1={q1}, Q3={q3}, IQR={iqr}, garduri: [{jos}, {sus}]')
print('outlieri:', sorted(a[(a < jos) | (a > sus)].tolist()))

fig, ax = plt.subplots(figsize=(4, 3.2))
ax.boxplot(a)
ax.set_title('absente')
plt.show()
""")
    c.md("""
Regula IQR prinde 15 (un elev cu multe absente, dar plauzibil) **si** pe 87 si 120 (aproape sigur greseli). Regula e un semnal de alarma, nu un verdict. Ce faci apoi depinde de context: corectezi daca stii valoarea, marchezi ca lipsa, limitezi la un maxim, sau pastrezi.

Ce face un outlier cu media? Animatia adauga o valoare care urca pas cu pas, peste primele 20 de note la matematica. Urmareste cele doua linii:
""")
    c.cod("""
anim_medie_mediana(elevi['nota_mate'].head(20), eticheta='nota_mate')
""")
    c.md("""
Media urmareste valoarea extrema, mediana abia se misca. Cu 245 de valori, un singur outlier misca media mult mai putin (il imparti la 245), dar in coloana `absente` sunt doua:
""")
    c.cod("""
a = elevi['absente']
print('cu tot cu outlieri :', round(a.mean(), 2), 'media |', a.median(), 'mediana')
sane = a[a < 50]
print('fara cele 2 extreme:', round(sane.mean(), 2), 'media |', sane.median(), 'mediana')
""")

    c.md("""
## 11. Relatii intre coloane: corelatie

Coeficientul de corelatie Pearson `r` (intre -1 si 1) masoara cat de bine se aliniaza doua coloane pe o **dreapta**: +1 = dreapta crescatoare perfecta, 0 = nicio aliniere liniara, -1 = descrescatoare. Formula de mana:

`r = suma((x - mx) * (y - my)) / radical(suma((x - mx)^2) * suma((y - my)^2))`
""")
    c.cod("""
%%vezi
x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 5]
n = len(x)
mx = sum(x) / n
my = sum(y) / n
sxy = 0
sxx = 0
syy = 0
for a, b in zip(x, y):
    sxy += (a - mx) * (b - my)     #: cat variaza impreuna x si y
    sxx += (a - mx) ** 2
    syy += (b - my) ** 2
r = sxy / (sxx * syy) ** 0.5       #: normalizam, ca sa iasa intre -1 si 1
""")
    c.cod("""
print(np.corrcoef([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])[0, 1])
cols = ['nota_mate', 'nota_info', 'ore_studiu', 'absente', 'calificat']
cm = elevi[cols].corr()          # NaN-urile sunt sarite pereche cu pereche
fig, ax = plt.subplots(figsize=(5.5, 4.2))
im = ax.imshow(cm, cmap='RdBu_r', vmin=-1, vmax=1)
ax.set_xticks(range(len(cols)), cols, rotation=45, ha='right')
ax.set_yticks(range(len(cols)), cols)
for i in range(len(cols)):
    for j in range(len(cols)):
        ax.text(j, i, f'{cm.iloc[i, j]:.2f}', ha='center', va='center', fontsize=8)
fig.colorbar(im)
plt.tight_layout()
plt.show()
""")
    c.md("""
Ce vezi: `nota_info` si `nota_mate` merg impreuna (~0.5), `ore_studiu` si `nota_info` mai slab (~0.33), iar `absente` e legat foarte slab de orice. Un scatter plot arata mai mult decat un numar:
""")
    c.cod("""
d = elevi.dropna(subset=['nota_info'])
plt.figure(figsize=(6, 3.8))
plt.scatter(d['nota_mate'], d['nota_info'], c=d['calificat'], cmap='coolwarm', s=18, alpha=0.8)
plt.xlabel('nota_mate')
plt.ylabel('nota_info')
plt.title('rosu = calificat, albastru = necalificat')
plt.show()
""")
    c.md("""
Un singur punct extrem poate strica corelatia. Animatia muta un punct in coltul de jos-dreapta al norului tau:
""")
    c.cod("""
anim_corelatie(elevi['nota_mate'], elevi['nota_info'], eticheta_x='nota_mate', eticheta_y='nota_info')
""")
    c.md("""
**Corelatia nu inseamna cauzalitate.** Ai vazut in prefata cursului de ce: doua lucruri pot merge impreuna pentru ca un al treilea le influenteaza pe amandoua, sau pur si simplu din intamplare. Aici, `ore_studiu` creste si nota la info, si sansa de calificare, deci si notele si calificarea "se misca" impreuna fara ca una s-o cauzeze neaparat pe cealalta.

Din intamplare? Doua miscari complet independente (nu au nimic de-a face una cu alta) pot iesi corelate puternic:
""")
    c.cod("""
rng = np.random.default_rng(7)
a = rng.normal(size=300).cumsum()      # un "drum" aleator
b = rng.normal(size=300).cumsum()      # alt drum, complet independent
print('corelatia dintre doua drumuri independente:', round(np.corrcoef(a, b)[0, 1], 2))
plt.figure(figsize=(6, 2.6))
plt.plot(a)
plt.plot(b)
plt.show()
""")

    c.md("""
## 12. Coloane categorice si tinta

Pentru o coloana categorica te intereseaza: cate categorii sunt, cat de des apare fiecare, si **cum se leaga de tinta**. Iar despre tinta: e echilibrata? Daca 95% dintre randuri au aceeasi clasa, un model care prezice mereu "da" are 95% acuratete si e inutil.
""")
    c.cod("""
print(elevi['calificat'].value_counts(normalize=True).round(3))
curat = elevi['meditatii'].str.strip().str.lower()    # strip taie spatiile de la capete, lower face literele mici
print(curat.value_counts(normalize=True).round(3))
print(elevi.groupby(curat)['calificat'].agg(['count', 'mean']))
""")
    c.md("""
33% dintre elevi sunt calificati: tinta e dezechilibrata, dar nu extrem. Iar `meditatii` nu pare sa schimbe mult rata de calificare (35% la "da", 31% la "nu"): diferenta e mica pe cate 77 si 155 de elevi si ar putea fi intamplare.
""")

    c.md("""
## 13. Checklist-ul EDA

Aceeasi lista pentru orice set de date. Nu o memora, tine-o in fata:

| # | intrebare | cum afli |
|---|---|---|
| 1 | Ce e un rand? Cate sunt? | `df.shape`, `df.head()` |
| 2 | Ce tip are fiecare coloana? Sunt tipurile corecte? | `df.info()` |
| 3 | Care e tinta? E echilibrata? | `df['tinta'].value_counts(normalize=True)` |
| 4 | Ce lipseste? Cat? | `df.isna().sum()` |
| 5 | Sunt randuri duplicate? | `df.duplicated().sum()` |
| 6 | Au sens intervalele? (minim, maxim) | `df.describe()` |
| 7 | Sunt categoriile scrise consecvent? | `df['c'].value_counts()` |
| 8 | Cum arata distributiile? | `df['c'].hist()` |
| 9 | Sunt outlieri? | regula IQR, boxplot |
| 10 | Ce relatii exista? | `df.corr()`, scatter |

Le aplicam pe `elevi.csv`, pe rand. Intrebarile 1, 2 si 3 le-ai facut deja (245 de randuri, un rand = un elev, tinta = `calificat`, tipurile sunt in regula, cu `meditatii` ca text).

**Intrebarea 4: ce lipseste?**
""")
    c.cod("""
lipsa = elevi.isna().sum()
print(pd.DataFrame({'lipsa': lipsa, 'procent': (lipsa / len(elevi) * 100).round(1)}))
print('randuri cu cel putin o valoare lipsa:', elevi.isna().any(axis=1).sum())
print('rata de lipsa la ore_studiu, pe clase:')
print(elevi.groupby('clasa')['ore_studiu'].apply(lambda s: s.isna().mean().round(3)))
""")
    c.md("""
Trei coloane au goluri. Iar `ore_studiu` lipseste mult mai des la clasa a 12-a (~29%) decat la celelalte (2-7%). Golurile nu sunt aleatoare. Ce faci cu ele e subiectul notebook-ului urmator.

**Intrebarea 5: duplicate?** **6: intervale?**
""")
    c.cod("""
print('randuri duplicate exact:', elevi.duplicated().sum())
print(elevi[elevi.duplicated(keep=False)].sort_values('id').head(4))

print('varste suspecte:')
print(elevi.loc[(elevi['varsta'] < 12) | (elevi['varsta'] > 20), ['id', 'clasa', 'varsta']])
""")
    c.md("""
Cinci randuri sunt copii exacte (aceeasi persoana, aceleasi valori, acelasi `id`), iar doua varste sunt imposibile: 150 (la un elev de clasa a 9-a) si 2 (la clasa a 11-a). Ai grija la comparatii: pe `NaN`, orice comparatie da `False`, deci mastile de mai sus nu le prind.

**Intrebarea 7: categorii.** Am vazut-o deja mai sus: `meditatii` are `da`, `Da`, `DA `, `nu`, ` nu`. Reparatia e `str.strip().str.lower()`.

**Intrebarile 8-10** (distributii, outlieri, relatii) le-am rezolvat la sectiunile 9-11: `absente` are 2 valori extreme (87, 120), `ore_studiu` e asimetrica la dreapta.

Rezultatul unei sesiuni de EDA e o **lista de probleme**, apoi o functie de curatare:
""")
    c.cod("""
curat = elevi.drop_duplicates().copy()
curat['meditatii'] = curat['meditatii'].str.strip().str.lower()
curat.loc[(curat['varsta'] < 12) | (curat['varsta'] > 20), 'varsta'] = np.nan

print(elevi.shape, '->', curat.shape)
print(curat['meditatii'].value_counts(dropna=False).to_dict())
print(curat['varsta'].describe().round(2).to_dict())
""")
    c.md("""
Am lasat `absente` neatinsa (decizia o iei cu cine a adus datele) si am lasat golurile: le tratam la topicul urmator. Vezi ca nu am modificat `elevi` original, ci o copie: pastrezi mereu datele brute.
""")

    c.md("""
### Aceeasi lista, pe `case.csv`

300 de apartamente, tinta = `pret_eur`. Aplicam checklist-ul pe scurt.
""")
    c.cod("""
case = pd.read_csv('date/case.csv')
print(case.shape, '| duplicate:', case.duplicated().sum())
print(case.isna().sum()[lambda s: s > 0].to_dict())
case.describe().round(1)
""")
    c.md("""
Prima diferenta fata de `elevi`: **scarile**. `pret_eur` e de ordinul sutelor de mii, `suprafata_mp` de ordinul zecilor, `camere` intre 1 si 6. Multe modele (KNN, regresie cu regularizare, retele) se vor lasa dominate de coloana cu numerele cele mai mari, de aceea vei invata scalarea. Iar `pret_eur` are maximul la 2,6 milioane cand mediana e 76.000: trei preturi extreme.
""")
    c.cod("""
p = case['pret_eur']
print('media:', round(p.mean()), '| mediana:', p.median(), '| skew:', round(p.skew(), 1))
ok = case[case['pret_eur'] < 500_000]
print('corelatie suprafata-pret cu extremele  :', round(case['suprafata_mp'].corr(case['pret_eur']), 2))
print('corelatie suprafata-pret fara extreme  :', round(ok['suprafata_mp'].corr(ok['pret_eur']), 2))

fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
ax[0].hist(p, bins=40, color='#2563eb', edgecolor='white')
ax[0].set_title('pret_eur: coada foarte lunga')
ax[1].scatter(case['suprafata_mp'], p, s=10, alpha=0.6)
ax[1].set_xlabel('suprafata_mp')
ax[1].set_ylabel('pret_eur')
plt.tight_layout()
plt.show()
print(case.groupby('oras')['pret_eur'].agg(['count', 'mean', 'median']).round(0))
""")
    c.md("""
Trei preturi extreme coboara corelatia de la ~0.90 la ~0.27. Iar la Bucuresti media (135.000) e mult peste mediana (80.000), exact din cauza lor. **Asta e motivul pentru care in date cu extreme te uiti la mediana si la corelatia calculata cu si fara ele.** Aceleasi preturi sunt outlieri reali sau greseli? De aici incolo e o decizie, nu un calcul.
""")

    c.md("""
## 14. Capcane

**Capcana 1: media ignora `NaN` in tacere.** `mean()` nu da eroare pe o coloana cu goluri, o face pe cele existente. Iar `len` numara si golurile.
""")
    c.cod("""
x = elevi['nota_info']
print('len:', len(x), '| count:', x.count(), '| lipsa:', x.isna().sum())
print('media pe', x.count(), 'valori:', round(x.mean(), 3))
""")
    c.md("""
**Capcana 2: modificarea in lant nu modifica nimic.** `df[masca]['col'] = ...` lucreaza pe o copie temporara. In pandas 2 primesti un avertisment, in pandas 3 nici macar asta. Foloseste `.loc[masca, 'col']`.
""")
    c.cod("""
import warnings
d = elevi.copy()
print('absente maxime la clasa a 12-a, inainte:', d.loc[d['clasa'] == 12, 'absente'].max())
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    d[d['clasa'] == 12]['absente'] = 0           # pare ca merge... dar nu
print('dupa atribuirea in lant                :', d.loc[d['clasa'] == 12, 'absente'].max())

d.loc[d['clasa'] == 12, 'absente'] = 0           # asa da
print('dupa .loc                              :', d.loc[d['clasa'] == 12, 'absente'].max())
""")
    c.md("""
**Capcana 3: corelatia zero nu inseamna "nicio relatie".** `r` masoara doar aliniere pe dreapta. O relatie perfecta, dar curba, poate da `r = 0`:
""")
    c.cod("""
x = np.linspace(-3, 3, 61)
y = x ** 2
print('r =', round(np.corrcoef(x, y)[0, 1], 3), '(dar y depinde total de x)')
plt.figure(figsize=(4, 2.6))
plt.scatter(x, y, s=8)
plt.show()
""")
    c.md("""
**Capcana 4: o coloana numerica citata ca text.** Daca intr-o coloana apare un singur `'n/a'` sau `'fara nota'`, pandas o citeste intreaga ca text (`object`), iar `mean()` nu mai merge cum crezi. `info()` te prinde (tipul nu e `float64`). `pd.to_numeric(errors='coerce')` transforma ce nu e numar in `NaN`.
""")
    c.cod("""
rating = pd.Series(['4', '5', 'fara nota', '3'])
print(rating.dtype)
nr = pd.to_numeric(rating, errors='coerce')
print(nr.tolist(), '| media:', nr.mean())
""")
    c.md("""
**Capcana 5: `id` (si orice numar de ordine) nu e feature.** Corelatia lui cu ceva poate iesi mica, dar un arbore de decizie poate imparti dupa `id` daca datele sunt sortate dupa tinta. Il scoti inainte de model.
""")

    c.md("""
### Cum citesti erorile de pandas

Aceleasi doua reguli: ultima linie spune *ce* s-a intamplat, numarul liniei spune *unde*.
""")
    c.cod("""
%%vezi
import pandas as pd
df = pd.DataFrame({'nota': [7, 9, 5], 'absente': [1, 4, 0]})
x = df['nota']
y = df['nota_info']     #: KeyError = numele coloanei nu exista (greseala de scriere?)
""")
    c.md("""
| eroare | de obicei inseamna |
|---|---|
| `KeyError: 'nota_info'` | coloana nu exista: verifica `df.columns` (spatii, litere mari?) |
| `ValueError: The truth value of a Series is ambiguous` | ai folosit `and` / `or` / `not` pe o coloana. Foloseste `&`, `|`, `~` |
| `TypeError: '>' not supported between 'str' and 'int'` | coloana e text (`object`) si o compari cu un numar: `info()` |
| `AttributeError: Can only use .str accessor with string values` | ai apelat `.str` pe o coloana numerica |
| `SettingWithCopyWarning` | modifici o copie: foloseste `.loc` sau `.copy()` |
""")

    c.md("""
## Exercitii

Pe rand. Fiecare are o celula de completat si una de verificare. Ai deja incarcat `elevi` (cu tot cu problemele lui, nu l-am curatat). Daca nu stii o functie, cauta-o in documentatie: la olimpiada asa faci.

**Exercitiul 1.** Media si mediana coloanei `nota_mate`.
""")
    c.ex("""
media_mate = None      # TODO
mediana_mate = None    # TODO
""", """
media_mate = elevi['nota_mate'].mean()
mediana_mate = elevi['nota_mate'].median()
""")
    c.cod(E('media', 'media_mate', "elevi['nota_mate'].mean()") + '\n' +
          E('mediana', 'mediana_mate', "elevi['nota_mate'].median()"))

    c.md("""
**Exercitiul 2.** Varianta de mana, cu un parametru `ddof` (0 = populatie, 1 = esantion). Fara `np.var`, fara `statistics`. O bucla si formula din sectiunea 3.
""")
    c.ex("""
def varianta(x, ddof):
    pass  # TODO
""", """
def varianta(x, ddof):
    m = sum(x) / len(x)
    s = 0
    for v in x:
        s += (v - m) ** 2
    return s / (len(x) - ddof)
""")
    c.cod("""
import random
verifica('varianta', varianta, [(([2, 4, 4, 4, 5, 5, 7, 9], 0), 4.0), (([2, 4, 4, 4, 5, 5, 7, 9], 1), 32 / 7)],
         ascunse=[(([5, 5, 5], 0), 0.0), (([1, 2], 1), 0.5)],
         referinta=lambda x, d: float(np.var(x, ddof=d)),
         generator=lambda: ([round(random.uniform(0, 20), 1) for _ in range(random.randint(3, 12))], random.choice([0, 1])),
         indiciu='media, apoi suma patratelor abaterilor, apoi impartirea la len(x) - ddof')
""")

    c.md("""
**Exercitiul 3.** Gardurile IQR de mana. Intoarce perechea `(gard_jos, gard_sus)`. Cuantilele le calculezi tu, cu interpolare liniara (sectiunea 4), nu cu `np.percentile`.
""")
    c.ex("""
def garduri_iqr(valori):
    s = sorted(valori)
    pass  # TODO: q1, q3 cu interpolare; apoi gardurile
""", """
def garduri_iqr(valori):
    s = sorted(valori)

    def cuantila(q):
        poz = q * (len(s) - 1)
        j = int(poz)
        if j + 1 < len(s):
            return s[j] + (poz - j) * (s[j + 1] - s[j])
        return s[j]

    q1, q3 = cuantila(0.25), cuantila(0.75)
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr
""")
    c.cod("""
import random


def garduri_ref(v):
    q1, q3 = np.percentile(v, [25, 75])
    return float(q1 - 1.5 * (q3 - q1)), float(q3 + 1.5 * (q3 - q1))


verifica('garduri_iqr', garduri_iqr, [(([2, 3, 4, 6, 8, 9, 10, 40],), (-4.5, 17.5)), (([1, 2, 3, 4, 5],), (-1.0, 7.0))],
         ascunse=[(([7],), (7.0, 7.0))],
         referinta=garduri_ref, generator=lambda: ([random.randint(0, 50) for _ in range(random.randint(4, 30))],),
         indiciu='pozitia lui Q1 este 0.25 * (n - 1) in lista sortata')
""")

    c.md("""
**Exercitiul 4.** Doua intrebari din checklist, cu pandas: cate randuri sunt duplicate exact in `elevi` (`nr_duplicate`) si ce **procent** din `ore_studiu` lipseste (`procent_lipsa_ore`, un numar intre 0 si 100).
""")
    c.ex("""
nr_duplicate = None        # TODO
procent_lipsa_ore = None   # TODO
""", """
nr_duplicate = elevi.duplicated().sum()
procent_lipsa_ore = elevi['ore_studiu'].isna().mean() * 100
""")
    c.cod(E('duplicate', 'nr_duplicate', 'elevi.duplicated().sum()') + '\n' +
          E('procent lipsa', 'procent_lipsa_ore', "elevi['ore_studiu'].isna().mean() * 100"))

    c.md("""
**Exercitiul 5.** Curata `meditatii` (spatii si litere mari), apoi numara cati dintre elevii cu meditatii (`'da'`) au `calificat == 1`. Atentie la duplicate: aici le lasam in pace, numaram pe randurile din `elevi` asa cum sunt.
""")
    c.ex("""
calificati_cu_meditatii = None   # TODO
""", """
med = elevi['meditatii'].str.strip().str.lower()
calificati_cu_meditatii = ((med == 'da') & (elevi['calificat'] == 1)).sum()
""")
    med = ELEVI['meditatii'].str.strip().str.lower()
    c.cod("verifica_egal('calificati cu meditatii', calificati_cu_meditatii, %s,\n               indiciu='str.strip().str.lower(), apoi doua conditii cu & si paranteze')"
          % R(((med == 'da') & (ELEVI['calificat'] == 1)).sum()))

    c.md("""
**Exercitiul 6.** Corelatia Pearson de mana, pe doua liste. Nu folosi `np.corrcoef`.
""")
    c.ex("""
def pearson(x, y):
    pass  # TODO
""", """
def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sxx = syy = 0
    for a, b in zip(x, y):
        sxy += (a - mx) * (b - my)
        sxx += (a - mx) ** 2
        syy += (b - my) ** 2
    return sxy / (sxx * syy) ** 0.5
""")
    c.cod("""
import random
verifica('pearson', pearson, [(([1, 2, 3, 4, 5], [2, 4, 6, 8, 10]), 1.0), (([1, 2, 3], [3, 2, 1]), -1.0),
                              (([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]), 0.7745966692414834)],
         referinta=lambda x, y: float(np.corrcoef(x, y)[0, 1]),
         generator=lambda: tuple(zip(*[(random.randint(0, 30), random.randint(0, 30)) for _ in range(random.randint(4, 15))])),
         indiciu='formula din sectiunea 11: suma produselor abaterilor / radical din produsul sumelor de patrate')
""")

    c.md("""
**Exercitiul 7.** Nota medie la informatica pe fiecare clasa, ca dictionar `{clasa: media}`. Ai nevoie de `groupby`, `mean` si `to_dict()`.
""")
    c.ex("""
medie_pe_clasa = None   # TODO
""", """
medie_pe_clasa = elevi.groupby('clasa')['nota_info'].mean().to_dict()
""")
    c.cod(E('medie pe clasa', 'medie_pe_clasa', "elevi.groupby('clasa')['nota_info'].mean().to_dict()",
            "indiciu=\"groupby('clasa')['nota_info'].mean().to_dict()\""))

    c.md("""
**Exercitiul 8.** Cati elevi au `nota_info >= 7` **si** cel mult 5 absente? Fii atent la paranteze.
""")
    c.ex("""
nr_buni = None   # TODO
""", """
nr_buni = ((elevi['nota_info'] >= 7) & (elevi['absente'] <= 5)).sum()
""")
    c.cod(E('nr_buni', 'nr_buni', "((elevi['nota_info'] >= 7) & (elevi['absente'] <= 5)).sum()") + '\n' + 'scor()')

    c.md("""
## Recapitulare

- EDA = intrebari puse datelor **inainte** de model. Aceeasi lista pentru orice set (checklist-ul din sectiunea 13).
- Tipuri de coloane: numeric, categoric, ordinal, tinta, identificator (nu e feature).
- De mana: media (`suma / n`), mediana (sortezi, iei mijlocul), varianta (`/ n` populatie, `/ (n - 1)` esantion; NumPy `ddof=0`, pandas `ddof=1`), cuantile prin interpolare liniara, IQR si gardurile `Q1 - 1.5 IQR`, `Q3 + 1.5 IQR`.
- Pandas/NumPy sunt mai rapide pentru ca bucla ruleaza in C pe memorie continua. Tu trebuie sa stii ce calculeaza.
- Masti: `&`, `|`, `~`, cu **paranteze** la fiecare conditie. Modificari: `.loc[masca, 'col'] = ...`, nu in lant.
- Outlierii: intreaba de ce sunt acolo. Media e trasa de ei, mediana nu.
- Corelatia masoara doar aliniere liniara, e sensibila la outlieri si nu e cauzalitate.
- Rezultatul EDA e o lista de probleme din date. Pe `elevi.csv`: valori lipsa (nu aleatoare), absente extreme, varsta imposibila, `meditatii` scris inconsistent, 5 duplicate.

Legatura cu ONIA: la orice sarcina cu un CSV, primele 10 minute sunt EDA. Datele murdare pierd mai multe puncte decat alegerea modelului. Tema (notebook-ul urmator) are un raport EDA complet, cu verificari automate.
""")
    c.salveaza('10-eda-predare')


# ---------------------------------------------------------------------------
# TEMA
# ---------------------------------------------------------------------------

def tema():
    c = Carnet('EDA: modelarea si explorarea datelor', 'tema',
               fisiere=('date/elevi.csv', 'date/case.csv', 'date/10_magazin.csv', 'anim_eda.py'))

    c.md("""
Tema are patru parti: **A** un raport EDA (10 intrebari cu verificare automata), **B** o sarcina de detectiv pe un set nou, **C** doua coduri de reparat si **D** un program in format concurs, plus o provocare.

La partea A fiecare intrebare e o **functie care primeste un DataFrame**, ca sa mearga pe orice set. Testele vizibile ruleaza pe `elevi.csv`, cele **ascunse** ruleaza pe alte seturi (`case.csv`, `10_magazin.csv`, bucati din `elevi`). Daca ai scris-o generala, trece. Daca ai scris `'nota_info'` direct in functie, pica la cele ascunse.

Pandas nu se memoreaza: cauta in documentatie ce iti trebuie. Nu cauta solutii gata facute, aici conteaza sa gandesti tu.
""")
    c.cod("""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

elevi = pd.read_csv('date/elevi.csv')
case = pd.read_csv('date/case.csv')
magazin = pd.read_csv('date/10_magazin.csv')
""")

    # ---------------- A
    c.md("""
## A. Raportul EDA

### A1. Procentul de valori lipsa

`procent_lipsa(df, col)` intoarce ce procent (0 - 100) din coloana `col` lipseste.
""")
    sol = """
def procent_lipsa(df, col):
    return df[col].isna().mean() * 100
"""
    exec(sol, NS)
    c.ex("""
def procent_lipsa(df, col):
    pass  # TODO
""", sol)
    c.cod(T('procent_lipsa', 'procent_lipsa', ["elevi, 'nota_info'", "elevi, 'ore_studiu'"],
            ["case, 'an_constructie'", "elevi, 'id'", "magazin, 'discount_pct'", "elevi.head(50), 'ore_studiu'"]))

    c.md("""
### A2. Ce coloane au goluri

`coloane_cu_lipsa(df)` intoarce un dictionar `{coloana: cate_lipsesc}`, **doar** pentru coloanele care au cel putin o valoare lipsa.
""")
    sol = """
def coloane_cu_lipsa(df):
    lipsa = df.isna().sum()
    return lipsa[lipsa > 0].to_dict()
"""
    exec(sol, NS)
    c.ex("""
def coloane_cu_lipsa(df):
    pass  # TODO
""", sol)
    c.cod(T('coloane_cu_lipsa', 'coloane_cu_lipsa', ['elevi'], ['case', 'magazin', 'elevi.head(30)', 'elevi.dropna()']))

    c.md("""
### A3. Randuri duplicate

`numar_duplicate(df)` intoarce cate randuri sunt copii exacte ale unui rand de mai sus. (Primul exemplar nu se numara.)
""")
    sol = """
def numar_duplicate(df):
    return int(df.duplicated().sum())
"""
    exec(sol, NS)
    c.ex("""
def numar_duplicate(df):
    pass  # TODO
""", sol)
    c.cod(T('numar_duplicate', 'numar_duplicate', ['elevi'], ['case', 'magazin', 'elevi.head(100)', 'pd.concat([case, case])']))

    c.md("""
### A4. Medie si mediana

`medie_mediana(df, col)` intoarce perechea `(media, mediana)` a coloanei.
""")
    sol = """
def medie_mediana(df, col):
    return df[col].mean(), df[col].median()
"""
    exec(sol, NS)
    c.ex("""
def medie_mediana(df, col):
    pass  # TODO
""", sol)
    c.cod(T('medie_mediana', 'medie_mediana', ["elevi, 'nota_mate'", "elevi, 'absente'"],
            ["case, 'pret_eur'", "magazin, 'cantitate'", "elevi, 'ore_studiu'"]))

    c.md("""
### A5. Outlieri dupa regula IQR (2 puncte)

`numar_outlieri(df, col)`: cate valori din coloana ies din gardurile `Q1 - 1.5 * IQR` si `Q3 + 1.5 * IQR`. Valorile lipsa nu se numara. Cuantilele: `Series.quantile`.
""")
    sol = """
def numar_outlieri(df, col):
    x = df[col]
    q1, q3 = x.quantile(0.25), x.quantile(0.75)
    iqr = q3 - q1
    return int(((x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)).sum())
"""
    exec(sol, NS)
    c.ex("""
def numar_outlieri(df, col):
    pass  # TODO
""", sol)
    c.cod(T('numar_outlieri', 'numar_outlieri', ["elevi, 'absente'", "elevi, 'nota_info'"],
            ["case, 'pret_eur'", "case, 'suprafata_mp'", "magazin, 'cantitate'", "elevi, 'ore_studiu'"],
            extra="puncte=2, indiciu='NaN nu e nici sub, nici peste gard: comparatiile cu NaN dau False'"))

    c.md("""
### A6. Cea mai corelata coloana

`cea_mai_corelata(df, col)` intoarce **numele** coloanei numerice (alta decat `col`) cu cea mai mare corelatie in valoare absoluta cu `col`. Hint: `df.corr(numeric_only=True)`.
""")
    sol = """
def cea_mai_corelata(df, col):
    cor = df.corr(numeric_only=True)[col].drop(col)
    return cor.abs().idxmax()
"""
    exec(sol, NS)
    c.ex("""
def cea_mai_corelata(df, col):
    pass  # TODO
""", sol)
    c.cod(T('cea_mai_corelata', 'cea_mai_corelata', ["elevi, 'calificat'", "elevi, 'nota_mate'"],
            ["case, 'pret_eur'", "case, 'camere'", "elevi, 'ore_studiu'"]))

    c.md("""
### A7. Media pe grupuri

`medie_pe_grup(df, grup, col)` intoarce un dictionar `{valoare_grup: media_lui_col}`.
""")
    sol = """
def medie_pe_grup(df, grup, col):
    return df.groupby(grup)[col].mean().to_dict()
"""
    exec(sol, NS)
    c.ex("""
def medie_pe_grup(df, grup, col):
    pass  # TODO
""", sol)
    c.cod(T('medie_pe_grup', 'medie_pe_grup', ["elevi, 'clasa', 'calificat'"],
            ["case, 'oras', 'pret_eur'", "case, 'camere', 'suprafata_mp'", "magazin, 'produs', 'pret_unitar'"]))

    c.md("""
### A8. Curata un text

`curata_text(serie)` intoarce seria cu spatiile de la capete taiate si toate literele mici. Valorile lipsa raman lipsa. Verificarea numara valorile din seria ta.
""")
    sol = """
def curata_text(serie):
    return serie.str.strip().str.lower()
"""
    exec(sol, NS)
    c.ex("""
def curata_text(serie):
    pass  # TODO
""", sol)
    pre = """
def _frecvente(df, col):
    return curata_text(df[col]).value_counts().to_dict()
"""
    c.cod(T('curata_text', '_frecvente', ["elevi, 'meditatii'"], ["magazin, 'oras'", "magazin, 'produs'", "elevi.head(40), 'meditatii'"], pre=pre))

    c.md("""
### A9. Curata tot setul (3 puncte)

`curata_elevi(df)` intoarce un DataFrame curatat, cu trei reparatii:

1. elimina randurile duplicate exacte (`drop_duplicates`);
2. curata `meditatii` (spatii si litere mici);
3. pune `NaN` la `varsta` pentru valorile imposibile: sub 12 sau peste 20.

Nu modifica `df` primit (lucreaza pe o copie). Verificarea se uita la forma rezultatului, la numarul de varste puse `NaN` si la frecventele din `meditatii`.
""")
    sol = """
def curata_elevi(df):
    d = df.drop_duplicates().copy()
    d['meditatii'] = d['meditatii'].str.strip().str.lower()
    d.loc[(d['varsta'] < 12) | (d['varsta'] > 20), 'varsta'] = np.nan
    return d
"""
    exec(sol, NS)
    c.ex("""
def curata_elevi(df):
    pass  # TODO
""", sol)
    pre = """
def _rezumat(df):
    d = curata_elevi(df)
    return d.shape, int(d['varsta'].isna().sum()), d['meditatii'].value_counts().to_dict()
"""
    c.cod(T('curata_elevi', '_rezumat', ['elevi'], ['elevi.head(60)', 'elevi.iloc[100:]', 'elevi.iloc[:45]'], pre=pre,
            extra="puncte=3, indiciu='drop_duplicates, str.strip().str.lower(), .loc[masca, \"varsta\"] = np.nan'"))

    c.md("""
### A10. Coada distributiei

`asimetrie(df, col)` intoarce `'dreapta'` daca `skew() > 0.5`, `'stanga'` daca `skew() < -0.5`, altfel `'simetric'`.
""")
    sol = """
def asimetrie(df, col):
    s = df[col].skew()
    if s > 0.5:
        return 'dreapta'
    if s < -0.5:
        return 'stanga'
    return 'simetric'
"""
    exec(sol, NS)
    c.ex("""
def asimetrie(df, col):
    pass  # TODO
""", sol)
    c.cod(T('asimetrie', 'asimetrie', ["elevi, 'ore_studiu'", "elevi, 'nota_info'"],
            ["case, 'pret_eur'", "elevi, 'absente'", "case, 'camere'", "elevi, 'clasa'"]))

    # ---------------- B detectiv
    c.md("""
## B. Detectiv: gaseste problemele din date

Setul `date/10_magazin.csv` are comenzi dintr-un magazin online. Cineva l-a pregatit in graba si a lasat in el mai multe probleme. Aplica checklist-ul din notebook-ul de predare si completeaza raspunsurile in dictionarul `probleme` de mai jos. Nu ti-am spus **unde** sunt problemele, doar ce sa numeri.

Cateva sunt vizibile in verificare, altele nu: nu poti nimeri la intamplare.
""")
    c.cod("""
magazin.head()
""")
    det = {
        'randuri_duplicate': int(MAGAZIN.duplicated().sum()),
        'preturi_negative': int((MAGAZIN['pret_unitar'] < 0).sum()),
        'discount_peste_100': int((MAGAZIN['discount_pct'] > 100).sum()),
        'rating_nenumeric': int(pd.to_numeric(MAGAZIN['rating'], errors='coerce').isna().sum()),
        'valori_lipsa_discount': int(MAGAZIN['discount_pct'].isna().sum()),
        'cantitate_maxima': int(MAGAZIN['cantitate'].max()),
        'orase_dupa_curatare': int(MAGAZIN['oras'].str.strip().str.lower().nunique()),
        'coloana_constanta': [k for k in MAGAZIN.columns if MAGAZIN[k].nunique() == 1][0],
        'coloana_numerica_citita_ca_text': 'rating',
    }
    c.ex("""
probleme = {
    'randuri_duplicate': None,                # cate randuri sunt copii exacte ale altor randuri
    'preturi_negative': None,                 # cate randuri au pret_unitar < 0
    'discount_peste_100': None,               # cate randuri au discount_pct > 100 (un procent nu trece de 100)
    'rating_nenumeric': None,                 # cate valori din rating nu sunt numere (pd.to_numeric cu errors='coerce')
    'valori_lipsa_discount': None,            # cate valori lipsa (NaN) are discount_pct
    'cantitate_maxima': None,                 # cea mai mare cantitate dintr-o comanda
    'orase_dupa_curatare': None,              # cate orase DIFERITE sunt dupa strip + lower
    'coloana_constanta': None,                # numele coloanei care are aceeasi valoare peste tot
    'coloana_numerica_citita_ca_text': None,  # numele coloanei care ar trebui sa fie numar, dar a fost citita ca text
}
""", "probleme = " + repr(det).replace("{'", "{\n    '").replace(", '", ",\n    '").replace("}", "\n}") + "\n")
    chei = list(det)
    vis = chei[:5]
    asc = chei[5:]
    c.cod("""
def _valoare(cheie):
    return probleme[cheie]


verifica('detectiv', _valoare, [((k,), v) for k, v in %s],
         ascunse=[((k,), v) for k, v in %s],
         puncte=3, indiciu='fiecare cheie e o intrebare din checklist: duplicated, isna, describe, value_counts, dtypes')
""" % (R([(k, det[k]) for k in vis]), R([(k, det[k]) for k in asc])))

    # ---------------- C repara
    c.md("""
## C. Repara codul

### C1. Elevii buni la info

Functia trebuie sa numere elevii cu `nota_info >= 7` **si** cel mult 5 absente. Are doua greseli: una o vezi imediat (crapa), cealalta nu (da un numar, dar gresit). Ruleaza celula de mai jos ca sa vezi ce se intampla, apoi repara functia.
""")
    c.cod("""
%%vezi
import numpy as np
nota_info = np.array([9.0, 6.5, 7.5])
absente = np.array([1, 0, 8])
masca = nota_info >= 7 & absente <= 5
""")
    sol = """
def cati_buni(df):
    masca = (df['nota_info'] >= 7) & (df['absente'] <= 5)
    return int(masca.sum())
"""
    exec(sol, NS)
    c.ex("""
def cati_buni(df):
    masca = df['nota_mate'] >= 7 & df['absente'] <= 5
    return int(masca.sum())
""", sol)
    c.cod(T('cati_buni', 'cati_buni', ['elevi'], ['elevi.head(80)', 'elevi.iloc[80:]', 'elevi[elevi["clasa"] == 12]'],
            extra="indiciu='paranteze la fiecare conditie, si verifica ce coloana cere enuntul'"))

    c.md("""
### C2. Coeficientul de variatie

Coeficientul de variatie e `deviatia standard / media`. In clasa ta ai `n` elevi si consideri ca ii ai pe **toti** (populatie, nu esantion). Functia intoarce un rezultat usor diferit de cel corect. De ce? Cine e `ddof`?
""")
    sol = """
def coef_variatie(valori):
    s = pd.Series(valori)
    return s.std(ddof=0) / s.mean()
"""
    exec(sol, NS)
    c.ex("""
def coef_variatie(valori):
    s = pd.Series(valori)
    return s.std() / s.mean()
""", sol)
    c.cod("""
import random
verifica('coef_variatie', coef_variatie, [(([2, 4, 4, 4, 5, 5, 7, 9],), 0.4), (([10, 10, 10],), 0.0)],
         referinta=lambda v: float(np.std(v) / np.mean(v)),
         generator=lambda: ([random.randint(1, 30) for _ in range(random.randint(3, 15))],),
         indiciu='pandas foloseste implicit ddof=1', puncte=1)
""")

    # ---------------- D program
    c.md("""
## D. Program in format concurs: statistici pe o linie

Pe prima linie primesti `n` (numarul de valori), pe a doua `n` numere (pot fi cu zecimale). Afiseaza pe prima linie **media si mediana**, cu doua zecimale, separate printr-un spatiu, iar pe a doua linie **numarul de outlieri** dupa regula IQR (cuantile cu interpolare liniara, ca in predare).

Exemplu: pentru `8` si `2 3 4 6 8 9 10 40` afisezi

```
10.25 7.00
1
```

Foloseste doar biblioteca standard (`sorted`, `sum`...): cuantila o scrii tu.
""")

    def ref_prog(inp):
        v = sorted(map(float, inp[1].split()))
        n = len(v)
        media = sum(v) / n
        mediana = v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2

        def cuant(q):
            poz = q * (n - 1)
            j = int(poz)
            return v[j] + (poz - j) * (v[j + 1] - v[j]) if j + 1 < n else v[j]
        q1, q3 = cuant(0.25), cuant(0.75)
        iqr = q3 - q1
        jos, sus = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        nr = sum(1 for x in v if x < jos or x > sus)
        return f'{media:.2f} {mediana:.2f}\n{nr}', min(min(abs(x - jos), abs(x - sus)) for x in v)

    def cazuri_prog(nr, sd):
        rnd = random.Random(sd)
        out = []
        while len(out) < nr:
            n = rnd.randint(1, 25)
            v = [round(rnd.gauss(50, 15), 1) for _ in range(n)]
            if rnd.random() < 0.6:
                v.append(round(rnd.uniform(120, 300), 1))
            n = len(v)
            inp = [str(n), ' '.join(str(x) for x in v)]
            rez, marja = ref_prog(inp)
            if marja > 1e-6:
                out.append((inp, rez))
        return out

    vis = [(['8', '2 3 4 6 8 9 10 40'], '10.25 7.00\n1'), (['5', '1 2 3 4 5'], '3.00 3.00\n0')]
    asc = [(['1', '7'], '7.00 7.00\n0')] + cazuri_prog(6, 11)
    c.ex("""
def main():
    pass  # TODO: citeste n si valorile, afiseaza media, mediana, numarul de outlieri
""", """
def main():
    n = int(input())
    v = sorted(map(float, input().split()))
    media = sum(v) / n
    mij = n // 2
    mediana = v[mij] if n % 2 else (v[mij - 1] + v[mij]) / 2

    def cuantila(q):
        poz = q * (n - 1)
        j = int(poz)
        if j + 1 < n:
            return v[j] + (poz - j) * (v[j + 1] - v[j])
        return v[j]

    q1, q3 = cuantila(0.25), cuantila(0.75)
    iqr = q3 - q1
    nr = sum(1 for x in v if x < q1 - 1.5 * iqr or x > q3 + 1.5 * iqr)
    print(f'{media:.2f} {mediana:.2f}')
    print(nr)
""")
    c.cod("verifica_program('statistici pe o linie', main,\n                 %s,\n                 ascunse=%s, puncte=2)" % (R(vis), R(asc)))

    # ---------------- E provocare
    c.md("""
## E. Provocare: outlier fata de propriul grup

Un pret de 250 de lei e normal pentru niste casti si ciudat pentru un pix. Un outlier nu e o proprietate a valorii, ci a valorii **in contextul ei**.

`outlieri_pe_grup(df, grup, col)` intoarce numarul de randuri a caror valoare din `col` iese din gardurile IQR calculate **doar pe grupul ei** (`Q1`, `Q3` din grupul respectiv). Randurile cu `NaN` in `col` nu se numara.

Hint: `df.groupby(grup)[col].transform(...)` intoarce o coloana de aceeasi lungime cu `df`, cu valoarea grupului pe fiecare rand. Poti calcula `q1` si `q3` asa si apoi compari cu `df[col]`.

Vezi si de ce conteaza: pe tot setul `magazin`, un pret negativ de `-25` nu iese din garduri (preturile merg de la 3 la 283). Pe grupul `pix`, da.
""")
    sol = """
def outlieri_pe_grup(df, grup, col):
    g = df.groupby(grup)[col]
    q1 = g.transform(lambda s: s.quantile(0.25))
    q3 = g.transform(lambda s: s.quantile(0.75))
    iqr = q3 - q1
    x = df[col]
    return int(((x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)).sum())
"""
    exec(sol, NS)
    c.ex("""
def outlieri_pe_grup(df, grup, col):
    pass  # TODO
""", sol)
    c.cod(T('outlieri_pe_grup', 'outlieri_pe_grup', ["magazin, 'produs', 'pret_unitar'", "case, 'oras', 'pret_eur'"],
            ["elevi, 'clasa', 'absente'", "case, 'camere', 'suprafata_mp'", "magazin, 'oras', 'cantitate'", "elevi, 'clasa', 'ore_studiu'"],
            extra="puncte=3") + '\nscor()')
    c.salveaza('10-eda-tema')


if __name__ == '__main__':
    predare()
    tema()
