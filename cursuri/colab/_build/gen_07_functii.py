"""Genereaza 07-functii-predare.ipynb si 07-functii-tema.ipynb (+ variantele cu solutii)."""
from nb import Carnet


def predare():
    c = Carnet('Functii si recursivitate', 'predare', fisiere=('anim_recursie.py',))

    c.md("""
## Ce e o functie

Ai folosit deja functii: `len`, `print`, `sorted`. Acum le scrii tu. O functie e o bucata de cod careia ii dai un nume, ca s-o poti chema de cate ori vrei, cu date diferite.

De ce merita: nu repeti cod, dai un nume unei idei (`este_prim(n)` se citeste mai usor decat 6 linii de bucla) si o poti **testa separat**. `verifica`, cu care lucrezi din primul notebook, e si ea o functie, iar prima ei intrare e o alta functie.

**Cum lucram.** In `%%vezi` vei vedea ceva nou: **stiva de apeluri**. Fiecare apel de functie primeste un cadru propriu, cu variabilele lui (galben = cadrul activ). Cand functia se termina, cadrul dispare.

## 1. `def`, `return`, valori intoarse

`def` doar **defineste** functia, nu o ruleaza. Se ruleaza cand o chemi. `return` scoate o valoare afara si opreste functia. Daca nu ai `return`, functia intoarce `None`.

**Prezice:** cat e `r` dupa `r = saluta('ana')`?

<details><summary>Raspuns</summary>

`None`. `print` doar **scrie** pe ecran, nu intoarce nimic. Confuzia `print` vs `return` e cea mai frecventa greseala de inceput: cu `print` vezi rezultatul, cu `return` il poti folosi mai departe.
</details>
""")
    c.cod("""
%%vezi
def dubleaza(x):                #: def doar defineste functia, nu o ruleaza
    return x * 2                #: return: valoarea care iese din functie

def saluta(nume):
    print('salut', nume)        #: fara return, functia intoarce None

def min_max(v):
    return min(v), max(v)       #: mai multe valori: un tuplu

a = dubleaza(5)                 #: apare un cadru nou, cu x = 5
r = saluta('ana')               #: r primeste None, nu textul afisat
m, M = min_max([4, 9, 1])       #: tuplul se despacheteaza in doua variabile
""")

    c.md("""
## 2. Parametri

- **pozitionali**: `putere(2, 10)`, conteaza ordinea.
- **cu valoare implicita**: `def putere(baza, exp=2)`, poti sa nu-l dai pe `exp`.
- **cu nume**: `putere(exp=3, baza=2)`, ordinea nu mai conteaza.
- `*args`: aduna oricate argumente pozitionale intr-un **tuplu**.
- `**kwargs`: aduna argumentele cu nume intr-un **dictionar**.

Uita-te in cadrul lui `descrie` cum arata `note` si `extra`.
""")
    c.cod("""
%%vezi
def putere(baza, exp=2):            #: exp are valoare implicita
    return baza ** exp

def descrie(nume, *note, **extra):  #: *note -> tuplu, **extra -> dictionar
    return len(note)

a = putere(5)                       #: exp lipseste: ia 2
b = putere(2, 10)                   #: pozitional
c = putere(exp=3, baza=2)           #: cu nume
d = descrie('ana', 9, 10, clasa=10, an=2025)
""")

    c.md("""
## 3. Domeniul variabilelor (scope)

Variabilele create **in** functie sunt locale: exista doar cat dureaza apelul. Daca functia are o variabila cu acelasi nume ca una globala, o **acopera** (o umbreste), dar nu o schimba.

**Prezice:** ce afiseaza acest cod?
```python
x = 10
def f():
    x = 5
f()
print(x)
```

<details><summary>Raspuns</summary>

`10`. In `f`, `x = 5` face un `x` nou, local. Cel global ramane neatins. Ca sa schimbi chiar variabila globala scrii `global x` in functie, dar rar merita: e mai curat sa **intorci** valoarea cu `return`.
</details>
""")
    c.cod("""
%%vezi
x = 10
def schimba():
    x = 5                   #: un x nou, LOCAL, in cadrul functiei
    return x
def mareste():
    global x                #: aici spui ca x e cel global
    x = x + 1
y = schimba()               #: global x ramane 10
mareste()                   #: acum chiar se schimba
""")

    c.md("""
## 4. Capcana argumentului implicit mutabil

Valoarea implicita se creeaza **o singura data**, la `def`, nu la fiecare apel. Cu un numar nu conteaza. Cu o **lista**, toate apelurile fara argument impart aceeasi lista.

**Prezice:** cat contine `b` la final?

<details><summary>Raspuns</summary>

`[1, 2]`, si `a` la fel. Uita-te la eticheta `@1`: `a` si `b` sunt aceeasi lista.
</details>

Reteta standard: valoare implicita `None`, iar lista o creezi **in** functie:
```python
def adauga(x, lista=None):
    if lista is None:
        lista = []
    lista.append(x)
    return lista
```
""")
    c.cod("""
%%vezi
def adauga(x, lista=[]):        #: lista=[] se creeaza O SINGURA DATA, cand rulezi def
    lista.append(x)
    return lista
a = adauga(1)
b = adauga(2)                   #: fara al doilea argument: aceeasi lista de data trecuta
""")

    c.md("""
## 5. Functiile sunt valori

O functie e un obiect ca oricare altul: o pui intr-o variabila, o dai ca argument, o intorci. Fara paranteze, `dubleaza` este functia; cu paranteze, `dubleaza(3)` este apelul ei.

**Din topor** - o functie care aplica o alta functie pe fiecare element:
""")
    c.cod("""
%%vezi
def dubleaza(x):
    return x * 2
def aplica(f, lista):             #: f e o functie primita ca argument
    rez = []
    for x in lista:
        rez.append(f(x))          #: apelam ce am primit
    return rez
g = dubleaza                      #: fara paranteze: g e alt nume pentru aceeasi functie
r = aplica(g, [1, 2, 3])
""")
    c.md("""
`map(f, lista)` face exact ce face `aplica`. La fel `sorted(lista, key=f)`: `key` primeste o **functie** si sorteaza dupa ce intoarce ea. Ca sa nu scrii un `def` intreg pentru o functie de o linie, exista **`lambda`**: `lambda x: x * 2` inseamna "functie care ia `x` si intoarce `x * 2`". E permisa o singura expresie, fara `return`. O folosesti aproape numai ca `key`.
""")
    c.cod("""
cuvinte = ['banana', 'kiwi', 'mar']
print(list(map(len, cuvinte)))                      # map: aplica len pe fiecare cuvant
print(sorted(cuvinte, key=len))                     # key primeste o functie
print(sorted(cuvinte, key=lambda w: w[-1]))         # dupa ultima litera
print(max(cuvinte, key=lambda w: w.count('a')))     # cuvantul cu cele mai multe 'a'
dubleaza = lambda x: x * 2                          # la fel ca def dubleaza(x): return x * 2
print(dubleaza(21))
""")

    c.md("""
## 6. Functii care intorc functii (closure)

O functie definita **in interiorul altei functii** isi aminteste variabilele acesteia, chiar dupa ce functia din exterior s-a terminat. Se numeste **closure**. Uita-te in cadrul lui `ridica`: are `x` (parametru) dar si `k`, luat de la fabrica.
""")
    c.cod("""
%%vezi
def fabrica_putere(k):
    def ridica(x):               #: o functie definita IN functie
        return x ** k            #: ridica isi aminteste k
    return ridica                #: intoarcem functia, nu un rezultat
patrat = fabrica_putere(2)       #: patrat e o functie noua, cu k = 2
cub = fabrica_putere(3)
r = patrat(5)
s = cub(2)
""")

    c.md("""
## 7. Functii pure si efecte secundare

O functie **pura** intoarce un rezultat care depinde doar de argumente si nu schimba nimic in afara ei. Sunt usor de testat si de inteles. O functie cu **efecte secundare** modifica ceva din exterior (o lista primita, o variabila globala, ecranul).

Listele se dau prin **referinta**: functia primeste chiar lista ta, nu o copie. Uita-te la `@1`: `v` din functie si `a` din afara sunt aceeasi lista. Asa se explica si capcana clasica `b = a.sort()`: `sort()` sorteaza pe loc si **intoarce `None`**, pe cand `sorted(a)` intoarce o lista noua.
""")
    c.cod("""
%%vezi
def fara_efecte(v):
    return sorted(v)             #: sorted intoarce o lista NOUA
def cu_efecte(v):
    v.sort()                     #: sort() schimba lista primita: se schimba si a din afara
a = [3, 1, 2]
b = fara_efecte(a)               #: a ramane [3, 1, 2]
c = cu_efecte(a)                 #: a devine [1, 2, 3]; functia nu intoarce nimic
x = a.sort()                     #: aceeasi capcana: sort() intoarce None
""")

    c.md("""
## 8. Cum testezi o functie

Dupa ce scrii o functie, o chemi cu cateva cazuri unde stii raspunsul. `assert conditie` nu face nimic daca `conditie` e adevarata si opreste programul cu `AssertionError` daca e falsa (iar dupa virgula poti pune un mesaj). Asta e ideea din spatele `verifica`.

Alege cazuri **limita**: `0`, lista goala, un singur element, valori egale. Acolo se ascund gresealile. Functia de mai jos are un bug: uita-te ce prinde `assert`-ul.
""")
    c.cod("""
%%vezi
def maxim(a, b):
    if a > b:
        return a
    return a                     #: bug: ar fi trebuit return b

assert maxim(5, 3) == 5          #: trece, chiar daca functia e gresita
assert maxim(2, 9) == 9, 'maxim(2, 9) trebuia sa dea 9'      #: cazul care o prinde
""")
    c.cod("""
# verifica de mana: verifica_mini primeste o FUNCTIE si o lista de cazuri; f(*args) desface tuplul in argumente.
# Docstring-ul (textul cu ghilimele triple, sub def) explica functia; '-> float' si 'r: float' sunt indicii
# de tip: Python nu le impune, dar ajuta cititorul si editorul.
import math

def aria_cerc(r: float) -> float:
    '''Aria unui cerc de raza r.'''
    return math.pi * r * r

def verifica_mini(f, teste):
    gresite = 0
    for args, asteptat in teste:
        obtinut = f(*args)
        if abs(obtinut - asteptat) > 1e-9:
            print('GRESIT:', f.__name__, args, 'am obtinut', obtinut, 'trebuia', asteptat)
            gresite += 1
    print(f'{len(teste) - gresite}/{len(teste)} teste trecute')

verifica_mini(aria_cerc, [((0,), 0), ((1,), math.pi), ((2,), 4 * math.pi), ((1,), 3.14)])
print(aria_cerc.__doc__)
""")

    c.md("""
## 9. Recursivitatea

O functie **recursiva** se apeleaza pe ea insasi, pe o problema mai mica. Ai nevoie de doua lucruri:

1. **cazul de baza**: problema atat de mica incat o rezolvi direct (aici se opreste);
2. **pasul**: rezolvi o versiune mai mica si combini rezultatul.

Fiecare apel are cadrul lui pe **stiva**. Cadrele se aduna pana la cazul de baza, apoi se intorc pe rand, fiecare cu rezultatul lui.

**Prezice:** cate cadre ale lui `factorial` sunt pe stiva in cel mai adanc moment al lui `factorial(3)`?

<details><summary>Raspuns</summary>

4: `factorial(3)`, `(2)`, `(1)` si `(0)`, cazul de baza. Numara-le in animatie, la pasul in care apare `return 1`.
</details>
""")
    c.cod("""
%%vezi
def factorial(n):
    if n == 0:                       #: cazul de baza: aici se opreste
        return 1
    return n * factorial(n - 1)      #: pasul: aceeasi problema, mai mica
def suma_cifre(n):                   #: acelasi tipar: ultima cifra + suma cifrelor restului
    if n < 10:                            #: o singura cifra: nu mai e nimic de despartit
        return n
    return n % 10 + suma_cifre(n // 10)   #: n % 10 = ultima cifra, n // 10 = ce ramane
r = factorial(3)
s = suma_cifre(472)
""")

    c.md("""
### Cand recursivitatea nu se opreste

Fara caz de baza, apelurile se aduna la nesfarsit. Python opreste programul dupa ~1000 de cadre cu **`RecursionError`**, ca sa nu-ti umple memoria. Mai jos, animatia e taiata dupa 30 de pasi (`vezi(cod, max_pasi=30)`): vezi doar cum creste stiva.
""")
    c.cod("""
cod = '''
def infinit(n):
    return infinit(n + 1)      #: nicio conditie de oprire
r = infinit(1)
'''
vezi(cod, max_pasi=30)

# si acum pe bune, fara animatie
import sys

def infinit(n):
    return infinit(n + 1)

try:
    infinit(1)
except RecursionError as e:
    print('RecursionError:', e)
print('limita:', sys.getrecursionlimit())

def suma_pana(n):
    return 0 if n == 0 else n + suma_pana(n - 1)

print(suma_pana(900))                 # merge
try:
    suma_pana(5000)
except RecursionError:
    print('5000 e prea adanc')
sys.setrecursionlimit(10000)          # se poate mari limita...
print(suma_pana(5000))
sys.setrecursionlimit(1000)           # (o punem la loc)
""")
    c.md("""
Deci poti mari limita cu `sys.setrecursionlimit`, dar fiecare cadru consuma memorie si o limita prea mare poate strica interpretorul. Regula practica: daca adancimea e de ordinul a mii, scrie o **bucla**. Recursivitatea e pentru lucruri care se **injumatatesc** (adancime ~ log n) sau au forma de arbore.

### Puterea rapida

`a ** n` cu `n` inmultiri e `O(n)`. Dar `a^10 = (a^5)^2`, iar `a^5 = a * a^4`, si asa mai departe: `n` se injumatateste la fiecare pas, deci ~`log2(n)` apeluri. Atentie sa faci **un singur** apel pe jumatate (`h * h`), nu doua (`f(n//2) * f(n//2)`): doua apeluri ar readuce `O(n)`.
""")
    c.cod("""
%%vezi
def putere(a, n):
    if n == 0:                        #: baza: a^0 = 1
        return 1
    if n % 2 == 0:
        h = putere(a, n // 2)         #: a^n = (a^(n/2))^2: UN singur apel
        return h * h
    return a * putere(a, n - 1)       #: n impar: scoatem un factor
r = putere(2, 10)                     #: doar 6 cadre pentru n = 10
""")
    c.cod("""
def putere_lenta(a, n):
    r = 1
    for _ in range(n):
        r *= a
    return r

apeluri = 0
def putere(a, n):
    global apeluri
    apeluri += 1
    if n == 0:
        return 1
    if n % 2 == 0:
        h = putere(a, n // 2)
        return h * h
    return a * putere(a, n - 1)

print(putere_lenta(3, 1000) == putere(3, 1000))
apeluri = 0
putere(3, 10**6)
print('apeluri pentru n = 1 000 000:', apeluri, '(in loc de 1 000 000 de inmultiri)')
print(pow(3, 10**18, 10**9 + 7))      # pow cu 3 argumente: putere modulara, tot O(log n)
""")

    c.md("""
### Cautarea binara

Lista e **sortata**. Te uiti la mijloc: daca e numarul cautat, ai terminat; daca elementul din mijloc e mai mic, cauti doar in dreapta, altfel doar in stanga. Jumatate din elemente dispar la fiecare pas: `O(log n)`. Din 1 000 000 de elemente ajungi la raspuns in ~20 de pasi.

Observa `@1` in cadre: lista `v` e aceeasi peste tot. Nu o taiem in bucati (`v[mij+1:]` ar copia, adica `O(n)` la fiecare pas), ci ne pasam doar **indicii** `st` si `dr`.
""")
    c.cod("""
%%vezi
def cauta(v, x, st, dr):
    if st > dr:                           #: interval gol: nu exista
        return -1
    mij = (st + dr) // 2
    if v[mij] == x:
        return mij
    if v[mij] < x:
        return cauta(v, x, mij + 1, dr)   #: cautam in dreapta
    return cauta(v, x, st, mij - 1)       #: cautam in stanga
v = [2, 5, 8, 12, 16, 23, 38, 56]
r = cauta(v, 23, 0, len(v) - 1)
""")

    c.md("""
### Turnurile din Hanoi

Muti `n` discuri de pe tija `A` pe `C`, unul cate unul, fara sa pui un disc mare peste unul mic. Recursiv e o idee de o linie: muti `n-1` discuri pe tija ajutatoare, muti discul cel mare, muti cele `n-1` peste el. Pentru `n` discuri sunt `2^n - 1` mutari, deci nici o functie nu o scoate mai repede: aici recursivitatea nu e o scurtatura, e doar cel mai clar mod de a scrie problema.
""")
    c.cod("""
%%vezi
def hanoi(n, sursa, tinta, aux):
    if n == 1:
        print('disc 1:', sursa, '->', tinta)
        return
    hanoi(n - 1, sursa, aux, tinta)                     #: n-1 discuri pe tija ajutatoare
    print('disc', n, ':', sursa, '->', tinta)           #: discul cel mare merge direct
    hanoi(n - 1, aux, tinta, sursa)                     #: apoi cele n-1 peste el
hanoi(3, 'A', 'C', 'B')
""")

    c.md("""
## 10. Fibonacci: cand recursivitatea costa scump

`fib(0) = 0`, `fib(1) = 1`, iar `fib(n) = fib(n-1) + fib(n-2)`. Se scrie in doua linii:

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

Problema e ca `fib(n-1)` si `fib(n-2)` isi refac unul altuia calculele. Ca sa vezi cat de tare, **numara apelurile** tu. Trebuie sa cresti un contor global la fiecare intrare in functie, apoi sa compari cu animatia de dupa.

**Prezice:** cate apeluri face `fib(6)`? (Mai putine de 10, intre 10 si 30, sau peste 30?)

<details><summary>Raspuns</summary>

25. Pentru `fib(10)`, 177. Vezi mai jos cum explodeaza.
</details>
""")
    c.md("""
**Exercitiul (fib cu contor).** Completeaza `fib` de mai jos: la fiecare apel creste `apeluri` cu 1 (de aceea ai `global apeluri`), apoi calculeaza `fib(n)` recursiv.
""")
    c.ex("""
apeluri = 0

def fib(n):
    global apeluri
    pass  # TODO: apeluri += 1, apoi cazul de baza si pasul recursiv
""", """
apeluri = 0

def fib(n):
    global apeluri
    apeluri += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
""")
    c.cod("""
apeluri = 0
r = fib(6)
verifica_egal('fib(6) si contorul', (r, apeluri), (8, 25))
apeluri = 0
fib(10)
verifica_egal('fib(10): numarul de apeluri', apeluri, 177, indiciu='numara si cazurile de baza: fiecare intrare in functie e un apel')
""")
    c.md("""
Acum ii dai animatiei numarul **tau**. Ea deseneaza arborele apelurilor, apel cu apel: verde = apel nou, rosu = apel repetat (aceeasi valoare a fost calculata deja), iar la final compara cu numarul tau.
""")
    c.cod("""
apeluri = 0
fib(6)
anim_arbore_fib(6, apeluri)
""")
    c.cod("""
# Cate apeluri se strang pana la n = 27? Numaram cu o functie proprie, ca sa nu depinzi de a ta.
# Fiecare n in plus inseamna de ~1.6 ori mai mult: O(2^n). Cu n = 50 ar dura ani.
import time

def fib_naiv(n, contor):
    contor[0] += 1
    if n < 2:
        return n
    return fib_naiv(n - 1, contor) + fib_naiv(n - 2, contor)

for n in [10, 15, 20, 25, 27]:
    contor = [0]
    t0 = time.perf_counter()
    fib_naiv(n, contor)
    print(f'fib({n}): {contor[0]:>8} apeluri, {time.perf_counter() - t0:.3f} s')
""")
    c.md("""
**Memoizare, din topor.** Tinem un dictionar `n -> fib(n)`. Inainte sa calculam, ne uitam in el. Fiecare valoare se calculeaza **o singura data**: `O(n)` in loc de `O(2^n)`. Uita-te cum se umple `memo` in animatie.
""")
    c.cod("""
%%vezi
memo = {}
def fib(n):
    if n in memo:                   #: l-am mai calculat? il luam din dictionar
        return memo[n]
    if n < 2:
        r = n
    else:
        r = fib(n - 1) + fib(n - 2)
    memo[n] = r                     #: il tinem minte pentru data viitoare
    return r
x = fib(5)
""")
    c.cod("""
anim_memo_fib(7)
""")
    c.md("""
Scris o data, il poti aplica oricarei functii. Iata **decoratorul** de mana: `memoizeaza` primeste o functie si intoarce alta, care tine minte rezultatele (o functie care intoarce o functie, cu un closure peste `memo`). In biblioteca standard, `functools.cache` e exact asta, doar mai rapid.

Atentie: `fib(3000)` recursiv cade oricum in `RecursionError` (adancime 3000). Pentru `n` mare, treci pe bucla: `a, b = b, a + b`.
""")
    c.cod("""
from functools import cache

def memoizeaza(f):
    memo = {}
    def invelita(n):
        if n not in memo:
            memo[n] = f(n)
        return memo[n]
    return invelita

def fib_lent(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)      # cheama 'fib', care va fi versiunea invelita

fib = memoizeaza(fib_lent)
print(fib(300))

@cache                                                   # @cache = fib_c = cache(fib_c)
def fib_c(n):
    return n if n < 2 else fib_c(n - 1) + fib_c(n - 2)

print(fib_c(300) == fib(300), fib_c.cache_info())
""")

    c.md("""
## 11. Unde apare in ML

- **`fit` si `predict` sunt functii** (metode) cu parametri: `fit(X, y)` primeste datele si isi ajusteaza parametrii, `predict(X)` foloseste ce a invatat. Un model antrenat e practic o functie `x -> y_hat` cu parametri (`w`, `b`) fixati. Iar functia de mai jos, care **intoarce o functie**, e chiar asta.
- O **functie de pierdere** (loss) e o functie `(y, y_hat) -> un numar`: cat de gresit e modelul. Antrenarea cauta parametrii care o fac mica, iar tu o poti da ca argument, ca pe orice functie. Cele doua clasice sunt `mse` (media patratelor erorilor) si `mae` (media valorilor absolute). Le scrii la exercitii.
- `key=lambda ...` din `sorted`, `max`, `min` e acelasi tipar: dai o functie ca argument.
""")
    c.cod("""
from sklearn.linear_model import LinearRegression

def model_liniar(w, b):
    return lambda x: w * x + b            # o functie care intoarce o functie: "modelul"

X, y = [[1], [2], [3]], [3, 5, 7]         # y = 2 * x + 1
m = LinearRegression().fit(X, y)          # fit: functie cu parametri (datele)
print(m.coef_, m.intercept_)              # ce a invatat: w = 2, b = 1
print(m.predict([[4]]))                   # predict: alta functie, foloseste ce a invatat
model = model_liniar(2, 1)                # aceeasi idee, scrisa de mana
print(model(4))
""")

    c.md("""
## 12. Capcane

Le-ai vazut pe cele mai mari: **argumentul implicit mutabil** (sectiunea 4), **`list.sort()` intoarce `None`** (sectiunea 7), **recursivitate fara caz de baza** (sectiunea 9). Mai sunt doua (a doua e in celula de dupa cea cu animatie).

**Capcana: modifici o variabila globala fara `global`.** Python vede `x += 1` ca pe o atribuire, deci decide ca `x` e local, iar la citire nu are ce sa citeasca:
""")
    c.cod("""
%%vezi
contor = 0
def creste():
    contor += 1              #: contor e considerat local, dar nu are inca nicio valoare
creste()
""")
    c.cod("""
# Capcana: lambda-urile dintr-o bucla isi amintesc VARIABILA i, nu valoarea ei din acel moment,
# iar cand le chemi, bucla s-a terminat de mult. Remediu: valoarea de acum devine argument implicit.
fs = [lambda x: x * i for i in range(3)]
print([f(10) for f in fs])                 # ai vrea [0, 10, 20]

fs = [lambda x, i=i: x * i for i in range(3)]   # i=i: valoarea de acum, prinsa in parametru
print([f(10) for f in fs])
""")

    c.md("""
### Cum citesti eroarea

Ultima linie iti spune ce s-a intamplat, iar linia rosie din animatie unde.

| eroare | de obicei inseamna |
|---|---|
| `TypeError: f() missing 1 required positional argument: 'y'` | ai chemat functia cu prea putine argumente |
| `TypeError: f() takes 2 positional arguments but 3 were given` | prea multe |
| `TypeError: 'NoneType' object is not subscriptable` (sau `... has no attribute ...`) | ai uitat `return`: functia a intors `None`, iar tu il folosesti ca pe o lista |
| `UnboundLocalError: local variable 'x' referenced before assignment` | ai atribuit lui `x` in functie, deci e local, dar l-ai citit inainte |
| `RecursionError: maximum recursion depth exceeded` | lipseste cazul de baza, sau pasul nu se apropie de el |
| `NameError: name 'x' is not defined` | ai folosit in afara functiei o variabila care e locala functiei |

Cea mai frecventa cauza, un `return` uitat:
""")
    c.cod("""
%%vezi
def prima_litera(w):
    w[0]                     #: am calculat, dar am uitat return

p = prima_litera('kiwi')     #: p e None
u = p[0]                     #: None nu se poate indexa
""")

    c.md("""
## Exercitii

Fiecare exercitiu are o celula de completat si una de verificare. Unele functii au si **teste ascunse** pe date mari: solutia trebuie sa fie rapida, nu doar corecta.
""")

    c.md("""
**Exercitiul 1.** `este_prim(n)`: `True` daca `n` e prim, altfel `False` (`0` si `1` nu sunt prime). Functie pura: nu afisezi nimic, doar intorci. Ajunge sa verifici divizorii pana la radacina patrata a lui `n`.
""")
    c.ex("""
def este_prim(n):
    pass  # TODO
""", """
def este_prim(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True
""")
    c.cod("""
import random

verifica('este_prim', este_prim,
         [((2,), True), ((1,), False), ((0,), False), ((97,), True), ((100,), False)],
         ascunse=[((7919,), True), ((1000003,), True), ((1000001,), False), ((49,), False)],
         referinta=lambda n: n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1)),
         generator=lambda: (random.randint(0, 2000),),
         indiciu='intorci False la n < 2; apoi cauti un divizor d cu d * d <= n', puncte=1)
""")

    c.md("""
**Exercitiul 2.** `cmmdc(a, b)`: cel mai mare divizor comun, cu **algoritmul lui Euclid**: `cmmdc(a, b) = cmmdc(b, a % b)`, iar cand `b` ajunge `0`, raspunsul e `a`. Recursiv sau cu bucla, cum vrei.
""")
    c.ex("""
def cmmdc(a, b):
    pass  # TODO
""", """
def cmmdc(a, b):
    if b == 0:
        return a
    return cmmdc(b, a % b)
""")
    c.cod("""
import math

verifica('cmmdc', cmmdc, [((12, 18), 6), ((7, 0), 7), ((0, 5), 5), ((17, 5), 1)],
         ascunse=[((10**9, 10**6), 10**6), ((48, 36), 12)],
         referinta=math.gcd, generator=lambda: (random.randint(0, 10**6), random.randint(0, 10**6)),
         indiciu='baza: b == 0 -> intorci a; pasul: cmmdc(b, a % b)', puncte=1)
""")

    c.md("""
**Exercitiul 3.** Doua functii scurte, pentru parametri. `suma_toate(*numere)` aduna oricate numere primite (fara sa folosesti `sum`), iar `putere(baza, exp=2)` ridica la putere, cu `2` implicit.
""")
    c.ex("""
def suma_toate(*numere):
    pass  # TODO


def putere(baza, exp=2):
    pass  # TODO
""", """
def suma_toate(*numere):
    total = 0
    for x in numere:
        total += x
    return total


def putere(baza, exp=2):
    return baza ** exp
""")
    c.cod("""
verifica('suma_toate', suma_toate, [((1, 2, 3), 6), ((5,), 5), ((), 0)], ascunse=[((1.5, 2.5), 4), ((-1, 1, -1), -1)])
verifica('putere', putere, [((5,), 25), ((2, 10), 1024), ((3, 0), 1)], ascunse=[((10, 3), 1000), ((0,), 0)])
""")

    c.md("""
**Exercitiul 4** e cel cu `fib` si contorul, din sectiunea 10.
""")

    c.md("""
**Exercitiul 5.** `putere_mod(a, n, m)`: `a` la puterea `n`, **modulo `m`** (`m >= 2`), recursiv si rapid: injumatatesti `n` la fiecare pas. Testele ascunse au `n` de ordinul `10^18`, unde nici bucla, nici recursivitatea pe `n - 1` nu ajung. Nu folosi `pow` cu trei argumente. Fa `% m` la fiecare inmultire.
""")
    c.ex("""
def putere_mod(a, n, m):
    pass  # TODO
""", """
def putere_mod(a, n, m):
    if n == 0:
        return 1 % m
    if n % 2 == 0:
        h = putere_mod(a, n // 2, m)
        return h * h % m
    return a * putere_mod(a, n - 1, m) % m
""")
    c.cod("""
verifica('putere_mod', putere_mod, [((2, 10, 1000), 24), ((3, 0, 7), 1), ((5, 3, 13), 8)],
         ascunse=[((2, 10**18, 10**9 + 7), pow(2, 10**18, 10**9 + 7)), ((7, 10**17 + 3, 998244353), pow(7, 10**17 + 3, 998244353))],
         referinta=pow, generator=lambda: (random.randint(0, 10**6), random.randint(0, 10**12), random.randint(2, 10**9)),
         indiciu='n par: h = putere_mod(a, n // 2, m), rezultat h * h % m; n impar: a * putere_mod(a, n - 1, m) % m', puncte=2)
""")

    c.md("""
**Exercitiul 6.** `cauta_binar(v, x, st=0, dr=None)`: cautare binara **recursiva** in lista sortata `v` (elemente distincte). Intoarce pozitia lui `x`, sau `-1` daca nu e in lista. Daca `dr` e `None`, il inlocuiesti cu `len(v) - 1`. Nu taia lista (`v[a:b]`), ci pasa indicii.
""")
    c.ex("""
def cauta_binar(v, x, st=0, dr=None):
    pass  # TODO
""", """
def cauta_binar(v, x, st=0, dr=None):
    if dr is None:
        dr = len(v) - 1
    if st > dr:
        return -1
    mij = (st + dr) // 2
    if v[mij] == x:
        return mij
    if v[mij] < x:
        return cauta_binar(v, x, mij + 1, dr)
    return cauta_binar(v, x, st, mij - 1)
""")
    c.cod("""
mare = list(range(0, 2 * 10**6, 2))          # un milion de elemente: adancimea recursiei trebuie sa fie ~20
verifica('cauta_binar', cauta_binar,
         [(([1, 3, 5, 7], 5), 2), (([1, 3, 5, 7], 4), -1), (([], 1), -1), (([9], 9), 0)],
         ascunse=[((mare, 1999998), 999999), ((mare, 7), -1), ((mare, 0), 0)],
         referinta=lambda v, x: v.index(x) if x in v else -1,
         generator=lambda: (sorted(random.sample(range(60), random.randint(0, 20))), random.randint(0, 60)),
         indiciu='baza: st > dr -> -1; compara cu v[mij] si cauta doar in jumatatea potrivita', puncte=2)
""")

    c.md("""
**Exercitiul 7.** O functie care **intoarce o functie**. `fabrica_putere(k)` intoarce o functie care ridica orice numar la puterea `k` (ca in sectiunea 6, dar o scrii tu).
""")
    c.ex("""
def fabrica_putere(k):
    pass  # TODO
""", """
def fabrica_putere(k):
    def ridica(x):
        return x ** k
    return ridica
""")
    c.cod("""
def aplica_fabrica(k, x):
    return fabrica_putere(k)(x)

verifica('fabrica_putere', aplica_fabrica, [((2, 5), 25), ((3, 2), 8), ((0, 9), 1), ((1, -4), -4)],
         ascunse=[((2, -3), 9), ((10, 2), 1024)],
         indiciu='defineste o functie in functie si intoarce-o (fara paranteze)')
""")

    c.md("""
**Exercitiul 8.** Doua functii de pierdere, de mana: `mse(y, y_hat)` (media patratelor diferentelor) si `mae(y, y_hat)` (media valorilor absolute ale diferentelor). `y` si `y_hat` sunt liste de aceeasi lungime, nevide. Verificarea le compara cu NumPy, adica cu ce ai folosi in practica.
""")
    c.ex("""
def mse(y, y_hat):
    pass  # TODO


def mae(y, y_hat):
    pass  # TODO
""", """
def mse(y, y_hat):
    total = 0
    for a, b in zip(y, y_hat):
        total += (a - b) ** 2
    return total / len(y)


def mae(y, y_hat):
    total = 0
    for a, b in zip(y, y_hat):
        total += abs(a - b)
    return total / len(y)
""")
    c.cod("""
import numpy as np

y = [3, 5, 8, 10]
y_hat = [2.5, 5, 9, 7]
verifica_egal('mse vs numpy', mse(y, y_hat), np.mean((np.array(y) - np.array(y_hat)) ** 2))
verifica_egal('mae vs numpy', mae(y, y_hat), np.mean(np.abs(np.array(y) - np.array(y_hat))))

def liste():
    n = random.randint(1, 10)
    return [random.uniform(-5, 5) for _ in range(n)], [random.uniform(-5, 5) for _ in range(n)]

verifica('mse', mse, [(([1, 2], [1, 2]), 0), (([0, 0], [3, 4]), 12.5)],
         referinta=lambda a, b: float(np.mean((np.array(a) - np.array(b)) ** 2)), generator=liste)
verifica('mae', mae, [(([1, 2], [1, 2]), 0), (([0, 0], [3, -4]), 3.5)],
         referinta=lambda a, b: float(np.mean(np.abs(np.array(a) - np.array(b)))), generator=liste)
scor()
""")

    c.md("""
## Recapitulare

- `def nume(parametri): ... return valoare`. Fara `return` = `None`. `print` nu e `return`.
- Parametri: pozitionali, cu valoare implicita, cu nume, `*args` (tuplu), `**kwargs` (dictionar). Mai multe valori intoarse = un tuplu.
- Variabilele create in functie sunt locale. Argumentul implicit se creeaza o singura data: nu pune liste/dictionare, pune `None`.
- Functiile sunt valori: le dai ca argument (`key=`, `map`), le intorci (closure, `fabrica_putere`), scrii `lambda` pentru cele de o linie.
- Functie pura = doar `return`, fara sa modifici nimic in afara. `list.sort()` modifica pe loc si intoarce `None`.
- Testezi cu `assert` si cu cazuri limita (asta e `verifica`).
- Recursivitate: caz de baza + pas mai mic; fiecare apel = un cadru pe stiva; limita ~1000. Se injumatateste (`putere_mod`, cautarea binara): `O(log n)`. Se ramifica peste aceleasi subprobleme (fib): memoizare, adica un dictionar sau `functools.cache`.
- ML: `fit`/`predict` sunt functii; o functie de pierdere (`mse`, `mae`) e o functie pe care o pasezi.

Tema: functii pure, recursivitate, o functie care intoarce o functie si o provocare in care memoizarea decide daca treci sau nu.
""")
    c.salveaza('07-functii-predare')


def tema():
    c = Carnet('Functii si recursivitate', 'tema')
    c.md("""
Exercitii de acasa. Testele vizibile iti arata daca ai inteles enuntul, cele **ascunse** verifica si cazurile limita si datele mari. La final, `scor()` aduna tot.
""")

    c.md("""
### 1. Ultimele k cifre

`ultimele_cifre(n, k=1)` intoarce numarul format din ultimele `k` cifre ale lui `n` (implicit, ultima cifra). De ex. `ultimele_cifre(1234, 2) = 34`, `ultimele_cifre(1234) = 4`, `ultimele_cifre(1005, 2) = 5`.
""")
    c.ex("""
def ultimele_cifre(n, k=1):
    pass  # TODO
""", """
def ultimele_cifre(n, k=1):
    return n % 10 ** k
""")
    c.cod("""
verifica('ultimele_cifre', ultimele_cifre, [((1234, 2), 34), ((1234,), 4), ((1005, 2), 5)],
         ascunse=[((5, 3), 5), ((1000, 2), 0), ((987654321, 4), 4321), ((0,), 0)], puncte=1)
""")

    c.md("""
### 2. Maximul, fara `max`

`maximul(*numere)` intoarce cel mai mare dintre numerele primite (oricate). Fara argumente, intoarce `None`. Nu folosi `max`.
""")
    c.ex("""
def maximul(*numere):
    pass  # TODO
""", """
def maximul(*numere):
    if not numere:
        return None
    m = numere[0]
    for x in numere:
        if x > m:
            m = x
    return m
""")
    c.cod("""
verifica('maximul', maximul, [((3, 9, 2), 9), ((5,), 5), ((), None)],
         ascunse=[((-5, -2, -9), -2), ((1.5, 1.4), 1.5), ((7, 7, 7), 7)],
         indiciu='numere e un tuplu: verifica daca e gol, apoi parcurge-l', puncte=1)
""")

    c.md("""
### 3. Suma cifrelor, recursiv

`suma_cifre(n)` pentru `n >= 0`, **recursiv**: fara bucle, fara `str`, fara `sum`. Baza: un numar cu o singura cifra.
""")
    c.ex("""
def suma_cifre(n):
    pass  # TODO
""", """
def suma_cifre(n):
    if n < 10:
        return n
    return n % 10 + suma_cifre(n // 10)
""")
    c.cod("""
import random

verifica('suma_cifre', suma_cifre, [((472,), 13), ((0,), 0), ((9,), 9), ((1000,), 1)],
         ascunse=[((999999,), 54), ((10**15 + 7,), 8)],
         referinta=lambda n: sum(map(int, str(n))), generator=lambda: (random.randint(0, 10**9),),
         indiciu='baza: n < 10 -> n; pasul: ultima cifra + suma_cifre(n // 10)', puncte=1)
""")

    c.md("""
### 4. Scrierea in baza 2, recursiv

`in_binar(n)` intoarce **textul** cu scrierea in baza 2 a lui `n >= 0`: `in_binar(5) = '101'`, `in_binar(0) = '0'`. Recursiv, fara `bin` si fara `format`. Ai nevoie de `n // 2` si `n % 2`; cifrele apar de la sfarsit spre inceput, deci rezultatul recursiv merge **in fata** ultimei cifre.
""")
    c.ex("""
def in_binar(n):
    pass  # TODO
""", """
def in_binar(n):
    if n < 2:
        return str(n)
    return in_binar(n // 2) + str(n % 2)
""")
    c.cod("""
verifica('in_binar', in_binar, [((5,), '101'), ((0,), '0'), ((1,), '1'), ((8,), '1000')],
         ascunse=[((255,), '11111111'), ((10**18,), bin(10**18)[2:])],
         referinta=lambda n: bin(n)[2:], generator=lambda: (random.randint(0, 10**6),),
         indiciu='baza: n < 2 -> str(n); altfel in_binar(n // 2) + str(n % 2)', puncte=2)
""")

    c.md("""
### 5. Compunerea a doua functii

`compune(f, g)` intoarce **o functie noua** `h` cu `h(x) = f(g(x))`. De ex. `compune(str, abs)(-5)` da `'5'`.
""")
    c.ex("""
def compune(f, g):
    pass  # TODO
""", """
def compune(f, g):
    def h(x):
        return f(g(x))
    return h
""")
    c.cod("""
def aplica_compusa(f, g, x):
    return compune(f, g)(x)

verifica('compune', aplica_compusa,
         [((lambda x: x + 1, lambda x: x * 2, 5), 11), ((str, abs, -5), '5'), ((len, str, 12345), 5)],
         ascunse=[((lambda x: x * 2, lambda x: x + 1, 5), 12), ((abs, abs, -3), 3)],
         indiciu='in interiorul lui compune defineste h(x) si intoarce h', puncte=2)
""")

    c.md("""
### 6. Pierderea medie, cu functia de pierdere ca argument

`pierdere_medie(loss, y, y_hat)` intoarce media valorilor `loss(a, b)` pentru fiecare pereche `(a, b)` din `y` si `y_hat` (liste de aceeasi lungime, nevide). Asa e scris codul de antrenare din bibliotecile de ML: pierderea e un parametru, deci acelasi cod merge cu `mse`, cu `mae` sau cu orice altceva. Verificarea o compara si cu NumPy.
""")
    c.ex("""
def pierdere_medie(loss, y, y_hat):
    pass  # TODO
""", """
def pierdere_medie(loss, y, y_hat):
    total = 0
    for a, b in zip(y, y_hat):
        total += loss(a, b)
    return total / len(y)
""")
    c.cod("""
import numpy as np

sq = lambda a, b: (a - b) ** 2
ab = lambda a, b: abs(a - b)
gresit = lambda a, b: a != b               # pierdere "0-1" (pentru clasificare)

y, y_hat = [3, 5, 8, 10], [2.5, 5, 9, 7]
verifica_egal('pierdere_medie(sq) vs numpy', pierdere_medie(sq, y, y_hat), np.mean((np.array(y) - np.array(y_hat)) ** 2))
verifica('pierdere_medie', pierdere_medie,
         [((sq, [1, 2], [1, 4]), 2), ((ab, [1, 2], [3, 0]), 2), ((gresit, [1, 1, 0, 0], [1, 0, 0, 1]), 0.5)],
         ascunse=[((ab, [5], [5]), 0), ((sq, [0, 0, 0], [1, 1, 1]), 1), ((gresit, ['a', 'b'], ['a', 'b']), 0)],
         indiciu='loss e o functie: o chemi cu loss(a, b) pentru fiecare pereche (zip)', puncte=2)
""")

    c.md("""
### 7. Repara codul

Functia trebuie sa adauge o nota la lista de note primita si sa intoarca lista, iar daca nu primeste nicio lista, sa porneasca una noua. Dar apelurile fara lista se **contamineaza** intre ele. Uita-te la `@1` in animatie, apoi repar-o.
""")
    c.cod("""
%%vezi
def aduna_note(nota, note=[]):
    note.append(nota)
    return note
a = aduna_note(9)
b = aduna_note(7)
""")
    c.ex("""
def aduna_note(nota, note=[]):
    note.append(nota)
    return note
""", """
def aduna_note(nota, note=None):
    if note is None:
        note = []
    note.append(nota)
    return note
""")
    c.cod("""
verifica('aduna_note', aduna_note,
         [((9,), [9]), ((7,), [7]), ((4, [1, 2]), [1, 2, 4])],
         ascunse=[((5,), [5]), ((1, []), [1]), ((3,), [3])],
         indiciu='argumentul implicit se creeaza o singura data: foloseste None si creeaza lista in functie', puncte=1)
""")

    c.md("""
### 8. Program: cmmdc si cmmmc

Pe prima linie este `t`, numarul de cazuri. Urmeaza `t` linii, fiecare cu doua numere naturale nenule `a` si `b`. Pentru fiecare linie afiseaza, pe o linie, `cmmdc(a, b)` si `cmmmc(a, b)`, separate prin spatiu. Sunt legate prin `cmmdc(a, b) * cmmmc(a, b) = a * b`. Scrie o functie `cmmdc` (Euclid) si foloseste-o in `main`.
""")
    c.ex("""
def cmmdc(a, b):
    pass  # TODO


def main():
    pass  # TODO: citeste t, apoi t linii; afiseaza 'cmmdc cmmmc' pe fiecare
""", """
def cmmdc(a, b):
    if b == 0:
        return a
    return cmmdc(b, a % b)


def main():
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        d = cmmdc(a, b)
        print(d, a // d * b)
""")
    c.cod("""
verifica_program('cmmdc si cmmmc', main,
                 [(['2', '12 18', '7 5'], '6 36\\n1 35'), (['1', '4 4'], '4 4')],
                 ascunse=[(['1', '1 1'], '1 1'), (['2', '100 75', '9 6'], '25 300\\n3 18'),
                          (['1', '1000000000 999999999'], '1 999999999000000000')],
                 indiciu='cmmmc = a // cmmdc * b', puncte=2)
""")

    c.md("""
### 9. Functie pura: fara duplicate

`fara_duplicate(lista)` intoarce o lista **noua** cu elementele din `lista`, fiecare o singura data, in ordinea primei aparitii. **Nu modifica** lista primita. Verificarea prinde si asta: pe langa rezultat, controleaza ca lista originala a ramas neschimbata.
""")
    c.ex("""
def fara_duplicate(lista):
    pass  # TODO
""", """
def fara_duplicate(lista):
    vazute = set()
    rez = []
    for x in lista:
        if x not in vazute:
            vazute.add(x)
            rez.append(x)
    return rez
""")
    c.cod("""
def testeaza_pur(lista):
    copie = list(lista)
    rezultat = fara_duplicate(lista)
    return rezultat, lista == copie           # (rezultatul, lista originala a ramas la fel?)

verifica('fara_duplicate', testeaza_pur,
         [(([1, 2, 1, 3, 2],), ([1, 2, 3], True)), (([],), ([], True)), ((['a', 'a'],), (['a'], True))],
         ascunse=[(([3, 3, 3, 1],), ([3, 1], True)), (([5, 4, 3],), ([5, 4, 3], True)), ((list(range(1000)) * 3,), (list(range(1000)), True))],
         indiciu='nu folosi lista.remove/sort pe lista primita: construieste alta', puncte=2)
""")

    c.md("""
### 10. Provocare: drumuri intr-o grila

Intr-o grila cu `n` linii si `m` coloane pleci din coltul de sus-stanga si ajungi in cel de jos-dreapta, mergand doar **in dreapta** sau **in jos**. Cate drumuri exista? Regula: `drumuri(n, m) = drumuri(n-1, m) + drumuri(n, m-1)`, iar daca `n == 1` sau `m == 1`, exista un singur drum.

Definitia recursiva de mai jos e corecta, dar exponentiala: refa aceleasi subprobleme la nesfarsit. Uita-te cum creste timpul:
""")
    c.cod("""
import time

def drumuri_lent(n, m):
    if n == 1 or m == 1:
        return 1
    return drumuri_lent(n - 1, m) + drumuri_lent(n, m - 1)

for k in [6, 9, 11, 12]:
    t0 = time.perf_counter()
    r = drumuri_lent(k, k)
    print(f'{k} x {k}: {r:>8} drumuri, {time.perf_counter() - t0:.3f} s')
""")
    c.md("""
Scrie `drumuri(n, m)` care intoarce acelasi lucru, dar **tine minte** rezultatele (dictionar sau `functools.cache`, ca la Fibonacci). Testele ascunse au grile de `100 x 100`, unde varianta lenta n-ar termina in viata ta. Adancimea recursiei e `n + m`, deci ramai sub limita.
""")
    c.ex("""
def drumuri(n, m):
    pass  # TODO: ca drumuri_lent, dar cu memoizare
""", """
from functools import cache


@cache
def drumuri(n, m):
    if n == 1 or m == 1:
        return 1
    return drumuri(n - 1, m) + drumuri(n, m - 1)
""")
    c.cod("""
def drumuri_ref(n, m):
    dp = [[1] * m for _ in range(n)]
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[-1][-1]

verifica('drumuri', drumuri, [((1, 1), 1), ((2, 2), 2), ((3, 3), 6), ((3, 7), 28)],
         ascunse=[((16, 16), drumuri_ref(16, 16)), ((40, 40), drumuri_ref(40, 40)), ((100, 120), drumuri_ref(100, 120)),
                  ((150, 150), drumuri_ref(150, 150)), ((1, 500), 1)],
         referinta=drumuri_ref, generator=lambda: (random.randint(1, 30), random.randint(1, 30)),
         indiciu='@cache de la functools sau un dictionar memo; fara memoizare, 16 x 16 are peste un miliard de apeluri',
         timp=3, puncte=3)
scor()
""")
    c.salveaza('07-functii-tema')


if __name__ == '__main__':
    predare()
    tema()
