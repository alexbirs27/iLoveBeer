"""Genereaza 04-liste-tablouri-predare.ipynb si 04-liste-tablouri-tema.ipynb (+ variantele cu solutii)."""
from nb import Carnet

FISIERE = ('anim_liste.py',)


def _spirala(n):
    """Matricea n x n cu 1..n*n in spirala (pentru testele ascunse)."""
    mat = [[0] * n for _ in range(n)]
    i = j = 0
    di, dj = 0, 1
    for k in range(1, n * n + 1):
        mat[i][j] = k
        ni, nj = i + di, j + dj
        if not (0 <= ni < n and 0 <= nj < n) or mat[ni][nj]:
            di, dj = dj, -di
            ni, nj = i + di, j + dj
        i, j = ni, nj
    return mat


def predare():
    c = Carnet('Liste si tablouri bidimensionale', 'predare', fisiere=FISIERE)

    c.md("""
## Liste: cea mai folosita structura din Python

Lista e structura pe care o vei folosi cel mai des: la olimpiada, in Pandas, in NumPy, in orice problema cu "n numere". In C++ aveai tablouri cu tip si lungime fixa. In Python lista creste singura, poate tine orice si se modifica pe loc.

Pretul: **listele sunt obiecte pe care mai multe nume le pot arata in acelasi timp**. Asta se numeste aliasing si e sursa nr. 1 de bug-uri de la acest nivel. Ii dedicam o sectiune intreaga, cu animatii.

Ce facem: indexare si felii, metode, sortare (de mana si cu `sorted`), comprehensii, citirea din input, aliasing, apoi matricile (liste de liste) cu parcurgeri, transpusa, rotire, spirala. La final, cat costa fiecare operatie.

Animatiile `%%vezi` iti arata memoria: o lista e o cutie cu indici deasupra, o matrice e un tabel, iar cutiile **partajate** primesc o eticheta mov `@1`. Foloseste sagetile stanga/dreapta de la tastatura (da click pe animatie mai intai).
""")

    c.md("""
## 1. Creare si indexare

Indicii pornesc de la 0, ca in C++. In plus ai indici **negativi**: `-1` e ultimul element, `-2` penultimul. Nu exista in C++ si te scapa de `v[len(v) - 1]`.
""")
    c.cod("""
%%vezi
note = [9, 7, 10, 6]         #: o lista: valori intre paranteze drepte, separate prin virgula
mix = ['ana', 3, 2.5, True]  #: poate tine tipuri diferite (rar e o idee buna)
goala = []                   #: lista goala
zerouri = [0] * 4            #: [0, 0, 0, 0]
n = len(note)                #: len = cate elemente are
primul = note[0]             #: primul element
ultimul = note[-1]           #: ultimul: -1
note[1] = 8                  #: listele se modifica pe loc (spre deosebire de text)
""")
    c.md("""
**Prezice:** pentru `v = [10, 20, 30, 40, 50]`, cat dau `v[-2]` si `v[len(v) - 1]`? Dar `v[5]`?

<details><summary>Raspuns</summary>

`v[-2]` este 40, `v[len(v) - 1]` este 50 (acelasi lucru cu `v[-1]`). `v[5]` da `IndexError`: indicii valizi sunt de la `-5` la `4`.
</details>
""")
    c.cod("""
v = [10, 20, 30, 40, 50]
print(v[-2], v[len(v) - 1], v[-1])
""")

    c.md("""
## 2. Feliile (slicing)

`a[start:stop:pas]` scoate o **lista noua**. `start` e inclus, `stop` e exclus, exact ca in `range(start, stop, pas)`. Poti lasa oricare parte goala.

| felie | ce da |
|---|---|
| `a[1:4]` | elementele de pe pozitiile 1, 2, 3 |
| `a[:3]` | primele 3 |
| `a[-3:]` | ultimele 3 |
| `a[::2]` | din 2 in 2 |
| `a[::-1]` | toata lista, invers |
""")
    c.cod("""
%%vezi
a = [10, 20, 30, 40, 50, 60]
b = a[1:4]        #: indicii 1, 2, 3 (4 e exclus). b e o lista NOUA
c = a[:2]         #: primele doua
d = a[-2:]        #: ultimele doua
e = a[::2]        #: din doi in doi: 10, 30, 50
f = a[::-1]       #: invers
b[0] = 99         #: schimb felia. a ramane neatinsa: felia e o copie
""")
    c.md("""
**Prezice:** ce dau `a[1:-1]` si `a[::-2]` pentru `a = [10, 20, 30, 40, 50, 60]`?

<details><summary>Raspuns</summary>

`a[1:-1]` este `[20, 30, 40, 50]` (fara primul si ultimul). `a[::-2]` este `[60, 40, 20]`: pornesti de la coada si sari din doi in doi.
</details>
""")
    c.cod("""
a = [10, 20, 30, 40, 50, 60]
print(a[1:-1])
print(a[::-2])
print(a[3:0:-1])       # pas negativ: mergi spre stanga, de la 3 pana la 1 (0 e exclus)
""")
    c.md("""
**Cazurile limita.** Feliile sunt ingaduitoare: daca depasesti capetele, se opresc la capat si **nu dau eroare**. Doar un index singur da eroare.
""")
    c.cod("""
%%vezi
a = [10, 20, 30, 40, 50]
x = a[2:100]      #: stop prea mare: se opreste la capat
y = a[4:2]        #: start dupa stop: lista goala
z = a[-100:2]     #: -100 e taiat la 0
w = a[10:]        #: start dupa capat: lista goala
t = a[10]         #: dar UN index singur care nu exista da eroare
""")

    c.md("""
## 3. Metodele listei

Regula de retinut: **aproape toate metodele modifica lista pe loc si intorc `None`**. Singurele care intorc ceva util: `pop`, `index`, `count`, `copy`.

| metoda | ce face |
|---|---|
| `append(x)` | pune `x` la sfarsit |
| `extend(alta)` | pune la sfarsit fiecare element din `alta` |
| `insert(i, x)` | pune `x` pe pozitia `i`, restul se muta la dreapta |
| `pop()` / `pop(i)` | scoate si intoarce ultimul / cel de pe `i` |
| `remove(x)` | sterge **prima** aparitie a lui `x` (`ValueError` daca nu exista) |
| `index(x)` / `count(x)` | pozitia primei aparitii / de cate ori apare |
| `sort()` / `reverse()` | sorteaza / inverseaza pe loc |
""")
    c.cod("""
%%vezi
a = [3, 1, 4]
a.append(1)          #: [3, 1, 4, 1]
a.insert(0, 9)       #: pe pozitia 0; restul se muta la dreapta
ultim = a.pop()      #: scoate ultimul si il intoarce
a.remove(1)          #: sterge PRIMA aparitie a lui 1
cate = a.count(4)
poz = a.index(4)
a.extend([7, 8])     #: lipeste elementele unei alte liste
""")
    c.cod("""
%%vezi
a = [1, 2]
b = [1, 2]
a.append([3, 4])     #: append pune obiectul intreg: o lista in lista
b.extend([3, 4])     #: extend pune pe rand elementele
c = [1, 2] + [3, 4]  #: + face o lista noua, nu modifica nimic
c += [5]             #: += modifica c pe loc (ca extend)
""")

    c.md("""
## 4. `len`, `sum`, `min`, `max`, `in` - de mana si scurt

Bibliotecile nu se memoreaza, dar trebuie sa poti scrie de mana ce face fiecare functie. Intai bucla, apoi functia:
""")
    c.cod("""
v = [4, 9, 2, 9, 5]

s = 0
for x in v:
    s += x                            # suma de mana

mx, poz = v[0], 0
for i in range(1, len(v)):
    if v[i] > mx:                     # > strict: ramane prima aparitie a maximului
        mx, poz = v[i], i

print(s, mx, poz)
print(sum(v), max(v), v.index(max(v)))    # aceleasi rezultate, fara bucla scrisa de tine
print(9 in v, 7 in v, 7 not in v)         # in: cauta element cu element
""")
    c.md("""
De ce e `sum(v)` mai rapida decat bucla ta? Face aceeasi treaba, dar bucla ruleaza in **C**, nu in Python: fara interpretarea fiecarei linii de fiecare data. Masoara:
""")
    c.cod("""
import time
v = list(range(10**6))

t0 = time.perf_counter()
s = 0
for x in v:
    s += x
t1 = time.perf_counter()
s2 = sum(v)
t2 = time.perf_counter()
print(f'bucla ta: {t1 - t0:.3f} s   sum: {t2 - t1:.4f} s   (~{(t1 - t0) / (t2 - t1):.0f} ori mai rapid)')
""")

    c.md("""
## 5. Sortarea: intai de mana

**Bubble sort**: compari vecinii, iar daca sunt in ordine gresita ii interschimbi. Dupa o trecere, cel mai mare element a ajuns la sfarsit. Repeti pentru restul.
""")
    c.cod("""
%%vezi
v = [4, 2, 5, 1]
n = len(v)
for i in range(n - 1):
    for j in range(n - 1 - i):        #: dupa fiecare trecere, sfarsitul e deja sortat
        if v[j] > v[j + 1]:
            v[j], v[j + 1] = v[j + 1], v[j]     #: interschimbarea din lectia 01
""")
    c.md("""
Acum notam lista dupa **fiecare interschimbare** si o dam animatiei. Observa `v.copy()`: daca ai pune `v` direct, toate instantaneele ar fi aceeasi lista (aliasing, vezi mai jos).
""")
    c.cod("""
v = [5, 2, 4, 1, 3, 8, 7, 6]
stari = [v.copy()]                    # instantaneu la inceput
n = len(v)
for i in range(n - 1):
    for j in range(n - 1 - i):
        if v[j] > v[j + 1]:
            v[j], v[j + 1] = v[j + 1], v[j]
            stari.append(v.copy())    # cate un instantaneu la fiecare schimbare

print(len(stari) - 1, 'schimbari')
anim_sortare(stari)
""")
    c.md("""
Acum varianta scurta. `sorted(x)` intoarce o lista **noua**, `x.sort()` sorteaza **pe loc** (si intoarce `None`). `key=` e o functie aplicata fiecarui element; sortarea se face dupa rezultat. Sortarea e **stabila**: elementele cu cheie egala isi pastreaza ordinea.
""")
    c.cod("""
v = [5, 2, 4, 1, 3]
print(sorted(v), v)                   # sorted: lista noua, v ramane la fel
print(sorted(v, reverse=True))
v.sort()                              # pe loc
print(v)

cuvinte = ['banana', 'kiwi', 'mar', 'portocala']
print(sorted(cuvinte, key=len))       # dupa lungime
elevi = [('Ana', 9), ('Dan', 7), ('Ioana', 10), ('Dragos', 9)]
print(sorted(elevi, key=lambda e: e[1], reverse=True))    # lambda = functie mica, fara nume
print(sorted(elevi, key=lambda e: (-e[1], e[0])))         # dupa nota descrescator, apoi dupa nume
print(sorted('salut'))                # merge pe orice iterabil si da mereu o lista
""")
    c.cod("""
import random
date = [random.randint(1, 10**6) for _ in range(1500)]

def bubble(v):
    v = v.copy()
    n = len(v)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if v[j] > v[j + 1]:
                v[j], v[j + 1] = v[j + 1], v[j]
    return v

t0 = time.perf_counter(); r1 = bubble(date); t1 = time.perf_counter()
r2 = sorted(date); t2 = time.perf_counter()
print(r1 == r2, f'bubble: {t1 - t0:.3f} s   sorted: {t2 - t1:.5f} s   (~{(t1 - t0) / (t2 - t1):.0f} ori)')
""")
    c.md("""
**De ce e `sorted` asa de rapid?** Doua motive. (1) Algoritmul: bubble sort face ~n^2/2 comparatii, `sorted` foloseste **Timsort**, cu ~n log n. Pentru 1500 de elemente e diferenta dintre ~1 milion si ~16 mii de comparatii. (2) Bucla ruleaza in C. Timsort profita si de portiunile deja sortate din lista: pe date aproape sortate ajunge la ~n.

Concluzie practica: la olimpiada sortezi cu `sorted`/`sort`. Bubble il scrii ca sa intelegi, nu ca sa-l folosesti.
""")

    c.md("""
## 6. Comprehensii, `enumerate`, `zip`

**Comprehensia** construieste o lista dintr-o singura expresie. Se citeste de la `for`: "pentru fiecare x din ..., daca ..., pune expresia". Intai bucla (din topor), apoi scurtatura:
""")
    c.cod("""
%%vezi
patrate = []
for x in range(1, 6):
    patrate.append(x * x)                         #: varianta cu bucla
patrate2 = [x * x for x in range(1, 6)]           #: aceeasi lista, intr-o linie
pare = [x for x in range(10) if x % 2 == 0]       #: cu conditie: intra doar ce trece de if
""")
    c.cod("""
nume = ['ana', 'dan', 'ioana']
note = [9, 7, 10]

for i in range(len(nume)):                # din topor: indice
    print(i, nume[i], note[i])

for i, n in enumerate(nume, start=1):     # enumerate iti da indicele si elementul deodata
    print(i, n)
for n, nt in zip(nume, note):             # zip merge pe doua liste in paralel
    print(n, nt)
print(list(zip(nume, note)))              # zip se opreste la lista cea mai scurta
print(['bun' if nt >= 9 else 'ok' for nt in note])     # if-else in fata, pentru a alege valoarea
""")

    c.md("""
## 7. Citirea listelor din input

Reteta de la lectia 01: `list(map(int, input().split()))`. Pentru a afisa o lista pe o linie: `print(*v)` (steluta desface lista in argumente separate).
""")
    c.cod("""
%%vezi 5 "3 8 1 9 4"
n = int(input())                          #: prima linie: cate numere urmeaza
v = list(map(int, input().split()))       #: a doua linie: numerele, toate pe o linie
print(sum(v), max(v))
print(*v)                                 #: * desface lista: print(3, 8, 1, 9, 4)
""")
    c.md("""
O matrice vine pe `n` linii, fiecare cu `m` numere. Citesti linie cu linie si pui fiecare linie (o lista) in lista mare. Valorile de intrare din animatie sunt scrise pe rand, intre ghilimele.
""")
    c.cod("""
%%vezi "2 3" "1 2 3" "4 5 6"
n, m = map(int, input().split())          #: dimensiunile
mat = []
for _ in range(n):
    mat.append(list(map(int, input().split())))   #: fiecare linie devine o lista
""")

    c.md("""
## 8. Aliasing: cea mai importanta sectiune

O variabila **nu contine** lista, ci pointeaza spre ea (ca un pointer din C++, dar fara steluta). `b = a` nu copiaza lista, mai pune un nume pe ea.

**Prezice:** ce afiseaza ultimul `print`?

<details><summary>Raspuns</summary>

`[1, 2, 3, 4]`. Animatia arata eticheta `@1` pe amandoua variabilele: e **aceeasi** lista. Modifici prin `b`, se vede prin `a`.
</details>
""")
    c.cod("""
%%vezi
a = [1, 2, 3]
b = a            #: NU se copiaza lista: b e un al doilea nume pentru aceeasi lista
b.append(4)      #: modific prin b...
print(a)         #: ...si a se vede schimbat
""")
    c.md("""
Ca sa ai o lista **independenta** o copiezi explicit. Trei variante echivalente pentru liste simple: `a.copy()`, `a[:]` (felia cu totul) si `list(a)`.
""")
    c.cod("""
%%vezi
a = [1, 2, 3]
b = a.copy()     #: lista noua, cu aceleasi valori
c = a[:]         #: felia cu totul: tot o copie
d = list(a)      #: si asta
b.append(4)
c[0] = 99
#: a nu s-a atins
""")
    c.md("""
**Dar** `copy()` e o copie *superficiala*: copiaza lista de sus, nu si ce e in ea. La o matrice, randurile raman aceleasi liste in ambele matrici. Uita-te la etichetele `@` de pe randuri:
""")
    c.cod("""
%%vezi
import copy
m = [[1, 2], [3, 4]]
n1 = m.copy()               #: copie a listei EXTERIOARE: randurile sunt aceleasi liste (@)
n1[0][0] = 99               #: schimb prin n1 si se schimba si m
n2 = copy.deepcopy(m)       #: copie in adancime: copiaza recursiv tot
n2[1][1] = 0                #: m si n1 raman neatinse
""")
    c.md("""
Aceeasi poveste apare cand dai o lista unei **functii**: primesti obiectul, nu o copie.
""")
    c.cod("""
%%vezi
def adauga_zero(v):
    v.append(0)            #: v e chiar lista de afara: se modifica si originalul
def cu_zero(v):
    return v + [0]         #: v + [0] face o lista noua: originalul ramane

a = [1, 2]
adauga_zero(a)
b = cu_zero(a)
""")
    c.md("""
**Capcana clasica: `[[0] * m] * n`.** `[0] * m` e o lista, iar `* n` pune **aceeasi** lista de `n` ori (copiaza referinta). Vezi eticheta `@1` pe ambele randuri, iar la final `gresit` are 5 pe *ambele* randuri. Corect: comprehensia evalueaza `[0] * m` de la zero la fiecare rand.

**Prezice:** dupa `gresit[0][0] = 5`, cum arata `gresit`? Dar `bun`?

<details><summary>Raspuns</summary>

`gresit` = `[[5, 0, 0], [5, 0, 0]]` (un singur rand, aratat de doua ori). `bun` = `[[5, 0, 0], [0, 0, 0]]`.
</details>
""")
    c.cod("""
%%vezi
n, m = 2, 3
gresit = [[0] * m] * n          #: [0] * m e O lista; * n o pune de n ori, fara sa o copieze
gresit[0][0] = 5                #: pare ca schimb un singur element
bun = [[0] * m for _ in range(n)]   #: comprehensia face un rand NOU la fiecare pas
bun[0][0] = 5
""")
    c.md("""
**Modificarea unei liste in timp ce o parcurgi.** Bucla tine minte pozitia (indexul), nu elementele. Daca stergi ceva, lista se scurteaza si elementele se muta la stanga, iar bucla sare peste unul. Aici vrem sa stergem numerele pare:
""")
    c.cod("""
%%vezi
v = [2, 4, 6, 1, 8]
for i, x in enumerate(v):
    if x % 2 == 0:
        v.remove(x)         #: lista se scurteaza; la pasul urmator i creste, deci se sare un element
""")
    c.md("""
Rezultat: `[4, 1]`. Numarul 4 (par) a ramas, pentru ca a fost sarit. Doua reparatii sigure: construiesti o lista noua, sau parcurgi o **copie**.
""")
    c.cod("""
v = [2, 4, 6, 1, 8]
print([x for x in v if x % 2 != 0])      # varianta 1: lista noua, cu ce pastrezi

for x in v[:]:                            # varianta 2: parcurgi copia, stergi din original
    if x % 2 == 0:
        v.remove(x)
print(v)
""")
    c.md("""
Un ultim aliasing, doar ca sa-l stii. Valorile implicite ale parametrilor se creeaza **o singura data**, la definirea functiei. O lista goala pusa ca valoare implicita devine partajata intre apeluri. Uita-te la `@1`:
""")
    c.cod("""
%%vezi
def aduna(x, lista=[]):        #: lista goala creata O SINGURA DATA, cand se defineste functia
    lista.append(x)
    return lista

r1 = aduna(1)
r2 = aduna(2)                  #: surpriza: e aceeasi lista de la primul apel
""")
    c.md("""
Reparatia standard e `lista=None` si `if lista is None: lista = []` in corp. Revii la asta cand scrii functii mai complicate.
""")

    c.md("""
## 9. Matrici: liste de liste

O matrice e o lista in care fiecare element e tot o lista (un rand). `mat[i][j]` = randul `i`, coloana `j`. Nu exista un tip separat pentru matrice. Animatia le arata ca **tabel**.
""")
    c.cod("""
%%vezi
n, m = 3, 4
mat = [[i * m + j for j in range(m)] for i in range(n)]   #: constructie corecta: un rand nou la fiecare i
x = mat[1][2]              #: randul 1, coloana 2
mat[0][3] = -1
linie = mat[2]             #: un rand e o lista
nr_linii = len(mat)        #: numarul de linii
nr_coloane = len(mat[0])   #: numarul de coloane = lungimea unui rand
""")
    c.md("""
**Parcurgerea pe linii** (cea mai naturala) are doua bucle: cea de afara pe `i` (randuri), cea din interior pe `j`. Daca inversezi cele doua bucle, parcurgi **pe coloane**.
""")
    c.cod("""
%%vezi
mat = [[1, 2, 3], [4, 5, 6]]
for i in range(2):
    for j in range(3):
        print(mat[i][j], end=' ')       #: pe linii: i afara, j inauntru
    print()
""")
    c.md("""
Ca sa **vezi ordinea**, colectam celulele vizitate intr-o lista `ordine` si o dam animatiei `anim_parcurgere(n, m, ordine)`. Ordinea o scrie codul tau, animatia doar o deseneaza. Mai intai parcurgerea pe **coloane** (bucla `j` afara):
""")
    c.cod("""
n, m = 4, 5
ordine = []
for j in range(m):
    for i in range(n):
        ordine.append((i, j))
anim_parcurgere(n, m, ordine)
""")
    c.md("""
**Sarpe** (zig-zag): pe randurile pare mergi la dreapta, pe cele impare la stanga. Se foloseste la parcurgeri de tabla si in unele probleme cu "drumul cel mai scurt".
""")
    c.cod("""
n, m = 4, 5
ordine = []
for i in range(n):
    if i % 2 == 0:
        coloane = range(m)
    else:
        coloane = range(m - 1, -1, -1)
    for j in coloane:
        ordine.append((i, j))
anim_parcurgere(n, m, ordine)
""")
    c.md("""
**Diagonale.** Pe o diagonala secundara (de sus-dreapta spre stanga-jos) suma `i + j` e constanta. Pe una principala, diferenta `j - i` e constanta. Deci: pentru fiecare valoare `s` a sumei, iei toate celulele valide cu `i + j == s`.
""")
    c.cod("""
n, m = 4, 5
ordine = []
for s in range(n + m - 1):        # suma i + j merge de la 0 la n + m - 2
    for i in range(n):
        j = s - i
        if 0 <= j < m:            # verificam ca j sa fie in matrice
            ordine.append((i, j))
anim_parcurgere(n, m, ordine)
""")
    c.cod("""
%%vezi
mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
n = 3
principala = 0
secundara = 0
for i in range(n):
    principala += mat[i][i]           #: diagonala principala: i == j
    secundara += mat[i][n - 1 - i]    #: diagonala secundara: i + j == n - 1
""")
    c.md("""
**Sume pe linii si pe coloane.** Pe linii e simplu: `sum(rand)`. Pe coloane trebuie sa aduni elementul `j` din fiecare rand.
""")
    c.cod("""
%%vezi
mat = [[1, 2, 3], [4, 5, 6]]
sume_linii = []
for rand in mat:
    sume_linii.append(sum(rand))         #: o suma pe rand
sume_col = [0] * 3
for rand in mat:
    for j in range(3):
        sume_col[j] += rand[j]           #: fiecare rand contribuie la fiecare coloana
""")
    c.md("""
**Transpusa** (liniile devin coloane): `t[j][i] = mat[i][j]`. Iar scurtatura: `zip(*mat)`. Steluta desface matricea in randuri separate, iar `zip` le ia in paralel: primele elemente, apoi al doilea din fiecare etc. Exact coloanele.
""")
    c.cod("""
%%vezi
mat = [[1, 2, 3], [4, 5, 6]]
n, m = 2, 3
t = [[0] * n for _ in range(m)]      #: transpusa are m linii si n coloane
for i in range(n):
    for j in range(m):
        t[j][i] = mat[i][j]          #: (i, j) ajunge la (j, i)
""")
    c.cod("""
mat = [[1, 2, 3], [4, 5, 6]]
print(list(zip(*mat)))                       # perechi (tupluri), nu liste
print([list(col) for col in zip(*mat)])      # transpusa, cu randuri-liste
print([sum(col) for col in zip(*mat)])       # sumele pe coloane, intr-o linie
""")
    c.md("""
**Rotirea cu 90 de grade** in sensul acelor de ceasornic: elementul de la `(i, j)` ajunge la `(j, n - 1 - i)`. Matricea `n x m` devine `m x n`.
""")
    c.cod("""
%%vezi
mat = [[1, 2, 3], [4, 5, 6]]
n, m = 2, 3
rot = [[0] * n for _ in range(m)]
for i in range(n):
    for j in range(m):
        rot[j][n - 1 - i] = mat[i][j]     #: (i, j) ajunge la (j, n - 1 - i)
""")
    c.cod("""
mat = [[1, 2, 3], [4, 5, 6]]
print([list(r) for r in zip(*mat[::-1])])   # scurt: inversezi randurile, apoi transpui
""")
    c.md("""
**Spirala**: pornesti din stanga-sus, mergi spre dreapta, jos, stanga, sus, apoi intri o coaja mai adanc. Tinem patru margini (`sus`, `jos`, `st`, `dr`) care se strang. Cele doua `if`-uri opresc parcurgerea sa se repete cand a ramas un singur rand sau o singura coloana.
""")
    c.cod("""
n, m = 4, 5
ordine = []
sus, jos, st, dr = 0, n - 1, 0, m - 1
while sus <= jos and st <= dr:
    for j in range(st, dr + 1):                 # spre dreapta, pe randul de sus
        ordine.append((sus, j))
    for i in range(sus + 1, jos + 1):           # in jos, pe coloana din dreapta
        ordine.append((i, dr))
    if sus < jos:
        for j in range(dr - 1, st - 1, -1):     # spre stanga, pe randul de jos
            ordine.append((jos, j))
    if st < dr:
        for i in range(jos - 1, sus, -1):       # in sus, pe coloana din stanga
            ordine.append((i, st))
    sus, jos, st, dr = sus + 1, jos - 1, st + 1, dr - 1     # strangem marginile
anim_parcurgere(n, m, ordine)
""")
    c.md("""
**Vecinii unei celule** (sus, jos, stanga, dreapta) apar in labirinturi, joc de viata, umplere de zone. Lista de deplasari `(di, dj)` te scapa de patru `if`-uri. **Verificarea limitelor e obligatorie**: vezi la Capcane de ce nu ajunge sa speri ca "da eroare".
""")
    c.cod("""
%%vezi
mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
n = m = 3
i, j = 0, 1
vecini = []
for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    ni, nj = i + di, j + dj
    if 0 <= ni < n and 0 <= nj < m:         #: verificarea limitelor: fara ea, ni = -1 ar lua ultimul rand
        vecini.append(mat[ni][nj])
""")
    c.cod("""
mat = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
n, m = len(mat), len(mat[0])
chenar = [mat[i][j] for i in range(n) for j in range(m) if i in (0, n - 1) or j in (0, m - 1)]
print(chenar, sum(chenar))          # elementele de pe margine: prima/ultima linie sau coloana
print([r[1:-1] for r in mat[1:-1]]) # interiorul, cu felii pe ambele dimensiuni
""")

    c.md("""
## 10. Cat costa fiecare operatie

Lista e un tablou de pointeri, unul dupa altul in memorie. De aici toata complexitatea:

| operatie | cost | de ce |
|---|---|---|
| `v[i]`, `v[i] = x`, `len(v)` | O(1) | adresa se calculeaza direct |
| `v.append(x)`, `v.pop()` | O(1) amortizat | se scrie la coada (din cand in cand lista isi mareste spatiul) |
| `v.insert(0, x)`, `v.pop(0)` | O(n) | toate elementele se muta cu o pozitie |
| `x in v`, `v.index(x)`, `v.count(x)` | O(n) | se cauta element cu element |
| `sorted(v)`, `v.sort()` | O(n log n) | Timsort |

**Prezice:** daca dublezi `n`, de cate ori creste timpul pentru `n` apeluri `append`? Dar pentru `n` apeluri `insert(0, x)`?

<details><summary>Raspuns</summary>

`append`: de ~2 ori (n operatii O(1)). `insert(0, x)`: de ~4 ori (n operatii O(n), deci n^2 in total). Masoara mai jos.
</details>
""")
    c.cod("""
def masoara(f):
    t0 = time.perf_counter()
    f()
    return time.perf_counter() - t0

def la_sfarsit(n):
    v = []
    for i in range(n):
        v.append(i)

def la_inceput(n):
    v = []
    for i in range(n):
        v.insert(0, i)

for n in (10_000, 20_000, 40_000):
    print(n, f'append: {masoara(lambda: la_sfarsit(n)):.4f} s    insert(0): {masoara(lambda: la_inceput(n)):.4f} s')
""")
    c.cod("""
def scoate_de_la_sfarsit(n):
    v = list(range(n))
    while v:
        v.pop()

def scoate_de_la_inceput(n):
    v = list(range(n))
    while v:
        v.pop(0)

for n in (10_000, 20_000, 40_000):
    print(n, f'pop(): {masoara(lambda: scoate_de_la_sfarsit(n)):.4f} s    pop(0): {masoara(lambda: scoate_de_la_inceput(n)):.4f} s')

v = list(range(10**6))
print(f'-1 in v (nu exista, se cauta peste tot): {masoara(lambda: -1 in v):.4f} s')
""")
    c.md("""
Daca ai nevoie des sa scoti de la **inceput** (o coada), foloseste `collections.deque`, unde ambele capete sunt O(1). Iar daca tot cauti `x in v` de multe ori, ai nevoie de alta structura: multimea, pe care o vezi in notebook-ul urmator.
""")

    c.md("""
## 11. Legatura cu ML: matricea e datasetul

Un dataset e o matrice: **randuri = exemple, coloane = trasaturi**. O imagine alb-negru e o matrice de intensitati. Exact asta e un `np.array`: aceeasi idee, dar cu memorie contigua si operatii vectorizate. `shape` iti da `(nr_linii, nr_coloane)`, adica `(n, m)`-ul de mai sus.
""")
    c.cod("""
import numpy as np
X = [[5.1, 3.5, 1.4], [4.9, 3.0, 1.4], [6.2, 3.4, 5.4], [5.9, 3.0, 5.1]]   # 4 flori, 3 trasaturi
print('de mana:', [round(sum(col) / len(X), 2) for col in zip(*X)])        # media fiecarei coloane

A = np.array(X)
print('numpy:  ', A.shape, A.mean(axis=0).round(2))
print(A[1], A[:, 0], A[:2, 1:])       # randul 1, coloana 0, felie pe doua dimensiuni

import matplotlib.pyplot as plt
img = [[0, 0, 255, 255], [0, 0, 255, 255], [255, 255, 0, 0], [255, 255, 0, 0]]
oglinda = [r[::-1] for r in img]      # oglindirea unei imagini = inversarea fiecarui rand
fig, ax = plt.subplots(1, 2, figsize=(4, 2))
ax[0].imshow(img, cmap='gray'); ax[1].imshow(oglinda, cmap='gray')
plt.show()
""")

    c.md("""
## 12. Capcane

**Capcana 1: `a = a.sort()`.** `sort`, `append`, `reverse` modifica pe loc si intorc `None`. Daca atribui rezultatul, pierzi lista:
""")
    c.cod("""
%%vezi
a = [3, 1, 2]
a = a.sort()         #: sort intoarce None si a ajunge pe None
print(a[0])          #: si de aici pica programul: None nu se poate indexa
""")
    c.md("""
**Capcana 2: indicii negativi nu dau eroare.** Cand cauti vecinii, `mat[i - 1]` pentru `i = 0` nu pica: ia **ultimul** rand. Programul merge, dar da rezultate gresite fara sa te avertizeze.
""")
    c.cod("""
%%vezi
mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
i, j = 0, 0
sus = mat[i - 1][j]      #: nu exista rand deasupra lui 0, dar -1 e valid: ia ultimul rand
""")
    c.md("""
**Capcana 3: `+=` vs `+` intr-o functie.** `v += x` modifica lista pe loc (ca `extend`), deci se vede in afara functiei. `v = v + x` face o lista noua, iar in afara nu se schimba nimic.
""")
    c.cod("""
%%vezi
def cu_plus_egal(v):
    v += [0]           #: pe loc: modifica lista de afara
def cu_plus(v):
    v = v + [0]        #: lista noua legata la numele local v: afara nu se vede

a = [1]
b = [1]
cu_plus_egal(a)
cu_plus(b)
""")
    c.md("""
**Capcana 4: `remove(x)` sterge doar prima aparitie**, iar `v[i + 1]` la ultimul indice iese din lista. Cand te uiti la vecinul urmator, opresti bucla mai devreme:
""")
    c.cod("""
v = [1, 2, 2, 3, 2]
v.remove(2)
print(v)                      # doar primul 2 a disparut
print([x for x in v if x != 2])   # sterge TOATE aparitiile

v = [1, 3, 2, 5]
print([v[i + 1] - v[i] for i in range(len(v) - 1)])   # diferente intre vecini: range(len(v) - 1), nu len(v)
""")

    c.md("""
## 13. Cum citesti eroarea

Erorile listelor sunt putine si se recunosc repede. Nu le citi de sus in jos: uita-te la **ultima linie** si la **linia rosie** din animatie.

| eroare | de obicei inseamna |
|---|---|
| `IndexError: list index out of range` | indice in afara listei (prea mare, sau `-len-1`) |
| `ValueError: list.remove(x): x not in list` | ai cerut `remove`/`index` pentru ceva ce nu exista |
| `TypeError: 'NoneType' object is not subscriptable` | ai indexat `None`, de obicei dupa `a = a.sort()` |
| `TypeError: list indices must be integers` | indice `float` sau text (`v[n / 2]` in loc de `v[n // 2]`) |
| `ValueError: invalid literal for int()` | ai uitat `.split()` la citire |
""")
    c.cod("""
%%vezi
mat = [[1, 2, 3], [4, 5, 6]]
i = 2
print(mat[i][0])         #: matricea are randurile 0 si 1
""")
    c.cod("""
%%vezi
v = [1, 2, 3, 4, 5]
mijloc = len(v) / 2      #: / da float: 2.5
print(v[mijloc])
""")
    c.cod("""
%%vezi "3 4"
v = int(input())         #: input() e textul '3 4', nu un singur numar
""")
    c.cod("""
%%vezi
a = [1, 2, 3]
a.remove(7)
""")

    c.md("""
## 14. Exemplu complet

Un program ca la concurs: prima linie `n`, a doua linia cu cele `n` numere. Afiseaza maximul si prima pozitie unde apare (numarotata de la 1).
""")
    c.cod("""
%%vezi 6 "4 9 2 9 5 1"
n = int(input())
v = list(map(int, input().split()))
mx = max(v)
print(mx, v.index(mx) + 1)     #: pozitia, numarotata de la 1 ca in enunt
""")

    c.md("""
## Exercitii

Le rezolvi tu. Fiecare are o celula de completat si una de verificare. Daca un test pica, iti spune ce ai intors si ce trebuia.
""")

    c.md("""
**Exercitiul 1.** Intoarce perechea `(maxim, pozitie)`, unde pozitia e a **primei** aparitii a maximului. Scrie bucla de mana, fara `max`. Lista are cel putin un element.
""")
    c.ex("""
def maxim_si_pozitie(v):
    pass  # TODO
""", """
def maxim_si_pozitie(v):
    mx, poz = v[0], 0
    for i in range(1, len(v)):
        if v[i] > mx:
            mx, poz = v[i], i
    return mx, poz
""")
    c.cod("""
verifica('maxim_si_pozitie', maxim_si_pozitie,
         [(([3, 9, 2, 9],), (9, 1)), (([5],), (5, 0)), (([-4, -1, -7],), (-1, 1))],
         ascunse=[(([7, 7, 7],), (7, 0)), (([1, 2, 3, 4, 5],), (5, 4)), (([5, 4, 3, 2, 1],), (5, 0))],
         indiciu='foloseste > strict ca sa ramai la prima aparitie')
""")

    c.md("""
**Exercitiul 2.** Inverseaza lista **pe loc**, fara `reverse()` si fara `[::-1]`: interschimbi elementul `i` cu `n - 1 - i` pentru prima jumatate a listei. Nu intorci nimic, modifici lista primita.
""")
    c.ex("""
def inverseaza(v):
    pass  # TODO: modifica v pe loc
""", """
def inverseaza(v):
    n = len(v)
    for i in range(n // 2):
        v[i], v[n - 1 - i] = v[n - 1 - i], v[i]
""")
    c.cod("""
verifica('inverseaza', inverseaza,
         [(([1, 2, 3, 4],), [4, 3, 2, 1]), (([1, 2, 3],), [3, 2, 1]), (([],), [])],
         ascunse=[(([7],), [7]), ((list(range(10)),), list(range(9, -1, -1)))], in_loc=True,
         indiciu='ajungi doar pana la jumatate; altfel inversezi de doua ori')
""")

    c.md("""
**Exercitiul 3.** Elimina duplicatele **pastrand ordinea primei aparitii**. `[3, 1, 3, 2, 1]` devine `[3, 1, 2]`. Intoarce o lista noua. (Cu multimi se face mai simplu, dar acolo ajungem in notebook-ul urmator. Acum cu `in`.)
""")
    c.ex("""
def fara_duplicate(v):
    pass  # TODO
""", """
def fara_duplicate(v):
    rez = []
    for x in v:
        if x not in rez:
            rez.append(x)
    return rez
""")
    c.cod("""
verifica('fara_duplicate', fara_duplicate,
         [(([3, 1, 3, 2, 1],), [3, 1, 2]), (([1, 2, 3],), [1, 2, 3]), (([],), [])],
         ascunse=[(([5, 5, 5, 5],), [5]), ((['a', 'b', 'a'],), ['a', 'b']), (([2, 1, 2, 1, 3],), [2, 1, 3])])
""")

    c.md("""
**Exercitiul 4.** Rotire la stanga cu `k` pozitii: `rotire_stanga([1, 2, 3, 4, 5], 2)` da `[3, 4, 5, 1, 2]`. Intoarce o lista noua. `k` poate fi 0 sau mai mare decat lungimea, iar lista poate fi goala. Ajuta-te de feliile din sectiunea 2.
""")
    c.ex("""
def rotire_stanga(v, k):
    pass  # TODO
""", """
def rotire_stanga(v, k):
    if not v:
        return []
    k = k % len(v)
    return v[k:] + v[:k]
""")
    c.cod("""
verifica('rotire_stanga', rotire_stanga,
         [(([1, 2, 3, 4, 5], 2), [3, 4, 5, 1, 2]), (([1, 2, 3], 0), [1, 2, 3]), (([1, 2, 3], 3), [1, 2, 3])],
         ascunse=[(([1, 2, 3, 4], 6), [3, 4, 1, 2]), (([], 5), []), (([9], 100), [9])],
         indiciu='k % len(v) rezolva k mare; atentie la lista goala (impartire la 0)')
""")

    c.md("""
**Exercitiul 5.** Pentru o matrice, intoarce perechea `(sume_linii, sume_coloane)`: lista sumelor pe linii si lista sumelor pe coloane. Matricea are cel putin o linie si o coloana.
""")
    c.ex("""
def sume(mat):
    pass  # TODO: intoarce (sume_linii, sume_coloane)
""", """
def sume(mat):
    return [sum(r) for r in mat], [sum(col) for col in zip(*mat)]
""")
    c.cod("""
verifica('sume', sume,
         [(([[1, 2, 3], [4, 5, 6]],), ([6, 15], [5, 7, 9])), (([[7]],), ([7], [7]))],
         ascunse=[(([[1, 1], [2, 2], [3, 3]],), ([2, 4, 6], [6, 6])), (([[1, 2, 3]],), ([6], [1, 2, 3]))])
""")

    c.md("""
**Exercitiul 6.** Transpusa unei matrici: intoarce o matrice noua, cu randuri **liste** (nu tupluri).
""")
    c.ex("""
def transpusa(mat):
    pass  # TODO
""", """
def transpusa(mat):
    return [list(col) for col in zip(*mat)]
""")
    c.cod("""
verifica('transpusa', transpusa,
         [(([[1, 2, 3], [4, 5, 6]],), [[1, 4], [2, 5], [3, 6]]), (([[1]],), [[1]])],
         ascunse=[(([[1, 2], [3, 4]],), [[1, 3], [2, 4]]), (([[1, 2, 3]],), [[1], [2], [3]])],
         indiciu='zip(*mat) da tupluri; transforma-le in liste')
""")

    c.md("""
**Exercitiul 7.** Construieste o matrice `n x m` plina cu `valoare`. Aici se testeaza si capcana din sectiunea 8: verificarea a doua schimba un element si se uita daca **s-a schimbat un singur rand**.
""")
    c.ex("""
def matrice(n, m, valoare):
    pass  # TODO
""", """
def matrice(n, m, valoare):
    return [[valoare] * m for _ in range(n)]
""")
    c.cod("""
def _schimba_unul(n, m):
    t = matrice(n, m, 0)
    t[0][0] = 1
    return t

verifica('matrice', matrice, [((2, 3, 0), [[0, 0, 0], [0, 0, 0]]), ((1, 2, 7), [[7, 7]])],
         ascunse=[((3, 1, 5), [[5], [5], [5]])])
verifica('matrice: randuri independente', _schimba_unul, [((2, 2), [[1, 0], [0, 0]]), ((3, 1), [[1], [0], [0]])],
         indiciu='foloseste [[valoare] * m for _ in range(n)], nu [[valoare] * m] * n')
""")

    c.md("""
**Exercitiul 8.** Program ca la concurs. Pe prima linie `n`, pe a doua cele `n` numere. Afiseaza pe primul rand suma lor, iar pe al doilea rand numerele **in ordine descrescatoare**, separate prin spatiu.
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    n = int(input())
    v = list(map(int, input().split()))
    print(sum(v))
    print(*sorted(v, reverse=True))
""")
    c.cod("""
verifica_program('suma si sortare', main,
                 [(['4', '3 1 4 2'], '10\\n4 3 2 1'), (['1', '5'], '5\\n5')],
                 ascunse=[(['5', '-1 -5 0 5 1'], '0\\n5 1 0 -1 -5'), (['3', '2 2 2'], '6\\n2 2 2')],
                 indiciu='print(*lista) afiseaza elementele separate prin spatiu')
scor()
""")

    c.md("""
## Recapitulare

- Lista: indici de la 0, negativi de la coada; felia `a[i:j:k]` e o **copie** noua, iar capetele depasite nu dau eroare.
- Metodele modifica pe loc si intorc `None` (`sort`, `append`, `reverse`...). `sorted(x)` da o lista noua, are `key=` si `reverse=`.
- `b = a` nu copiaza. Copie: `a.copy()`, `a[:]`, `list(a)`. Pentru liste de liste: `copy.deepcopy` sau o comprehensie.
- Matricea: `[[0] * m for _ in range(n)]`, niciodata `[[0] * m] * n`. `mat[i][j]`, `len(mat)`, `len(mat[0])`.
- Transpusa: `zip(*mat)`. Vecini: lista de `(di, dj)` plus verificarea limitelor.
- Cost: `append`/`pop()` O(1), `insert(0)`/`pop(0)`/`in` O(n), `sorted` O(n log n).
- Datasetul e o matrice (randuri = exemple, coloane = trasaturi), ca in NumPy.

Tema are exercitii cu teste ascunse, un "repara codul", doua programe si o provocare (matricea spirala).
""")
    c.salveaza('04-liste-tablouri-predare')


def tema():
    c = Carnet('Liste si tablouri bidimensionale', 'tema', fisiere=FISIERE)
    c.md("""
Exercitiile de acasa. Testele vizibile iti arata daca ai inteles enuntul, cele **ascunse** verifica si cazurile limita (liste goale, un singur element, dimensiuni mari). Poti rula o celula de verificare de cate ori vrei; `scor()` de la final aduna tot.

Daca te blochezi, inapoi la notebook-ul de predare (animatiile `%%vezi` te ajuta sa vezi ce face codul tau).
""")

    c.md("""
### 1. Al doilea maxim

Intoarce cea mai mare valoare **diferita** de maxim. Daca lista nu are cel putin doua valori diferite, intoarce `None`. Lista are cel putin un element. `[5, 5, 4]` da `4`, `[7, 7]` da `None`.
""")
    c.ex("""
def al_doilea_maxim(v):
    pass  # TODO
""", """
def al_doilea_maxim(v):
    mx = max(v)
    mai_mici = [x for x in v if x < mx]
    return max(mai_mici) if mai_mici else None
""")
    c.cod("""
verifica('al_doilea_maxim', al_doilea_maxim,
         [(([3, 1, 4, 1, 5],), 4), (([7, 7, 7],), None), (([5, 5, 4],), 4)],
         ascunse=[(([2],), None), (([-1, -5, -3],), -3), (([1, 2],), 1), (([9, 9, 8, 8],), 8)], puncte=2)
""")

    c.md("""
### 2. Sortare dupa ultima cifra

Sorteaza numerele naturale dupa **ultima cifra**; la ultima cifra egala, dupa valoare. Intoarce o lista noua. `[19, 21, 33, 40, 5]` da `[40, 21, 33, 5, 19]`. Foloseste `sorted` cu `key=`, unde cheia poate fi un tuplu.
""")
    c.ex("""
def dupa_ultima_cifra(v):
    pass  # TODO
""", """
def dupa_ultima_cifra(v):
    return sorted(v, key=lambda x: (x % 10, x))
""")
    c.cod("""
verifica('dupa_ultima_cifra', dupa_ultima_cifra,
         [(([19, 21, 33, 40, 5],), [40, 21, 33, 5, 19]), (([11, 21, 1],), [1, 11, 21])],
         ascunse=[(([],), []), (([100, 10, 20, 1],), [10, 20, 100, 1]), (([15, 5, 25],), [5, 15, 25])], puncte=2)
""")

    c.md("""
### 3. Interclasare

Cele doua liste `a` si `b` sunt deja sortate crescator. Intoarce lista sortata cu toate elementele din ambele, in **O(n + m)**: tii doi indici, iar la fiecare pas iei cel mai mic dintre cele doua elemente curente. Testele ascunse au liste de sute de mii de elemente.
""")
    c.ex("""
def interclaseaza(a, b):
    pass  # TODO: doi indici, o bucla while
""", """
def interclaseaza(a, b):
    rez = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            rez.append(a[i])
            i += 1
        else:
            rez.append(b[j])
            j += 1
    rez += a[i:]
    rez += b[j:]
    return rez
""")
    c.cod("""
import random
mari_a = sorted(random.randint(0, 10**9) for _ in range(200_000))
mari_b = sorted(random.randint(0, 10**9) for _ in range(200_000))
verifica('interclaseaza', interclaseaza,
         [(([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6]), (([1, 2], []), [1, 2]), (([], [3]), [3])],
         ascunse=[(([1, 1, 2], [1, 3]), [1, 1, 1, 2, 3]), (([5], [1, 2, 3]), [1, 2, 3, 5]), (([], []), []),
                  ((mari_a, mari_b), sorted(mari_a + mari_b))],
         referinta=lambda a, b: sorted(a + b),
         generator=lambda: (sorted(random.randint(0, 20) for _ in range(random.randint(0, 8))),
                            sorted(random.randint(0, 20) for _ in range(random.randint(0, 8)))),
         puncte=2, timp=5)
""")

    c.md("""
### 4. Diagonalele

Pentru o matrice patrata, intoarce perechea `(suma_principala, suma_secundara)`. Daca `n` e impar, elementul din centru apartine ambelor diagonale si se aduna in ambele sume.
""")
    c.ex("""
def diagonale(mat):
    pass  # TODO
""", """
def diagonale(mat):
    n = len(mat)
    return sum(mat[i][i] for i in range(n)), sum(mat[i][n - 1 - i] for i in range(n))
""")
    c.cod("""
verifica('diagonale', diagonale,
         [(([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), (15, 15)), (([[1, 2], [3, 4]],), (5, 5)), (([[7]],), (7, 7))],
         ascunse=[(([[1, 0, 0, 5], [0, 1, 6, 0], [0, 7, 1, 0], [8, 0, 0, 1]],), (4, 26)), (([[-1, 2], [3, -4]],), (-5, 5))],
         puncte=1)
""")

    c.md("""
### 5. Chenarul

Suma elementelor de pe **margine** (prima si ultima linie, prima si ultima coloana) a unei matrici `n x m` oarecare. Fiecare element se aduna o singura data, chiar daca e pe doua margini (colturile), iar pentru o matrice cu o singura linie sau coloana se aduna tot.
""")
    c.ex("""
def suma_chenar(mat):
    pass  # TODO
""", """
def suma_chenar(mat):
    n, m = len(mat), len(mat[0])
    return sum(mat[i][j] for i in range(n) for j in range(m) if i in (0, n - 1) or j in (0, m - 1))
""")
    c.cod("""
verifica('suma_chenar', suma_chenar,
         [(([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), 40), (([[5]],), 5), (([[1, 2], [3, 4]],), 10)],
         ascunse=[(([[1, 2, 3, 4]],), 10), (([[1], [2], [3]],), 6), (([[1, 1, 1, 1], [1, 9, 9, 1], [1, 9, 9, 1], [1, 1, 1, 1]],), 12)],
         puncte=1)
""")

    c.md("""
### 6. Vecinii unei celule

Intoarce lista valorilor celor (pana la 4) vecini ai celulei `(i, j)`, in aceasta ordine: **sus, jos, stanga, dreapta**. Vecinii care ies din matrice se omit. Nu te baza pe `IndexError` (indicii negativi nu dau eroare!).
""")
    c.ex("""
def vecini(mat, i, j):
    pass  # TODO
""", """
def vecini(mat, i, j):
    n, m = len(mat), len(mat[0])
    rez = []
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < m:
            rez.append(mat[ni][nj])
    return rez
""")
    c.cod("""
m3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
verifica('vecini', vecini,
         [((m3, 1, 1), [2, 8, 4, 6]), ((m3, 0, 0), [4, 2]), ((m3, 2, 2), [6, 8])],
         ascunse=[((m3, 0, 1), [5, 1, 3]), ((m3, 1, 0), [1, 7, 5]), (([[5]], 0, 0), []), (([[1, 2, 3]], 0, 2), [2])],
         puncte=2, indiciu='un 0 <= ni < n inainte de a citi mat[ni][nj]')
""")

    c.md("""
### 7. Rotire cu 90 de grade

Roteste o matrice `n x m` cu 90 de grade **in sensul acelor de ceasornic**. Rezultatul are `m` linii si `n` coloane. `[[1, 2, 3], [4, 5, 6]]` da `[[4, 1], [5, 2], [6, 3]]`. Randurile rezultatului sunt liste.
""")
    c.ex("""
def roteste(mat):
    pass  # TODO
""", """
def roteste(mat):
    return [list(r) for r in zip(*mat[::-1])]
""")
    c.cod("""
import random

def matrice_aleatoare():
    h, w = random.randint(1, 5), random.randint(1, 5)
    return ([[random.randint(0, 9) for _ in range(w)] for _ in range(h)],)

verifica('roteste', roteste,
         [(([[1, 2, 3], [4, 5, 6]],), [[4, 1], [5, 2], [6, 3]]), (([[1, 2], [3, 4]],), [[3, 1], [4, 2]]), (([[7]],), [[7]])],
         ascunse=[(([[1, 2, 3]],), [[1], [2], [3]]), (([[1], [2]],), [[2, 1]])],
         referinta=lambda m: [[m[len(m) - 1 - k][j] for k in range(len(m))] for j in range(len(m[0]))],
         generator=matrice_aleatoare, puncte=2)
""")

    c.md("""
### 8. Repara codul: matricea diagonala

Functia trebuie sa construiasca matricea `n x n` cu `1` pe diagonala principala si `0` in rest (matricea identitate). Gaseste bug-ul cu animatia de mai jos si repara functia.
""")
    c.cod("""
%%vezi
n = 3
mat = [[0] * n] * n
for i in range(n):
    mat[i][i] = 1
""")
    c.ex("""
def identitate(n):
    mat = [[0] * n] * n
    for i in range(n):
        mat[i][i] = 1
    return mat
""", """
def identitate(n):
    mat = [[0] * n for _ in range(n)]
    for i in range(n):
        mat[i][i] = 1
    return mat
""")
    c.cod("""
verifica('identitate', identitate, [((3,), [[1, 0, 0], [0, 1, 0], [0, 0, 1]]), ((1,), [[1]])],
         ascunse=[((2,), [[1, 0], [0, 1]]), ((4,), [[1 if i == j else 0 for j in range(4)] for i in range(4)])],
         indiciu='cate liste diferite are mat? Uita-te la etichetele @ din animatie', puncte=1)
""")

    c.md("""
### 9. Repara codul: numerele negative

Functia trebuie sa intoarca lista fara numerele **negative**, in aceeasi ordine, dar sare peste elemente. Repar-o.
""")
    c.ex("""
def fara_negative(v):
    for x in v:
        if x < 0:
            v.remove(x)
    return v
""", """
def fara_negative(v):
    return [x for x in v if x >= 0]
""")
    c.cod("""
verifica('fara_negative', fara_negative,
         [(([1, -2, 3],), [1, 3]), (([-1, -2, -3, 4],), [4]), (([5, 6],), [5, 6])],
         ascunse=[(([-1, -1, -1],), []), (([],), []), (([0, -1, 0, -2, 2],), [0, 0, 2])],
         indiciu='nu modifica lista in timp ce o parcurgi', puncte=1)
""")

    c.md("""
### 10. Program: peste medie

Pe prima linie `n`, pe a doua cele `n` numere intregi. Afiseaza **cate** dintre ele sunt strict mai mari decat media aritmetica a tuturor. De exemplu, pentru `1 2 3 4 5` media e 3, deci raspunsul e `2`.
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    n = int(input())
    v = list(map(int, input().split()))
    medie = sum(v) / n
    print(sum(1 for x in v if x > medie))
""")
    c.cod("""
verifica_program('peste medie', main,
                 [(['5', '1 2 3 4 5'], '2'), (['3', '2 2 2'], '0'), (['4', '-1 -2 -3 10'], '1')],
                 ascunse=[(['1', '7'], '0'), (['2', '1 2'], '1'), (['6', '10 20 30 40 50 60'], '3')], puncte=2)
""")

    c.md("""
### 11. Program: sume pe coloane

Pe prima linie `n` si `m`, apoi `n` linii cu cate `m` numere. Afiseaza, pe o singura linie, suma fiecarei coloane, separate prin spatiu.
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    n, m = map(int, input().split())
    mat = [list(map(int, input().split())) for _ in range(n)]
    print(*[sum(col) for col in zip(*mat)])
""")
    c.cod("""
verifica_program('sume pe coloane', main,
                 [(['2 3', '1 2 3', '4 5 6'], '5 7 9'), (['1 1', '7'], '7')],
                 ascunse=[(['3 2', '1 -1', '2 -2', '3 -3'], '6 -6'), (['1 4', '1 2 3 4'], '1 2 3 4'), (['3 1', '5', '6', '7'], '18')],
                 puncte=2)
""")

    c.md("""
### 12. Provocare: matricea spirala

Construieste matricea `n x n` in care numerele `1, 2, ..., n * n` sunt scrise **in spirala**, pornind din stanga-sus spre dreapta, in sensul acelor de ceasornic. Pentru `n = 3`:

```
1 2 3
8 9 4
7 6 5
```

Ai vazut la predare cum se genereaza ordinea celulelor. Acum trebuie sa scrii un numar in fiecare celula pe masura ce o vizitezi.
""")
    c.ex("""
def matrice_spirala(n):
    pass  # TODO
""", """
def matrice_spirala(n):
    mat = [[0] * n for _ in range(n)]
    sus, jos, st, dr = 0, n - 1, 0, n - 1
    k = 1
    while sus <= jos and st <= dr:
        for j in range(st, dr + 1):
            mat[sus][j] = k
            k += 1
        for i in range(sus + 1, jos + 1):
            mat[i][dr] = k
            k += 1
        if sus < jos:
            for j in range(dr - 1, st - 1, -1):
                mat[jos][j] = k
                k += 1
        if st < dr:
            for i in range(jos - 1, sus, -1):
                mat[i][st] = k
                k += 1
        sus, jos, st, dr = sus + 1, jos - 1, st + 1, dr - 1
    return mat
""")
    c.cod(f"""
verifica('matrice_spirala', matrice_spirala,
         [((1,), [[1]]), ((2,), [[1, 2], [4, 3]]), ((3,), [[1, 2, 3], [8, 9, 4], [7, 6, 5]])],
         ascunse=[((4,), {_spirala(4)!r}), ((5,), {_spirala(5)!r}), ((6,), {_spirala(6)!r}), ((7,), {_spirala(7)!r})],
         puncte=3)
scor()
""")
    c.salveaza('04-liste-tablouri-tema')


if __name__ == '__main__':
    predare()
    tema()
