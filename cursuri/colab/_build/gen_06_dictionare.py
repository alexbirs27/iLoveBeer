"""Genereaza 06-dictionare-predare.ipynb si 06-dictionare-tema.ipynb (+ variantele cu solutii)."""
from nb import Carnet


def predare():
    c = Carnet('Dictionare', 'predare', fisiere=('date/elevi.csv',))

    c.md("""
## Ce e un dictionar

O lista te lasa sa cauti dupa **pozitie**: `note[2]`. Dar cine e elementul 2? Un dictionar te lasa sa cauti dupa **nume**: `note['ana']`. Fiecare element e o pereche `cheie: valoare`, ca intr-o agenda (dupa nume gasesti numarul).

Dictionarul e cea mai folosita structura din Python dupa liste. Numarat, grupat, cautat repede, coduri pentru categorii, vocabulare de cuvinte, obiecte JSON: totul e dictionar. Il vei folosi si in Pandas fara sa-ti dai seama.

Cheile sunt **unice** si cautarea dupa cheie e rapida (in medie `O(1)`, adica nu conteaza cate elemente sunt). Vezi mai jos de ce.
""")

    c.md("""
## 1. Creare, acces, adaugare, stergere

Acolade, perechi `cheie: valoare` separate prin virgula. Cauti cu `d[cheie]`. Aceeasi paranteza patrata scrie: cheie noua se adauga, cheie veche isi schimba valoarea.

**Prezice:** cate elemente are `note` la final? (Uita-te la ultimele doua modificari.)

<details><summary>Raspuns</summary>

3. `'eli'` e cheie noua (se adauga), dar `'dan'` exista deja: ii schimbi doar valoarea. Cheile sunt unice, nu poti avea doi `'dan'`.
</details>
""")
    c.cod("""
%%vezi
note = {'ana': 9, 'dan': 7}
x = note['ana']                 #: cauti dupa cheie, nu dupa pozitie
note['eli'] = 10                #: cheie noua: se adauga
note['dan'] = 8                 #: cheie existenta: se suprascrie valoarea
del note['ana']                 #: del sterge perechea
y = note.pop('eli')             #: pop sterge si iti da valoarea inapoi
z = note.pop('kiwi', -1)        #: cu al doilea argument, cheia lipsa nu crapa
note.update({'mihai': 5, 'dan': 6})   #: adauga/suprascrie mai multe deodata
print(len(note), x, y, z)
""")

    c.md("""
## 2. Cand cheia lipseste

`d[cheie]` pe o cheie care nu exista da **`KeyError`**. E cea mai frecventa eroare cu dictionare. Doua remedii: `.get(cheie, implicit)` da o valoare de rezerva (sau `None` daca nu ii dai una), iar `cheie in d` intreaba **daca exista cheia** (`True` / `False`). Atentie: `in` se uita doar la chei, nu la valori.

In animatie, ultima linie crapa: programul se opreste chiar acolo, iar linia rosie iti arata unde.
""")
    c.cod("""
%%vezi
note = {'ana': 9, 'dan': 7}
a = note.get('mihai')           #: .get nu crapa: da None
b = note.get('mihai', 0)        #: sau valoarea ta implicita
if 'mihai' in note:             #: 'in' cauta printre CHEI
    print('are nota')
else:
    print('nu are nota')
print(7 in note)                #: 7 e o valoare, nu o cheie: False
print(note['mihai'])            #: fara .get, cheia lipsa: KeyError
print('aici nu ajunge')
""")

    c.md("""
## 3. Parcurgerea

`for k in d` da **cheile**. Pentru valori: `.values()`. Pentru amandoua deodata: `.items()`, care da perechi `(cheie, valoare)`. Din 3.7, dictionarul tine ordinea in care ai adaugat cheile.

**Prezice:** in ce ordine apar cheile la `print(list(d))`?
```python
d = {}
d['z'] = 1
d['a'] = 2
d['m'] = 3
d['z'] = 99
```

<details><summary>Raspuns</summary>

`['z', 'a', 'm']`. Ordinea e cea a **primei** aparitii a cheii. Cand suprascrii `'z'` ea ramane pe locul ei. (Nu e sortare! Nu e alfabetica, e ordinea de adaugare.)
</details>
""")
    c.cod("""
%%vezi
note = {'ana': 9, 'dan': 7, 'eli': 10}
total = 0
for nume in note:                  #: fara nimic altceva, parcurgi cheile
    total += note[nume]
for nume, nota in note.items():    #: items() da perechi (cheie, valoare)
    print(nume, nota)
print(list(note.keys()), list(note.values()))
""")

    c.md("""
## 4. Ce poate fi cheie

Cheia trebuie sa fie **hashable**, adica un lucru care nu se schimba: `int`, `float`, `str`, `bool`, `tuple` (de lucruri nemodificabile). O **lista nu poate** fi cheie, nici alt dictionar, nici un set.

De ce? Dictionarul calculeaza din cheie un numar (`hash`) care ii spune unde sa o caute. Daca cheia s-ar putea schimba, numarul s-ar schimba si perechea s-ar pierde. Vezi imediat cum lucreaza asta.

Tuplurile sunt cheile potrivite pentru coordonate: `(linie, coloana)`.
""")
    c.cod("""
%%vezi
harta = {}
harta[(0, 0)] = 'start'         #: un tuplu e ok ca cheie
harta[(2, 3)] = 'iesire'
print(harta[(2, 3)])
harta[[1, 2]] = 'lista'         #: lista nu e hashable: TypeError
""")

    c.md("""
## 5. De ce e rapid

Cautarea intr-o lista de perechi te obliga sa te uiti la fiecare pereche pana o gasesti: `O(n)`. Dictionarul face altceva: transforma cheia intr-un numar si se duce **direct** la locul potrivit.

Varianta de topor, cu numere: 8 "sertare", iar cheia `k` merge in sertarul `k % 8`. Ca sa o cauti, deschizi un singur sertar, nu pe toate. Python are un mecanism mai fin, dar ideea e aceasta.
""")
    c.cod("""
%%vezi
tabel = [[] for _ in range(8)]        #: 8 sertare goale
for cheie in [3, 10, 5, 13]:
    sertar = cheie % 8                #: numarul cheii spune in ce sertar o punem
    tabel[sertar].append(cheie)       #: 13 % 8 = 5, ca la 5: doua chei in acelasi sertar (coliziune)
gasit = 13 in tabel[13 % 8]           #: cautare: deschizi UN sertar si te uiti doar prin cateva chei
""")
    c.md("""
Acum masuram. Aceleasi date, o data intr-o lista de perechi, o data intr-un dictionar. Cautam de 300 de ori cheia care e ultima in lista (cel mai rau caz). Cu `n` de 10 ori mai mare, lista devine de 10 ori mai lenta, dictionarul ramane la fel. De aceea, cand un exercitiu spune "pentru fiecare element, cauta ceva", gandeste-te prima data la un dictionar.
""")
    c.cod("""
import time

n = 20000
perechi = [(i, i * i) for i in range(n)]      # lista de perechi (cheie, valoare)
d = dict(perechi)                             # aceleasi date, ca dictionar

t0 = time.perf_counter()
for _ in range(300):
    for cheie, val in perechi:                # scanare pana gasesti
        if cheie == n - 1:
            break
t1 = time.perf_counter()
for _ in range(300):
    val = d[n - 1]                            # un singur pas
t2 = time.perf_counter()

print(f'lista de perechi: {t1 - t0:.4f} s')
print(f'dictionar:        {t2 - t1:.6f} s')
print(f'dictionarul e de circa {(t1 - t0) / (t2 - t1):.0f} ori mai rapid')
""")

    c.md("""
## 6. Numaratul: de topor, apoi scurtaturi

Problema cea mai des intalnita: **de cate ori apare fiecare?** Litere intr-un text, cuvinte intr-o propozitie, clase intr-un set de date.

**Din topor** - dictionarul incepe gol. Cand vezi un element, daca il ai deja ii cresti numarul, altfel il pornesti de la 1:
""")
    c.cod("""
%%vezi
text = 'ana'
frecv = {}
for c in text:
    if c in frecv:                #: am mai vazut litera asta
        frecv[c] = frecv[c] + 1
    else:
        frecv[c] = 1              #: prima aparitie
frecv2 = {}                       #: SCURTATURA 1: .get(c, 0) da 0 cand litera nu e inca in dictionar
for c in text:
    frecv2[c] = frecv2.get(c, 0) + 1     #: nu mai ai nevoie de if
""")
    c.md("""
**Scurtatura 2** - dupa `if` si `.get`, `Counter` din `collections` face exact acest lucru, gata scris. E un dictionar in plus cu cateva metode utile. Nu trebuie sa il memorezi (la olimpiada ai documentatia), dar trebuie sa poti scrie de mana ce face.

**Prezice:** ce afiseaza `Counter('banana').most_common(1)`?

<details><summary>Raspuns</summary>

`[('a', 3)]`. Nu doar `'a'`: e o **lista** de perechi `(element, numar)`, cu cele mai frecvente primele.
</details>
""")
    c.cod("""
from collections import Counter

f = Counter('banana')
print(f)
print(f.most_common(2))     # cele mai frecvente 2, ca lista de perechi
print(f['z'])               # cheie lipsa: 0, nu KeyError
print(dict(f) == {'b': 1, 'a': 3, 'n': 2})

# Mai rapid decat bucla ta? Un milion de litere. Ambele fac o trecere (O(n)),
# dar bucla din Counter ruleaza in C, nu in Python.
import random, time

text = ''.join(random.choice('abcdefghij') for _ in range(10**6))

t0 = time.perf_counter()
frecv = {}
for c in text:
    frecv[c] = frecv.get(c, 0) + 1
t1 = time.perf_counter()
f = Counter(text)
t2 = time.perf_counter()

print(f'de mana: {t1 - t0:.3f} s   Counter: {t2 - t1:.3f} s')
print('acelasi rezultat:', frecv == f)
""")

    c.md("""
## 7. Sortarea dupa valoare

Un dictionar nu se sorteaza direct. Sortezi lista lui de perechi, `d.items()`, si spui **dupa ce** sa sorteze cu `key=`. `key` primeste o functie care, dat fiind un element (aici o pereche), intoarce ce vrei sa compari. Functiile le inveti in notebook-ul 07; deocamdata copiezi forma `lambda p: p[1]` ("pentru perechea `p`, ia elementul de pe pozitia 1", adica valoarea).

**Prezice:** `ana` si `eli` au amandoua 8 puncte. In ce ordine apar la sortare descrescatoare dupa valoare, cu `reverse=True`?

<details><summary>Raspuns</summary>

`ana` inainte de `eli`. Sortarea din Python e **stabila**: elementele cu aceeasi cheie isi pastreaza ordinea initiala, chiar si cu `reverse=True`.
</details>
""")
    c.cod("""
puncte = {'ana': 8, 'dan': 9, 'eli': 8, 'mihai': 5}

print(sorted(puncte.items(), key=lambda p: p[1], reverse=True))       # dupa valoare, descrescator
print(sorted(puncte.items(), key=lambda p: (-p[1], p[0])))            # egalitate: alfabetic dupa nume
print(dict(sorted(puncte.items(), key=lambda p: p[1])))               # dict nou, crescator
print(max(puncte, key=puncte.get))                                    # doar cheia cu valoarea cea mai mare
""")

    c.md("""
## 8. Gruparea

Numaratul da `cheie -> numar`. Gruparea da `cheie -> lista de elemente`: pui cuvintele intr-o "cutie" dupa prima litera, elevii dupa clasa, imaginile dupa eticheta. Din topor, cu grija la prima aparitie a cheii:
""")
    c.cod("""
%%vezi
cuvinte = ['ana', 'bob', 'alex', 'bea', 'dan']
grupe = {}
for w in cuvinte:
    k = w[0]                      #: regula de grupare: prima litera
    if k not in grupe:
        grupe[k] = []             #: prima data cand vedem grupa: lista goala
    grupe[k].append(w)
""")
    c.cod("""
import collections

cuvinte = ['ana', 'bob', 'alex', 'bea', 'dan']

grupe = {}
for w in cuvinte:
    grupe.setdefault(w[0], []).append(w)     # setdefault: pune [] doar daca lipseste, si o intoarce

grupe2 = collections.defaultdict(list)       # defaultdict: face asta singur la orice cheie noua
for w in cuvinte:
    grupe2[w[0]].append(w)

print(grupe)
print(grupe == grupe2)
""")

    c.md("""
## 9. Dictionare in dictionare

Valoarea poate fi orice: numar, text, lista, alt dictionar. Asa modelezi lucruri cu mai multe campuri. Citesti cu un sir de paranteze patrate: mai intai iei valoarea de sus, apoi pe cea dinauntru.
""")
    c.cod("""
%%vezi
elev = {'nume': 'Ana', 'clasa': 10, 'note': {'info': 9, 'mate': 8}, 'olimpiade': ['ONIA', 'OJI']}
print(elev['note']['info'])         #: doua paranteze: intai 'note', apoi 'info'
elev['note']['fizica'] = 10         #: adaugi in dictionarul din interior
elev['olimpiade'].append('ONI')     #: sau in lista din interior
""")
    c.cod("""
import json

# O lista de dictionare e un TABEL: fiecare dictionar e un rand, cheile sunt numele coloanelor.
# Asa arata datele in JSON, formatul in care primesti date de la aproape orice API.
# Si un DataFrame din Pandas e, la baza, un dictionar de coloane.
clasa = [{'nume': 'Ana', 'nota': 9}, {'nume': 'Dan', 'nota': 7}]
print(sorted(clasa, key=lambda r: r['nota'])[0]['nume'])     # cel cu nota cea mai mica

text = json.dumps(clasa)            # dictionar Python -> text JSON
print(text)
print(json.loads(text) == clasa)    # si inapoi
""")

    c.md("""
## 10. Dictionar prin comprehensiune

Ca la liste: `{cheie: valoare for ... in ...}`, cu `if` la sfarsit daca vrei sa filtrezi. Prima data varianta pe care o stii, apoi cea scurta:
""")
    c.cod("""
patrate = {}
for x in range(5):
    patrate[x] = x * x

patrate2 = {x: x * x for x in range(5)}
print(patrate == patrate2)

scumpe = {nume: pret for nume, pret in {'pix': 3, 'carte': 40, 'ghiozdan': 120}.items() if pret > 10}
print(scumpe)

invers = {v: k for k, v in {'a': 1, 'b': 2}.items()}      # cheile devin valori si invers
print(invers)
""")

    c.md("""
## 11. Unde apare in ML

Trei lucruri pe care le vei face in orice proiect cu date, de fiecare data cu un dictionar. Le scriem de mana, apoi vezi ca bibliotecile fac exact asta.

### Codificarea etichetelor

Un model lucreaza cu numere, nu cu cuvinte. Prima idee: fiecare categorie primeste un numar. Dictionarul `eticheta -> cod` se construieste pe parcurs, iar `len(cod)` este mereu urmatorul numar liber:
""")
    c.cod("""
%%vezi
clase = ['pisica', 'caine', 'pisica', 'pasare', 'caine']
cod = {}
for e in clase:
    if e not in cod:
        cod[e] = len(cod)              #: urmatorul numar liber = cate coduri avem deja
y = [cod[e] for e in clase]            #: fiecare eticheta e inlocuita cu codul ei
invers = {v: k for k, v in cod.items()}    #: dictionarul invers: din cod inapoi in eticheta
""")
    c.md("""
`LabelEncoder` din scikit-learn face acelasi lucru, doar ca numeroteaza in ordine **alfabetica** (la tine e ordinea in care apar). Varianta alfabetica de mana: `{e: i for i, e in enumerate(sorted(set(clase)))}`. O vei scrie in tema.

### One-hot

Problema cu numerele de mai sus: modelul crede ca `pasare (2)` e "mai mare" decat `caine (0)`. Pentru categorii fara ordine, faci cate o **coloana de 0 si 1** pentru fiecare categorie. Rezultatul e un dictionar de liste (adica un tabel, pe coloane):
""")
    c.cod("""
%%vezi
clase = ['pisica', 'caine', 'pisica']
unice = ['caine', 'pisica']
one_hot = {}
for u in unice:
    one_hot[u] = [1 if e == u else 0 for e in clase]     #: coloana lui u: 1 unde eticheta e u
""")
    c.md("""
### Bag of words

Un text nu e un numar. Ii dai numere astfel: alegi un **vocabular** (dictionar `cuvant -> pozitie`), iar propozitia devine un vector cu cate un numar pe pozitie: de cate ori apare cuvantul. Asta e `CountVectorizer` din scikit-learn, iar prelucrarea textului e in programa ONIA.
""")
    c.cod("""
%%vezi
vocabular = {'ana': 0, 'are': 1, 'mere': 2, 'pere': 3}     #: fiecare cuvant are o pozitie fixa
propozitie = 'ana are mere mere'
vector = [0] * len(vocabular)                #: [0, 0, 0, 0]
for w in propozitie.split():
    vector[vocabular[w]] += 1                #: pozitia cuvantului creste cu 1
""")
    c.cod("""
# Un mic corpus, de mana, comparat cu scikit-learn (care numeroteaza cuvintele alfabetic, deci facem la fel)
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

corpus = ['ana are mere', 'ana are mere mere', 'dan are pere']

vocabular = {}
for prop in corpus:
    for w in prop.split():
        vocabular[w] = 0
vocabular = {w: i for i, w in enumerate(sorted(vocabular))}

matrice = []
for prop in corpus:
    vector = [0] * len(vocabular)
    for w in prop.split():
        vector[vocabular[w]] += 1
    matrice.append(vector)

cv = CountVectorizer()
X = cv.fit_transform(corpus).toarray()
print(vocabular)
print(cv.get_feature_names_out().tolist())
print(np.array(matrice))
verifica_egal('bag of words = CountVectorizer', np.array(matrice), X)
""")
    c.md("""
(Vectorii reali sunt aproape numai zerouri, asa ca bibliotecile ii tin "rar", fara zerouri. Ideea ramane cea de mai sus.)

### Frecventa claselor din `elevi.csv`

Inainte sa antrenezi orice, te uiti cate exemple are fiecare clasa. Citim fisierul cu modulul `csv` (Pandas vine mai tarziu): `DictReader` da fiecare rand ca dictionar `nume_coloana -> text`. Aproape doua treimi din elevi sunt `0` la `calificat`: un "model" care raspunde mereu `0` are deci vreo 67% acuratete fara sa invete nimic. De aceea te uiti la distributia claselor inainte sa te bucuri de o acuratete.
""")
    c.cod("""
import csv

with open('date/elevi.csv') as f:
    randuri = list(csv.DictReader(f))      # lista de dictionare: cate unul pe rand

print(len(randuri), randuri[0])
print(Counter([r['calificat'] for r in randuri]))
print(Counter([r['meditatii'] for r in randuri]))     # acelasi Counter te prinde si cand datele sunt murdare

# medie pe grupe, fara Pandas: dictionar de liste, apoi media fiecarei liste (sarim peste valorile lipsa)
# Peste cateva notebook-uri asta devine df.groupby('clasa')['nota_info'].mean()
note_pe_clasa = {}
for r in randuri:
    if r['nota_info'] != '':
        note_pe_clasa.setdefault(r['clasa'], []).append(float(r['nota_info']))

for clasa in sorted(note_pe_clasa):
    n = note_pe_clasa[clasa]
    print(clasa, len(n), round(sum(n) / len(n), 2))
""")

    c.md("""
## 12. Capcane

**Capcana 1: modifici dictionarul cat il parcurgi.** Python te opreste cu `RuntimeError`:
""")
    c.cod("""
%%vezi
note = {'ana': 4, 'dan': 9, 'eli': 3}
for nume in note:
    if note[nume] < 5:
        del note[nume]           #: stergi din dict in timp ce il parcurgi: RuntimeError
""")
    c.cod("""
# Solutia: parcurgi o COPIE a cheilor (list(note)) si modifici originalul
note = {'ana': 4, 'dan': 9, 'eli': 3}
for nume in list(note):              # list(note) e o copie a cheilor
    if note[nume] < 5:
        del note[nume]
print(note)

note = {'ana': 4, 'dan': 9, 'eli': 3}
print({k: v for k, v in note.items() if v >= 5})     # sau: dict nou, fara sa-l modifici pe cel vechi
""")
    c.md("""
**Capcana 2: `dict.fromkeys(chei, [])` pune ACEEASI lista la toate cheile.** Nu cate o lista pentru fiecare: una singura, cu mai multe nume. Uita-te la eticheta `@1` din animatie: e semnul ca e acelasi obiect in doua locuri.

**Prezice:** ce contine `grupe['b']` dupa linia 2?

<details><summary>Raspuns</summary>

`[1]`, desi ai modificat doar `grupe['a']`. Lista e una singura. Corect: `{k: [] for k in chei}`, care creeaza o lista noua la fiecare cheie.
</details>
""")
    c.cod("""
%%vezi
grupe = dict.fromkeys(['a', 'b'], [])   #: aceeasi lista pusa la ambele chei
grupe['a'].append(1)                    #: modifici lista lui 'a'...
ok = {k: [] for k in ['a', 'b']}        #: varianta corecta: cate o lista noua
ok['a'].append(1)
""")
    c.md("""
**Capcana 3: `1`, `1.0` si `True` sunt aceeasi cheie.** Sunt egale si au acelasi `hash`, deci dictionarul le vede ca pe una. Pierzi date fara nicio eroare, mai ales cand amesteci numere intregi si zecimale din date citite.

**Capcana 4: `b = a` nu copiaza.** Sunt doua nume pentru acelasi dictionar (la fel ca la liste). Copia se face cu `.copy()` (superficiala: dictionarele si listele din interior raman comune) sau cu `copy.deepcopy`.

**Capcana 5: `defaultdict` creeaza cheia si cand doar citesti din el.** O cautare "nevinovata" adauga o cheie noua.
""")
    c.cod("""
import copy

# capcana 3
d = {}
d[1] = 'int'
d[1.0] = 'float'
d[True] = 'bool'
print(d, len(d), hash(1) == hash(1.0) == hash(True))

# capcana 4
a = {'x': 1, 'lista': [1, 2]}
b = a
c = a.copy()
e = copy.deepcopy(a)
b['x'] = 99                # a se schimba, b e acelasi obiect
c['lista'].append(3)       # a se schimba si aici: lista din interior e comuna
print(a, a is b, a is c, a is e)
print(e)

# capcana 5
g = collections.defaultdict(list)
g['a'].append(1)
if g['zzz']:               # doar ne uitam...
    pass
print(dict(g))             # ...dar 'zzz' a aparut in dictionar
""")

    c.md("""
### Cum citesti eroarea

Ultima linie iti spune ce s-a intamplat. Cele patru erori tipice cu dictionare (primele trei le-ai vazut deja in animatii mai sus):

| eroare | de obicei inseamna |
|---|---|
| `KeyError: 'mihai'` | ai cerut `d['mihai']`, dar cheia nu exista. Foloseste `.get` sau verifica cu `in` |
| `TypeError: unhashable type: 'list'` | ai pus o lista (sau dict, set) drept cheie. Transforma in tuplu |
| `RuntimeError: dictionary changed size during iteration` | ai adaugat/sters chei in timp ce parcurgeai. Parcurge `list(d)` |
| `TypeError: 'dict' object is not callable` | ai scris `d('ana')` cu paranteze rotunde in loc de `d['ana']` |

Ultima:
""")
    c.cod("""
%%vezi
puncte = {'ana': 9}
print(puncte('ana'))            #: paranteze rotunde = apel de functie. Aici trebuiau [ ]
""")

    c.md("""
## Exercitii

Fiecare exercitiu are o celula de completat si una de verificare. Incearca intai de mana (`for`, `if`, `.get`), `Counter` si `defaultdict` sunt permise dar nu obligatorii.
""")

    c.md("""
**Exercitiul 1.** Intoarce un dictionar cu **de cate ori apare fiecare caracter** din text (inclusiv spatiile si literele mari, separat de cele mici).
""")
    c.ex("""
def frecventa(text):
    pass  # TODO: caracter -> numar de aparitii
""", """
def frecventa(text):
    frecv = {}
    for ch in text:
        frecv[ch] = frecv.get(ch, 0) + 1
    return frecv
""")
    c.cod("""
import random
from collections import Counter

verifica('frecventa', frecventa, [(('banana',), {'b': 1, 'a': 3, 'n': 2}), (('',), {}), (('aAa',), {'a': 2, 'A': 1})],
         ascunse=[(('a b a',), {'a': 2, ' ': 2, 'b': 1}), (('zzzz',), {'z': 4})],
         referinta=lambda t: dict(Counter(t)),
         generator=lambda: (''.join(random.choice('ab cD') for _ in range(random.randint(0, 30))),),
         indiciu='dictionar gol, apoi frecv[ch] = frecv.get(ch, 0) + 1')
""")

    c.md("""
**Exercitiul 2.** Inverseaza un dictionar: din `{cheie: valoare}` intoarce `{valoare: cheie}`. Valorile sunt unice.
""")
    c.ex("""
def inverseaza(d):
    pass  # TODO
""", """
def inverseaza(d):
    return {v: k for k, v in d.items()}
""")
    c.cod("""
verifica('inverseaza', inverseaza,
         [(({'a': 1, 'b': 2},), {1: 'a', 2: 'b'}), (({},), {})],
         ascunse=[(({'ana': 'A', 'dan': 'D', 'eli': 'E'},), {'A': 'ana', 'D': 'dan', 'E': 'eli'}), (({1: 2},), {2: 1})])
""")

    c.md("""
**Exercitiul 3.** Combina doua dictionare cu valori numerice intr-unul nou: cheile din oricare, iar la cheile comune **aduni** valorile. Nu modifica dictionarele primite.
""")
    c.ex("""
def combina(d1, d2):
    pass  # TODO
""", """
def combina(d1, d2):
    rez = dict(d1)
    for k, v in d2.items():
        rez[k] = rez.get(k, 0) + v
    return rez
""")
    c.cod("""
verifica('combina', combina,
         [(({'a': 1, 'b': 2}, {'b': 3, 'c': 4}), {'a': 1, 'b': 5, 'c': 4}), (({}, {'x': 1}), {'x': 1})],
         ascunse=[(({'x': 5}, {}), {'x': 5}), (({'a': 1, 'b': 1}, {'a': 1, 'b': 1}), {'a': 2, 'b': 2}),
                  (({'a': 0.5}, {'a': 0.25}), {'a': 0.75})],
         indiciu='porneste de la o copie a lui d1, apoi adauga fiecare pereche din d2 cu .get')
""")

    c.md("""
**Exercitiul 4.** Cel mai frecvent cuvant dintr-un text (cuvintele sunt separate prin spatii, nu conteaza litera mare/mica). La egalitate, intoarce-l pe cel mai mic **alfabetic**. Textul are cel putin un cuvant.
""")
    c.ex("""
def cuvant_frecvent(text):
    pass  # TODO
""", """
def cuvant_frecvent(text):
    frecv = {}
    for w in text.lower().split():
        frecv[w] = frecv.get(w, 0) + 1
    return min(frecv, key=lambda w: (-frecv[w], w))
""")
    c.cod("""
verifica('cuvant_frecvent', cuvant_frecvent,
         [(('la fel ca la ea',), 'la'), (('b a b a',), 'a'), (('Ana ana ANA dan',), 'ana')],
         ascunse=[(('unul',), 'unul'), (('z y x',), 'x'), (('a b c a b c d',), 'a')],
         indiciu='numara cu .get, apoi alege dupa (-numar, cuvant): min cu key= pe o pereche')
""")

    c.md("""
**Exercitiul 5.** Grupeaza cuvintele dupa **lungime**: intoarce `{lungime: [cuvintele cu acea lungime, in ordinea data]}`.
""")
    c.ex("""
def grupeaza_dupa_lungime(cuvinte):
    pass  # TODO
""", """
def grupeaza_dupa_lungime(cuvinte):
    grupe = {}
    for w in cuvinte:
        grupe.setdefault(len(w), []).append(w)
    return grupe
""")
    c.cod("""
verifica('grupeaza_dupa_lungime', grupeaza_dupa_lungime,
         [((['ana', 'are', 'mere', 'pe'],), {3: ['ana', 'are'], 4: ['mere'], 2: ['pe']}), (([],), {})],
         ascunse=[((['a', 'b', 'cc', 'd'],), {1: ['a', 'b', 'd'], 2: ['cc']}), ((['xyz'],), {3: ['xyz']})])
""")

    c.md("""
**Exercitiul 6.** Vector bag-of-words: pentru o propozitie si un `vocabular` (`cuvant -> pozitie`) intoarce lista cu de cate ori apare fiecare cuvant din vocabular. Cuvintele care nu sunt in vocabular se ignora.
""")
    c.ex("""
def vector_bow(propozitie, vocabular):
    pass  # TODO
""", """
def vector_bow(propozitie, vocabular):
    v = [0] * len(vocabular)
    for w in propozitie.split():
        if w in vocabular:
            v[vocabular[w]] += 1
    return v
""")
    c.cod("""
voc = {'ana': 0, 'are': 1, 'mere': 2, 'pere': 3}
verifica('vector_bow', vector_bow,
         [(('ana are mere mere', voc), [1, 1, 2, 0]), (('', voc), [0, 0, 0, 0]), (('pere pere pere', voc), [0, 0, 0, 3])],
         ascunse=[(('dan are pere', voc), [0, 1, 0, 1]), (('ana', {'ana': 0}), [1]), (('x y z', voc), [0, 0, 0, 0])],
         indiciu='vectorul are len(vocabular) pozitii; foloseste `w in vocabular` ca sa sari cuvintele necunoscute')
""")

    c.md("""
**Exercitiul 7.** Program ca la concurs. Pe prima linie este `n`, apoi `n` cuvinte, cate unul pe linie. Afiseaza fiecare cuvant distinct, in ordine alfabetica, urmat de un spatiu si de numarul lui de aparitii.
""")
    c.ex("""
def main():
    pass  # TODO: citeste n, apoi cuvintele; afiseaza 'cuvant numar' pentru fiecare, alfabetic
""", """
def main():
    n = int(input())
    frecv = {}
    for _ in range(n):
        w = input()
        frecv[w] = frecv.get(w, 0) + 1
    for w in sorted(frecv):
        print(w, frecv[w])
""")
    c.cod("""
verifica_program('numara cuvinte', main,
                 [(['4', 'ana', 'are', 'ana', 'mere'], 'ana 2\\nare 1\\nmere 1'), (['1', 'x'], 'x 1')],
                 ascunse=[(['5', 'b', 'a', 'b', 'a', 'b'], 'a 2\\nb 3'), (['3', 'z', 'y', 'x'], 'x 1\\ny 1\\nz 1')],
                 indiciu='pentru ordine alfabetica: for w in sorted(frecv)')
scor()
""")

    c.md("""
## Recapitulare

- Dictionar = perechi `cheie: valoare`, cheile unice si **hashable** (nu liste). Cautarea dupa cheie e `O(1)` in medie; in lista de perechi e `O(n)`.
- `d[k]` pe cheie lipsa = `KeyError`. Alternative: `d.get(k, implicit)` si `k in d` (doar chei).
- `for k in d`, `d.values()`, `d.items()`. Ordinea = ordinea adaugarii. `sorted(d.items(), key=...)` pentru sortare.
- Numarat: `d[k] = d.get(k, 0) + 1`, apoi `Counter`. Grupat: `setdefault(k, [])`, apoi `defaultdict(list)`.
- Capcane: nu modifici dictionarul cat il parcurgi; `fromkeys(chei, [])` imparte o singura lista; `1`, `1.0`, `True` sunt aceeasi cheie; `b = a` nu copiaza.
- In ML: codificarea etichetelor, one-hot, bag of words, frecventa claselor, media pe grupe. Toate sunt dictionare scrise de mana.

Tema are exercitii cu teste ascunse: anagrame, un `two-sum` care trebuie sa fie rapid si un program de concurs.
""")
    c.salveaza('06-dictionare-predare')


def tema():
    c = Carnet('Dictionare', 'tema', fisiere=('date/elevi.csv',))
    c.md("""
Exercitii de acasa. Testele vizibile iti arata daca ai inteles enuntul, cele **ascunse** verifica si cazurile limita (text gol, chei care lipsesc, date mari). La final, `scor()` aduna tot.

Cateva exercitii au o parte "gandeste-te la complexitate": o solutie corecta dar lenta pica pe testele mari.
""")

    c.md("""
### 1. Primul caracter unic

Intoarce primul caracter din `text` care apare **o singura data**, sau `None` daca nu exista. De ex. `'aabcb' -> 'c'`, `'abab' -> None`.
""")
    c.ex("""
def prima_unica(text):
    pass  # TODO
""", """
def prima_unica(text):
    frecv = {}
    for ch in text:
        frecv[ch] = frecv.get(ch, 0) + 1
    for ch in text:
        if frecv[ch] == 1:
            return ch
    return None
""")
    c.cod("""
verifica('prima_unica', prima_unica, [(('aabcb',), 'c'), (('abab',), None), (('x',), 'x')],
         ascunse=[(('',), None), (('aabbccd',), 'd'), (('abcabcz',), 'z'), (('leetcode',), 'l')],
         indiciu='doua treceri: prima numara, a doua cauta in ordinea textului', puncte=1)
""")

    c.md("""
### 2. Cele mai frecvente k cuvinte

Intoarce lista celor `k` cuvinte cele mai frecvente, ca perechi `(cuvant, numar)`. Sortare: mai intai dupa numar (descrescator), apoi alfabetic. Cuvintele sunt separate prin spatiu; nu conteaza litera mare/mica (le scrii cu litere mici). Daca sunt mai putin de `k` cuvinte distincte, le intorci pe toate.
""")
    c.ex("""
def top_k(text, k):
    pass  # TODO
""", """
def top_k(text, k):
    frecv = {}
    for w in text.lower().split():
        frecv[w] = frecv.get(w, 0) + 1
    perechi = sorted(frecv.items(), key=lambda p: (-p[1], p[0]))
    return perechi[:k]
""")
    c.cod("""
verifica('top_k', top_k,
         [(('a b a c b a', 2), [('a', 3), ('b', 2)]), (('x y', 5), [('x', 1), ('y', 1)]), (('Ana ana ANA b', 1), [('ana', 3)])],
         ascunse=[(('', 3), []), (('z y x', 2), [('x', 1), ('y', 1)]), (('b a b a c', 2), [('a', 2), ('b', 2)])],
         indiciu='sorted(frecv.items(), key=lambda p: (-p[1], p[0])), apoi taie cu [:k]', puncte=2)
""")

    c.md("""
### 3. Grupuri de anagrame

Doua cuvinte sunt anagrame daca au aceleasi litere (`'ana'` si `'naa'`). Grupeaza cuvintele in liste de anagrame. Intoarce **doar grupurile cu cel putin doua cuvinte**, ca lista de liste: grupurile in ordinea primei aparitii, iar in fiecare grup cuvintele in ordinea data.

Indiciu: doua anagrame au acelasi `sorted(cuvant)`. Cheia trebuie sa fie hashable, deci `''.join(sorted(cuvant))` (un `str`), nu lista.
""")
    c.ex("""
def anagrame(cuvinte):
    pass  # TODO
""", """
def anagrame(cuvinte):
    grupe = {}
    for w in cuvinte:
        grupe.setdefault(''.join(sorted(w)), []).append(w)
    return [g for g in grupe.values() if len(g) >= 2]
""")
    c.cod("""
import random

def anagrame_ref(cuvinte):
    g = {}
    for w in cuvinte:
        g.setdefault(''.join(sorted(w)), []).append(w)
    return [x for x in g.values() if len(x) > 1]

verifica('anagrame', anagrame,
         [((['ana', 'mere', 'naa', 'emer', 'x'],), [['ana', 'naa'], ['mere', 'emer']]), (([],), []), ((['a', 'b'],), [])],
         ascunse=[((['abc', 'cba', 'bca', 'abd'],), [['abc', 'cba', 'bca']]), ((['a', 'a'],), [['a', 'a']])],
         referinta=anagrame_ref,
         generator=lambda: ([''.join(random.choice('abc') for _ in range(random.randint(1, 4))) for _ in range(12)],),
         puncte=2)
""")

    c.md("""
### 4. Codificarea etichetelor

Primesti o lista de etichete text. Intoarce o pereche `(coduri, mapare)`: `mapare` da fiecarei etichete distincte un numar, in **ordine alfabetica** (prima eticheta alfabetic primeste `0`), iar `coduri` e lista etichetelor inlocuite cu numerele lor. Exact ca `LabelEncoder`.
""")
    c.ex("""
def codifica(etichete):
    pass  # TODO: (coduri, mapare)
""", """
def codifica(etichete):
    mapare = {e: i for i, e in enumerate(sorted(set(etichete)))}
    return [mapare[e] for e in etichete], mapare
""")
    c.cod("""
verifica('codifica', codifica,
         [((['pisica', 'caine', 'pisica', 'pasare'],), ([2, 0, 2, 1], {'caine': 0, 'pasare': 1, 'pisica': 2})),
          (([],), ([], {}))],
         ascunse=[((['b', 'a', 'b'],), ([1, 0, 1], {'a': 0, 'b': 1})), ((['x'],), ([0], {'x': 0}))],
         puncte=2)
""")

    c.md("""
### 5. One-hot

Din lista de etichete intoarce un dictionar: pentru fiecare eticheta distincta, o lista de `0` / `1` (una pe pozitie in lista originala): `1` unde eticheta de acolo este cea a cheii. De ex. `['a', 'b', 'a'] -> {'a': [1, 0, 1], 'b': [0, 1, 0]}`.
""")
    c.ex("""
def one_hot(etichete):
    pass  # TODO
""", """
def one_hot(etichete):
    return {u: [1 if e == u else 0 for e in etichete] for u in set(etichete)}
""")
    c.cod("""
verifica('one_hot', one_hot,
         [((['a', 'b', 'a'],), {'a': [1, 0, 1], 'b': [0, 1, 0]}), (([],), {})],
         ascunse=[((['x', 'x'],), {'x': [1, 1]}), ((['c', 'a', 'b'],), {'a': [0, 1, 0], 'b': [0, 0, 1], 'c': [1, 0, 0]})],
         puncte=2)
""")

    c.md("""
### 6. Calificati pe clasa din `elevi.csv`

Citeste fisierul CSV de la calea `cale` (cu modulul `csv`) si intoarce un dictionar `{clasa: cati_elevi_calificati}`, cu `clasa` **numar intreg**. Un elev e calificat cand coloana `calificat` este `'1'`. Numara toate randurile din fisier, exact cum sunt.

Sablon de citire: `csv.DictReader(f)` da, pentru fiecare rand, un dictionar `{'clasa': '12', 'calificat': '1', ...}` (totul e text!).
""")
    c.ex("""
import csv


def calificati_pe_clasa(cale):
    pass  # TODO
""", """
import csv


def calificati_pe_clasa(cale):
    rez = {}
    with open(cale) as f:
        for r in csv.DictReader(f):
            k = int(r['clasa'])
            rez[k] = rez.get(k, 0) + (1 if r['calificat'] == '1' else 0)
    return rez
""")
    c.cod("""
import os, tempfile
import pandas as pd

mic = os.path.join(tempfile.gettempdir(), 'mic_06.csv')      # fisier de test, in folderul temporar
with open(mic, 'w') as f:
    f.write('id,clasa,calificat\\n1,9,1\\n2,9,0\\n3,10,1\\n4,10,1\\n5,12,0\\n')

# rezultatul corect il calculam aici cu Pandas (o vei putea face si tu intr-o linie, curand)
corect = {int(k): int(v) for k, v in pd.read_csv('date/elevi.csv').groupby('clasa')['calificat'].sum().items()}

verifica('calificati_pe_clasa', calificati_pe_clasa,
         [(('date/elevi.csv',), corect), ((mic,), {9: 1, 10: 2, 12: 0})],
         indiciu='clasa e text in CSV: int(r["clasa"]); numeri doar cand r["calificat"] == "1", dar cheia trebuie creata si pentru 0', puncte=2)
""")

    c.md("""
### 7. Repara codul

Functia trebuie sa grupeze cuvintele dupa prima litera, dar cuvintele ajung in **toate** grupele. Uita-te in animatie unde apare eticheta `@1` si gaseste vinovatul.
""")
    c.cod("""
%%vezi
cuvinte = ['ana', 'bob', 'alex']
grupe = dict.fromkeys([w[0] for w in cuvinte], [])
for w in cuvinte:
    grupe[w[0]].append(w)
""")
    c.ex("""
def grupeaza_dupa_prima(cuvinte):
    grupe = dict.fromkeys([w[0] for w in cuvinte], [])
    for w in cuvinte:
        grupe[w[0]].append(w)
    return grupe
""", """
def grupeaza_dupa_prima(cuvinte):
    grupe = {w[0]: [] for w in cuvinte}
    for w in cuvinte:
        grupe[w[0]].append(w)
    return grupe
""")
    c.cod("""
verifica('grupeaza_dupa_prima', grupeaza_dupa_prima,
         [((['ana', 'bob', 'alex'],), {'a': ['ana', 'alex'], 'b': ['bob']}), (([],), {})],
         ascunse=[((['x'],), {'x': ['x']}), ((['ab', 'ba', 'ac', 'bc'],), {'a': ['ab', 'ac'], 'b': ['ba', 'bc']})],
         indiciu='dict.fromkeys(chei, []) pune aceeasi lista la toate cheile', puncte=1)
""")

    c.md("""
### 8. Program: modul unui sir

Pe prima linie este `n`, pe a doua `n` numere intregi separate prin spatiu. Afiseaza **valoarea care apare cel mai des** si de cate ori apare, separate prin spatiu. La egalitate, valoarea cea mai mica.
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    n = int(input())
    v = list(map(int, input().split()))
    frecv = {}
    for x in v:
        frecv[x] = frecv.get(x, 0) + 1
    best = min(frecv, key=lambda x: (-frecv[x], x))
    print(best, frecv[best])
""")
    c.cod("""
verifica_program('modul', main,
                 [(['6', '1 2 2 3 3 3'], '3 3'), (['4', '5 5 7 7'], '5 2'), (['1', '-4'], '-4 1')],
                 ascunse=[(['5', '9 8 7 6 5'], '5 1'), (['7', '0 0 1 1 2 2 -1'], '0 2'), (['3', '-2 -2 -1'], '-2 2')],
                 indiciu='numara cu un dictionar, alege cu min si key=(-frecventa, valoare)', puncte=2)
""")

    c.md("""
### 9. Provocare: doua numere cu suma data

Ai o lista `v` de numere intregi si un numar `tinta`. Exista **exact o pereche** de pozitii `i < j` cu `v[i] + v[j] == tinta`. Intoarce `(i, j)` ca tuplu.

Solutia cu doua bucle are complexitate `O(n^2)`: la 200000 de numere ar dura ore. Cu un dictionar merge in `O(n)`: pentru fiecare `x` te intrebi "am vazut deja `tinta - x`?" si ii tii minte pozitia. Testele ascunse au liste mari si timp limitat.
""")
    c.ex("""
def doua_sume(v, tinta):
    pass  # TODO: intoarce (i, j)
""", """
def doua_sume(v, tinta):
    vazut = {}
    for j, x in enumerate(v):
        if tinta - x in vazut:
            return vazut[tinta - x], j
        vazut[x] = j
""")
    c.cod("""
import random

rnd = random.Random(2026)
mare = rnd.sample(range(10**15), 200000)          # valori distincte, foarte multe, suma perechii e unica in practica
tinta_mare = mare[123] + mare[199000]

verifica('doua_sume', doua_sume,
         [(([2, 7, 11, 15], 9), (0, 1)), (([3, 2, 4], 6), (1, 2)), (([3, 3], 6), (0, 1))],
         ascunse=[(([1, 5, 9, 14], 23), (2, 3)), (([-3, 4, 3, 90], 0), (0, 2)), ((mare, tinta_mare), (123, 199000))],
         indiciu='dictionar valoare -> pozitie; pentru fiecare x verifica daca tinta - x e deja in el', timp=3, puncte=3)
""")

    c.md("""
### 10. Catalog imbricat

`catalog` e un dictionar de dictionare de liste: `{elev: {materie: [note]}}`. Scrie functia care adauga o nota si **modifica `catalog` pe loc** (nu intoarce nimic). Daca elevul sau materia nu exista, le creezi.
""")
    c.ex("""
def adauga_nota(catalog, elev, materie, nota):
    pass  # TODO: modifica catalog pe loc
""", """
def adauga_nota(catalog, elev, materie, nota):
    catalog.setdefault(elev, {}).setdefault(materie, []).append(nota)
""")
    c.cod("""
verifica('adauga_nota', adauga_nota,
         [(({'ana': {'info': [9]}}, 'ana', 'info', 10), {'ana': {'info': [9, 10]}}),
          (({}, 'dan', 'mate', 7), {'dan': {'mate': [7]}})],
         ascunse=[(({'ana': {'info': [9]}}, 'ana', 'mate', 8), {'ana': {'info': [9], 'mate': [8]}}),
                  (({'ana': {}}, 'dan', 'info', 5), {'ana': {}, 'dan': {'info': [5]}})],
         in_loc=True, indiciu='setdefault(elev, {}) si apoi setdefault(materie, []), apoi append', puncte=2)
scor()
""")
    c.salveaza('06-dictionare-tema')


if __name__ == '__main__':
    predare()
    tema()
