"""Genereaza 08-clase-predare.ipynb si 08-clase-tema.ipynb (+ variantele cu solutii)."""
from nb import Carnet


def predare():
    c = Carnet('Clase si obiecte', 'predare', fisiere=('anim_clase.py',))

    c.md(r"""
## De ce clase

Pana acum ai avut date (liste, dictionare) si functii care le prelucreaza, separate. O **clasa** le pune impreuna: datele si functiile care au voie sa le schimbe stau in acelasi loc.

Nu e un moft. `scikit-learn` e facut din clase. Uite un model real, cu tot ce vei scrie tu singur la sfarsitul notebook-ului:
""")
    c.cod(r"""
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=3)      # creezi un obiect din clasa
model.fit([[0], [1], [2], [3]], [0, 0, 1, 1])     # metoda fit: invata (isi retine datele)
print(model.predict([[0.4], [2.6]]))             # metoda predict: da raspunsurile
""")
    c.md(r"""
`KNeighborsClassifier` e **clasa**, `model` e un **obiect**, `fit` si `predict` sunt **metode**. La fel arata `StandardScaler`, `LinearRegression`, `DecisionTreeClassifier`: acelasi tipar, alta matematica in spate. Daca il intelegi o data, le intelegi pe toate.

Cum lucram: in animatiile `%%vezi` obiectele apar ca niste casete cu atributele lor, iar cand rulezi o metoda vezi in memorie un cadru nou, cu `self`. Uita-te mai ales la ce se schimba (clipeste).
""")

    c.md(r"""
## 1. Din topor: un punct fara clase

Un punct e doua numere. Fara clase il tii intr-un dictionar si scrii o functie separata care il muta:
""")
    c.cod(r"""
%%vezi
p = {'x': 1, 'y': 2}

def muta(p, dx):
    p['x'] += dx      #: functia sta in afara datelor. Nimic nu ne opreste sa scriem p['z'] = 5 sau sa uitam o cheie

muta(p, 3)
""")
    c.md(r"""
Merge. Dar datele (`p`) si functiile lor (`muta`) sunt lucruri separate, iar cine citeste codul trebuie sa ghiceasca ce functie merge cu ce dictionar. Clasa le leaga.
""")

    c.md(r"""
## 2. Clasa si obiectul

**Clasa** e planul: ce atribute are un punct si ce stie sa faca. **Obiectul** e un punct concret construit dupa plan. Dintr-o clasa faci oricate obiecte, fiecare cu datele lui.

`__init__` se ruleaza singur cand scrii `Punct(1, 2)` (se numeste constructor). `self` e obiectul care se construieste chiar atunci. Tu nu scrii `self` la apel, il pune Python.
""")
    c.cod(r"""
%%vezi
class Punct:
    def __init__(self, x, y):
        self.x = x       #: self e obiectul nou, inca gol. Il umplem cu atribute
        self.y = y

p = Punct(1, 2)         #: Punct(...) construieste obiectul si ruleaza __init__
q = Punct(5, 0)         #: alt obiect, alte valori, acelasi plan
p.x = 10                #: schimbam doar p. q ramane cum era
""")

    c.md(r"""
## 3. `self`: cum stie metoda pe ce obiect lucreaza

`p.muta(3)` arata ca o functie apelata "pe" `p`. In spate, Python face `Punct.muta(p, 3)`: primul parametru, `self`, este chiar obiectul din fata punctului.

In animatie, cand esti in `muta`, `self` si `p` au aceeasi eticheta (`@1`). Nu sunt doua obiecte, e **acelasi** obiect cu doua nume.
""")
    c.cod(r"""
%%vezi
class Punct:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def muta(self, dx):
        self.x += dx      #: self este obiectul p (vezi @1 in memorie)

p = Punct(1, 2)
p.muta(3)                #: asa scrii de obicei
Punct.muta(p, 3)         #: asa scrie Python in spate, cu p pus de mana
""")

    c.md(r"""
## 4. Cum se afiseaza un obiect: `__repr__` si `__str__`

**Prezice:** ce afiseaza `print(p)` pentru un `Punct` simplu, fara nicio metoda speciala?

<details><summary>Raspuns</summary>

Ceva de genul `<__main__.Punct object at 0x7f3a...>`: numele clasei si o adresa de memorie. Python nu are de unde sa stie cum vrei tu sa arate un punct.
</details>
""")
    c.cod(r"""
class Punct:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Punct(1, 2)
print(p)
""")
    c.md(r"""
`__repr__` intoarce textul cu care se afiseaza obiectul. Regula buna: sa arate ca *codul care il construieste*. Se foloseste si cand obiectul e intr-o lista sau intr-un mesaj de eroare, deci e cel mai util cand depanezi.

`__str__` e varianta "pentru oameni", folosita de `print` si de f-string. Daca o scrii doar pe una, scrie `__repr__`: `__str__` o foloseste cand lipseste.
""")
    c.cod(r"""
class Punct:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Punct({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'

p = Punct(1, 2)
print(p)                     # __str__
print([p, Punct(3, 4)])      # in liste apare __repr__
print(repr(p), f'{p}')
""")

    c.md(r"""
## 5. Atribute de instanta si atribute de clasa

- **atribut de instanta**: `self.nume = ...` in `__init__`. Fiecare obiect are al lui.
- **atribut de clasa**: scris direct in corpul clasei. E **unul singur**, comun tuturor obiectelor (bun pentru constante: `Cerc.PI`).

Cand citesti `a.scoala`, Python se uita intai in obiect si, daca nu gaseste, in clasa. Cand *scrii* `a.scoala = ...`, creezi mereu un atribut in obiect, care il "umbreste" pe cel din clasa. Urmareste ce apare in caseta lui `a`:
""")
    c.cod(r"""
%%vezi
class Elev:
    scoala = 'Liceul 1'       #: atribut de clasa: unul singur
    def __init__(self, nume):
        self.nume = nume      #: atribut de instanta: al fiecarui obiect

a = Elev('Ana')
b = Elev('Dan')
x = a.scoala                  #: a nu are scoala, Python o ia din clasa
Elev.scoala = 'Liceul 2'      #: schimbam in clasa: se vede la toti
y = b.scoala
a.scoala = 'Altul'            #: aici a primeste propriul atribut (apare in caseta lui a)
z = b.scoala                  #: b nu a fost afectat
""")

    c.md(r"""
## 6. Obiectele sunt referinte

Ca la liste: `b = a` nu copiaza obiectul, pune un al doilea nume pe el. Ti-a aparut deja eticheta `@1` mai sus.

**Prezice:** ce afiseaza ultima linie?

```python
a = Punct(1, 2)
b = a
b.x = 99
print(a.x)
```

<details><summary>Raspuns</summary>

`99`. Exista un singur obiect. `b.x = 99` l-a schimbat, iar `a` il vede la fel. Pentru o copie adevarata: `copy.copy(a)` (sau `copy.deepcopy` daca obiectul contine alte obiecte).
</details>
""")
    c.cod(r"""
%%vezi
import copy

class Punct:
    def __init__(self, x, y):
        self.x = x
        self.y = y

a = Punct(1, 2)
b = a                #: b nu e o copie: e al doilea nume al aceluiasi obiect (@1)
b.x = 99
c = copy.copy(a)     #: asta e copie: alt obiect (fara eticheta)
c.x = 0
r1 = a is b          #: 'is' intreaba daca e ACELASI obiect
r2 = a is c
""")
    c.md(r"""
Si la functii e la fel: daca dai un obiect unei functii, ea primeste **acelasi** obiect si il poate schimba. Metodele care isi schimba `self` fac exact asta.
""")

    c.md(r"""
## 7. `__eq__`: cand sunt doua obiecte egale

**Prezice:** `Punct(1, 2) == Punct(1, 2)`: `True` sau `False`?

<details><summary>Raspuns</summary>

`False`. Fara `__eq__`, `==` intreaba "sunt acelasi obiect?", nu "au aceleasi valori?". Sunt doua obiecte diferite, deci `False`. Trebuie sa-i explici tu ce inseamna egalitate.
</details>
""")
    c.cod(r"""
%%vezi
class A:
    def __init__(self, x):
        self.x = x

class B:
    def __init__(self, x):
        self.x = x
    def __eq__(self, other):
        return self.x == other.x      #: self e obiectul din stanga lui ==, other cel din dreapta

print(A(1) == A(1))     #: fara __eq__: compara identitatea, deci False
print(B(1) == B(1))     #: Python cheama B.__eq__(prima, a doua)
""")

    c.md(r"""
## 8. `__lt__` si sortarea obiectelor

`sorted` si `.sort()` compara elementele doar cu `<`. Daca obiectele tale stiu `__lt__`, se sorteaza direct, la fel si `min` si `max`.

Alternativa, de multe ori mai buna: `key=`, care nu cere sa modifici clasa si iti da libertatea sa sortezi dupa alt criteriu altadata.
""")
    c.cod(r"""
%%vezi
class Elev:
    def __init__(self, nume, nota):
        self.nume = nume
        self.nota = nota
    def __lt__(self, other):
        return self.nota < other.nota    #: "a e inaintea lui b" daca are nota mai mica

a = Elev('Ana', 9)
b = Elev('Dan', 7)
r = b < a                #: Python cheama b.__lt__(a)
lista = sorted([a, b])   #: sorted foloseste tot __lt__ (aici, o singura comparatie)
""")
    c.cod(r"""
class Elev:
    def __init__(self, nume, nota):
        self.nume = nume
        self.nota = nota
    def __repr__(self):
        return f'{self.nume}({self.nota})'
    def __lt__(self, other):
        return self.nota < other.nota

elevi = [Elev('Ana', 9), Elev('Dan', 7), Elev('Eva', 10), Elev('Bia', 9)]
print(sorted(elevi))                                    # dupa __lt__
print(max(elevi))                                       # si max foloseste <
print(sorted(elevi, key=lambda e: e.nume))              # alt criteriu, fara sa atingi clasa
print(sorted(elevi, key=lambda e: (-e.nota, e.nume)))   # nota descrescator, la egal dupa nume
""")

    c.md(r"""
## 9. Operatori: `__add__`

Cand scrii `a + b`, Python cheama `a.__add__(b)`. Poti da acest inteles oricarei clase. Vezi cadrul `__add__` din animatie: `self` e `a`, `other` e `b`.
""")
    c.cod(r"""
%%vezi
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)    #: construim alt obiect, nu le schimbam pe cele vechi

a = Vector2D(1, 2)
b = Vector2D(10, 20)
c = a + b                #: Python cheama a.__add__(b)
""")
    c.md(r"""
Alti operatori se cer la fel:

| scrii | Python cheama |
|---|---|
| `a + b`, `a - b`, `a * b` | `__add__`, `__sub__`, `__mul__` |
| `a == b`, `a < b` | `__eq__`, `__lt__` |
| `len(a)` | `__len__` |
| `a[i]` | `__getitem__` |
| `print(a)` / lista | `__str__` / `__repr__` |

Regula: supraincarci un operator doar cand intelesul e evident (vectori, fractii, bani). Un `Elev + Elev` n-are nicio semnificatie, deci nu-l scrie nimeni.
""")

    c.md(r"""
## 10. Compunere: "are un"

Un atribut poate fi la randul lui un obiect. Un `Cerc` **are un** centru, care e un `Punct`. Asta se numeste compunere si e cea mai des folosita legatura intre clase.
""")
    c.cod(r"""
%%vezi
class Punct:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Cerc:
    def __init__(self, centru, raza):
        self.centru = centru      #: un atribut poate fi alt obiect
        self.raza = raza
    def muta(self, dx, dy):
        self.centru.x += dx       #: mergem prin lant: cerc -> centru -> x
        self.centru.y += dy

c = Cerc(Punct(0, 0), 5)
c.muta(2, 3)
""")

    c.md(r"""
## 11. Mostenire si `super()`

Mostenirea spune "**este un**": un `Patrat` este un `Dreptunghi`. Clasa copil primeste tot ce are parintele si poate adauga sau *suprascrie* lucruri.

`super()` inseamna "clasa parinte". De obicei il folosesti in `__init__` ca sa lasi parintele sa-si puna atributele. In animatie vezi doua cadre `__init__` unul peste altul: intai al copilului, apoi al parintelui.
""")
    c.cod(r"""
%%vezi
class Dreptunghi:
    def __init__(self, l, L):
        self.l = l
        self.L = L
    def aria(self):
        return self.l * self.L

class Patrat(Dreptunghi):                 #: Patrat mosteneste din Dreptunghi
    def __init__(self, latura):
        super().__init__(latura, latura)  #: parintele pune l si L

p = Patrat(4)
a = p.aria()          #: Patrat n-are aria, dar o gaseste in Dreptunghi
""")
    c.md(r"""
Cum gaseste Python metoda `aria` pentru un `Patrat`? Urca pe lant: intai in clasa obiectului, apoi in parinte, apoi mai sus, pana la `object`. Prima gasita castiga. Asa functioneaza si suprascrierea: daca `Patrat` are propriul `descrie`, acela se opreste primul.

Aceleasi clase, acum in notebook, ca sa le poti folosi in animatia de mai jos:
""")
    c.cod(r"""
class Dreptunghi:
    def __init__(self, l, L):
        self.l = l
        self.L = L
    def aria(self):
        return self.l * self.L
    def descrie(self):
        return f'dreptunghi {self.l} x {self.L}'

class Patrat(Dreptunghi):
    def __init__(self, latura):
        super().__init__(latura, latura)
    def descrie(self):                    # suprascrie descrie din Dreptunghi
        return f'patrat cu latura {self.l}'

p = Patrat(4)
print(p.aria(), '|', p.descrie(), '|', isinstance(p, Dreptunghi))
anim_mro(Patrat, 'aria')
""")
    c.cod(r"""
anim_mro(Patrat, 'descrie')       # aici se opreste chiar in Patrat
""")
    c.md(r"""
**Prefera compunerea.** Mostenirea are sens cand relatia e cu adevarat "este un" si vrei sa refolosesti cod. In rest, "are un" (atribut care e obiect) e mai simpla si mai putin fragila. In practica vei scrie rar clase cu mostenire, dar clasele din scikit-learn le folosesc peste tot (de exemplu, toate modelele mostenesc `fit` sau `score` dintr-o clasa de baza).
""")

    c.md(r"""
## 12. `@property` si conventii

`@property` face o metoda sa se comporte ca un atribut (o scrii fara paranteze). E utila cand o valoare *se calculeaza* din altele si nu vrei sa o tii separat, ca sa nu se dezacordeze:
""")
    c.cod(r"""
class Cerc:
    def __init__(self, raza):
        self.raza = raza

    @property
    def diametru(self):
        return 2 * self.raza

c = Cerc(5)
print(c.diametru)     # fara paranteze
c.raza = 10
print(c.diametru)     # se recalculeaza singur
""")
    c.md(r"""
Conventii (nu reguli, Python nu interzice nimic):

- `_x` = "intern, nu te atinge din afara clasei". Python nu il apara, dar toata lumea intelege semnalul.
- Clasele se scriu `CamelCase`, metodele si atributele `snake_case`.
- O metoda care schimba obiectul intoarce de obicei `None`. Metodele din scikit-learn intorc `self` (`fit` intoarce `self`), ca sa poti scrie lanturi: `Model().fit(X, y).predict(Xt)`.
""")

    c.md(r"""
## 13. Cand NU faci o clasa

Clasa nu e mai "profesionista" decat o functie. Nu o folosi cand:

- ai o singura functie de apelat (o clasa cu `__init__` si o singura metoda e o functie deghizata);
- ai doar date simple, fara comportament: un tuplu, un dictionar (sau `namedtuple` / `dataclass`, pe care le vei intalni) sunt de ajuns;
- rezolvi o problema clasica de concurs: acolo aproape mereu functii, liste si dictionare bat clasele ca viteza de scris.

O clasa merita cand ai **stare care se schimba in timp** si mai multe operatii care o folosesc: un cont bancar, o stiva, un model care invata.
""")

    c.md(r"""
## 14. De ce clase pentru ML: `fit` si `predict`

Un model are **stare** (ce a invatat) si doua momente distincte:

- `fit(X, y)`: se uita la date si isi schimba starea (invata);
- `predict(X)`: foloseste ce a invatat, fara sa se schimbe.

Conventia scikit-learn: lucrurile invatate se pun in atribute care se termina cu `_` (`media_`, `min_`). Daca vezi `model.ceva_`, stii ca apare doar dupa `fit`.

### MediaRegressor

Cel mai simplu model posibil: prezice mereu **media** valorilor din antrenare. E prost, dar util: e baza de comparatie ("baseline"). Un model serios trebuie sa-l bata, altfel nu face nimic.

**Din topor**, fara clase, ai nevoie de doua functii si trebuie sa duci `medie` dupa tine peste tot:
""")
    c.cod(r"""
def antreneaza(y):
    return sum(y) / len(y)

def prezice(medie, X):
    return [medie] * len(X)

medie = antreneaza([100, 200, 150, 250])
print(prezice(medie, ['a', 'b', 'c']))
""")
    c.md(r"""
Cu un singur numar merge. Cand modelul invata cinci lucruri (media, minimul, maximul pe fiecare coloana...), duci cinci variabile dupa tine si le incurci. Clasa le pune intr-un singur obiect. Uita-te cum apare atributul `media_` abia dupa `fit`:
""")
    c.cod(r"""
%%vezi
class MediaRegressor:
    def fit(self, X, y):
        self.media_ = sum(y) / len(y)     #: atributul apare abia acum: modelul a "invatat"
        return self                       #: intoarcem self, ca in scikit-learn

    def predict(self, X):
        return [self.media_] * len(X)

model = MediaRegressor()                  #: obiect gol, nu stie nimic inca
model.fit([[50], [80], [60], [90]], [100, 200, 150, 250])
rez = model.predict([[70], [10]])         #: X nu conteaza: oricare ar fi intrarea, raspunsul e media
""")
    c.md(r"""
Acum clasa in notebook si o comparatie cu cea din scikit-learn (`DummyRegressor` cu `strategy='mean'` face exact asta):
""")
    c.cod(r"""
import numpy as np
from sklearn.dummy import DummyRegressor

class MediaRegressor:
    def fit(self, X, y):
        self.media_ = sum(y) / len(y)
        return self

    def predict(self, X):
        return [self.media_] * len(X)

X = [[50], [80], [60], [90]]
y = [100, 200, 150, 250]
Xt = [[70], [10], [55]]

al_meu = MediaRegressor().fit(X, y)
sk = DummyRegressor(strategy='mean').fit(X, y)
verifica_egal('MediaRegressor = DummyRegressor', np.array(al_meu.predict(Xt)), sk.predict(Xt))
""")

    c.md(r"""
### MinMaxScalerManual

Alta clasa pe care o vei tot intalni: **normalizarea**. Aduce valorile unei coloane in intervalul `[0, 1]` cu formula

`z = (x - min) / (max - min)`

De ce si cum o folosesti in ML vezi in notebook-urile 12 si 13. Aici ne intereseaza doar de ce e o clasa. **Din topor**, pentru o lista:
""")
    c.cod(r"""
v = [10, 20, 40]
mn, mx = min(v), max(v)
print([(x - mn) / (mx - mn) for x in v])
""")
    c.md(r"""
Problema: mai tarziu vin date noi (setul de test) si trebuie scalate **cu acelasi `mn` si `mx`** ca la antrenare, nu cu ale lor. Deci `mn` si `mx` trebuie *pastrate* undeva. Iata de ce e o clasa: `fit` le calculeaza si le tine, `transform` le foloseste oricand, `inverse_transform` face drumul invers (`x = z * (max - min) + min`).

**Prezice:** dupa `fit` pe `[10, 20, 40]`, ce iese la `transform` pentru valoarea `100`?

<details><summary>Raspuns</summary>

`(100 - 10) / (40 - 10) = 3.0`. Nu e o greseala: valorile noi pot iesi din `[0, 1]`, pentru ca `min` si `max` vin din antrenare. Scalerul nu "taie" nimic.
</details>
""")
    c.cod(r"""
%%vezi
import numpy as np

class MinMaxScalerManual:
    def fit(self, X):
        self.min_ = X.min(axis=0)         #: minimul pe fiecare coloana
        self.max_ = X.max(axis=0)
        return self
    def transform(self, X):
        return (X - self.min_) / (self.max_ - self.min_)
    def inverse_transform(self, Z):
        return Z * (self.max_ - self.min_) + self.min_
    def fit_transform(self, X):
        return self.fit(X).transform(X)   #: prescurtare: fit, apoi transform

tren = np.array([[2, 10], [4, 30], [6, 20], [10, 50]])
test = np.array([[12, 0]])
sc = MinMaxScalerManual()
z = sc.fit_transform(tren)               #: min_ si max_ se calculeaza pe antrenare
zt = sc.transform(test)                  #: pe test folosim aceleasi min_ si max_: iese din [0, 1]
inapoi = sc.inverse_transform(z)         #: ne intoarcem la valorile originale
""")
    c.md(r"""
Aceeasi clasa in notebook, verificata pe rand cu `MinMaxScaler` din scikit-learn:
""")
    c.cod(r"""
from sklearn.preprocessing import MinMaxScaler

class MinMaxScalerManual:
    def fit(self, X):
        self.min_ = X.min(axis=0)
        self.max_ = X.max(axis=0)
        return self

    def transform(self, X):
        return (X - self.min_) / (self.max_ - self.min_)

    def inverse_transform(self, Z):
        return Z * (self.max_ - self.min_) + self.min_

    def fit_transform(self, X):
        return self.fit(X).transform(X)

tren = np.array([[2., 10.], [4., 30.], [6., 20.], [10., 50.]])
test = np.array([[12., 0.], [5., 25.]])

al_meu = MinMaxScalerManual()
sk = MinMaxScaler()
verifica_egal('fit_transform', al_meu.fit_transform(tren), sk.fit_transform(tren))
verifica_egal('transform pe test', al_meu.transform(test), sk.transform(test))
verifica_egal('inverse_transform', al_meu.inverse_transform(sk.transform(test)), test)
verifica_egal('min_ si max_', np.array([al_meu.min_, al_meu.max_]), np.array([sk.data_min_, sk.data_max_]))
""")
    c.md(r"""
**De ce sunt `fit` si `transform` separate.** Ca sa poti face `fit` doar pe datele de antrenare si `transform` pe amandoua. Daca faci `fit` pe *tot* setul (inclusiv test), modelul a "vazut" testul: se numeste **scurgere de informatie** (data leakage) si da rezultate false. Vei vedea asta pe date reale mai tarziu.

Ce ai scris aici e, pe fond, ce face `MinMaxScaler`. Scikit-learn adauga tratarea cazurilor rare, dar scheletul e acesta.
""")

    c.md(r"""
## 15. Capcane

**Capcana 1: lista pusa la nivel de clasa.** Un atribut de clasa e unul singur. Daca e o lista, toti elevii o impart. Uita-te la etichetele `@1` din memorie:
""")
    c.cod(r"""
%%vezi
class Elev:
    note = []                        #: atribut de CLASA: o singura lista pentru toti
    def __init__(self, nume):
        self.nume = nume
    def adauga(self, n):
        self.note.append(n)          #: self.note nu exista in obiect, deci Python o ia din clasa

a = Elev('Ana')
b = Elev('Dan')
a.adauga(10)
note_a = a.note
note_b = b.note                      #: aceeasi lista (@1): Dan are nota 10 fara sa fi primit-o
""")
    c.md(r"""
Reparatia: lista trebuie creata **pentru fiecare obiect**, deci in `__init__`, cu `self.note = []`.
""")
    c.cod(r"""
class Elev:
    def __init__(self, nume):
        self.nume = nume
        self.note = []               # acum fiecare Elev isi are lista lui

a, b = Elev('Ana'), Elev('Dan')
a.note.append(10)
print(a.note, b.note)
""")

    c.md(r"""
**Capcana 2: valoare implicita mutabila.** Aceeasi boala, alta forma. Valoarea implicita a unui parametru se creeaza **o singura data**, cand se defineste functia, nu la fiecare apel:
""")
    c.cod(r"""
%%vezi
class Elev:
    def __init__(self, nume, note=[]):    #: lista implicita se face o singura data
        self.nume = nume
        self.note = note

a = Elev('Ana')
b = Elev('Dan')
a.note.append(10)                        #: ambii elevi au acum aceeasi lista (@1)
""")
    c.md(r"""
Reparatia clasica: `note=None` in semnatura, iar in corp `self.note = [] if note is None else note`. Regula: **niciodata `[]` sau `{}` ca valoare implicita.**

**Capcana 3: `__eq__` fara `__hash__`.** Cand definesti `__eq__`, Python scoate singur `__hash__` (doua obiecte egale ar trebui sa aiba acelasi hash, iar el nu poate garanta asta). Rezultat: obiectul nu mai intra in `set` si nu mai poate fi cheie de dictionar.
""")
    c.cod(r"""
%%vezi
class Punct:
    def __init__(self, x):
        self.x = x
    def __eq__(self, other):
        return self.x == other.x

p = Punct(1)
d = {p: 'a'}          #: cheile de dictionar trebuie sa aiba hash
""")
    c.md(r"""
Reparatia: definesti si `__hash__`, pe baza acelorasi atribute pe care le compara `__eq__`. Face sens doar daca obiectul nu se mai schimba dupa ce a intrat in set:
""")
    c.cod(r"""
class Punct:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))

print(len({Punct(1, 2), Punct(1, 2), Punct(3, 4)}))      # 2: cele doua Punct(1, 2) sunt unul singur
""")
    c.md(r"""
**Capcana 4: coloana constanta.** `MinMaxScalerManual` imparte la `max - min`. Daca o coloana are aceeasi valoare peste tot, e `0 / 0`:
""")
    c.cod(r"""
X = np.array([[1., 5.], [2., 5.], [3., 5.]])
print(MinMaxScalerManual().fit_transform(X))       # a doua coloana: nan, plus un avertisment
print(MinMaxScaler().fit_transform(X))             # scikit-learn pune 0
""")
    c.md(r"""
Scikit-learn tine cont de asta: cand `max - min` e 0, il inlocuieste cu 1. Asa arata diferenta dintre codul tau de antrenament si o biblioteca folosita de milioane de oameni: bucla de cazuri ciudate.
""")

    c.md(r"""
## 16. Cum citesti eroarea

Erorile de la clase sunt putine si se repeta. Le vezi in animatie: linia rosie e cea care a crapat.

**`TypeError: ... takes 1 positional argument but 2 were given`** - ai uitat `self` in definitia metodei. Cand scrii `p.muta(5)`, Python trimite si `p`, deci "2 argumente" (`p` si `5`), iar metoda are loc doar pentru unul.
""")
    c.cod(r"""
%%vezi
class Punct:
    def __init__(self, x):
        self.x = x
    def muta(dx):            #: aici lipseste self
        self.x += dx

p = Punct(1)
p.muta(5)
""")
    c.md(r"""
**`AttributeError: 'Punct' object has no attribute 'x'`** - ai scris `x = x` in loc de `self.x = x` (variabila locala dispare la sfarsitul lui `__init__`), sau ai gresit numele atributului.
""")
    c.cod(r"""
%%vezi
class Punct:
    def __init__(self, x):
        x = x                #: fara self, x ramane doar local

p = Punct(1)
print(p.x)
""")
    c.md(r"""
**`TypeError: __init__() missing 1 required positional argument`** - ai creat obiectul cu prea putine argumente.
""")
    c.cod(r"""
%%vezi
class Punct:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Punct(1)
""")
    c.md(r"""
**Erori scrise de tine cu `raise`.** Cand cineva foloseste gresit clasa ta (retrage mai mult decat are in cont), nu returna un numar ciudat: ridica o eroare cu un mesaj clar. Se prinde cu `try/except`.
""")
    c.cod(r"""
%%vezi
class Cont:
    def __init__(self, sold):
        self.sold = sold
    def retrage(self, suma):
        if suma > self.sold:
            raise ValueError('fonduri insuficiente')     #: oprim executia aici, cu mesaj
        self.sold -= suma

c = Cont(100)
c.retrage(30)
try:
    c.retrage(500)
except ValueError:
    mesaj = 'refuzat'            #: eroarea a fost prinsa, programul merge mai departe
""")
    c.md(r"""
| eroare | de obicei inseamna |
|---|---|
| `TypeError: ... but 2 were given` | ai uitat `self` in `def` |
| `TypeError: missing ... argument` | prea putine argumente la `Clasa(...)` |
| `AttributeError: ... has no attribute` | atribut nedefinit (`x = x` in loc de `self.x = x`, sau nume gresit) |
| `TypeError: unhashable type` | ai `__eq__` fara `__hash__` si folosesti obiectul in set / dict |
| `NameError: name 'x' is not defined` in metoda | ai scris `x` in loc de `self.x` |
""")

    c.md(r"""
## Exercitii

Le rezolvi tu. Fiecare exercitiu are o celula de completat (o clasa) si una de verificare. Verificarea creeaza obiecte din clasa ta si le foloseste, apoi compara cu ce trebuia sa iasa. Clasele goale (`pass`) pica, e normal.
""")

    c.md(r"""
**Exercitiul 1.** Clasa `Dreptunghi` cu constructorul `Dreptunghi(l, L)` si metodele `aria()`, `perimetru()`, `este_patrat()` (adevarat cand laturile sunt egale).
""")
    c.ex(r"""
class Dreptunghi:
    pass  # TODO: __init__(self, l, L), aria, perimetru, este_patrat
""", r"""
class Dreptunghi:
    def __init__(self, l, L):
        self.l = l
        self.L = L

    def aria(self):
        return self.l * self.L

    def perimetru(self):
        return 2 * (self.l + self.L)

    def este_patrat(self):
        return self.l == self.L
""")
    c.cod(r"""
def t_dreptunghi(l, L):
    d = Dreptunghi(l, L)
    return d.aria(), d.perimetru(), d.este_patrat()

verifica('Dreptunghi', t_dreptunghi, [((3, 4), (12, 14, False)), ((5, 5), (25, 20, True))],
         ascunse=[((1, 1), (1, 4, True)), ((0, 7), (0, 14, False)), ((2, 10), (20, 24, False))],
         indiciu='metodele apartin clasei: primul parametru e self, iar l si L se citesc cu self.l si self.L')
""")

    c.md(r"""
**Exercitiul 2.** Clasa `ContBancar` cu `ContBancar(sold=0)`, metodele `depune(suma)` si `retrage(suma)`, si atributul `sold`. Suma trebuie sa fie pozitiva, iar retragerea nu poate depasi soldul: in caz contrar ridica `ValueError` (si nu schimba soldul).
""")
    c.ex(r"""
class ContBancar:
    pass  # TODO: __init__(self, sold=0), depune, retrage (ValueError la suma gresita)
""", r"""
class ContBancar:
    def __init__(self, sold=0):
        self.sold = sold

    def depune(self, suma):
        if suma <= 0:
            raise ValueError('suma trebuie sa fie pozitiva')
        self.sold += suma

    def retrage(self, suma):
        if suma <= 0:
            raise ValueError('suma trebuie sa fie pozitiva')
        if suma > self.sold:
            raise ValueError('fonduri insuficiente')
        self.sold -= suma
""")
    c.cod(r"""
def t_cont(sold, operatii):
    cont = ContBancar(sold)
    rez = []
    for op, suma in operatii:
        try:
            getattr(cont, op)(suma)
            rez.append('ok')
        except ValueError:
            rez.append('eroare')
    return rez, cont.sold

verifica('ContBancar', t_cont,
         [((100, [('depune', 50), ('retrage', 30)]), (['ok', 'ok'], 120)),
          ((10, [('retrage', 50), ('depune', -5)]), (['eroare', 'eroare'], 10))],
         ascunse=[((0, [('retrage', 1)]), (['eroare'], 0)), ((5, [('retrage', 5)]), (['ok'], 0)),
                  ((5, [('depune', 0)]), (['eroare'], 5))],
         indiciu='if conditie: raise ValueError(...) la inceputul metodei, inainte sa modifici self.sold')
""")

    c.md(r"""
**Exercitiul 3.** Clasa `Vector2D(x, y)` cu suma (`+`), egalitate (`==`) si afisare de forma `Vector2D(1, 2)`.
""")
    c.ex(r"""
class Vector2D:
    pass  # TODO: __init__, __add__, __eq__, __repr__
""", r"""
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Vector2D({self.x}, {self.y})'
""")
    c.cod(r"""
def t_vector(a, b):
    u, v = Vector2D(*a), Vector2D(*b)
    s = u + v
    return repr(s), s == Vector2D(a[0] + b[0], a[1] + b[1]), u == v

verifica('Vector2D', t_vector, [(((1, 2), (3, 4)), ('Vector2D(4, 6)', True, False)),
                                (((1, 1), (1, 1)), ('Vector2D(2, 2)', True, True))],
         ascunse=[(((0, 0), (0, 0)), ('Vector2D(0, 0)', True, True)), (((-1, 5), (1, -5)), ('Vector2D(0, 0)', True, False))],
         indiciu='__add__ intoarce un Vector2D NOU; __repr__ intoarce un text (nu face print)')
""")

    c.md(r"""
**Exercitiul 4.** Clasa `Student(nume, nota)` care se sorteaza cu `sorted(...)` **fara** `key=`: mai intai dupa nota (crescator), iar la note egale dupa nume (alfabetic). Ai nevoie doar de `__lt__`. Trucul: compara tupluri, `(self.nota, self.nume) < (other.nota, other.nume)`.
""")
    c.ex(r"""
class Student:
    pass  # TODO: __init__(self, nume, nota) si __lt__
""", r"""
class Student:
    def __init__(self, nume, nota):
        self.nume = nume
        self.nota = nota

    def __lt__(self, other):
        return (self.nota, self.nume) < (other.nota, other.nume)
""")
    c.cod(r"""
import random

def t_student(date):
    return [s.nume for s in sorted(Student(n, x) for n, x in date)]

def ref_student(date):
    return [n for n, x in sorted(date, key=lambda t: (t[1], t[0]))]

def gen_student():
    return ([(random.choice('ABCDEFG'), random.randint(4, 10)) for _ in range(random.randint(0, 9))],)

verifica('Student', t_student,
         [((([('Ana', 9), ('Dan', 7), ('Eva', 10)]),), ['Dan', 'Ana', 'Eva']),
          ((([('Bia', 8), ('Ana', 8)]),), ['Ana', 'Bia'])],
         referinta=ref_student, generator=gen_student,
         indiciu='__lt__(self, other) intoarce True daca self trebuie sa fie inaintea lui other')
""")

    c.md(r"""
**Exercitiul 5.** Cel mai simplu clasificator: `MajoritateClasificator`. `fit(X, y)` retine cea mai frecventa clasa din `y` in `self.clasa_` (la egalitate, cea mai mica) si intoarce `self`. `predict(X)` intoarce o lista cu aceasta clasa pentru fiecare rand din `X`. In scikit-learn se cheama `DummyClassifier(strategy='most_frequent')` si e baseline-ul pentru clasificare.
""")
    c.ex(r"""
class MajoritateClasificator:
    pass  # TODO: fit (intoarce self) si predict
""", r"""
class MajoritateClasificator:
    def fit(self, X, y):
        numar = {}
        for e in y:
            numar[e] = numar.get(e, 0) + 1
        self.clasa_ = max(sorted(numar), key=lambda e: numar[e])
        return self

    def predict(self, X):
        return [self.clasa_] * len(X)
""")
    c.cod(r"""
import random
from sklearn.dummy import DummyClassifier

def t_maj(y, n):
    m = MajoritateClasificator().fit([[0]] * len(y), y)
    return m.predict([[0]] * n)

def ref_maj(y, n):
    return DummyClassifier(strategy='most_frequent').fit([[0]] * len(y), y).predict([[0]] * n).tolist()

verifica('MajoritateClasificator', t_maj,
         [(([0, 1, 1, 2], 3), [1, 1, 1]), (([5, 5, 7], 2), [5, 5])],
         ascunse=[(([1, 2], 2), [1, 1]), (([3], 1), [3])],
         referinta=ref_maj, generator=lambda: ([random.randint(0, 3) for _ in range(random.randint(1, 12))], random.randint(0, 5)),
         indiciu='fit trebuie sa intoarca self, altfel .fit(...).predict(...) nu merge')
""")

    c.md(r"""
**Exercitiul 6.** Clasa `Cutie` care numara cate obiecte s-au creat vreodata, intr-un **atribut de clasa** `numar` (deci nu `self.numar`). Fiecare `Cutie()` il mareste cu 1.
""")
    c.ex(r"""
class Cutie:
    pass  # TODO: atributul de clasa numar si __init__
""", r"""
class Cutie:
    numar = 0

    def __init__(self):
        Cutie.numar += 1
""")
    c.cod(r"""
def t_cutie(n):
    Cutie.numar = 0
    for _ in range(n):
        Cutie()
    return Cutie.numar

verifica('Cutie', t_cutie, [((3,), 3), ((0,), 0)], ascunse=[((10,), 10), ((1,), 1)],
         indiciu='in __init__ scrie Cutie.numar += 1 (nu self.numar, care ar crea un atribut al obiectului)')
""")

    c.md(r"""
## Recapitulare

- **Clasa** = plan, **obiect** = instanta. `__init__` construieste, `self` e obiectul curent, `p.metoda(x)` inseamna `Clasa.metoda(p, x)`.
- Atribute de instanta (`self.x`, ale fiecarui obiect) contra atribute de clasa (comune). Niciodata `[]` la nivel de clasa sau ca valoare implicita.
- `b = a` nu copiaza obiectul. Copie: `copy.copy` / `copy.deepcopy`.
- Metode speciale: `__repr__`, `__str__`, `__eq__` (+ `__hash__`), `__lt__` (sortare), `__add__` si ceilalti operatori.
- Compunere ("are un") inainte de mostenire ("este un"). `super()` ajunge la clasa parinte.
- Fara clasa cand ajunge o functie sau un dictionar.
- **ML:** un model e o clasa cu `fit` (isi schimba starea, atribute cu `_`) si `predict` / `transform` (o folosesc). Ai scris singur `MediaRegressor` si `MinMaxScalerManual`.

Tema (notebook-ul urmator) are Stiva, Coada, Fractie si un KNN scris de mana, comparat cu cel din scikit-learn.
""")
    c.salveaza('08-clase-predare')


def tema():
    c = Carnet('Clase si obiecte', 'tema')
    c.md(r"""
Exercitiile de acasa. Testele vizibile iti arata daca ai inteles enuntul, cele **ascunse** verifica si cazurile limita. Poti rula verificarile de cate ori vrei. La final, `scor()` aduna tot.

Verificarile creeaza obiecte din clasele tale. Daca o clasa e inca goala (`pass`), verificarea o sa spuna "mai ai de lucru": e normal.
""")

    c.md(r"""
### 1. Cerc

Clasa `Cerc(raza)` cu atributul de clasa `PI` (egal cu `math.pi`) si metodele `aria()` si `perimetru()`.
""")
    c.ex(r"""
import math


class Cerc:
    pass  # TODO
""", r"""
import math


class Cerc:
    PI = math.pi

    def __init__(self, raza):
        self.raza = raza

    def aria(self):
        return Cerc.PI * self.raza ** 2

    def perimetru(self):
        return 2 * Cerc.PI * self.raza
""")
    c.cod(r"""
import math

def t_cerc(r):
    c = Cerc(r)
    return c.aria(), c.perimetru(), Cerc.PI

verifica('Cerc', t_cerc, [((1,), (math.pi, 2 * math.pi, math.pi)), ((2,), (4 * math.pi, 4 * math.pi, math.pi))],
         ascunse=[((0,), (0, 0, math.pi)), ((10,), (100 * math.pi, 20 * math.pi, math.pi)), ((0.5,), (math.pi / 4, math.pi, math.pi))],
         puncte=1, indiciu='PI se scrie in corpul clasei, nu in __init__; il citesti cu Cerc.PI')
""")

    c.md(r"""
### 2. Segment (compunere)

`Punct` e dat (cu `__eq__` si `__repr__`). Scrie `Segment(a, b)`, unde `a` si `b` sunt obiecte `Punct`. Metodele: `lungime()` (distanta dintre capete) si `mijloc()` (un **`Punct`** nou, la jumatatea segmentului). Un segment *are* doua puncte, deci nu mosteneste nimic.
""")
    c.ex(r"""
class Punct:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Punct({self.x}, {self.y})'


class Segment:
    pass  # TODO: __init__(self, a, b), lungime, mijloc
""", r"""
class Punct:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Punct({self.x}, {self.y})'


class Segment:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def lungime(self):
        return ((self.a.x - self.b.x) ** 2 + (self.a.y - self.b.y) ** 2) ** 0.5

    def mijloc(self):
        return Punct((self.a.x + self.b.x) / 2, (self.a.y + self.b.y) / 2)
""")
    c.cod(r"""
def t_segment(x1, y1, x2, y2):
    s = Segment(Punct(x1, y1), Punct(x2, y2))
    m = s.mijloc()
    return s.lungime(), (m.x, m.y), isinstance(m, Punct)

verifica('Segment', t_segment, [((0, 0, 3, 4), (5, (1.5, 2), True)), ((1, 1, 1, 1), (0, (1, 1), True))],
         ascunse=[((-2, 0, 2, 0), (4, (0, 0), True)), ((0, 0, 1, 1), (2 ** 0.5, (0.5, 0.5), True))],
         puncte=1, indiciu='mijloc() trebuie sa intoarca un Punct, nu un tuplu')
""")

    c.md(r"""
### 3. Stiva

`Stiva` cu metodele `push(x)` (pune deasupra), `pop()` (scoate si intoarce ultimul pus; pe stiva goala ridica `IndexError`), `varf()` (ultimul element, fara sa-l scoata), `este_goala()` si `len(stiva)`. Tine elementele intr-o lista (`self.elemente`).
""")
    c.ex(r"""
class Stiva:
    pass  # TODO: __init__, push, pop, varf, este_goala, __len__
""", r"""
class Stiva:
    def __init__(self):
        self.elemente = []

    def push(self, x):
        self.elemente.append(x)

    def pop(self):
        if not self.elemente:
            raise IndexError('stiva goala')
        return self.elemente.pop()

    def varf(self):
        return self.elemente[-1]

    def este_goala(self):
        return not self.elemente

    def __len__(self):
        return len(self.elemente)
""")
    c.cod(r"""
def t_stiva(ops):
    s = Stiva()
    rez = []
    for op in ops:
        if op[0] == 'push':
            s.push(op[1])
        elif op[0] == 'pop':
            try:
                rez.append(s.pop())
            except IndexError:
                rez.append('gol')
        elif op[0] == 'varf':
            rez.append(s.varf())
        elif op[0] == 'goala':
            rez.append(s.este_goala())
        else:
            rez.append(len(s))
    return rez

verifica('Stiva', t_stiva,
         [(([('push', 1), ('push', 2), ('varf',), ('pop',), ('pop',), ('goala',)],), [2, 2, 1, True]),
          (([('pop',), ('push', 5), ('len',)],), ['gol', 1])],
         ascunse=[(([('goala',), ('push', 'a'), ('goala',), ('len',)],), [True, False, 1]),
                  (([('push', 1), ('push', 2), ('push', 3), ('pop',), ('varf',), ('len',)],), [3, 2, 2])],
         puncte=2, indiciu='pop() pe stiva goala: if not self.elemente: raise IndexError(...)')
""")

    c.md(r"""
### 4. Coada (si o masuratoare)

`Coada` cu `adauga(x)` (la sfarsit), `scoate()` (primul adaugat; pe coada goala `IndexError`) si `len(coada)`. Foloseste `collections.deque` (`append` si `popleft`) ca sa fie rapida.
""")
    c.ex(r"""
from collections import deque


class Coada:
    pass  # TODO: __init__, adauga, scoate, __len__
""", r"""
from collections import deque


class Coada:
    def __init__(self):
        self.elemente = deque()

    def adauga(self, x):
        self.elemente.append(x)

    def scoate(self):
        if not self.elemente:
            raise IndexError('coada goala')
        return self.elemente.popleft()

    def __len__(self):
        return len(self.elemente)
""")
    c.cod(r"""
def t_coada(ops):
    q = Coada()
    rez = []
    for op in ops:
        if op[0] == 'adauga':
            q.adauga(op[1])
        elif op[0] == 'scoate':
            try:
                rez.append(q.scoate())
            except IndexError:
                rez.append('gol')
        else:
            rez.append(len(q))
    return rez

verifica('Coada', t_coada,
         [(([('adauga', 1), ('adauga', 2), ('scoate',), ('len',), ('scoate',)],), [1, 1, 2]),
          (([('scoate',)],), ['gol'])],
         ascunse=[(([('adauga', 'x'), ('adauga', 'y'), ('scoate',), ('adauga', 'z'), ('scoate',), ('scoate',), ('scoate',)],),
                   ['x', 'y', 'z', 'gol'])],
         puncte=2, indiciu='primul intrat, primul iesit: popleft() scoate din stanga')
""")
    c.md(r"""
**De ce `deque` si nu lista?** `lista.pop(0)` scoate primul element, dar apoi **muta toate celelalte** o pozitie la stanga: O(n). `deque.popleft()` e O(1). Masuram (celula nu depinde de clasa ta):
""")
    c.cod(r"""
import time
from collections import deque

def masoara(n):
    lista = list(range(n))
    t = time.perf_counter()
    while lista:
        lista.pop(0)
    t_lista = time.perf_counter() - t

    dq = deque(range(n))
    t = time.perf_counter()
    while dq:
        dq.popleft()
    t_deque = time.perf_counter() - t
    return t_lista, t_deque

for n in (5_000, 20_000, 80_000):
    a, b = masoara(n)
    print(f'n={n:>7}: lista.pop(0) {a:.4f}s | deque.popleft() {b:.4f}s')
""")
    c.md(r"""
Cand `n` se inmulteste cu 4, timpul listei creste de ~16 ori (patratic: n scoateri, fiecare O(n)), iar cel al lui `deque` doar de ~4 ori (liniar). Pentru o coada cu multe elemente, alegerea structurii face diferenta dintre 0,01 s si un timeout.
""")

    c.md(r"""
### 5. Repara codul: cosul comun

Clasa `Cos` ar trebui sa tina preturile produselor unui cos de cumparaturi. Dar doua cosuri diferite par sa aiba aceleasi produse. Uita-te la animatie (cauta eticheta `@1`) si repara clasa.
""")
    c.cod(r"""
%%vezi
class Cos:
    produse = []
    def adauga(self, pret):
        self.produse.append(pret)

c1 = Cos()
c2 = Cos()
c1.adauga(10)
p1 = c1.produse
p2 = c2.produse
""")
    c.ex(r"""
class Cos:
    produse = []

    def adauga(self, pret):
        self.produse.append(pret)

    def total(self):
        return sum(self.produse)
""", r"""
class Cos:
    def __init__(self):
        self.produse = []

    def adauga(self, pret):
        self.produse.append(pret)

    def total(self):
        return sum(self.produse)
""")
    c.cod(r"""
def t_cos(a, b):
    c1, c2 = Cos(), Cos()
    for x in a:
        c1.adauga(x)
    for x in b:
        c2.adauga(x)
    return c1.total(), c2.total()

verifica('Cos', t_cos, [(([10, 20], [5]), (30, 5)), (([], [7, 3]), (0, 10))],
         ascunse=[(([1], [1, 1]), (1, 2)), (([100], []), (100, 0))],
         puncte=1, indiciu='fiecare obiect are nevoie de propria lista: creeaz-o in __init__')
""")

    c.md(r"""
### 6. Repara codul: cronometrul

Aici sunt **doua** greseli, ambele cu `self`. Ruleaza verificarea, citeste mesajul de eroare (ultima linie conteaza), repara, ruleaza din nou. Dupa prima reparatie, va aparea urmatoarea eroare.
""")
    c.ex(r"""
class Cronometru:
    def __init__(self):
        secunde = 0

    def tick(self, n):
        self.secunde += n

    def minute(self):
        return secunde // 60
""", r"""
class Cronometru:
    def __init__(self):
        self.secunde = 0

    def tick(self, n):
        self.secunde += n

    def minute(self):
        return self.secunde // 60
""")
    c.cod(r"""
def t_cron(ticks):
    c = Cronometru()
    for n in ticks:
        c.tick(n)
    return c.secunde, c.minute()

verifica('Cronometru', t_cron, [(([30, 45, 90],), (165, 2)), (([],), (0, 0))],
         ascunse=[(([60],), (60, 1)), (([59, 1],), (60, 1))],
         puncte=1, indiciu='in interiorul unei metode, atributele se scriu mereu cu self.')
""")

    c.md(r"""
### 7. Program: depozitul

Program ca la concurs, dar cu o clasa. Prima linie: `n`. Urmeaza `n` comenzi, cate una pe linie:

- `+ produs cantitate` adauga in stoc;
- `- produs cantitate` scoate din stoc. Daca nu e destul, afiseaza `LIPSA` si nu schimba nimic;
- `? produs` afiseaza stocul curent (0 daca produsul nu a aparut niciodata).

Scrie clasa `Depozit` (metodele `adauga`, `scoate` care ridica `ValueError` la stoc insuficient, `cate`) si `main`, care prinde eroarea si afiseaza `LIPSA`.
""")
    c.ex(r"""
class Depozit:
    pass  # TODO: __init__, adauga(produs, cant), scoate(produs, cant), cate(produs)


def main():
    pass  # TODO: citeste n si cele n comenzi
""", r"""
class Depozit:
    def __init__(self):
        self.stoc = {}

    def adauga(self, produs, cant):
        self.stoc[produs] = self.stoc.get(produs, 0) + cant

    def scoate(self, produs, cant):
        if self.stoc.get(produs, 0) < cant:
            raise ValueError('stoc insuficient')
        self.stoc[produs] -= cant

    def cate(self, produs):
        return self.stoc.get(produs, 0)


def main():
    d = Depozit()
    n = int(input())
    for _ in range(n):
        comanda = input().split()
        if comanda[0] == '+':
            d.adauga(comanda[1], int(comanda[2]))
        elif comanda[0] == '-':
            try:
                d.scoate(comanda[1], int(comanda[2]))
            except ValueError:
                print('LIPSA')
        else:
            print(d.cate(comanda[1]))
""")
    c.cod(r"""
verifica_program('depozit', main,
                 [(['4', '+ mere 10', '- mere 4', '? mere', '? pere'], '6\n0'),
                  (['3', '+ apa 5', '- apa 9', '? apa'], 'LIPSA\n5')],
                 ascunse=[(['1', '? x'], '0'), (['5', '+ a 2', '+ a 3', '- a 5', '? a', '- a 1'], '0\nLIPSA'),
                          (['2', '- gol 1', '? gol'], 'LIPSA\n0')],
                 puncte=2, indiciu='dictionar in clasa: self.stoc.get(produs, 0); ValueError in scoate, try/except in main')
""")

    c.md(r"""
### 8. Provocare: clasa `Fractie`

Scrie `Fractie(a, b)` (numarator, numitor). Cerinte:

- fractia se **simplifica** automat (`math.gcd`) si numitorul e mereu pozitiv (`Fractie(2, -4)` devine `-1/2`); numitor 0 ridica `ValueError`;
- `+`, `-`, `*`, `/` intre doua fractii (`__add__`, `__sub__`, `__mul__`, `__truediv__`);
- `==` si `<` (compara prin produse incrucisate, nu prin impartire cu zecimale);
- `repr` de forma `'a/b'` (chiar si pentru intregi: `'3/1'`).

Testele compara cu `fractions.Fraction` din biblioteca standard.
""")
    c.ex(r"""
import math


class Fractie:
    pass  # TODO
""", r"""
import math


class Fractie:
    def __init__(self, a, b):
        if b == 0:
            raise ValueError('numitor 0')
        if b < 0:
            a, b = -a, -b
        g = math.gcd(a, b)
        self.a = a // g
        self.b = b // g

    def __add__(self, other):
        return Fractie(self.a * other.b + other.a * self.b, self.b * other.b)

    def __sub__(self, other):
        return Fractie(self.a * other.b - other.a * self.b, self.b * other.b)

    def __mul__(self, other):
        return Fractie(self.a * other.a, self.b * other.b)

    def __truediv__(self, other):
        return Fractie(self.a * other.b, self.b * other.a)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __lt__(self, other):
        return self.a * other.b < other.a * self.b

    def __repr__(self):
        return f'{self.a}/{self.b}'
""")
    c.cod(r"""
import random
from fractions import Fraction

def t_fractie(a, b, c, d):
    x, y = Fractie(a, b), Fractie(c, d)
    return repr(x + y), repr(x - y), repr(x * y), x == y, x < y

def ref_fractie(a, b, c, d):
    x, y = Fraction(a, b), Fraction(c, d)
    f = lambda r: f'{r.numerator}/{r.denominator}'
    return f(x + y), f(x - y), f(x * y), x == y, x < y

def t_impartire(a, b, c, d):
    return repr(Fractie(a, b) / Fractie(c, d))

def t_zero():
    try:
        Fractie(1, 0)
    except ValueError:
        return 'ValueError'
    return 'nimic'

verifica('Fractie', t_fractie, [((1, 2, 1, 3), ('5/6', '1/6', '1/6', False, False)),
                                ((2, 4, 1, 2), ('1/1', '0/1', '1/4', True, False))],
         referinta=ref_fractie, generator=lambda: (random.randint(-20, 20), random.randint(1, 20), random.randint(-20, 20), random.randint(1, 20)),
         puncte=2, indiciu='simplifica in __init__ cu gcd; daca b < 0 schimba semnul ambelor')
verifica('Fractie: impartire si zero', lambda: (t_impartire(1, 2, 3, 4), t_impartire(-1, 3, -2, 5), t_zero()), [((), ('2/3', '5/6', 'ValueError'))],
         puncte=1, indiciu='a/b : c/d = (a*d)/(b*c); numitor 0 -> raise ValueError')
""")

    c.md(r"""
### 9. Provocare: KNN scris de mana

Cel mai mare exercitiu: `KNNClasificator(k)`, cu aceeasi interfata ca `KNeighborsClassifier`.

- `fit(X, y)`: retine datele (`self.X_`, `self.y_`) si intoarce `self`. Atat: KNN nu "invata" nimic, doar tine datele.
- `predict(X)`: pentru fiecare punct nou, calculeaza distanta euclidiana pana la **fiecare** punct retinut (`sqrt` din suma patratelor diferentelor, cu bucle simple), ia cei `k` mai apropiati si intoarce clasa cu cele mai multe voturi. La egalitate de voturi, clasa cea mai mica.

`X` e o lista de liste de numere, `y` o lista de clase, iar `predict` intoarce o **lista** de clase. Fara NumPy, fara scikit-learn in solutia ta. Sub celula gasesti verificarea pe un set fix si pe multe seturi aleatoare, comparate cu `KNeighborsClassifier`.
""")
    c.ex(r"""
class KNNClasificator:
    def __init__(self, k=3):
        self.k = k

    # TODO: fit, predict (poti adauga o metoda ajutatoare pentru distanta)
""", r"""
class KNNClasificator:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X_ = X
        self.y_ = y
        return self

    def _distanta(self, a, b):
        return sum((p - q) ** 2 for p, q in zip(a, b)) ** 0.5

    def _prezice_unul(self, x):
        dist = sorted((self._distanta(x, xi), i) for i, xi in enumerate(self.X_))
        voturi = {}
        for _, i in dist[:self.k]:
            e = self.y_[i]
            voturi[e] = voturi.get(e, 0) + 1
        return max(sorted(voturi), key=lambda e: voturi[e])

    def predict(self, X):
        return [self._prezice_unul(x) for x in X]
""")
    c.cod(r"""
import random
from sklearn.neighbors import KNeighborsClassifier

def t_knn(X, y, Xt, k):
    return KNNClasificator(k).fit(X, y).predict(Xt)

def ref_knn(X, y, Xt, k):
    return KNeighborsClassifier(n_neighbors=k).fit(X, y).predict(Xt).tolist()

def gen_knn():
    n = random.randint(8, 25)
    X = [[random.uniform(0, 10), random.uniform(0, 10)] for _ in range(n)]
    y = [random.randint(0, 2) for _ in range(n)]
    Xt = [[random.uniform(0, 10), random.uniform(0, 10)] for _ in range(5)]
    return X, y, Xt, random.choice([1, 3, 5])

Xa = [[1, 1], [1, 2], [2, 1], [2, 2], [6, 6], [6, 7], [7, 6], [7, 7], [4, 4]]
ya = [0, 0, 0, 0, 1, 1, 1, 1, 1]
Xq = [[1.5, 1.5], [6.5, 6.5], [4.5, 3.2], [5, 2]]
asteptat = ref_knn(Xa, ya, Xq, 3)

verifica('KNN pe set fix', t_knn, [((Xa, ya, Xq, 3), asteptat)],
         puncte=1, indiciu='sortezi perechi (distanta, indice) si iei primele k; voturile le numeri cu un dictionar')
verifica('KNN vs scikit-learn', t_knn, [((Xa, ya, Xq, 1), ref_knn(Xa, ya, Xq, 1))],
         referinta=ref_knn, generator=gen_knn, n=30, puncte=3,
         indiciu='k=1 e cel mai simplu caz: clasa celui mai apropiat punct')
scor()
""")
    c.salveaza('08-clase-tema')


if __name__ == '__main__':
    predare()
    tema()
