"""Genereaza 05-multimi-predare.ipynb si 05-multimi-tema.ipynb (+ variantele cu solutii)."""
from nb import Carnet

FISIERE = ('anim_multimi.py',)


def predare():
    c = Carnet('Multimi (set)', 'predare', fisiere=FISIERE)

    c.md("""
## Multimea: ce e si cand o folosesti

O multime (`set`) e o colectie de elemente **distincte**, fara ordine. Nu are indici, nu are dubluri. In schimb face un lucru pe care lista nu-l poate face: raspunde la "exista `x` aici?" aproape instant, oricat de mare ar fi ea.

Asta o face potrivita pentru: eliminat dubluri, "am mai vazut asta?", comparat doua colectii (ce au in comun, ce difera), verificat ca doua seturi de date nu se suprapun. La olimpiada, multe solutii care dau "time limit exceeded" cu liste trec cand schimbi lista cu un set.

Ce facem: creare si capcana `{}`, operatiile pe multimi (in animatie, cu diagrame Venn), de ce cautarea e rapida (cu o tabela hash animata), legatura cu ML, capcane si erori.

**Cum lucram.** Celulele `%%vezi` ruleaza codul pas cu pas si arata memoria. Multimile apar ca o cutie `set`, iar animatia le afiseaza sortate ca text, ca sa nu se mute la fiecare pas. Python **nu** garanteaza nicio ordine.
""")

    c.md("""
## 1. Creare

Cu acolade si elemente, sau cu `set(ceva)` dintr-un iterabil (lista, text, `range`...). Dublurile dispar. **Multimea goala** se face doar cu `set()`.

**Prezice:** ce tip are `{}`?

<details><summary>Raspuns</summary>

`dict` (dictionar). Acoladele goale au fost luate de dictionare inainte sa existe multimile. Multimea goala e `set()`.
</details>
""")
    c.cod("""
%%vezi
a = {3, 1, 2, 3, 1}        #: dublurile dispar
b = set([5, 5, 6])         #: dintr-o lista
c = set('banana')          #: dintr-un text: caracterele distincte
gol = set()                #: multimea goala
d = {}                     #: ATENTIE: acolada goala este un DICTIONAR
n = len(a)
""")
    c.cod("""
print(type({}), type(set()), type({1}), type({1: 2}))
""")

    c.md("""
## 2. Unicitate: din topor, apoi `set`

Sa scoatem dublurile dintr-o lista. Varianta de mana: pentru fiecare element, cauti daca l-ai pus deja. `x not in unice` cauta prin lista, deci in total ai **O(n^2)**.
""")
    c.cod("""
%%vezi
v = [3, 1, 3, 2, 1]
unice = []
for x in v:
    if x not in unice:      #: cautare in lista: se uita la fiecare element
        unice.append(x)
scurt = set(v)              #: acelasi rezultat, dar fara ordine garantata
""")
    c.md("""
`set(v)` e mai scurta si mult mai rapida (vezi mai jos de ce), dar **pierzi ordinea**. Daca ordinea primei aparitii conteaza, tii un set doar pentru "am mai vazut?" si o lista pentru rezultat. Asta e primul exercitiu.
""")

    c.md("""
## 3. Adaugare si stergere

| metoda | ce face |
|---|---|
| `add(x)` | adauga `x` (daca exista deja, nu se intampla nimic) |
| `remove(x)` | sterge `x`; `KeyError` daca nu exista |
| `discard(x)` | sterge `x`; **fara eroare** daca nu exista |
| `pop()` | scoate un element **oarecare** |
| `x in s` | e in multime? |
""")
    c.cod("""
%%vezi
s = {1, 2, 3}
s.add(4)           #: adauga
s.add(2)           #: 2 exista deja: nimic nu se schimba
s.remove(1)        #: sterge; KeyError daca nu exista
s.discard(9)       #: sterge; NU da eroare daca nu exista
x = s.pop()        #: scoate un element oarecare (nu stii care)
ok = 3 in s        #: in: rapid
""")

    c.md("""
## 4. Fara ordine, fara index

Nu poti scrie `s[0]`: nu exista "primul element". Iar ordinea la afisare nu e garantata. La numere mici pare sortata (pentru ca un `int` isi e propriul hash), dar asta e o intamplare de implementare, nu o regula.
""")
    c.cod("""
%%vezi
s = {30, 10, 20}
p = s[0]           #: multimile nu au indici
""")
    c.cod("""
import os, subprocess, sys
print({3, 1, 2}, {100, 5, 33})      # primul pare sortat, al doilea nu

cod = "print({'ana', 'dan', 'ion', 'eva'})"
for seed in ('1', '2', '3'):        # acelasi cod, trei porniri ale lui Python
    r = subprocess.run([sys.executable, '-c', cod], capture_output=True, text=True,
                       env={**os.environ, 'PYTHONHASHSEED': seed})
    print(seed, r.stdout.strip())
""")
    c.md("""
Textele au un hash **randomizat** la fiecare pornire (o masura de securitate), deci ordinea difera de la o rulare la alta. Regula: daca ai nevoie de ordine, `sorted(s)` iti da o lista sortata.
""")

    c.md("""
## 5. Operatii pe multimi

Ai patru operatii, fiecare ca operator si ca metoda:

| operator | metoda | rezultat |
|---|---|---|
| `a \\| b` | `a.union(b)` | reuniune: elementele din `a` sau din `b` |
| `a & b` | `a.intersection(b)` | intersectie: din amandoua |
| `a - b` | `a.difference(b)` | diferenta: in `a`, dar nu in `b` |
| `a ^ b` | `a.symmetric_difference(b)` | diferenta simetrica: in exact una dintre ele |

Si variantele care modifica pe loc: `a |= b` (`update`), `a &= b`, `a -= b`.
""")
    c.cod("""
%%vezi
a = {1, 2, 3, 4}
b = {3, 4, 5}
u = a | b          #: reuniune
i = a & b          #: intersectie
d = a - b          #: in a, dar nu in b
s = a ^ b          #: in exact una dintre ele
""")
    c.md("""
**Prezice:** pentru `A = {1, 2, 3, 4, 5, 6}` si `B = {4, 5, 6, 7, 8}`, ce contine `A ^ B`?

<details><summary>Raspuns</summary>

`{1, 2, 3, 7, 8}`: tot ce e in una singura, fara `4, 5, 6`. Uita-te in ultima diagrama de mai jos.
</details>

Diagramele arata fiecare operatie. Zona colorata e rezultatul; elementele sunt verificate pe rand.
""")
    c.cod("""
A = {1, 2, 3, 4, 5, 6}
B = {4, 5, 6, 7, 8}
anim_venn(A, B, '|')      # reuniune
""")
    c.cod("""
anim_venn(A, B, '&')      # intersectie
""")
    c.cod("""
anim_venn(A, B, '-')      # diferenta A - B
""")
    c.cod("""
anim_venn(A, B, '^')      # diferenta simetrica
""")
    c.md("""
Metodele accepta **orice iterabil** (lista, text), operatorii cer multime de ambele parti:
""")
    c.cod("""
%%vezi
a = {1, 2, 3}
u1 = a.union([7, 8])       #: metoda accepta o lista
u2 = a | [7, 8]            #: operatorul nu: TypeError
""")
    c.cod("""
%%vezi
a = {1, 2}
b = {1, 2, 3}
x = a <= b                 #: a e submultime a lui b (a.issubset(b))
y = a < b                  #: submultime stricta
z = b >= a                 #: b e supermultime a lui a
w = a.isdisjoint({7, 8})   #: nu au niciun element comun
""")

    c.md("""
## 6. Intersectia: din topor, apoi cu operatorul

De mana ai nevoie de doua bucle: pentru fiecare element din `a`, cauti prin tot `b`. Costa **O(n * m)**.
""")
    c.cod("""
%%vezi
a = [1, 2, 3, 4]
b = [3, 4, 5]
comune = []
for x in a:
    for y in b:            #: pentru fiecare x, se cauta prin tot b
        if x == y:
            comune.append(x)
rapid = set(a) & set(b)    #: aceeasi treaba, dar fara cele doua bucle
""")
    c.cod("""
import time, random

def masoara(f):
    t0 = time.perf_counter()
    f()
    return time.perf_counter() - t0

def comune_topor(a, b):
    rez = []
    for x in a:
        if x in b:              # cautare in lista
            rez.append(x)
    return rez

a = random.sample(range(10**6), 4000)
b = random.sample(range(10**6), 4000)
print(f'de mana (liste): {masoara(lambda: comune_topor(a, b)):.4f} s   set(a) & set(b): {masoara(lambda: set(a) & set(b)):.5f} s')
""")

    c.md("""
## 7. Comprehensii si `frozenset`

Ca la liste, dar cu acolade: `{expresie for x in ceva if conditie}`. Dublurile dispar automat.
""")
    c.cod("""
%%vezi
patrate = {x * x for x in range(-3, 4)}                   #: -3 si 3 dau acelasi patrat: apare o singura data
litere = {c for c in 'banana bread' if c != ' '}          #: literele distincte, fara spatiu
""")
    c.md("""
**Ce poate intra intr-o multime?** Doar elemente **hashabile**, adica imuabile: numere, texte, tupluri, `frozenset`. O lista sau o alta multime pot fi modificate, deci nu au un hash stabil si nu intra. Pentru coordonate (celule vizitate intr-un labirint) folosesti **tupluri**: `{(0, 1), (2, 3)}`. `frozenset` e multimea imuabila, buna ca element in alta multime.
""")
    c.cod("""
%%vezi
vizitate = {(1, 2), (3, 4)}                    #: tuplurile sunt hashabile: bune pentru coordonate
inghetat = frozenset([1, 2])                   #: multime imuabila
grupuri = {inghetat, frozenset([3])}           #: o multime de multimi
gresit = {[1, 2], [3]}                         #: lista se poate modifica: TypeError
""")

    c.md("""
## 8. De ce `x in set` e rapid

Masoara mai intai. Cautam 20 de valori care **nu** exista (cazul cel mai rau pentru lista, ea se uita peste tot).

**Prezice:** cu `10**6` elemente in loc de `10**5`, cum se schimba timpul pentru lista? Dar pentru multime?

<details><summary>Raspuns</summary>

Lista: creste de ~10 ori (cauta prin tot: O(n)). Multimea: aproape deloc (O(1) in medie).
</details>
""")
    c.cod("""
for N in (10**5, 10**6):
    lista = list(range(N))
    multime = set(lista)
    cautate = [-i for i in range(1, 21)]          # niciuna nu exista
    t_l = masoara(lambda: [x in lista for x in cautate])
    t_s = masoara(lambda: [x in multime for x in cautate])
    t_c = masoara(lambda: set(lista))
    print(f'N={N:>8}: 20 cautari in lista {t_l * 1000:9.3f} ms | in set {t_s * 1000:7.4f} ms | construirea setului {t_c * 1000:8.2f} ms')
""")
    c.md("""
Observa si ultima coloana: **construirea** multimii costa O(n). Daca cauti o singura data, nu merita sa transformi lista in set. Daca cauti de multe ori, merita mult.

**De ce?** O multime e o tabela cu "buckete" (cosuri). Un element ajunge in bucketul `hash(x) % nr_buckete`. Pentru a-l cauta calculezi acelasi numar si te uiti **doar in acel bucket**. Intai varianta de mana, cu liste de liste:
""")
    c.cod("""
%%vezi
valori = [10, 25, 3, 18, 7, 42]
b = 8
bucket = [[] for _ in range(b)]        #: 8 buckete goale
for x in valori:
    k = x % b                          #: hash-ul simplu: restul la nr. de buckete
    bucket[k].append(x)                #: x merge in bucketul k

cautat = 42
gasit = cautat in bucket[cautat % b]   #: ne uitam DOAR intr-un bucket, nu peste tot
""")
    c.md("""
10, 18 si 42 au dat toate restul 2: au ajuns in acelasi bucket. Asta e o **coliziune**. E normala; conteaza ca bucketele raman scurte. Animatia arata cum se umple tabela si cum decurge o cautare (aici hash-ul e chiar numarul, ca sa poti verifica de mana):
""")
    c.cod("""
anim_hash([10, 25, 3, 18, 7, 42, 11], buckete=8, cauta=26)
""")
    c.md("""
Cu texte: hash-ul nostru didactic e suma codurilor caracterelor (`hash_simplu`). Cel real al lui Python e altul si **randomizat** la fiecare pornire, dar ideea e aceeasi.
""")
    c.cod("""
anim_hash(['ana', 'maria', 'ion', 'dan', 'nai', 'eva'], buckete=8, cauta='dan')
""")
    c.md("""
Ce tine minte din animatie:

- Cautarea compara cu cateva elemente, nu cu toate: costa **O(1) in medie**. Lista compara cu toate: O(n).
- Python mareste tabela cand se umple (~2/3), ca bucketele sa ramana scurte. CPython foloseste "adresare deschisa" in loc de liste in bucket, dar principiul e acelasi.
- De aceea elementele trebuie sa fie **imuabile**: daca o lista si-ar schimba continutul, hash-ul s-ar schimba si elementul ar ramane in bucketul gresit, pierdut.
- Elementele egale trebuie sa aiba acelasi hash (`hash(1) == hash(1.0) == hash(True)`).
""")
    c.cod("""
print(hash(42), hash(1) == hash(1.0) == hash(True))
print(hash('ana'))           # se schimba la fiecare pornire a lui Python
""")

    c.md("""
## 9. Legatura cu ML: etichete, vocabular, scurgeri de date

Trei locuri unde apar multimile, toate din munca de zi cu zi:

- **Etichetele distincte** dintr-un set de date: `set(y)` iti spune cate clase ai.
- **Vocabularul** unui set de texte (NLP): cuvintele distincte din toate documentele.
- **Verificarea ca train si test nu se suprapun**. Daca acelasi exemplu apare si la antrenare, si la test, scorul e umflat artificial: e o *scurgere de date* (data leakage). Verificarea e o intersectie de multimi si e clasica.
""")
    c.cod("""
y = ['pisica', 'caine', 'pisica', 'pasare', 'caine', 'pisica']
clase = sorted(set(y))                             # etichetele distincte, intr-o ordine fixa
print(clase, len(clase), 'clase')
print([clase.index(e) for e in y])                 # eticheta -> numar (mai bine cu dictionar, lectia urmatoare)

texte = ['am un caine', 'ana are un caine mic', 'pisica mica']
vocab = sorted({w for t in texte for w in t.split()})
print(vocab)                                       # vocabularul: cuvintele distincte din toate textele
""")
    c.cod("""
random.seed(0)
ids = list(range(100))
random.shuffle(ids)
train = ids[:80]
test = ids[70:]                        # bug: feliile se suprapun (ai vrut ids[80:])
comune = set(train) & set(test)
print(len(comune), 'id-uri apar in ambele:', sorted(comune)[:5], '...')

test = ids[80:]
print(set(train).isdisjoint(test))     # True: fara suprapunere
""")
    c.md("""
Pe 10^5 exemple, aceeasi verificare cu bucle si liste ar dura minute. Cu multimi dureaza cateva milisecunde. `train_test_split` din scikit-learn face taierea corect, dar verificarea o poti pastra in orice proiect.
""")

    c.md("""
## 10. Capcane

**Capcana 1: modifici multimea in timp ce o parcurgi.** Spre deosebire de liste (care sar elemente), la multimi Python te opreste cu o eroare, pentru ca structura interna s-ar strica.
""")
    c.cod("""
%%vezi
s = {1, 2, 3, 4}
for x in s:
    if x % 2 == 0:
        s.remove(x)        #: se schimba marimea multimii in timpul parcurgerii
""")
    c.md("""
Reparatia: parcurgi o **copie** (`for x in list(s)`) sau construiesti o multime noua cu comprehensie: `{x for x in s if x % 2 != 0}`.

**Capcana 2: `1`, `1.0` si `True` sunt "acelasi" element.** Sunt egale si au acelasi hash, deci multimea le pastreaza doar pe primul.

**Prezice:** cate elemente are `{1, 1.0, True, 'a'}`?

<details><summary>Raspuns</summary>

Doua: `1` si `'a'`. Ai atentie cand amesteci tipuri.
</details>
""")
    c.cod("""
%%vezi
s = {1, 1.0, True, 'a'}     #: 1 == 1.0 == True, deci intra o singura data
n = len(s)
""")
    c.md("""
**Capcana 3: multimea uita de cate ori apare un element.** `set('aab') == set('abb')` e adevarat, dar cuvintele nu sunt anagrame. Pentru anagrame ai nevoie de frecvente (sau de `sorted`). Iar `set('abc')` desface textul in caractere, pe cand `{'abc'}` e o multime cu un singur element.
""")
    c.cod("""
print(set('aab') == set('abb'), sorted('aab') == sorted('abb'))
print(set('abc'), {'abc'})
""")

    c.md("""
## 11. Cum citesti eroarea

| eroare | de obicei inseamna |
|---|---|
| `TypeError: unhashable type: 'list'` | ai pus o lista (sau multime, dictionar) intr-o multime; foloseste tuplu |
| `KeyError: 9` la `remove` | elementul nu exista; foloseste `discard` |
| `TypeError: 'set' object is not subscriptable` | ai scris `s[0]`; multimile nu au indici |
| `AttributeError: 'dict' object has no attribute 'add'` | ai scris `s = {}`, care e dictionar; foloseste `set()` |
| `RuntimeError: Set changed size during iteration` | ai modificat multimea in bucla |
""")
    c.cod("""
%%vezi
unice = {}
unice.add(5)          #: unice e un dictionar, nu o multime
""")
    c.cod("""
%%vezi
s = {1, 2}
s.remove(9)
""")

    c.md("""
## 12. Exemplu complet

Program ca la concurs: `n`, apoi `n` numere pe o linie. Afiseaza cate valori distincte sunt.
""")
    c.cod("""
%%vezi 6 "4 9 2 9 4 1"
n = int(input())
v = list(map(int, input().split()))
print(len(set(v)))       #: set(v) elimina dublurile, len le numara
""")

    c.md("""
## Exercitii

Le rezolvi tu; fiecare are o celula de completat si una de verificare. Rezultatele care sunt multimi le cerem ca **liste sortate**, ca sa fie comparabile.
""")

    c.md("""
**Exercitiul 1.** Elimina duplicatele **pastrand ordinea primei aparitii**: `[3, 1, 3, 2, 1]` da `[3, 1, 2]`. Tine un set cu ce ai vazut deja (verificarea `x in vazute` e O(1)) si o lista cu rezultatul.
""")
    c.ex("""
def fara_duplicate(v):
    pass  # TODO
""", """
def fara_duplicate(v):
    vazute = set()
    rez = []
    for x in v:
        if x not in vazute:
            vazute.add(x)
            rez.append(x)
    return rez
""")
    c.cod("""
verifica('fara_duplicate', fara_duplicate,
         [(([3, 1, 3, 2, 1],), [3, 1, 2]), (([1, 2, 3],), [1, 2, 3]), (([],), [])],
         ascunse=[(([5, 5, 5],), [5]), ((['a', 'b', 'a'],), ['a', 'b']), ((list(range(50_000)) * 2,), list(range(50_000)))],
         indiciu='set pentru "am mai vazut?", lista pentru rezultat')
""")

    c.md("""
**Exercitiul 2.** Elementele comune ale listelor `a` si `b`, fara dubluri, intr-o **lista sortata**.
""")
    c.ex("""
def comune(a, b):
    pass  # TODO
""", """
def comune(a, b):
    return sorted(set(a) & set(b))
""")
    c.cod("""
verifica('comune', comune,
         [(([1, 2, 3, 4], [3, 4, 5]), [3, 4]), (([1, 2], [3, 4]), []), (([1, 1, 2, 2], [2, 2, 3]), [2])],
         ascunse=[(([], [1]), []), (([5, 4, 3], [3, 4, 5]), [3, 4, 5]), (([-1, 0], [0, -1, 7]), [-1, 0])])
""")

    c.md("""
**Exercitiul 3.** Elementele care sunt in `a`, dar **nu** in `b`, fara dubluri, ca lista sortata.
""")
    c.ex("""
def doar_in_a(a, b):
    pass  # TODO
""", """
def doar_in_a(a, b):
    return sorted(set(a) - set(b))
""")
    c.cod("""
verifica('doar_in_a', doar_in_a,
         [(([1, 2, 3, 4], [3, 4, 5]), [1, 2]), (([1, 1, 2], [2]), [1]), (([1, 2], [1, 2, 3]), [])],
         ascunse=[(([], [1]), []), (([3, 2, 1], []), [1, 2, 3]), (([7, 7, 7], [8]), [7])])
""")

    c.md("""
**Exercitiul 4.** Sunt doua liste **disjuncte** (nu au niciun element comun)? Intoarce `True` sau `False`. Ai o metoda gata facuta, dar scrie-o si cu un `set` si o bucla.
""")
    c.ex("""
def sunt_disjuncte(a, b):
    pass  # TODO
""", """
def sunt_disjuncte(a, b):
    return set(a).isdisjoint(b)
""")
    c.cod("""
verifica('sunt_disjuncte', sunt_disjuncte,
         [(([1, 2, 3], [4, 5]), True), (([1, 2, 3], [3, 4]), False), (([], []), True)],
         ascunse=[(([1], [1]), False), ((list(range(0, 20_000, 2)), list(range(1, 20_000, 2))), True),
                  ((list(range(20_000)), [19_999]), False)])
""")

    c.md("""
**Exercitiul 5.** Numarul de cuvinte **distincte** dintr-un text. Cuvintele se despart dupa spatii, iar `Ana` si `ana` sunt acelasi cuvant (transforma in litere mici).
""")
    c.ex("""
def cuvinte_distincte(text):
    pass  # TODO
""", """
def cuvinte_distincte(text):
    return len(set(text.lower().split()))
""")
    c.cod("""
verifica('cuvinte_distincte', cuvinte_distincte,
         [(('Ana are mere si ana are pere',), 5), (('a a a',), 1), (('',), 0)],
         ascunse=[(('Un Om Un om',), 2), (('unu doi trei',), 3), (('  spatii   multe  ',), 2)])
""")

    c.md("""
**Exercitiul 6.** Din `v` lipseste un singur numar dintre `1, 2, ..., n`. Toate celelalte apar exact o data, in orice ordine. `v` are `n - 1` elemente. Gaseste numarul lipsa.
""")
    c.ex("""
def numar_lipsa(v, n):
    pass  # TODO
""", """
def numar_lipsa(v, n):
    return (set(range(1, n + 1)) - set(v)).pop()
""")
    c.cod("""
import random
def _lipsa_aleator():
    n = random.randint(2, 500)
    lipsa = random.randint(1, n)
    v = [x for x in range(1, n + 1) if x != lipsa]
    random.shuffle(v)
    return (v, n)

verifica('numar_lipsa', numar_lipsa,
         [(([1, 2, 4], 4), 3), (([2, 3], 3), 1), (([1], 2), 2)],
         referinta=lambda v, n: n * (n + 1) // 2 - sum(v), generator=_lipsa_aleator,
         indiciu='diferenta dintre {1..n} si set(v) are un singur element')
""")

    c.md("""
**Exercitiul 7.** Program ca la concurs. Pe prima linie `n`, pe a doua cele `n` numere. Afiseaza pe primul rand **cate valori distincte** sunt, iar pe al doilea rand valorile distincte **in ordine crescatoare**, separate prin spatiu.
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    n = int(input())
    v = list(map(int, input().split()))
    unice = sorted(set(v))
    print(len(unice))
    print(*unice)
""")
    c.cod("""
verifica_program('valori distincte', main,
                 [(['6', '4 9 2 9 4 1'], '4\\n1 2 4 9'), (['3', '5 5 5'], '1\\n5')],
                 ascunse=[(['1', '-3'], '1\\n-3'), (['5', '3 2 1 0 -1'], '5\\n-1 0 1 2 3')],
                 indiciu='sorted(set(v)) si print(*lista)')
scor()
""")

    c.md("""
## Recapitulare

- `set()` e multimea goala; `{}` e un dictionar. Elementele sunt distincte, fara ordine si fara index.
- `add`, `remove` (KeyError), `discard` (fara eroare), `pop` (element oarecare), `in`.
- `|` reuniune, `&` intersectie, `-` diferenta, `^` diferenta simetrica (si metodele lor). `<=` submultime, `isdisjoint`.
- Elementele trebuie sa fie hashabile: numere, texte, tupluri. Lista in set da `TypeError`.
- `x in set` e O(1) in medie (tabela hash), `x in lista` e O(n). Construirea setului e O(n).
- Capcane: `1 == 1.0 == True`, multimea nu tine frecventele (anagrame), nu modifici in timpul parcurgerii.
- ML: `set(y)` pentru clase, vocabular NLP, `set(train) & set(test)` pentru scurgeri de date.

Tema are mai multe exercitii cu teste ascunse, un "repara codul", doua programe si o provocare care da time limit cu liste.
""")
    c.salveaza('05-multimi-predare')


def tema():
    c = Carnet('Multimi (set)', 'tema', fisiere=FISIERE)
    c.md("""
Exercitiile de acasa. Testele vizibile iti arata daca ai inteles enuntul, cele **ascunse** verifica si cazurile limita (liste goale, dubluri, date mari). Poti rula o celula de verificare de cate ori vrei; `scor()` de la final aduna tot.

Cand rezultatul e o colectie, il cerem ca **lista sortata**, ca sa poata fi comparat.
""")

    c.md("""
### 1. Diferenta simetrica

Intoarce, ca lista sortata, elementele care apar in **exact una** dintre listele `a` si `b` (fara dubluri).
""")
    c.ex("""
def diferenta_simetrica(a, b):
    pass  # TODO
""", """
def diferenta_simetrica(a, b):
    return sorted(set(a) ^ set(b))
""")
    c.cod("""
verifica('diferenta_simetrica', diferenta_simetrica,
         [(([1, 2, 3], [2, 3, 4]), [1, 4]), (([1, 1], [1]), []), (([], [5, 5]), [5])],
         ascunse=[(([1, 2], [3, 4]), [1, 2, 3, 4]), (([], []), []), (([7, 8, 9], [9, 8, 7]), [])], puncte=1)
""")

    c.md("""
### 2. Cuvinte comune

Primesti doua texte. Intoarce, ca lista sortata, cuvintele care apar in **amandoua** (fara diferenta intre litere mari si mici, cuvintele se despart dupa spatii, iar rezultatul e cu litere mici).
""")
    c.ex("""
def cuvinte_comune(t1, t2):
    pass  # TODO
""", """
def cuvinte_comune(t1, t2):
    return sorted(set(t1.lower().split()) & set(t2.lower().split()))
""")
    c.cod("""
verifica('cuvinte_comune', cuvinte_comune,
         [(('Ana are mere', 'ana are pere'), ['ana', 'are']), (('a b', 'c d'), []), (('X x x', 'x'), ['x'])],
         ascunse=[(('', 'a'), []), (('Doi DOI trei', 'trei doi'), ['doi', 'trei']), (('un om', 'UN OM'), ['om', 'un'])], puncte=2)
""")

    c.md("""
### 3. Primul element care se repeta

Parcurgi lista de la stanga la dreapta. Intoarce **primul element care a mai aparut inainte**, sau `None` daca toate sunt distincte. `[2, 5, 1, 5, 2]` da `5` (al doilea `5` apare inaintea celui de-al doilea `2`).
""")
    c.ex("""
def primul_repetat(v):
    pass  # TODO
""", """
def primul_repetat(v):
    vazute = set()
    for x in v:
        if x in vazute:
            return x
        vazute.add(x)
    return None
""")
    c.cod("""
verifica('primul_repetat', primul_repetat,
         [(([2, 5, 1, 5, 2],), 5), (([1, 2, 3],), None), (([4, 4],), 4)],
         ascunse=[(([],), None), (([1, 2, 3, 2, 1],), 2), (([7],), None), ((list(range(100_000)) + [3],), 3)], puncte=2)
""")

    c.md("""
### 4. Anagrame

Doua cuvinte sunt anagrame daca au **aceleasi litere, de acelasi numar de ori**. Intoarce `True`/`False`. Atentie: `set` singur nu ajunge, se pierde numarul de aparitii (`'aab'` si `'abb'` au aceeasi multime de litere).
""")
    c.ex("""
def anagrame(s, t):
    pass  # TODO
""", """
def anagrame(s, t):
    return sorted(s) == sorted(t)
""")
    c.cod("""
verifica('anagrame', anagrame,
         [(('roma', 'amor'), True), (('ana', 'nana'), False), (('aab', 'abb'), False)],
         ascunse=[(('', ''), True), (('a', 'a'), True), (('abc', 'cab'), True), (('abc', 'abd'), False), (('aa', 'a'), False)],
         indiciu='set(s) == set(t) e gresit: nu numara aparitiile', puncte=2)
""")

    c.md("""
### 5. Duplicatul si lipsa

Lista `v` are `n` numere din `1..n` (n >= 2). Un numar apare de **doua ori**, iar altul **lipseste**. Intoarce perechea `(duplicat, lipsa)`. De exemplu `[1, 2, 2, 4]` da `(2, 3)`.
""")
    c.ex("""
def duplicat_si_lipsa(v):
    pass  # TODO
""", """
def duplicat_si_lipsa(v):
    n = len(v)
    distincte = set(v)
    duplicat = sum(v) - sum(distincte)
    lipsa = n * (n + 1) // 2 - sum(distincte)
    return duplicat, lipsa
""")
    c.cod("""
verifica('duplicat_si_lipsa', duplicat_si_lipsa,
         [(([1, 2, 2, 4],), (2, 3)), (([3, 1, 3],), (3, 2)), (([2, 2],), (2, 1))],
         ascunse=[(([1, 1],), (1, 2)), (([4, 3, 2, 4],), (4, 1)), (([5, 1, 2, 3, 3],), (3, 4))], puncte=2)
""")

    c.md("""
### 6. Repara codul: multimea care e dictionar

Functia trebuie sa numere valorile distincte din `v`, dar crapa. Ruleaza animatia si vezi mesajul, apoi repar-o.
""")
    c.cod("""
%%vezi
unice = {}
for x in [3, 1, 3]:
    unice.add(x)
""")
    c.ex("""
def valori_distincte(v):
    unice = {}
    for x in v:
        unice.add(x)
    return len(unice)
""", """
def valori_distincte(v):
    unice = set()
    for x in v:
        unice.add(x)
    return len(unice)
""")
    c.cod("""
verifica('valori_distincte', valori_distincte,
         [(([3, 1, 3],), 2), (([],), 0), (([5, 5, 5],), 1)],
         ascunse=[(([1, 2, 3, 4],), 4), ((list('abracadabra'),), 5)],
         indiciu='cum se face o multime goala?', puncte=1)
""")

    c.md("""
### 7. Repara codul: numerele negative

Functia primeste o **multime** si trebuie sa intoarca multimea fara numerele negative. Codul actual da eroare. Repar-o.
""")
    c.ex("""
def fara_negative(s):
    for x in s:
        if x < 0:
            s.remove(x)
    return s
""", """
def fara_negative(s):
    return {x for x in s if x >= 0}
""")
    c.cod("""
verifica('fara_negative', fara_negative,
         [(({1, -2, 3},), {1, 3}), (({-1, -2, -3},), set()), (({5, 6},), {5, 6})],
         ascunse=[((set(),), set()), (({0, -1, 2, -3, 4, -5},), {0, 2, 4}), ((set(range(-50, 50)),), set(range(0, 50)))],
         indiciu='nu modifica multimea in timp ce o parcurgi', puncte=1)
""")

    c.md("""
### 8. Program: scurgere de date

Pe prima linie sunt id-urile exemplelor de **antrenare**, pe a doua id-urile din **test** (numere separate prin spatiu). Daca nu au niciun id comun, afiseaza `OK`. Altfel afiseaza `SCAPARE k`, unde `k` e numarul de id-uri **distincte** comune. Testele ascunse au sute de mii de id-uri.
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    train = set(input().split())
    test = set(input().split())
    comune = train & test
    print(f'SCAPARE {len(comune)}' if comune else 'OK')
""")
    c.cod("""
mare1 = ' '.join(map(str, range(100_000)))
mare2 = ' '.join(map(str, range(100_000, 200_000)))
mare3 = ' '.join(map(str, range(99_990, 199_990)))
verifica_program('scurgere de date', main,
                 [(['1 2 3', '4 5 6'], 'OK'), (['1 2 3 4', '3 4 5'], 'SCAPARE 2')],
                 ascunse=[(['1 1 2', '1'], 'SCAPARE 1'), (['7', '7 7 7'], 'SCAPARE 1'), ([mare1, mare2], 'OK'), ([mare1, mare3], 'SCAPARE 10')],
                 indiciu='set(input().split()) pentru fiecare linie, apoi intersectie', puncte=2, timp=5)
""")

    c.md("""
### 9. Program: cuvinte distincte

Pe o singura linie ai un text. Afiseaza numarul de cuvinte **distincte** (fara diferenta intre litere mari si mici).
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    text = input()
    print(len(set(text.lower().split())))
""")
    c.cod("""
verifica_program('cuvinte distincte', main,
                 [(['Ana are mere si ana are pere'], '5'), (['a A a'], '1')],
                 ascunse=[(['unu doi trei'], '3'), (['x'], '1'), ([' '.join(['abc', 'ABC', 'abd'] * 5000)], '2')], puncte=2)
""")

    c.md("""
### 10. Provocare: doua numere cu suma data

Intoarce `True` daca exista **doua pozitii diferite** `i != j` cu `v[i] + v[j] == s`, altfel `False`. Acelasi element nu se poate folosi de doua ori: in `[5, 1]` nu exista pereche cu suma 10, dar in `[5, 5]` exista.

Cu doua bucle imbricate (sau `s - x in v` pe lista) primesti **time limit** la testele mari (`n = 100 000`). Cu un set, o singura trecere e de ajuns: pentru fiecare `x`, te uiti daca `s - x` a mai aparut inainte.
""")
    c.ex("""
def exista_pereche(v, s):
    pass  # TODO: O(n), cu un set
""", """
def exista_pereche(v, s):
    vazute = set()
    for x in v:
        if s - x in vazute:
            return True
        vazute.add(x)
    return False
""")
    c.cod("""
import random
mare = [2 * i for i in range(100_000)]          # toate numerele pare
random.Random(1).shuffle(mare)
verifica('exista_pereche', exista_pereche,
         [(([1, 4, 5, 3], 8), True), (([1, 2, 3], 10), False), (([5, 1], 10), False), (([5, 5], 10), True)],
         ascunse=[(([], 0), False), (([3], 6), False), (([-2, 7, 9], 8), False), (([-2, 9, 1], 7), True),
                  ((mare, 3), False), ((mare, 2 * 99_999 + 2 * 99_998), True), ((mare, 2 * 99_999 * 2), False)],
         puncte=3, timp=3)
scor()
""")
    c.salveaza('05-multimi-tema')


if __name__ == '__main__':
    predare()
    tema()
