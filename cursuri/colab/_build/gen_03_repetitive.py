"""Genereaza 03-structuri-repetitive-predare.ipynb si 03-structuri-repetitive-tema.ipynb (+ variantele cu solutii)."""
import math

from nb import Carnet


# valori asteptate pentru testele ascunse, calculate aici (nu le scriem de mana)
def _fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _collatz(n):
    p = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        p += 1
    return p


def _nd(n):
    k = 0
    for d in range(1, math.isqrt(n) + 1):
        if n % d == 0:
            k += 1 if d * d == n else 2
    return k


def _cel_mai_mic_n(S):
    n = math.isqrt(2 * S)
    while n * (n + 1) // 2 < S:
        n += 1
    while n > 1 and (n - 1) * n // 2 >= S:
        n -= 1
    return n


def _multipli(n, k):
    return sum(range(k, n + 1, k))


def predare():
    c = Carnet('Structuri repetitive', 'predare', fisiere=('anim_repetitive.py',))

    c.md("""
## Repetitia

Calculatorul face un singur lucru bine: acelasi pas de un milion de ori, fara sa oboseasca. Bucla e unealta pentru asta. Cu `if` si bucle scrii aproape orice algoritm de olimpiada.

Sunt doua feluri: `for` cand stii pe ce te plimbi (un interval, o lista, un text) si `while` cand repeti *pana se intampla ceva*. Si o veste proasta: aici apar primele programe care nu se mai opresc. Le vedem si pe ele.

**Ce urmaresti in animatii:** cum se schimba variabilele de la o tura la alta. Cine intelege asta intelege buclele.

## 1. for si range

`for i in range(n)` da lui `i` valorile `0, 1, ..., n-1`. Ultima valoare **nu** intra. In C++ ai scrie `for (int i = 0; i < n; i++)`.

| scriere | valorile lui i |
|---|---|
| `range(5)` | 0 1 2 3 4 |
| `range(2, 5)` | 2 3 4 |
| `range(0, 10, 3)` | 0 3 6 9 |
| `range(5, 0, -1)` | 5 4 3 2 1 |

Forma completa e `range(inceput, sfarsit, pas)`: sfarsitul e exclus, inceputul implicit 0, pasul implicit 1.

**Prezice:** ce valori dau `range(5, 0)` si `range(10, 0, -3)`?

<details><summary>Raspuns</summary>

`range(5, 0)` e gol: pasul e +1, iar de la 5 in sus nu ajungi niciodata la 0. `range(10, 0, -3)` da `10 7 4 1`.
</details>
""")
    c.cod("""
print(list(range(5)), list(range(2, 5)), list(range(0, 10, 3)))
print(list(range(5, 0, -1)), list(range(5, 0)), list(range(10, 0, -3)))
""")
    c.cod("""
%%vezi
s = 0
for i in range(1, 5):       #: i primeste pe rand 1, 2, 3, 4 (5 nu intra)
    s = s + i               #: adunam i la total
print(s)
""")

    c.md("""
## 2. for pe liste si pe text

Nu esti obligat sa numeri. `for` poate lua elementele direct dintr-o lista, dintr-un text, din orice colectie. E mai scurt si nu ai cum sa gresesti indicele. Folosesti `range(len(v))` doar cand chiar ai nevoie de pozitie.
""")
    c.cod("""
%%vezi
note = [9, 7, 10]
total = 0
for nota in note:           #: nota este chiar elementul, nu pozitia lui
    total += nota
for litera in 'ana':        #: si textul e o colectie: litera cu litera
    print(litera)
""")

    c.md("""
## 3. while

`while conditie:` repeta blocul cat timp conditia e adevarata. Conditia se verifica **inainte** de fiecare tura, deci blocul poate sa nu ruleze deloc. Regula: `for` cand stii de cate ori, `while` cand nu stii.

Intrebare la care `for` nu prea ajuta: de cate ori il dublezi pe 1 pana treci de 100?
""")
    c.cod("""
%%vezi
x = 1
pasi = 0
while x <= 100:             #: conditia se verifica INAINTE de fiecare tura
    x = x * 2               #: schimbam ceva din conditie, altfel bucla nu se mai termina
    pasi += 1
""")
    c.md("""
Asta e cheia: in corpul buclei trebuie sa se schimbe ceva ce afecteaza conditia. Daca uiti, ai o **bucla infinita**. Animatia se opreste singura dupa un numar de pasi si iti spune asta (in Colab, pe un program adevarat, opresti cu patratelul de langa celula):
""")
    c.cod("""
vezi('''
x = 1
while x <= 100:             #: x nu se schimba niciodata: conditia ramane adevarata
    print('tura')
''', max_pasi=25)
""")

    c.md("""
## 4. break, continue si else la bucla

- `break` iese din bucla pe loc
- `continue` sare la urmatoarea tura
- `else` la `for` / `while` ruleaza doar daca bucla s-a terminat **fara** `break`
""")
    c.cod("""
%%vezi
s = 0
for x in [4, -2, 7, 10, 3]:
    if x < 0:
        continue            #: numerele negative se sar
    if x > 8:
        break               #: la primul numar mare iesim de tot: 3 nu mai e citit
    s += x
""")
    c.md("""
`else`-ul de la bucla are un nume ciudat. Citeste-l ca "daca nu s-a oprit cu `break`". E ideal cand cauti ceva si vrei sa stii ca **nu** l-ai gasit:
""")
    c.cod("""
for n in (7, 9):
    for d in range(2, n):
        if n % d == 0:
            print(n, 'se imparte la', d)
            break
    else:
        print(n, 'nu are divizori proprii: e prim')
""")

    c.md("""
## 5. Acumulatori

Jumatate din problemele de olimpiada sunt un acumulator. O variabila care se "umple" pe parcurs:

- **suma:** porneste de la `0`, `s += x`
- **produs:** porneste de la `1` (nu de la 0, ca iese mereu 0), `p *= x`
- **contor:** porneste de la `0`, `k += 1` cand conditia e adevarata
- **maxim / minim:** porneste de la **primul element**, `m = v[0]`
- **flag:** `gasit = False`, devine `True` cand gasesti ce cautai

Un singur parcurs poate face mai multe. Uita-te cum se schimba `s`, `k` si `m` la fiecare element:
""")
    c.cod("""
%%vezi
v = [4, -9, 2, 7]
s = 0
k = 0
m = v[0]                    #: campionul incepe cu primul element
for x in v:
    s += x                  #: suma
    if x % 2 == 0:
        k += 1              #: contor: cate numere pare
    if x > m:
        m = x               #: x il bate pe campion
""")
    c.md("""
**Prezice:** de ce nu scriem `m = 0` la maxim? Ce iese pentru lista `[-5, -2, -9]`?

<details><summary>Raspuns</summary>

Iese `0`, un numar care nici nu e in lista, pentru ca niciun element nu e mai mare decat 0. Initializezi mereu cu **un element real**. (Acelasi motiv pentru care minimul nu porneste de la 0, ci de la `v[0]`.)
</details>
""")
    c.cod("""
v = [-5, -2, -9]
m = 0
for x in v:
    if x > m:
        m = x
print('cu m = 0    :', m)

m = v[0]
for x in v:
    if x > m:
        m = x
print('cu m = v[0] :', m)

exista_par = False              # flag
for x in [3, 7, 10, 5]:
    if x % 2 == 0:
        exista_par = True
        break
print('exista par:', exista_par)
""")

    c.md("""
## 6. Din topor, apoi scurtatura

Toti acumulatorii de mai sus exista gata facuti: `sum`, `max`, `min`, `len`, `sorted`, `lista.count`. Nu ii memora, la olimpiada ai documentatie. Dar trebuie sa poti scrie ce fac (adica buclele de mai sus), pentru ca in ziua in care conditia devine "cel mai mare numar **par**", functia gata facuta nu mai ajuta.
""")
    c.cod("""
v = [4, -9, 2, 7, 10]
print(sum(v), max(v), min(v), len(v))
print(sorted(v))
print(v.count(7))               # de cate ori apare 7
print(sum(v) / len(v))          # media
""")
    c.md("""
**De ce sunt mai rapide?** Bucla ta `for x in v: s += x` ruleaza in interpretorul Python: la fiecare tura el citeste instructiunea, verifica tipurile, creeaza obiecte. `sum(v)` face aceeasi bucla, dar scrisa in **C**, direct pe date, fara toate astea. Masuram pe un milion de numere (cifrele difera de la un calculator la altul, raportul nu):
""")
    c.cod("""
import time


def timp_ms(f, *args):
    t = time.perf_counter()
    f(*args)
    return (time.perf_counter() - t) * 1000


def suma_mea(v):
    s = 0
    for x in v:
        s += x
    return s


def maxim_meu(v):
    m = v[0]
    for x in v:
        if x > m:
            m = x
    return m


v = list(range(1_000_000))
for nume, a, b in [('suma', suma_mea, sum), ('maxim', maxim_meu, max)]:
    ta, tb = timp_ms(a, v), timp_ms(b, v)
    print(f'{nume:6} bucla mea {ta:6.1f} ms | functia din Python {tb:6.1f} ms | de {ta / max(tb, 1e-6):.0f} ori mai rapida')
""")

    c.md("""
## 7. Gauss: uneori bucla nici nu trebuie

Suma `1 + 2 + ... + n`. Bucla face `n` pasi (spunem **O(n)**: timpul creste proportional cu n). Gauss: `n * (n + 1) // 2` este **un singur calcul**, oricat de mare e `n` (**O(1)**). Cea mai buna optimizare e sa scapi de bucla.
""")
    c.cod("""
n = 5_000_000
print('bucla  :', suma_mea(range(1, n + 1)), f'{timp_ms(suma_mea, range(1, n + 1)):.1f} ms')
print('formula:', n * (n + 1) // 2, f'{timp_ms(lambda n: n * (n + 1) // 2, n):.4f} ms')
""")

    c.md("""
## 8. Bucla in bucla

Bucla interioara ruleaza **complet** pentru fiecare tura a celei exterioare. Daca fiecare are `n` ture, in total sunt `n * n`. Aici, linia `i` are `i` stelute:
""")
    c.cod("""
%%vezi
for i in range(1, 4):
    linie = ''
    for j in range(i):          #: interioara: se reia de la zero la fiecare i
        linie = linie + '*'
    print(linie)
""")
    c.cod("""
for i in range(1, 4):           # tabla inmultirii
    for j in range(1, 4):
        print(i * j, end=' ')
    print()                     # trecem la rand nou dupa fiecare linie
""")
    c.md("""
Ca sa vezi ordinea in care se parcurg perechile `(i, j)`, le strangem intr-o lista cu `append` si le dam animatiei. Triunghiul are `1 + 2 + ... + n` perechi, adica tot ordinul lui `n^2`:
""")
    c.cod("""
perechi = []
for i in range(6):
    for j in range(i + 1):
        perechi.append((i, j))
print(len(perechi), 'perechi')
anim_perechi(perechi, 'for i in range(6): for j in range(i + 1)')
""")

    c.md("""
## 9. Cifrele unui numar, cu while

Aici se leaga totul: din notebook-ul 1 stii ca `n % 10` e ultima cifra si `n // 10` e numarul fara ea. Acum le pui intr-o bucla care merge **pana se termina numarul**. Nu stii cate cifre are, deci e `while`.
""")
    c.cod("""
%%vezi
n = 4729
s = 0
while n > 0:                #: cat timp mai are cifre
    c = n % 10              #: ultima cifra
    s += c
    n //= 10                #: taiem ultima cifra
""")
    c.md("""
Aceeasi bucla da si numarul de cifre (`k += 1`) sau numarul **rasturnat** (`r = r * 10 + c`, il faci la exercitii). Atentie la `n = 0`: bucla nu ruleaza deloc, iar `0` totusi are o cifra.

## 10. Numere prime, pana la radical

`n` e prim daca nu are divizori intre 2 si `n-1`. Varianta de topor incearca toate numerele: `n - 2` pasi. Dar divizorii vin in **perechi** `(d, n / d)`, iar daca unul depaseste radicalul, celalalt e sub el. Deci ajunge sa cauti pana la `sqrt(n)`: **O(sqrt n)**. Cu `d * d <= n` eviti si radicalul cu zecimale.

`91 = 7 * 13` pare prim, dar nu e. Uita-te unde se opreste:
""")
    c.cod("""
%%vezi
n = 91
prim = True
d = 2
while d * d <= n:           #: ne oprim cand d trece de radical
    if n % d == 0:
        prim = False        #: am gasit un divizor: nu mai are rost sa continuam
        break
    d += 1
""")
    c.cod("""
import math


def este_prim(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


for x in range(20):
    if este_prim(x):
        print(x, end=' ')
print()
print(este_prim(1_000_000_007))      # instant: doar ~31600 de pasi
print(math.isqrt(1_000_000_007), 'pasi cu radical, contra', 1_000_000_005, 'daca incercam tot')
""")

    c.md("""
## 11. Cel mai mare divizor comun (Euclid)

De topor: incerci toate numerele de la `min(a, b)` in jos pana gasesti unul care le imparte pe amandoua. Euclid e mult mai rapid: `cmmdc(a, b) = cmmdc(b, a % b)`, pana cand restul e 0. Numerele scad foarte repede, deci sunt putini pasi (**O(log n)**).
""")
    c.cod("""
%%vezi
a, b = 48, 18
while b != 0:               #: cat timp mai avem rest
    a, b = b, a % b         #: (48, 18) -> (18, 12) -> (12, 6) -> (6, 0)
""")
    c.cod("""
import math
print(math.gcd(48, 18))                         # asta face bucla de mai sus
print(48 * 18 // math.gcd(48, 18))              # cel mai mic multiplu comun
""")

    c.md("""
## 12. Collatz

Ia un numar. Daca e par, il injumatatesti, daca e impar, il faci `3n + 1`. Repeta pana ajungi la 1. Nimeni nu a demonstrat ca se termina mereu, dar nimeni nu a gasit un numar la care sa nu se termine. Exemplu perfect de `while`: nu stii de cate ori repeti.
""")
    c.cod("""
%%vezi
n = 6
pasi = 0
while n != 1:
    if n % 2 == 0:
        n = n // 2          #: par: jumatate
    else:
        n = 3 * n + 1       #: impar: 3n + 1
    pasi += 1
""")
    c.md("""
## 13. Fibonacci, enumerate, zip, append

Fibonacci iterativ: tii doar ultimele doua numere. Atribuirea multipla (`a, b = b, a + b`) face treaba fara variabila ajutatoare. Simbolul `_` inseamna "nu ma intereseaza valoarea buclei".

`enumerate` iti da si pozitia, `zip` merge pe doua liste deodata, `append` construieste o lista pe parcurs.
""")
    c.cod("""
a, b = 0, 1
for _ in range(10):
    print(a, end=' ')
    a, b = b, a + b
print()

nume = ['Ana', 'Bo', 'Cris']
note = [9, 7, 10]
for i, n in enumerate(nume):
    print(i, n)
for n, nt in zip(nume, note):
    print(n, nt)

patrate = []
for i in range(1, 6):
    patrate.append(i * i)
print(patrate)
""")
    c.md("""
`zip` e felul in care calculezi un **produs scalar** (`sum(x * y for ...)`): la ML il vei vedea peste tot, iar NumPy il face intr-o singura linie.

## 14. Cate pasi face bucla mea?

Nu ne intereseaza secundele (depind de calculator), ci **cum creste numarul de pasi cand creste `n`**. Asta e complexitatea. O masuram cinstit: punem un contor in bucla si il crestem la fiecare pas.

| forma buclei | complexitate | exemplu |
|---|---|---|
| o bucla pana la n | O(n) | suma, maxim |
| doua bucle una in alta | O(n^2) | toate perechile |
| `while d * d <= n` | O(sqrt n) | prim |
| n se injumatateste (sau se imparte la 10) | O(log n) | Euclid, numarul de cifre |

Cele patru bucle de mai jos sunt scrise de tine, la fel ca mai sus, doar ca returneaza **numarul de pasi**. Apoi le rulezi pentru mai multe valori ale lui `n` si dai listele animatiei.
""")
    c.cod("""
def pasi_liniar(n):
    pasi = 0
    for i in range(n):
        pasi += 1
    return pasi


def pasi_patratic(n):
    pasi = 0
    for i in range(n):
        for j in range(n):
            pasi += 1
    return pasi


def pasi_radical(n):
    pasi = 0
    d = 2
    while d * d <= n:
        pasi += 1
        d += 1
    return pasi


def pasi_log(n):
    pasi = 0
    while n > 1:
        n //= 2
        pasi += 1
    return pasi


ns = list(range(25, 401, 25))
serii = {
    'O(n)': [pasi_liniar(n) for n in ns],
    'O(n^2)': [pasi_patratic(n) for n in ns],
    'O(sqrt n)': [pasi_radical(n) for n in ns],
    'O(log n)': [pasi_log(n) for n in ns],
}
print(serii['O(n^2)'][:5], serii['O(log n)'][:5])
anim_crestere_pasi(ns, serii)
""")
    c.md("""
Uita-te la panta din dreapta (scara logaritmica): `O(n)` e o dreapta cu panta 1, `O(n^2)` cu panta 2, `O(sqrt n)` cu panta 1/2, iar `O(log n)` aproape se turteste. La stanga vezi de ce conteaza: `n^2` "pleaca in sus" si celelalte par lipite de axa.

**Regula de buzunar pentru concurs:** Python face cam `10^7` pasi simpli pe secunda. Deci un `O(n)` e ok pana pe la `10^7`, dar un `O(n^2)` doar pana pe la `3000`. Sa vedem cat inseamna `10^7` pasi la tine:
""")
    c.cod("""
def gol():
    for _ in range(10 ** 7):
        pass


print(f'10^7 ture goale: {timp_ms(gol):.0f} ms')
""")

    c.md("""
## 15. Capcane

**Capcana 1: off-by-one.** `range(1, n)` se opreste la `n - 1`. Cand vrei de la 1 la `n`, scrii `range(1, n + 1)`. La fel, `range(n)` da `n` valori (0..n-1), deci `v[n]` iese din lista. Jumatate din bug-urile la bucle sunt de asta.

**Capcana 2: variabila buclei.** Daca o schimbi in corp, nu strici bucla: la tura urmatoare `for` ii da din nou valoarea din `range`. Iar dupa bucla, variabila **ramane** cu ultima valoare.
""")
    c.cod("""
n = 4
print(sum(range(1, n)), sum(range(1, n + 1)))       # 6 (lipseste 4) contra 10

for i in range(3):
    print('inceput tura, i =', i)
    i = i * 10
    print('    dupa i = i * 10, i =', i)
print('dupa bucla, i =', i)                         # ramane vie: valoarea de la ultima tura
""")
    c.md("""
**Capcana 3: float in bucla.** `0.1` nu are reprezentare exacta, iar erorile se aduna. Un `while x != 1.0` cu pas de `0.1` nu se opreste niciodata:
""")
    c.cod("""
x = 0.0
for _ in range(10):
    x += 0.1
print(x, x == 1.0)

vezi('''
x = 0.0
while x != 1.0:             #: x sare peste 1.0 (0.9999999999999999, apoi 1.0999999999999999...)
    x += 0.1
''', max_pasi=45)
""")
    c.md("""
Corect: numeri cu un `int` (`for k in range(10): x = k / 10`) sau folosesti `<` in loc de `!=`.

**Capcana 4: `break` iese doar din bucla lui.** In bucle imbricate, cea exterioara continua:
""")
    c.cod("""
%%vezi
for i in range(3):
    for j in range(3):
        if j == 1:
            break           #: iese doar din bucla cu j
        print(i, j)         #: dar bucla cu i merge mai departe
""")
    c.md("""
**Capcana 5: nu modifica o lista in timp ce o parcurgi.** Elementele se muta, iar bucla sare peste unele. **Prezice:** ce ramane din `[2, 4, 5, 6]` dupa ce stergem toate numerele pare?

<details><summary>Raspuns</summary>

`[4, 5]`, nu `[5]`. Dupa ce `2` e sters, `4` se muta pe pozitia lui, iar bucla merge la pozitia urmatoare si il sare. Parcurge o **copie** (`for x in v[:]`) sau construieste o lista noua.
</details>
""")
    c.cod("""
%%vezi
v = [2, 4, 5, 6]
for x in v:
    if x % 2 == 0:
        v.remove(x)         #: lista se scurteaza, elementele se muta cu o pozitie
""")

    c.md("""
## 16. Cum citesti eroarea

| eroare | de obicei inseamna |
|---|---|
| `TypeError: 'int' object is not iterable` | ai scris `for i in 5`, nu `for i in range(5)` |
| `TypeError: 'float' object cannot be interpreted as an integer` | `range(n / 2)`: `/` da float, foloseste `//` |
| `IndexError: list index out of range` | ai cerut `v[i]` cu `i` prea mare: `range(len(v) + 1)` |
| `ValueError: range() arg 3 must not be zero` | pas 0 |
| (nimic, programul nu se opreste) | bucla infinita: conditia nu se schimba niciodata |

Ultima nu e eroare, e ce vezi cand ai uitat sa modifici ceva in `while`. In Colab o opresti cu patratelul de la celula.
""")
    c.cod("""
%%vezi 9
n = int(input())
for i in range(n / 2):      #: n / 2 = 4.5, iar range vrea numar intreg
    print(i)
""")
    c.cod("""
%%vezi
v = [5, 6, 7]
for i in range(len(v) + 1): #: un pas in plus: i ajunge la 3, iar lista are indici 0, 1, 2
    print(v[i])
""")

    c.md("""
## Exercitii

Fiecare are o celula de completat si una de verificare, cu teste ascunse. Unele teste ascunse sunt **mari** (cu limita de timp): daca bucla ta face prea multi pasi, iti spune ca dureaza prea mult.
""")

    c.md("""
**Exercitiul 1.** Suma `1 + 2 + ... + n` cu o bucla (pentru `n = 0` rezultatul e `0`).
""")
    c.ex("""
def suma_pana_la(n):
    pass  # TODO
""", """
def suma_pana_la(n):
    s = 0
    for i in range(1, n + 1):
        s += i
    return s
""")
    c.cod("""
verifica('suma_pana_la', suma_pana_la, [((5,), 15), ((1,), 1), ((0,), 0)],
         ascunse=[((100,), 5050), ((1000,), 500500), ((10,), 55)],
         indiciu='range(1, n + 1), ca sa il incluzi si pe n')
""")

    c.md("""
**Exercitiul 2.** `n!` = `1 * 2 * ... * n`, cu `0! = 1`. Atentie de unde porneste produsul.
""")
    c.ex("""
def factorial(n):
    pass  # TODO
""", """
def factorial(n):
    p = 1
    for i in range(2, n + 1):
        p *= i
    return p
""")
    c.cod("""
import math, random
verifica('factorial', factorial, [((5,), 120), ((0,), 1), ((1,), 1)],
         ascunse=[((10,), 3628800), ((20,), 2432902008176640000)],
         referinta=math.factorial, generator=lambda: (random.randint(0, 25),),
         indiciu='produsul porneste de la 1, nu de la 0')
""")

    c.md("""
**Exercitiul 3.** Numarul de divizori ai lui `n` (`n >= 1`), inclusiv 1 si `n`. De ex. `12` are 6 divizori: 1, 2, 3, 4, 6, 12. Un contor si o bucla pana la `n`.
""")
    c.ex("""
def nr_divizori(n):
    pass  # TODO
""", """
def nr_divizori(n):
    k = 0
    for d in range(1, n + 1):
        if n % d == 0:
            k += 1
    return k
""")
    c.cod(f"""
verifica('nr_divizori', nr_divizori, [((12,), 6), ((1,), 1), ((7,), 2)],
         ascunse=[((36,), {_nd(36)}), ((100,), {_nd(100)}), ((97,), {_nd(97)}), ((360,), {_nd(360)}), ((5040,), {_nd(5040)})])
""")

    c.md("""
**Exercitiul 4.** `este_prim(n)`, cu bucla pana la radical (sectiunea 10). `0` si `1` nu sunt prime. Unele teste ascunse au numere de ordinul `10^9`: cu `n - 2` pasi nu termini.
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
verifica('este_prim', este_prim,
         [((2,), True), ((1,), False), ((0,), False), ((17,), True), ((15,), False), ((91,), False)],
         ascunse=[((97,), True), ((100,), False), ((7919,), True), ((25,), False), ((561,), False),
                  ((1000000007,), True), ((999999937,), True), ((1000000008,), False)],
         indiciu='while d * d <= n (cu egal! 25 = 5 * 5); iesi cu return False la primul divizor')
""")

    c.md("""
**Exercitiul 5.** Suma cifrelor lui `n` (`n >= 0`), cu `while`, **fara** `str`.
""")
    c.ex("""
def suma_cifre(n):
    pass  # TODO
""", """
def suma_cifre(n):
    s = 0
    while n > 0:
        s += n % 10
        n //= 10
    return s
""")
    c.cod("""
verifica('suma_cifre', suma_cifre, [((4729,), 22), ((0,), 0), ((1000,), 1)],
         referinta=lambda n: sum(map(int, str(n))), generator=lambda: (random.randint(0, 10 ** 12),),
         ascunse=[((9,), 9), ((99999,), 45)])
""")

    c.md("""
**Exercitiul 6.** Cel mai mare divizor comun al lui `a` si `b` cu algoritmul lui Euclid (`a, b >= 0`, nu ambele 0).
""")
    c.ex("""
def cmmdc(a, b):
    pass  # TODO
""", """
def cmmdc(a, b):
    while b != 0:
        a, b = b, a % b
    return a
""")
    c.cod("""
verifica('cmmdc', cmmdc, [((12, 18), 6), ((17, 5), 1), ((100, 75), 25)],
         ascunse=[((0, 5), 5), ((7, 7), 7), ((1, 1), 1), ((10 ** 12, 10 ** 6), 10 ** 6)],
         referinta=math.gcd, generator=lambda: (random.randint(1, 10 ** 12), random.randint(1, 10 ** 12)))
""")

    c.md("""
**Exercitiul 7.** Program ca la concurs: citeste `n`. Afiseaza `n` linii; linia `i` contine numerele de la `1` la `i`, separate prin spatiu:

```
1
1 2
1 2 3
```
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    n = int(input())
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            print(j, end=' ')
        print()
""")
    c.cod("""
verifica_program('triunghi de numere', main,
                 [(['1'], '1'), (['3'], '1\\n1 2\\n1 2 3')],
                 ascunse=[(['5'], '1\\n1 2\\n1 2 3\\n1 2 3 4\\n1 2 3 4 5'), (['2'], '1\\n1 2')],
                 indiciu='doua bucle imbricate; dupa cea interioara un print() gol')
scor()
""")

    c.md("""
## Recapitulare

- `for i in range(a, b, pas)`: `b` nu intra. `for x in lista` merge direct pe elemente. `while` cand nu stii de cate ori.
- `break` iese, `continue` sare peste tura, `else` la bucla ruleaza daca nu s-a facut `break`.
- Acumulatori: suma pleaca de la 0, produsul de la 1, maximul de la primul element, flag-ul de la `False`.
- `sum`, `max`, `min`, `len`, `sorted` fac aceleasi bucle, dar in C: de 2-10 ori mai repede, dupa functie. Scrie-le de mana ca sa stii ce fac, foloseste-le in rest.
- Gauss: `n * (n + 1) // 2` bate bucla. Prim: pana la radical. Cifre: `% 10` si `// 10`. Euclid: `a, b = b, a % b`.
- Complexitate: O(n), O(n^2), O(sqrt n), O(log n). In Python, ~`10^7` pasi pe secunda.
- Capcane: off-by-one, `while` fara actualizare, `float` in conditii de oprire, `break` doar din bucla lui, lista modificata in timpul parcurgerii.

Tema are 12 exercitii, cu trei provocari in care solutia lenta pica la timp.
""")
    c.salveaza('03-structuri-repetitive-predare')


def tema():
    c = Carnet('Structuri repetitive', 'tema')
    c.md("""
Exercitiile de acasa. Testele ascunse verifica granitele si **viteza**: la ultimele trei, solutia cea mai directa dureaza prea mult, deci trebuie sa gandesti. Poti rula o celula de verificare de cate ori vrei. La final, `scor()`.

Daca te blochezi, pune bucla ta intr-un `%%vezi` cu un exemplu mic si uita-te la variabile tura cu tura.
""")

    c.md("""
### 1. Peste medie

Intoarce **cate elemente** ale listei sunt strict mai mari decat media listei (lista nu e goala). De ex. `[1, 2, 3, 4, 5]` are media 3, deci raspunsul e 2. Calculeaza media de mana, cu o bucla.
""")
    c.ex("""
def peste_medie(v):
    pass  # TODO
""", """
def peste_medie(v):
    s = 0
    for x in v:
        s += x
    medie = s / len(v)
    k = 0
    for x in v:
        if x > medie:
            k += 1
    return k
""")
    c.cod("""
import random, math
verifica('peste_medie', peste_medie, [(([1, 2, 3, 4, 5],), 2), (([5, 5, 5],), 0), (([10],), 0), (([1, 100],), 1)],
         ascunse=[(([-3, -1, -2],), 1), (([0, 0, 0, 9],), 1)],
         referinta=lambda v: sum(1 for x in v if x > sum(v) / len(v)),
         generator=lambda: ([random.randint(-20, 20) for _ in range(random.randint(1, 15))],),
         puncte=1)
""")

    c.md("""
### 2. Produs scalar

Intoarce produsul scalar a doua liste de aceeasi lungime: `a[0]*b[0] + a[1]*b[1] + ...`. Foloseste `zip`. (In ML asta e baza unui neuron; NumPy il face cu `np.dot`.)
""")
    c.ex("""
def produs_scalar(a, b):
    pass  # TODO
""", """
def produs_scalar(a, b):
    s = 0
    for x, y in zip(a, b):
        s += x * y
    return s
""")
    c.cod("""
verifica('produs_scalar', produs_scalar, [(([1, 2, 3], [4, 5, 6]), 32), (([2], [3]), 6), (([], []), 0)],
         ascunse=[(([1, -1], [1, 1]), 0), (([0.5, 2], [4, 0.25]), 2.5), (([1, 2, 3, 4], [4, 3, 2, 1]), 20)], puncte=1)
""")

    c.md("""
### 3. Fibonacci

`fib(0) = 0`, `fib(1) = 1`, iar de acolo `fib(n) = fib(n-1) + fib(n-2)`. Intoarce `fib(n)` cu o bucla (tii doar ultimele doua numere). Python nu are overflow, deci `fib(300)` iese corect.
""")
    c.ex("""
def fib(n):
    pass  # TODO
""", """
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
""")
    c.cod(f"""
verifica('fib', fib, [((0,), 0), ((1,), 1), ((10,), 55)],
         ascunse=[((2,), 1), ((50,), {_fib(50)}), ((90,), {_fib(90)}), ((300,), {_fib(300)})], puncte=1)
""")

    c.md("""
### 4. Repara codul: suma multiplilor

`suma_multipli(n, k)` trebuie sa intoarca suma multiplilor lui `k` care sunt `<= n`. De ex. pentru `n = 10` si `k = 5`: `5 + 10 = 15`. Functia da 5. Uita-te in animatie ce ii lipseste.
""")
    c.cod("""
%%vezi
n = 10
k = 5
s = 0
for i in range(k, n, k):    #: range(5, 10, 5) contine doar 5: sfarsitul e exclus
    s += i
""")
    c.ex("""
def suma_multipli(n, k):
    s = 0
    for i in range(k, n, k):
        s += i
    return s
""", """
def suma_multipli(n, k):
    s = 0
    for i in range(k, n + 1, k):
        s += i
    return s
""")
    c.cod(f"""
verifica('suma_multipli', suma_multipli, [((10, 5), 15), ((10, 3), 18), ((9, 3), 18), ((5, 10), 0)],
         ascunse=[((100, 7), {_multipli(100, 7)}), ((1, 1), 1), ((6, 3), 9), ((0, 5), 0), ((1000, 1), 500500)],
         indiciu='off-by-one: range se opreste inainte de al doilea argument', puncte=1)
""")

    c.md("""
### 5. Numarul rasturnat

Intoarce numarul cu cifrele in ordine inversa (`1234 -> 4321`, `1200 -> 21`, `0 -> 0`). Fara `str`: `while`, `% 10`, `// 10` si `r = r * 10 + c`.
""")
    c.ex("""
def rasturnat(n):
    pass  # TODO
""", """
def rasturnat(n):
    r = 0
    while n > 0:
        r = r * 10 + n % 10
        n //= 10
    return r
""")
    c.cod("""
verifica('rasturnat', rasturnat, [((1234,), 4321), ((1200,), 21), ((7,), 7), ((0,), 0)],
         ascunse=[((100,), 1), ((98765,), 56789)],
         referinta=lambda n: int(str(n)[::-1]), generator=lambda: (random.randint(0, 10 ** 9),), puncte=2)
""")

    c.md("""
### 6. Palindrom

Un numar e palindrom daca se citeste la fel invers (`121`, `1221`, `7`). Intoarce `True` / `False`. Refoloseste functia de la 5 (ea trebuie sa fie corecta).
""")
    c.ex("""
def este_palindrom(n):
    pass  # TODO
""", """
def este_palindrom(n):
    return n == rasturnat(n)
""")
    c.cod("""
verifica('este_palindrom', este_palindrom,
         [((121,), True), ((123,), False), ((7,), True), ((10,), False), ((1221,), True)],
         ascunse=[((0,), True), ((100,), False), ((12321,), True), ((1000021,), False)],
         referinta=lambda n: str(n) == str(n)[::-1], generator=lambda: (random.randint(0, 3000),),
         indiciu='10 rasturnat e 1, deci nu e palindrom', puncte=2)
""")

    c.md("""
### 7. Pasi Collatz

Pornind de la `n`, cate operatii (injumatatire sau `3n + 1`) sunt necesare pana ajungi la 1? Pentru `n = 6`: `6, 3, 10, 5, 16, 8, 4, 2, 1` sunt 8 pasi. Pentru `n = 1` sunt 0.
""")
    c.ex("""
def pasi_collatz(n):
    pass  # TODO
""", """
def pasi_collatz(n):
    pasi = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        pasi += 1
    return pasi
""")
    c.cod(f"""
verifica('pasi_collatz', pasi_collatz, [((1,), 0), ((6,), 8), ((7,), 16), ((27,), 111)],
         ascunse=[((2,), 1), ((3,), 7), ((97,), {_collatz(97)}), ((871,), {_collatz(871)}), ((837799,), {_collatz(837799)})],
         puncte=2)
""")

    c.md("""
### 8. Program: tabla inmultirii

Citeste `n`. Afiseaza tabla inmultirii `n x n`: `n` linii, iar linia `i` contine `i*1, i*2, ..., i*n` separate prin spatiu. Pentru `n = 3`:

```
1 2 3
2 4 6
3 6 9
```
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    n = int(input())
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            print(i * j, end=' ')
        print()
""")
    c.cod("""
verifica_program('tabla inmultirii', main,
                 [(['1'], '1'), (['3'], '1 2 3\\n2 4 6\\n3 6 9')],
                 ascunse=[(['4'], '1 2 3 4\\n2 4 6 8\\n3 6 9 12\\n4 8 12 16'), (['2'], '1 2\\n2 4')],
                 indiciu='doua bucle imbricate; print(..., end=" ") si un print() gol dupa cea interioara', puncte=2)
""")

    c.md("""
### 9. Program: cifrele unui numar

Citeste un numar natural `n`. Pe o singura linie afiseaza, separate prin spatiu: **numarul de cifre**, **cifra maxima** si **suma cifrelor**. Pentru `4729`: `4 9 22`. Atentie: `0` are o cifra.
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    n = int(input())
    cifre = 0
    maxim = 0
    suma = 0
    while n > 0:
        c = n % 10
        cifre += 1
        suma += c
        if c > maxim:
            maxim = c
        n //= 10
    if cifre == 0:
        cifre = 1
    print(cifre, maxim, suma)
""")
    c.cod("""
verifica_program('cifrele unui numar', main,
                 [(['4729'], '4 9 22'), (['1000'], '4 1 1'), (['0'], '1 0 0')],
                 ascunse=[(['9'], '1 9 9'), (['1234567890'], '10 9 45'), (['555'], '3 5 15'), (['10'], '2 1 1')],
                 indiciu='pentru n = 0 bucla while nu ruleaza deloc: trateaza separat', puncte=2)
""")

    c.md("""
### 10. Provocare: numarul de divizori, rapid

La predare ai numarat divizorii pana la `n`. Acum `n` poate fi de ordinul `10^12`, iar `10^12` de pasi nu se termina in viata ta. Foloseste faptul ca divizorii vin in perechi `(d, n / d)`: parcurge `d` doar cat `d * d <= n` si numara **doi** divizori de fiecare data, cu o singura exceptie (cand `d * d == n`, cei doi coincid).
""")
    c.ex("""
def nr_divizori_rapid(n):
    pass  # TODO
""", """
def nr_divizori_rapid(n):
    k = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            if d * d == n:
                k += 1
            else:
                k += 2
        d += 1
    return k
""")
    c.cod(f"""
verifica('nr_divizori_rapid', nr_divizori_rapid, [((12,), 6), ((1,), 1), ((36,), 9), ((97,), 2)],
         ascunse=[((10 ** 12,), {_nd(10 ** 12)}), ((999999999989,), {_nd(999999999989)}), ((963761198400,), {_nd(963761198400)}),
                  ((10 ** 10,), {_nd(10 ** 10)}), ((2,), 2)],
         indiciu='patratele perfecte: 36 = 6 * 6, divizorul 6 se numara o singura data', puncte=3)
""")

    c.md("""
### 11. Provocare: cel mai mic n

Intoarce cel mai mic `n` natural pentru care `1 + 2 + ... + n >= S` (`S >= 1`). De ex. `S = 10` da `4` (suma e 10), iar `S = 11` da `5`.

Solutia directa (aduni `1, 2, 3, ...` pana treci de `S`) face `~sqrt(2S)` pasi, si e in regula pana pe la `S = 10^12`. Testele ascunse merg pana la `S = 10^18`, unde ar trebui `1,4 * 10^9` pasi. Gandeste-te la Gauss: suma pana la `n` o stii dintr-un singur calcul, deci poti **verifica rapid un n**. Iar cand poti verifica rapid, poti cauta prin injumatatire (cautare binara): dublezi `n` pana treci de `S`, apoi injumatatesti intervalul. Sunt `O(log S)` pasi.
""")
    c.ex("""
def cel_mai_mic_n(S):
    pass  # TODO
""", """
def cel_mai_mic_n(S):
    lo, hi = 1, 1
    while hi * (hi + 1) // 2 < S:
        hi *= 2
    while lo < hi:
        mij = (lo + hi) // 2
        if mij * (mij + 1) // 2 >= S:
            hi = mij
        else:
            lo = mij + 1
    return lo
""")
    c.cod(f"""
verifica('cel_mai_mic_n', cel_mai_mic_n, [((1,), 1), ((10,), 4), ((11,), 5), ((15,), 5), ((16,), 6)],
         ascunse=[((10 ** 12,), {_cel_mai_mic_n(10 ** 12)}), ((10 ** 16 + 1,), {_cel_mai_mic_n(10 ** 16 + 1)}),
                  ((10 ** 18,), {_cel_mai_mic_n(10 ** 18)}), ((3,), 2), ((6,), 3)],
         indiciu='dublezi hi cat timp suma pana la hi e < S, apoi injumatatesti intervalul [lo, hi]', puncte=3)
""")

    c.md("""
### 12. Provocare: numerele perfecte

Un numar e **perfect** daca este egal cu suma divizorilor lui proprii (fara el insusi): `6 = 1 + 2 + 3`, `28 = 1 + 2 + 4 + 7 + 14`. Intoarce **lista** numerelor perfecte `<= n`, in ordine.

Iata solutia care iti vine prima, cu suma divizorilor calculata prin bucla pana la `i - 1`. E corecta, dar uita-te cum creste timpul cand dublezi `n` (celula de mai jos o masoara):
""")
    c.cod("""
import time


def perfecte_lent(n):
    rez = []
    for i in range(2, n + 1):
        s = 0
        for d in range(1, i):
            if i % d == 0:
                s += d
        if s == i:
            rez.append(i)
    return rez


for n in (1000, 2000, 4000):
    t = time.perf_counter()
    perfecte_lent(n)
    print(f'n = {n}: {time.perf_counter() - t:.2f} s')
""")
    c.md("""
De fiecare data cand dublezi `n`, timpul se **inmulteste cu 4**: `O(n^2)`. Pentru `n = 40000` ar trebui de 100 de ori mai mult decat pentru `4000`. Testele ascunse au limita de 3 secunde. Gaseste o varianta mai rapida: cauta divizorii doar pana la radical (si aduna ambii din pereche), sau, mai sus in clasa, aduna fiecare `d` la toti multiplii lui.
""")
    c.ex("""
def perfecte(n):
    pass  # TODO
""", """
def perfecte(n):
    s = [1] * (n + 1)
    s[0] = 0
    for d in range(2, n // 2 + 1):
        for m in range(2 * d, n + 1, d):
            s[m] += d
    return [i for i in range(2, n + 1) if s[i] == i]
""")
    c.cod("""
verifica('perfecte', perfecte, [((10,), [6]), ((30,), [6, 28]), ((500,), [6, 28, 496]), ((5,), [])],
         ascunse=[((10000,), [6, 28, 496, 8128]), ((40000,), [6, 28, 496, 8128]), ((6,), [6]), ((1,), [])],
         indiciu='sqrt: pentru d pana la radical, adauga d si i // d (atentie la d == i // d); sau adauga fiecare d la multiplii lui',
         timp=3, puncte=3)
scor()
""")
    c.salveaza('03-structuri-repetitive-tema')


if __name__ == '__main__':
    predare()
    tema()
