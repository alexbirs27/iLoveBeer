"""Genereaza 02-structuri-decizionale-predare.ipynb si 02-structuri-decizionale-tema.ipynb (+ variantele cu solutii)."""
from nb import Carnet

# incarcarea datelor din elevi.csv + masurarea acuratetei (folosita in predare si in tema)
AJUTOR_ELEVI = """
import csv

ELEVI = []
with open('date/elevi.csv') as f:
    for r in csv.DictReader(f):
        try:
            ELEVI.append((float(r['nota_info']), float(r['ore_studiu']), int(r['absente']), int(r['calificat'])))
        except ValueError:
            pass    # sarim randurile cu valori lipsa (le tratam alta data)


def acuratete(regula):
    bune = 0
    for nota, ore, absente, y in ELEVI:
        if regula(nota, ore, absente) == y:
            bune += 1
    return bune / len(ELEVI)
"""


def predare():
    c = Carnet('Structuri decizionale', 'predare', fisiere=('date/elevi.csv',))

    c.md("""
## Programe care aleg

Pana acum programul tau mergea de sus in jos, fara sa hotarasca nimic. Un program care nu alege nu poate face mare lucru: nu poate verifica o nota, nu poate refuza o data gresita, nu poate spune "da" sau "nu". Aici inveti sa alegi.

E si baza pentru ceva mai mare. Un **arbore de decizie** din ML este un lant de `if`-uri, doar ca pragurile (`nota >= 6.5`) le gaseste calculatorul din date, nu tu. La final scrii unul de mana, pe datele din `elevi.csv`.

In animatii, linia galbena e cea care se executa. De data asta uita-te mai ales la **liniile care nu se executa**. Acolo e toata treaba.

## 1. if / else

`if` primeste o conditie (ceva care e `True` sau `False`). Daca e adevarata, ruleaza blocul de sub ea. `else` ruleaza in caz contrar.

Doua reguli de sintaxa, ambele la fel de importante:

- dupa conditie pui **doua puncte** (`:`)
- blocul de dedesubt este **indentat** (4 spatii). Nu exista acolade: **indentarea este sintaxa**. Ce e la acelasi nivel apartine aceluiasi bloc.

**Prezice:** ce afiseaza programul pentru `15`? Dar pentru `18`? Care linii nu se executa deloc?

<details><summary>Raspuns</summary>

Pentru 15 afiseaza `minor`, pentru 18 `major` (`>=` il include pe 18). La 15 se sar cele doua linii din `if`, la 18 se sare peste `else`. Ultimul `print` nu e indentat, deci nu tine de `if` si se executa mereu.
</details>
""")
    c.cod("""
%%vezi 15
varsta = int(input())
if varsta >= 18:            #: 15 nu e >= 18, deci conditia e falsa: sarim peste tot blocul indentat
    mesaj = 'major'
    print('poti vota')
else:
    mesaj = 'minor'         #: blocul din else se executa doar cand if-ul a picat
print(mesaj)                #: nu e indentat, nu tine de if: se executa oricum
""")

    c.md("""
## 2. Mai mult de doua variante: elif

Cand ai mai multe cazuri nu pui `if` in `if`, folosesti `elif` (de la "else if"). Python verifica conditiile **de sus in jos si se opreste la prima adevarata**. Restul nu se mai citesc.

Din asta iese regula cea mai importanta din notebook: **ordinea conditiilor conteaza**.
""")
    c.cod("""
%%vezi 8
nota = int(input())
if nota >= 9:
    calificativ = 'foarte bine'
elif nota >= 7:             #: ajungem aici doar daca prima conditie a fost falsa
    calificativ = 'bine'
elif nota >= 5:
    calificativ = 'suficient'
else:                       #: else = "nimic din ce a fost mai sus"
    calificativ = 'insuficient'
print(calificativ)
""")
    c.md("""
**Prezice:** acelasi program, dar am pus conditiile invers, de la cea mai mica. Ce calificativ primeste `9`?

<details><summary>Raspuns</summary>

`suficient`. Pe `9 >= 5` il prinde prima conditie, si ce e dedesubt nu se mai verifica. Programul nu da nicio eroare, doar raspunde gresit, iar bug-urile de felul asta sunt cele mai urate.
</details>
""")
    c.cod("""
%%vezi 9
nota = int(input())
if nota >= 5:               #: 9 >= 5 e adevarat, si aici se termina cautarea. Cele doua elif nu se mai verifica niciodata
    calificativ = 'suficient'
elif nota >= 7:
    calificativ = 'bine'
elif nota >= 9:
    calificativ = 'foarte bine'
else:
    calificativ = 'insuficient'
print(calificativ)
""")

    c.md("""
## 3. elif, if-uri separate si if imbricat

Doua `if`-uri una sub alta sunt **independente**: fiecare isi verifica conditia, indiferent ce s-a intamplat inainte. Un `elif` depinde de tot ce e deasupra.

- cazuri care se **exclud** (un singur calificativ): `if` / `elif` / `else`
- lucruri **independente** (poate fi si trecut, si premiat): `if`-uri separate
""")
    c.cod("""
%%vezi 9
nota = int(input())
a = ''
if nota >= 5:               #: primul if separat
    a = a + 'trecut '
if nota >= 9:               #: al doilea se verifica oricum, chiar daca primul a fost adevarat
    a = a + 'premiu'
b = ''
if nota >= 9:               #: acum acelasi lucru cu elif
    b = 'premiu'
elif nota >= 5:             #: nu se mai verifica: prima conditie a fost adevarata
    b = 'trecut'
""")
    c.md("""
Un `if` **in interiorul** altui `if` se cheama imbricat. Cel de-al doilea se verifica doar daca primul a fost adevarat. Uita-te la ce linii sunt sarite pentru un elev de 15 ani:
""")
    c.cod("""
%%vezi 15 1
varsta = int(input())
permis = int(input())
if varsta >= 18:
    if permis == 1:         #: permisul se verifica doar pentru cine are varsta
        print('poti conduce')
    else:
        print('fara permis')
else:
    print('prea tanar')     #: 15 ani: nici nu ne uitam la permis
""")

    c.md("""
## 4. Comparatii

| operator | inseamna |
|---|---|
| `==` `!=` | egal, diferit |
| `<` `<=` `>` `>=` | mai mic, mai mic sau egal, mai mare, mai mare sau egal |

Rezultatul unei comparatii este un `bool`.

**Lantul de comparatii.** Python te lasa sa scrii `1 < x < 10`, ca la matematica, si il intelege exact asa: `(1 < x) and (x < 10)`. In C++ aceeasi scriere inseamna altceva: `(1 < x) < 10`, adica compari un 0 sau 1 cu 10, si iese mereu adevarat. Daca vii din C++, asta e diferenta cea mai mare.
""")
    c.cod("""
%%vezi
x = 15
a = 1 < x < 10              #: Python: (1 < x) si (x < 10). 15 nu e mai mic decat 10, deci False
b = (1 < x) < 10            #: asa citeste C++ scrierea: True devine 1, si 1 < 10 e adevarat
c = 1 < x and x < 10        #: varianta lunga, acelasi rezultat ca la a
""")
    c.md("""
**`=` este atribuire, `==` este comparatie**, iar `is` nu compara valori: verifica daca doua nume arata spre **acelasi obiect** din memorie. Uita-te la eticheta `@1` din animatie (o poarta containerele care apar in mai multe locuri).
""")
    c.cod("""
%%vezi
a = [1, 2]
b = [1, 2]
c = a
r1 = a == b                 #: aceleasi valori? Da
r2 = a is b                 #: acelasi obiect? Nu, sunt doua liste separate
r3 = a is c                 #: c e alt nume pentru aceeasi lista (aceeasi eticheta @)
""")
    c.md("""
Foloseste `is` doar pentru `None` (`if x is None:`). Pentru orice altceva, `==`.

## 5. Adevarat si fals

`True` si `False` sunt valori de tip `bool`. In plus, **orice valoare** poate sta intr-un `if`: Python o transforma in bool. Cele "goale" sunt `False`: `0`, `0.0`, `''`, `[]`, `{}`, `None`. Orice altceva e `True`.

**Prezice:** cat dau `bool('False')`, `bool([0])` si `bool(' ')`?

<details><summary>Raspuns</summary>

De trei ori `True`. `'False'` e un text nevid, `[0]` e o lista cu un element (chiar daca acela e 0), iar `' '` are un spatiu in el.
</details>
""")
    c.cod("""
# bucla for o inveti in notebook-ul urmator; acum doar citeste iesirea
for v in [0, 1, -3, 0.0, 0.1, '', 'a', 'False', ' ', [], [0], None]:
    print(f'{v!r:8} -> {bool(v)}')
""")

    c.md("""
## 6. and, or, not

| | |
|---|---|
| `a and b` | adevarat doar daca ambele sunt adevarate |
| `a or b` | adevarat daca macar unul e adevarat |
| `not a` | inverseaza |

**Precedenta:** mai intai `not`, apoi `and`, apoi `or` (ca `*` inaintea lui `+`). Nu te baza pe ea, pune paranteze. Cine citeste codul (tu, peste o luna) nu trebuie sa numere.

**Prezice:** cat da `True or False and False`?

<details><summary>Raspuns</summary>

`True`. Se face intai `False and False` = `False`, apoi `True or False` = `True`. Cu paranteze, `(True or False) and False` da `False`.
</details>
""")
    c.cod("""
print(True or False and False)
print((True or False) and False)
print(not True or True)         # (not True) or True
print(not (True or True))
""")
    c.md("""
**Scurtcircuit.** `and` si `or` se opresc imediat ce stiu raspunsul. `False and ...` e fals oricum, deci partea a doua nici nu se calculeaza. Uita-te in memorie: functia `zgomot` se apeleaza sau nu?

Si un detaliu care surprinde: `and` / `or` nu intorc neaparat `True` / `False`, ci **unul dintre operanzi**. `or` il intoarce pe primul adevarat, `and` pe primul fals (sau ultimul, daca toti sunt adevarati).
""")
    c.cod("""
%%vezi
def zgomot():
    print('zgomot() a fost apelata')
    return True

a = False and zgomot()      #: False and ...: raspunsul e sigur, zgomot() nici nu porneste
b = True or zgomot()        #: True or ...: la fel
c = True and zgomot()       #: aici trebuie sa afle a doua valoare, deci o apeleaza
d = 0 or 7                  #: 0 e fals, deci or trece la 7 si il intoarce pe el
e = 5 and 7                 #: 5 e adevarat, and trece mai departe si intoarce ultimul: 7
f = '' or 'anonim'          #: modelul pe care il vei vedea des: "valoarea mea, sau una implicita"
""")
    c.cod("""
n = 0
if n != 0 and 10 / n > 2:       # n != 0 e "garda": daca e falsa, impartirea nu se mai face
    print('mare')
else:
    print('nu impart la 0')

varsta, permis = 20, 1
if varsta >= 18 and permis == 1:    # if-ul imbricat de mai sus, intr-o singura conditie
    print('poti conduce')
""")

    c.md("""
## 7. in si expresia conditionala

`in` verifica daca ceva se afla intr-o colectie: un caracter intr-un text, un element intr-o lista sau un tuplu. `not in` e opusul. Iti scurteaza lanturile de `or`.

**Expresia conditionala (ternar).** Cand un `if/else` doar alege o valoare, il scrii pe o linie: `valoare_daca_adevarat if conditie else valoare_daca_fals`. Nu inlantui mai multe, devin ilizibile: la 3 cazuri foloseste `elif`.
""")
    c.cod("""
# in / not in
litera = 'e'
print(litera in 'aeiou')
luna = 4
print(luna in (1, 3, 5, 7, 8, 10, 12))      # luni cu 31 de zile
print('x' not in 'abc')
print('ana' in 'banana')                    # merge si pentru bucati de text

# expresia conditionala
varsta = 20
tip = 'major' if varsta >= 18 else 'minor'
print(tip)
a, b = 4, 9
print(a if a > b else b)            # maximul a doua numere
x = -5
print(x if x >= 0 else -x)          # valoarea absoluta
""")

    c.md("""
## 8. Valori de granita

`>` si `>=` difera intr-un singur punct, si exact acolo pica cele mai multe teste. Cand scrii o conditie, incearc-o pe **granita si pe cele doua vecine**: pentru "major la 18 ani", 17, 18 si 19.
""")
    c.cod("""
def major_gresit(v):
    return v > 18

def major(v):
    return v >= 18

print(17, major_gresit(17), major(17))
print(18, major_gresit(18), major(18))      # aici difera
print(19, major_gresit(19), major(19))
""")

    c.md("""
## 9. Din topor, apoi scurtatura

Cel mai mare din trei numere. **Din topor:** presupui ca primul e cel mai mare, apoi il provoci pe rand cu celelalte. Ideea ("un campion actualizat pe parcurs") o folosesti si pe liste de o mie de elemente.
""")
    c.cod("""
%%vezi 4 9 6
a = int(input())
b = int(input())
c = int(input())
m = a                   #: presupunem ca a e cel mai mare
if b > m:               #: b il bate pe campion?
    m = b               #: da: b devine noul campion
if c > m:               #: si c?
    m = c
print(m)
""")
    c.md("""
**Scurtatura:** Python are functiile `max`, `min`, `abs` si `sorted`.
""")
    c.cod("""
print(max(4, 9, 6), min(4, 9, 6), abs(-7))
print(sorted([4, 9, 6]))                # lista sortata crescator
print(sorted([4, 9, 6])[1])             # elementul din mijloc: mediana din 3
print(max('ana', 'mihai', 'zoe'))       # merge si pe text (ordine alfabetica)
""")
    c.md("""
**De ce `max` in loc de comparatii scrise de mana?** Nu poti incurca un `>` cu un `<`, merge pentru oricate valori (sau pentru o lista intreaga) si e mai scurt. Pe liste mari e si mai rapid: bucla din `max` ruleaza in C, nu in Python (o masuram in notebook-ul cu bucle).

Nu memora functiile, la olimpiada ai documentatie. Dar trebuie sa poti scrie varianta de mana (exercitiul 2), pentru ca uneori conditia e a ta ("cel mai mare numar **par**") si `max` simplu nu ajunge.

## 10. match (doar sa-l recunosti)

Din Python 3.10 exista `match`, un fel de `switch`. Face ce face un `if/elif` cu `==`, deci noi nu-l folosim, dar il vei vedea in codul altora:

```python
match comanda:
    case 'start':
        print('pornesc')
    case 'stop' | 'pauza':
        print('opresc')
    case _:                      # orice altceva
        print('comanda necunoscuta')
```

## 11. Capcane

**Capcana 1: `if x == 1 or 2`.** Il scrii cum il spui in romana: "x e 1 sau 2". Python il citeste `(x == 1) or 2`, iar `2` e mereu adevarat.

**Prezice:** ce afiseaza programul pentru `x = 5`?

<details><summary>Raspuns</summary>

Afiseaza `x e 1 sau 2`, desi x e 5. Iar `print(x == 1 or 2)` da `2`, fiindca `or` intoarce operandul. Corect: `x == 1 or x == 2`, sau mai frumos `x in (1, 2)`.
</details>
""")
    c.cod("""
%%vezi 5
x = int(input())
print(x == 1 or 2)          #: False or 2 -> 2. Nu e un bool, e chiar operandul
if x == 1 or 2:             #: (x == 1) or 2 -> 2, iar 2 e adevarat
    print('x e 1 sau 2')    #: x e 5 si tot am ajuns aici
""")
    c.md("""
**Capcana 2: floaturile nu se compara cu `==`.** Ai vazut in primul notebook ca `0.1 + 0.2 != 0.3`. Compari diferenta cu o toleranta.

**Capcana 3: textul se compara alfabetic, nu numeric.** **Prezice:** cat da `'10' < '9'`?

<details><summary>Raspuns</summary>

`True`. Textele se compara caracter cu caracter, iar `'1'` e inaintea lui `'9'`. Tot de aici: `'Ana' != 'ana'` (litera mare e alt caracter) si `'Z' < 'a'`. Transformi inainte cu `int(...)` sau `.lower()`. In plus, `'5' == 5` nu da eroare, e doar mereu `False`.
</details>
""")
    c.cod("""
print(0.1 * 3 == 0.3, abs(0.1 * 3 - 0.3) < 1e-9)
print('10' < '9', int('10') < int('9'))
print('Ana' == 'ana', 'Ana'.lower() == 'ana', 'Z' < 'a')
print('5' == 5)
""")
    c.md("""
**Capcana 4: `0` e o valoare buna, dar e falsa.** Daca un elev are nota 0, `if nota:` zice ca nu are nota. Cand "lipsa" inseamna `None`, verifica `is None`. (Exact problema din datele reale: un 0 nu e o valoare lipsa.)

**Capcana 5: `x == 5` pe o linie proprie nu atribuie nimic.** Compara, si arunca rezultatul.
""")
    c.cod("""
nota = 0
print('are nota' if nota else 'nu are nota')                     # gresit
print('are nota' if nota is not None else 'nu are nota')         # corect

x = 3
x == 5              # compara si uita rezultatul
print(x)            # x tot 3 a ramas
""")

    c.md("""
## 12. Cum citesti eroarea

Erorile tipice cand lucrezi cu decizii. In animatii apar in rosu, pe linia cu pricina.

| eroare | de obicei inseamna |
|---|---|
| `IndentationError` | blocul nu e indentat, sau indentarile sunt amestecate |
| `SyntaxError` | doua puncte uitate, `=` in loc de `==`, paranteza lipsa |
| `TypeError` | compari tipuri care nu se potrivesc (text cu numar) |
| `NameError` | variabila exista doar pe o ramura care nu s-a executat |

Prima e in fond un fel de `SyntaxError` (animatia o afiseaza asa; in terminal vezi `IndentationError`). La erorile de sintaxa nu se executa **nicio linie**, nici cele de dinaintea greselii: Python citeste intai tot programul.
""")
    c.cod("""
%%vezi
x = 7
if x > 5:
print('mare')
""")
    c.cod("""
%%vezi 5
x = int(input())
if x = 5:
    print('cinci')
""")
    c.md("""
Urmatoarele doua sunt erori de **executie**: programul porneste si crapa la mijloc. Prima, clasica: variabila e definita doar pe unele ramuri. A doua: compari textul de la `input()` cu un numar.
""")
    c.cod("""
%%vezi -3
x = int(input())
if x > 0:
    semn = 'pozitiv'
elif x == 0:
    semn = 'zero'
print(semn)                 #: pentru x negativ nicio ramura nu s-a executat, deci semn nu exista
""")
    c.cod("""
%%vezi 7
nota = input()              #: input() da text
if nota >= 5:               #: text >= numar: Python nu stie sa compare asa ceva
    print('trecut')
""")
    c.md("""
Reparatiile: pui un `else` (sau dai lui `semn` o valoare de start inainte de `if`) si scrii `int(input())`.

## 13. Din ML: un arbore de decizie e un lant de if-uri

In `date/elevi.csv` fiecare rand e un elev: `nota_info`, `ore_studiu`, `absente`, ... si `calificat` (1 = a trecut mai departe). Scrii o functie care **ghiceste** `calificat` din trei numere. Un arbore de decizie face exact asta, doar ca **pragurile si le gaseste singur din date**.

Uita-te cum decurge un apel: valorile intra ca parametri, iar `return` iese pe prima ramura care se potriveste.
""")
    c.cod("""
%%vezi
def calificat_probabil(nota_info, ore, absente):
    if nota_info >= 7:              #: 6.2 nu ajunge la 7
        return 1
    elif nota_info >= 6 and ore >= 8:     #: dar are peste 6 si a invatat mult: ramura asta e adevarata
        return 1
    else:
        return 0

r = calificat_probabil(6.2, 9.5, 3)      #: un elev cu nota 6.2, 9.5 ore de studiu, 3 absente
""")
    c.md("""
Cat de buna e regula? Masuram **acuratetea**: din cati elevi ghiceste corect. Celula de mai jos citeste fisierul si numara (contine o bucla, o inveti la notebook-ul urmator; acum o folosesti). "Mereu 0" e linia de baza: daca o regula nu o bate, nu valoreaza nimic.
""")
    c.cod(AJUTOR_ELEVI + """

def calificat_probabil(nota_info, ore, absente):
    if nota_info >= 7:
        return 1
    elif nota_info >= 6 and ore >= 8:
        return 1
    else:
        return 0


print(len(ELEVI), 'elevi cu toate valorile prezente')
print('mereu 0    :', round(acuratete(lambda n, o, a: 0), 3))
print('regula mea :', round(acuratete(calificat_probabil), 3))
""")
    c.md("""
Acum lasam calculatorul sa gaseasca pragurile. `DecisionTreeClassifier` din scikit-learn invata un arbore, iar `export_text` ti-l afiseaza. Citeste-l ca pe un `if` in `if`:
""")
    c.cod("""
from sklearn.tree import DecisionTreeClassifier, export_text

X = [r[:3] for r in ELEVI]
y = [r[3] for r in ELEVI]
arbore = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X, y)
print(export_text(arbore, feature_names=['nota_info', 'ore', 'absente']))
print('acuratete:', round(arbore.score(X, y), 3))
""")
    c.md("""
Sunt praguri gasite de algoritm (`nota_info <= 6.02`...), exact ca ale tale, doar mai fine, si i-au iesit mai bine decat regulii tale. Atentie: acuratetea e masurata pe aceleasi date pe care a invatat, deci e optimista. Mai tarziu vezi cum o masori cinstit.

**Praguri = categorii.** Aceeasi tehnica transforma un numar intr-o categorie (*binning*). Modelele si graficele au adesea nevoie de asa ceva. In pandas, `pd.cut` face asta pe o coloana intreaga; acum stii ce se intampla in spate.
""")
    c.cod("""
def categorie_ore(ore):
    if ore < 3:
        return 'putin'
    elif ore < 8:
        return 'mediu'
    else:
        return 'mult'


print(categorie_ore(1.5), categorie_ore(3), categorie_ore(7.9), categorie_ore(8), categorie_ore(20))
""")

    c.md("""
## Exercitii

Fiecare are o celula de completat si una de verificare. Verificarea are si teste ascunse, cu cazurile de granita: nu le vezi, dar iti spune cate trec. Foloseste animatiile de mai sus daca nu-ti iese un caz.
""")

    c.md("""
**Exercitiul 1.** Semnul unui numar: `1` daca e pozitiv, `-1` daca e negativ, `0` daca e zero.
""")
    c.ex("""
def semn(x):
    pass  # TODO
""", """
def semn(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
""")
    c.cod("""
verifica('semn', semn, [((5,), 1), ((-3,), -1), ((0,), 0)],
         ascunse=[((0.5,), 1), ((-0.001,), -1), ((10 ** 9,), 1)],
         indiciu='trei cazuri: mai mare, mai mic, egal cu 0')
""")

    c.md("""
**Exercitiul 2.** Cel mai mare din trei numere, **fara** `max`. Foloseste ideea cu "campionul" din sectiunea 9.
""")
    c.ex("""
def maxim3(a, b, c):
    pass  # TODO
""", """
def maxim3(a, b, c):
    m = a
    if b > m:
        m = b
    if c > m:
        m = c
    return m
""")
    c.cod("""
import random
verifica('maxim3', maxim3, [((4, 9, 6), 9), ((-1, -5, -3), -1), ((7, 7, 7), 7)],
         ascunse=[((1, 2, 3), 3), ((3, 2, 1), 3), ((2, 3, 1), 3)],
         referinta=lambda a, b, c: max(a, b, c),
         generator=lambda: (random.randint(-9, 9), random.randint(-9, 9), random.randint(-9, 9)))
""")

    c.md("""
**Exercitiul 3.** An bisect. Un an e bisect daca se imparte la 4, **dar** nu se imparte la 100, **cu exceptia** anilor care se impart la 400 (`2000` e bisect, `1900` nu). Intoarce `True` / `False`.
""")
    c.ex("""
def este_bisect(an):
    pass  # TODO
""", """
def este_bisect(an):
    if an % 400 == 0:
        return True
    if an % 100 == 0:
        return False
    return an % 4 == 0
""")
    c.cod("""
import calendar
verifica('este_bisect', este_bisect, [((2024,), True), ((1900,), False), ((2000,), True), ((2023,), False)],
         ascunse=[((1600,), True), ((2100,), False), ((4,), True), ((1,), False)],
         referinta=calendar.isleap, generator=lambda: (random.randint(1, 3000),),
         indiciu='ordinea conteaza: intai cazul cel mai special (400), apoi 100, apoi 4')
""")

    c.md("""
**Exercitiul 4.** Calificativul dupa nota (poate fi cu zecimale): `>= 9` "Foarte bine", `>= 7` "Bine", `>= 5` "Suficient", altfel "Insuficient". Atentie la granite!
""")
    c.ex("""
def calificativ(nota):
    pass  # TODO
""", """
def calificativ(nota):
    if nota >= 9:
        return 'Foarte bine'
    elif nota >= 7:
        return 'Bine'
    elif nota >= 5:
        return 'Suficient'
    else:
        return 'Insuficient'
""")
    c.cod("""
verifica('calificativ', calificativ,
         [((10,), 'Foarte bine'), ((7,), 'Bine'), ((5,), 'Suficient'), ((4.99,), 'Insuficient')],
         ascunse=[((9,), 'Foarte bine'), ((8.99,), 'Bine'), ((6.99,), 'Suficient'), ((0,), 'Insuficient'), ((7.5,), 'Bine')],
         indiciu='9 intra la Foarte bine, 8.99 nu')
""")

    c.md("""
**Exercitiul 5.** Salutul dupa ora (0-23): de la 5 la 11 "Buna dimineata", de la 12 la 17 "Buna ziua", de la 18 la 21 "Buna seara", in rest "Noapte buna". Incearca lantul de comparatii `a <= ora < b`.
""")
    c.ex("""
def salut(ora):
    pass  # TODO
""", """
def salut(ora):
    if 5 <= ora < 12:
        return 'Buna dimineata'
    elif 12 <= ora < 18:
        return 'Buna ziua'
    elif 18 <= ora < 22:
        return 'Buna seara'
    else:
        return 'Noapte buna'
""")
    c.cod("""
def salut_ref(ora):
    if 5 <= ora <= 11:
        return 'Buna dimineata'
    if 12 <= ora <= 17:
        return 'Buna ziua'
    if 18 <= ora <= 21:
        return 'Buna seara'
    return 'Noapte buna'


verifica('salut', salut, [((8,), 'Buna dimineata'), ((15,), 'Buna ziua'), ((20,), 'Buna seara'), ((2,), 'Noapte buna')],
         referinta=salut_ref, generator=lambda: (random.randint(0, 23),), n=30,
         ascunse=[((4,), 'Noapte buna'), ((5,), 'Buna dimineata'), ((11,), 'Buna dimineata'), ((12,), 'Buna ziua'),
                  ((17,), 'Buna ziua'), ((18,), 'Buna seara'), ((21,), 'Buna seara'), ((22,), 'Noapte buna')])
""")

    c.md("""
**Exercitiul 6.** Tipul unui triunghi cu laturile `a`, `b`, `c`: `'nu exista'`, `'echilateral'`, `'isoscel'` sau `'scalen'`. Un triunghi exista doar daca toate laturile sunt pozitive si **fiecare** latura e mai mica decat suma celorlalte doua (`1, 2, 3` nu formeaza triunghi). Intai verifica existenta.
""")
    c.ex("""
def tip_triunghi(a, b, c):
    pass  # TODO
""", """
def tip_triunghi(a, b, c):
    if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:
        return 'nu exista'
    if a == b == c:
        return 'echilateral'
    if a == b or b == c or a == c:
        return 'isoscel'
    return 'scalen'
""")
    c.cod("""
verifica('tip_triunghi', tip_triunghi,
         [((3, 4, 5), 'scalen'), ((2, 2, 2), 'echilateral'), ((5, 5, 8), 'isoscel'), ((1, 2, 3), 'nu exista')],
         ascunse=[((1, 1, 5), 'nu exista'), ((0, 0, 0), 'nu exista'), ((-3, 4, 5), 'nu exista'), ((5, 8, 5), 'isoscel'),
                  ((8, 5, 5), 'isoscel'), ((7, 7, 7), 'echilateral'), ((2, 3, 4), 'scalen'), ((10, 1, 1), 'nu exista')],
         indiciu='cazul "nu exista" se verifica primul; 1 + 2 = 3 nu e suficient (trebuie strict mai mare)')
""")

    c.md("""
**Exercitiul 7.** Program ca la concurs: citeste un numar intreg `n`. Pe prima linie afiseaza `par` sau `impar`, pe a doua `pozitiv`, `negativ` sau `zero`. Sunt doua decizii independente, deci doua lanturi separate.
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    n = int(input())
    if n % 2 == 0:
        print('par')
    else:
        print('impar')
    if n > 0:
        print('pozitiv')
    elif n < 0:
        print('negativ')
    else:
        print('zero')
""")
    c.cod("""
verifica_program('par/impar si semn', main,
                 [(['7'], 'impar\\npozitiv'), (['-4'], 'par\\nnegativ'), (['0'], 'par\\nzero')],
                 ascunse=[(['-3'], 'impar\\nnegativ'), (['100'], 'par\\npozitiv'), (['1'], 'impar\\npozitiv')],
                 indiciu='restul lui -3 la 2 e 1 in Python, deci merge fara cazuri speciale')
scor()
""")

    c.md("""
## Recapitulare

- `if` / `elif` / `else`: se executa **prima** ramura adevarata. Ordinea conditiilor conteaza (cea mai specifica intai).
- Doua `if`-uri separate sunt independente, un `elif` depinde de cele de deasupra.
- Blocurile se marcheaza prin `:` si indentare. Nu exista acolade.
- `1 < x < 10` merge ca la matematica (spre deosebire de C++). `==` compara valori, `is` doar pentru `None`.
- Fals: `0`, `0.0`, `''`, `[]`, `{}`, `None`. `and` / `or` intorc un operand si se opresc devreme. Precedenta: `not`, `and`, `or`, dar pune paranteze.
- `x == 1 or 2` e mereu adevarat: scrie `x in (1, 2)`. Textele se compara alfabetic. Floaturile nu se compara cu `==`.
- Testeaza mereu la granita: 17, 18, 19.
- `max`, `min`, `abs`, `sorted` fac treaba scurt si sigur, dar trebuie sa stii sa o scrii si de mana.
- ML: un arbore de decizie = if-uri cu praguri invatate din date.

Tema (notebook-ul urmator) are 10 exercitii cu teste ascunse, inclusiv una in care iti scrii singur arborele pe datele elevilor.
""")
    c.salveaza('02-structuri-decizionale-predare')


def tema():
    c = Carnet('Structuri decizionale', 'tema', fisiere=('date/elevi.csv',))
    c.md("""
Exercitiile de acasa. Testele vizibile iti arata daca ai inteles enuntul, cele **ascunse** verifica granitele si cazurile ciudate. Poti rula o celula de verificare de cate ori vrei. La final, `scor()` aduna tot.

Daca te blochezi, intoarce-te la notebook-ul de predare si deseneaza-ti pe hartie ramurile (sau pune codul intr-un `%%vezi`). Aici conteaza sa gandesti tu.
""")

    c.md("""
### 1. Cel mai apropiat de 10

Intoarce dintre `a` si `b` numarul care e mai aproape de 10. Daca sunt la aceeasi distanta (de ex. `8` si `12`), intoarce-l pe cel **mai mic**.
""")
    c.ex("""
def mai_aproape_de_10(a, b):
    pass  # TODO
""", """
def mai_aproape_de_10(a, b):
    da = abs(a - 10)
    db = abs(b - 10)
    if da < db:
        return a
    elif db < da:
        return b
    return min(a, b)
""")
    c.cod("""
verifica('mai_aproape_de_10', mai_aproape_de_10, [((9, 15), 9), ((8, 12), 8), ((10, 3), 10)],
         ascunse=[((12, 8), 8), ((-5, 30), -5), ((11, 9), 9), ((10, 10), 10), ((0, 21), 0)], puncte=1)
""")

    c.md("""
### 2. Ecuatia de gradul 2

Pentru `a*x^2 + b*x + c = 0` (cu `a != 0`), intoarce **lista** radacinilor reale, in ordine crescatoare: `[]` daca nu are, `[x]` daca are una, `[x1, x2]` daca are doua. Discriminantul: `d = b*b - 4*a*c`. Radicalul il faci cu `d ** 0.5`.

Atentie: pentru `a < 0` radacina cu `-` si cea cu `+` vin in ordine inversa.
""")
    c.ex("""
def radacini(a, b, c):
    pass  # TODO
""", """
def radacini(a, b, c):
    d = b * b - 4 * a * c
    if d < 0:
        return []
    elif d == 0:
        return [-b / (2 * a)]
    x1 = (-b - d ** 0.5) / (2 * a)
    x2 = (-b + d ** 0.5) / (2 * a)
    return sorted([x1, x2])
""")
    c.cod("""
verifica('radacini', radacini, [((1, -3, 2), [1, 2]), ((1, 2, 1), [-1]), ((1, 0, 1), [])],
         ascunse=[((-1, 0, 4), [-2, 2]), ((2, -4, -6), [-1, 3]), ((1, 0, 0), [0]), ((-2, 4, -2), [1]),
                  ((1, 1, -1), [(-1 - 5 ** 0.5) / 2, (-1 + 5 ** 0.5) / 2]), ((3, 0, 5), [])],
         indiciu='trei cazuri dupa semnul lui d; pentru a < 0 ordoneaza radacinile (sorted)', puncte=3)
""")

    c.md("""
### 3. Data valida

Intoarce `True` daca `zi/luna/an` este o data reala din calendar (`an >= 1`). Nu uita: aprilie, iunie, septembrie si noiembrie au 30 de zile, februarie are 28 sau 29 (an bisect), restul 31.
""")
    c.ex("""
def data_valida(zi, luna, an):
    pass  # TODO
""", """
def data_valida(zi, luna, an):
    if an < 1 or luna < 1 or luna > 12 or zi < 1:
        return False
    if luna in (4, 6, 9, 11):
        maxim = 30
    elif luna == 2:
        bisect = an % 400 == 0 or (an % 4 == 0 and an % 100 != 0)
        maxim = 29 if bisect else 28
    else:
        maxim = 31
    return zi <= maxim
""")
    c.cod("""
import datetime, random


def data_ref(zi, luna, an):
    try:
        datetime.date(an, luna, zi)
        return True
    except ValueError:
        return False


verifica('data_valida', data_valida,
         [((29, 2, 2024), True), ((29, 2, 2023), False), ((31, 4, 2020), False), ((31, 12, 1999), True), ((0, 5, 2000), False)],
         ascunse=[((29, 2, 1900), False), ((29, 2, 2000), True), ((28, 2, 1900), True), ((30, 2, 2024), False),
                  ((15, 13, 2000), False), ((15, 0, 2000), False), ((-1, 3, 2000), False), ((31, 6, 2000), False)],
         referinta=data_ref, n=60,
         generator=lambda: (random.randint(-2, 33), random.randint(-1, 14), random.randint(1, 3000)),
         indiciu='verifica intai luna (1..12), apoi ziua fata de numarul de zile al lunii', puncte=3)
""")

    c.md("""
### 4. Termostatul

Un termostat primeste temperatura `temp` (grade) si umiditatea `um` (procente) si intoarce o actiune. Regulile, **in ordinea prioritatii**:

1. `temp >= 40` sau `temp <= 0`: `'alarma'`
2. `temp > 24`: `'racire'`
3. `temp < 18`: `'incalzire'`
4. altfel (temperatura e ok), dar `um > 60`: `'ventilatie'`
5. altfel: `'ok'`

Ordinea din enunt e cea din cod: daca o schimbi, iese alt raspuns.
""")
    c.ex("""
def termostat(temp, um):
    pass  # TODO
""", """
def termostat(temp, um):
    if temp >= 40 or temp <= 0:
        return 'alarma'
    elif temp > 24:
        return 'racire'
    elif temp < 18:
        return 'incalzire'
    elif um > 60:
        return 'ventilatie'
    return 'ok'
""")
    c.cod("""
verifica('termostat', termostat,
         [((40, 50), 'alarma'), ((30, 40), 'racire'), ((10, 40), 'incalzire'), ((20, 80), 'ventilatie'), ((20, 40), 'ok')],
         ascunse=[((0, 50), 'alarma'), ((-5, 10), 'alarma'), ((24, 50), 'ok'), ((24.1, 30), 'racire'), ((18, 61), 'ventilatie'),
                  ((17.9, 90), 'incalzire'), ((20, 60), 'ok'), ((39, 80), 'racire'), ((1, 99), 'incalzire')], puncte=2)
""")

    c.md("""
### 5. Repara codul: reducerea

Un magazin da reducere dupa suma cumparata: peste `100` lei `5%`, peste `500` lei `10%`, peste `1000` lei `20%` (praguri **incluse**: exact 100 lei dau 5%). Functia de mai jos pare buna, dar cine cumpara de `700` lei primeste doar `5%`. Uita-te in animatie de ce.
""")
    c.cod("""
%%vezi 700
suma = int(input())
if suma >= 100:             #: 700 >= 100 e adevarat...
    procent = 5             #: ...si de aici nu mai pleaca nicaieri
elif suma >= 500:
    procent = 10
elif suma >= 1000:
    procent = 20
else:
    procent = 0
print(procent)
""")
    c.ex("""
def reducere(suma):
    if suma >= 100:
        return 5
    elif suma >= 500:
        return 10
    elif suma >= 1000:
        return 20
    else:
        return 0
""", """
def reducere(suma):
    if suma >= 1000:
        return 20
    elif suma >= 500:
        return 10
    elif suma >= 100:
        return 5
    else:
        return 0
""")
    c.cod("""
verifica('reducere', reducere, [((700,), 10), ((50,), 0), ((1500,), 20), ((100,), 5)],
         ascunse=[((99,), 0), ((499,), 5), ((500,), 10), ((999,), 10), ((1000,), 20), ((0,), 0)],
         indiciu='cea mai mare conditie trebuie prima: 700 >= 100 e adevarat, dar 700 >= 500 e mai specific', puncte=1)
""")

    c.md("""
### 6. Inchirierea unei masini

O firma inchiriaza o masina daca persoana are **cel putin 21 de ani**, permis de **cel putin 2 ani** si (**card** de credit **sau** depozit in numerar). Parametrii `card` si `depozit` sunt `True` / `False`. Intoarce `True` / `False`, fara `if`: o singura expresie booleana. Atentie la paranteze si la precedenta lui `and` fata de `or`.
""")
    c.ex("""
def poate_inchiria(varsta, ani_permis, card, depozit):
    pass  # TODO
""", """
def poate_inchiria(varsta, ani_permis, card, depozit):
    return varsta >= 21 and ani_permis >= 2 and (card or depozit)
""")
    c.cod("""
verifica('poate_inchiria', poate_inchiria,
         [((25, 5, True, False), True), ((25, 5, False, False), False), ((19, 3, True, True), False)],
         ascunse=[((21, 2, False, True), True), ((20, 2, True, True), False), ((30, 1, True, True), False),
                  ((16, 0, False, True), False), ((40, 10, True, True), True), ((21, 2, False, False), False)],
         indiciu='fara paranteze, `a and b and c or d` se citeste `(a and b and c) or d`', puncte=2)
""")

    c.md("""
### 7. Program: trei numere in ordine

Pe o singura linie ai trei numere intregi separate prin spatiu. Afiseaza-le **in ordine crescatoare**, tot pe o linie, separate prin spatiu. (Poti folosi `sorted`, dar incearca si varianta de mana in cap: cate comparatii ti trebuie?)
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    v = list(map(int, input().split()))
    print(*sorted(v))
""")
    c.cod("""
verifica_program('trei numere sortate', main,
                 [(['5 2 9'], '2 5 9'), (['1 2 3'], '1 2 3'), (['-1 -5 0'], '-5 -1 0')],
                 ascunse=[(['3 3 1'], '1 3 3'), (['10 9 8'], '8 9 10'), (['0 0 0'], '0 0 0'), (['100 -100 5'], '-100 5 100')],
                 indiciu='print(*lista) afiseaza elementele separate prin spatiu', puncte=2)
""")

    c.md("""
### 8. Program: cadranul

Pe o linie ai coordonatele `x y` ale unui punct (numere intregi). Afiseaza cadranul in care se afla: `1` (x>0, y>0), `2` (x<0, y>0), `3` (x<0, y<0), `4` (x>0, y<0). Daca punctul e pe una dintre axe (sau in origine) afiseaza `axa`.
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    x, y = map(int, input().split())
    if x == 0 or y == 0:
        print('axa')
    elif x > 0 and y > 0:
        print(1)
    elif x < 0 and y > 0:
        print(2)
    elif x < 0 and y < 0:
        print(3)
    else:
        print(4)
""")
    c.cod("""
verifica_program('cadran', main,
                 [(['3 5'], '1'), (['-3 5'], '2'), (['-3 -5'], '3'), (['3 -5'], '4'), (['0 5'], 'axa')],
                 ascunse=[(['0 0'], 'axa'), (['7 0'], 'axa'), (['-1 -1'], '3'), (['1000000 -1'], '4'), (['-2 0'], 'axa')], puncte=2)
""")

    c.md("""
### 9. Provocare: arborele tau de decizie

Scrie `calificat_probabil(nota_info, ore, absente)` care intoarce `1` sau `0`, cu **regulile tale**, astfel incat sa ghiceasca corect **cel putin 77%** din elevii din `elevi.csv`. Ca sa ai repere: "mereu 0" are 66%, regula din predare 72%, iar arborele cu adancime 2 invatat de scikit-learn 76.7%. Tu trebuie sa-l bati.

Sfat: incepe cu un singur prag pe `nota_info`, apoi vezi daca `ore` sau `absente` mai ajuta, si masoara cu `acuratete(...)` dupa fiecare schimbare. Nu te astepta la 100%: datele sunt zgomotoase. Un arbore mai adanc ar ajunge si la 83% pe datele astea, dar ar fi memorat zgomotul si ar ghici prost pe elevi noi.
""")
    c.cod(AJUTOR_ELEVI)
    c.ex("""
def calificat_probabil(nota_info, ore, absente):
    pass  # TODO: intoarce 1 sau 0
""", """
def calificat_probabil(nota_info, ore, absente):
    if nota_info >= 6.5:
        return 1
    elif nota_info >= 5.5 and ore >= 10:
        return 1
    return 0
""")
    c.cod("""
print('acuratete:', round(acuratete(calificat_probabil), 3))
verifica_egal('acuratete >= 77%', acuratete(calificat_probabil) >= 0.77, True,
              indiciu='un singur prag pe nota_info da ~75%; mai adauga o conditie cu ore sau absente si masoara cu acuratete(...)', puncte=3)
""")

    c.md("""
### 10. Provocare: intersectia a doua intervale

Ai intervalele `[a, b]` si `[c, d]` (cu `a <= b` si `c <= d`). Intoarce intersectia lor ca tuplu `(inceput, sfarsit)`, sau `None` daca nu au niciun punct comun. Intervalele care doar se ating (`[1, 3]` si `[3, 5]`) au intersectia `(3, 3)`. Aici `max` si `min` chiar merita.
""")
    c.ex("""
def intersectie(a, b, c, d):
    pass  # TODO
""", """
def intersectie(a, b, c, d):
    inceput = max(a, c)
    sfarsit = min(b, d)
    if inceput <= sfarsit:
        return (inceput, sfarsit)
    return None
""")
    c.cod("""
verifica('intersectie', intersectie, [((1, 5, 3, 8), (3, 5)), ((1, 2, 3, 4), None), ((1, 3, 3, 5), (3, 3))],
         ascunse=[((0, 10, 2, 3), (2, 3)), ((5, 6, 1, 2), None), ((-5, -1, -3, 4), (-3, -1)), ((2, 3, 0, 10), (2, 3)),
                  ((1, 1, 1, 1), (1, 1)), ((1, 4, 5, 9), None)],
         indiciu='intersectia incepe la max(a, c) si se termina la min(b, d); exista doar daca inceput <= sfarsit', puncte=2)
scor()
""")
    c.salveaza('02-structuri-decizionale-tema')


if __name__ == '__main__':
    predare()
    tema()
