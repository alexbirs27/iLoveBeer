"""Genereaza 01-structuri-liniare-predare.ipynb si 01-structuri-liniare-tema.ipynb (+ variantele cu solutii)."""
from nb import Carnet


def predare():
    c = Carnet('Structuri liniare', 'predare')

    c.md("""
## Ce e un program liniar

Un program liniar face lucrurile in ordine, de sus in jos, fiecare instructiune o singura data. Nu sare, nu se repeta, nu alege. Alegerea (`if`) si repetarea (`for`, `while`) vin in notebook-urile urmatoare.

Pare putin, dar aici se pierd cele mai multe puncte la inceput: citesti gresit datele, uiti ca `input()` da text, imparti cu `/` cand voiai `//`. Le luam pe rand.

**Cum lucram.** Text scurt, cod, apoi animatie. Celulele care incep cu `%%vezi` nu doar ruleaza codul, ti-l arata pas cu pas: in stanga linia curenta (galben), in dreapta memoria, jos ce afiseaza programul. Ce se schimba la un pas clipeste. Foloseste butoanele, slider-ul sau sagetile stanga/dreapta de la tastatura (da click pe animatie mai intai).
""")

    c.md("""
## 1. Un program e o lista de pasi

**Prezice inainte sa rulezi:** cat e `s` la final?

<details><summary>Raspuns</summary>

`s` este 12. Dar uita-te in animatie la ordine: `s` nu exista pana la linia 3, si abia acolo se calculeaza `a + b`.
</details>
""")
    c.cod("""
%%vezi
a = 5           #: a primeste valoarea 5
b = 7           #: b primeste valoarea 7
s = a + b       #: mai intai se calculeaza a + b, abia apoi rezultatul intra in s
print(s)        #: print scrie in zona neagra de jos
""")

    c.md("""
## 2. Variabile si tipuri

O variabila e un nume pus pe o valoare. **Nu declari tipul**, Python il stie din valoare, si acelasi nume poate ajunge pe alt tip mai tarziu (ceea ce e comod si periculos in acelasi timp).

| tip | ce tine | exemplu |
|---|---|---|
| `int` | numar intreg, oricat de mare | `42`, `-7`, `10**30` |
| `float` | numar cu zecimale | `3.14`, `-0.5`, `2e3` |
| `str` | text | `'ana'`, `"ana"` |
| `bool` | adevarat / fals | `True`, `False` |
| `NoneType` | "nimic" | `None` |

Un `int` din Python nu se depaseste niciodata (nu exista overflow ca la C++). Un `10**30` e in regula.
""")
    c.cod("""
%%vezi
x = 42              #: x e int
x = 3.14            #: acelasi nume, acum float
x = 'salut'         #: si acum str. Vechea valoare nu mai e legata de nimic
gata = x == 'salut' #: o comparatie da un bool
print(type(x))
""")

    c.cod("""
for v in [42, 3.14, 'ana', True, None, 10**30]:
    print(repr(v), '->', type(v).__name__)
""")

    c.md("""
## 3. Atribuirea

Semnul `=` **nu e egalitate**, e ordin: "calculeaza ce e in dreapta si pune rezultatul pe numele din stanga".

**Din topor** - cum interschimbi doua valori la C++ (si aici merge la fel), cu o variabila ajutatoare:
""")
    c.cod("""
%%vezi
a = 3
b = 8
aux = a          #: o punem pe a la adapost
a = b            #: acum a poate fi suprascris
b = aux          #: b ia vechea valoare a lui a
""")
    c.md("""
**Varianta Python** - atribuire multipla. Partea dreapta se calculeaza complet inainte sa se atribuie ceva, de-asta merge fara `aux`:
""")
    c.cod("""
%%vezi
a = 3
b = 8
a, b = b, a      #: dreapta devine (8, 3), apoi se pune in (a, b)
""")

    c.md("""
## 4. Citirea datelor

**Regula de aur: `input()` intoarce mereu text (`str`), chiar daca ai scris cifre.**

Iata capcana clasica. Vezi ce iese cand aduni doua "numere" citite direct (animatia primeste ca date de intrare `3` si `4`, scrise pe prima linie a celulei):
""")
    c.cod("""
%%vezi 3 4
a = input()      #: textul '3', nu numarul 3 (uita-te la ghilimele)
b = input()
print(a + b)     #: la text, + inseamna lipire
""")
    c.md("""
Il transformi cu `int()` (sau `float()` pentru zecimale):
""")
    c.cod("""
%%vezi 3 4
a = int(input())
b = int(input())
print(a + b)
""")
    c.md("""
**Doua numere pe aceeasi linie** (asa vin datele in aproape orice problema). Intai pas cu pas, ca sa vezi ce face fiecare bucata:
""")
    c.cod("""
%%vezi 3 4
linie = input()           #: o singura linie, ca text: '3 4'
bucati = linie.split()    #: o taie dupa spatii: ['3', '4']
a = int(bucati[0])        #: fiecare bucata trebuie transformata separat
b = int(bucati[1])
print(a + b)
""")
    c.md("""
Acum scurtatura pe care o vei folosi mereu. Stii ce face, deci nu mai e magie:

```python
a, b = map(int, input().split())          # doua numere
v = list(map(int, input().split()))       # oricate numere, intr-o lista
```

`map(int, ...)` aplica `int` pe fiecare bucata. Asa nu scrii `int(...)` de n ori.
""")

    c.md("""
## 5. Afisarea

`print` pune spatiu intre argumente si `\\n` la sfarsit. Le schimbi cu `sep=` si `end=`:
""")
    c.cod("""
%%vezi
print('a', end=' ')        #: end=' ' -> nu trece la linie noua
print('b', end=' ')
print('c')
print(1, 2, 3, sep='-')   #: sep schimba ce pune intre argumente
print()                   #: o linie goala
""")
    c.md("""
**f-string** = text cu valori inauntru, intre acolade. Dupa `:` spui cum sa arate valoarea. `:.2f` inseamna "2 zecimale":
""")
    c.cod("""
nume, nota, medie = 'Ana', 9, 8.6666
print(f'{nume} are nota {nota}')
print(f'media este {medie:.2f}')       # rotunjeste la afisare, nu modifica medie
print(f'media este {medie:8.2f}|')     # 8 caractere latime, aliniat la dreapta
print('Ana' + ' are ' + str(9) + ' puncte')   # varianta veche: trebuie str(...) pe numere
""")

    c.md("""
## 6. Operatii aritmetice

| operator | ce face | exemplu |
|---|---|---|
| `+ - *` | ca in matematica | `17 * 5 = 85` |
| `/` | impartire, **mereu float** | `17 / 5 = 3.4` |
| `//` | catul intreg | `17 // 5 = 3` |
| `%` | restul | `17 % 5 = 2` |
| `**` | ridicare la putere | `2 ** 10 = 1024` |

**Prezice:** cat dau `-7 // 2` si `-7 % 3`? Daca te-ai obisnuit cu C++, raspunsul te poate surprinde.

<details><summary>Raspuns</summary>

`-7 // 2 = -4` si `-7 % 3 = 2`. Python **rotunjeste catul spre minus infinit**, iar restul are mereu semnul impartitorului. C++ taie catul spre 0 (`-7 / 2 = -3`) si da `-7 % 3 = -1`. Legatura care ramane adevarata in ambele: `a == (a // b) * b + a % b`.
</details>
""")
    c.cod("""
print(17 / 5, 17 // 5, 17 % 5, 2 ** 10)
print(-7 // 2, -7 % 3)
print(divmod(17, 5))          # catul si restul deodata
print(int(-2.7), round(-2.7)) # int() taie zecimalele
print(round(2.5), round(3.5)) # round merge la cel mai apropiat PAR la jumatati
""")

    c.md("""
## 7. Cifrele unui numar

Cea mai folosita tehnica din acest notebook. **Ultima cifra** = `n % 10`. **Numarul fara ultima cifra** = `n // 10`. Cu doua operatii extragi tot.

Uita-te cum "se tocesc" numarul si cum iese fiecare cifra:
""")
    c.cod("""
%%vezi
n = 4729
c1 = n % 10       #: restul la 10 = ultima cifra
n = n // 10       #: catul la 10 = numarul fara ultima cifra
c2 = n % 10
n = n // 10
c3 = n % 10
n = n // 10
c4 = n
""")
    c.md("""
**Alta cale:** transformi numarul in text si iei caracterele. Merge, dar fiecare caracter trebuie readus la numar. Aritmetica ramane varianta de baza: iti da si ultima cifra, si "restul de numar", si o vei folosi in bucle la notebook-ul urmator.
""")
    c.cod("""
n = 4729
s = str(n)
print(s[0], s[-1], int(s[0]) + int(s[-1]))
print(sum(map(int, str(n))))      # suma cifrelor intr-o linie; stii acum ce face fiecare bucata
""")

    c.md("""
## 8. Modulul `math`

Functiile matematice mai rare nu sunt "din start", le aduci cu `import`:
""")
    c.cod("""
import math

print(math.sqrt(16), 16 ** 0.5)           # radacina patrata, doua feluri
print(math.floor(-2.5), math.ceil(-2.5))  # rotunjire in jos / in sus
print(math.gcd(12, 18), math.pi)
print(math.hypot(3, 4))                   # sqrt(3*3 + 4*4)
""")

    c.md("""
## 9. Capcane (le vezi acum ca sa nu te prinda la concurs)

**Capcana 1: zecimalele nu sunt exacte.** Calculatorul tine numerele in binar, iar `0.1` nu are reprezentare exacta. Nu compara doua `float` cu `==`, compara diferenta cu o toleranta:
""")
    c.cod("""
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print(abs((0.1 + 0.2) - 0.3) < 1e-9)
print(math.isclose(0.1 + 0.2, 0.3))
""")
    c.md("""
**Capcana 2: sa acoperi o functie din Python cu o variabila.** `sum`, `max`, `min`, `list`, `len`, `str`, `input` sunt nume obisnuite in Python. Daca le folosesti pentru variabile, functia dispare, si eroarea apare mult mai tarziu:
""")
    c.cod("""
%%vezi
sum = 10            #: am pus numele 'sum' pe un numar
print(sum([1, 2]))  #: acum sum nu mai e functia, e numarul 10
""")
    c.md("""
**Capcana 3: variabila care nu exista.** Un nume nu exista pana nu ii dai o valoare. Aici uitam sa citim `b`:
""")
    c.cod("""
%%vezi
a = 5
print(a + b)
""")
    c.md("""
### Cum citesti o eroare

Nu te panica si nu o citi de sus in jos. Doua lucruri conteaza: **ultima linie** (ce s-a intamplat: `NameError`, `TypeError`, `ValueError`, `ZeroDivisionError`...) si **numarul liniei** din codul tau. In animatie, linia rosie e exact linia care a esuat.

| eroare | de obicei inseamna |
|---|---|
| `NameError` | ai scris gresit un nume sau nu l-ai definit inca |
| `TypeError` | ai combinat tipuri care nu se potrivesc (`5 + 'a'`) |
| `ValueError` | tipul e bun, valoarea nu (`int('abc')`) |
| `ZeroDivisionError` | impartire la 0 |
| `SyntaxError` | ai gresit scrierea (paranteza, doua puncte, ghilimele) |
""")
    c.cod("""
%%vezi
x = int('12a')
""")

    c.md("""
## 10. Exemplu complet

Aria si perimetrul unui dreptunghi, citit de la tastatura. In concurs scrii direct codul; aici il punem intr-o functie `main`, ca sa-l putem verifica automat. Corpul functiei e exact codul pe care l-ai scrie si fara functie.
""")
    c.cod("""
%%vezi 4 6
l = int(input())
L = int(input())
aria = l * L
perimetru = 2 * (l + L)
print(aria, perimetru)
""")

    c.md("""
## Exercitii

Acum le rezolvi tu. Fiecare exercitiu are o celula de completat si una de verificare. Daca un test pica, iti spune ce ai intors si ce trebuia. Nu ai nevoie de nimic in plus fata de ce ai vazut mai sus.

Pentru exercitii folosim functii (`def`). Nu te grabi sa le intelegi, o sa le inveti in detaliu mai tarziu. Acum doar completezi corpul: ce e dupa `return` este formula ta.
""")

    c.md("""
**Exercitiul 1.** Aria unui dreptunghi cu laturile `l` si `L`.
""")
    c.ex("""
def aria(l, L):
    pass  # TODO: intoarce aria
""", """
def aria(l, L):
    return l * L
""")
    c.cod("""
verifica('aria', aria, [((3, 4), 12), ((10, 10), 100)],
         ascunse=[((1, 1), 1), ((0, 5), 0), ((7, 2), 14)],
         indiciu='aria este latime * lungime; nu uita sa scrii return')
""")

    c.md("""
**Exercitiul 2.** Din grade Celsius in Fahrenheit: `F = C * 9 / 5 + 32`.
""")
    c.ex("""
def celsius_in_fahrenheit(c):
    pass  # TODO
""", """
def celsius_in_fahrenheit(c):
    return c * 9 / 5 + 32
""")
    c.cod("""
verifica('celsius', celsius_in_fahrenheit, [((100,), 212), ((0,), 32), ((-40,), -40)],
         ascunse=[((36.6,), 97.88), ((25,), 77)])
""")

    c.md("""
**Exercitiul 3.** Ultima cifra a unui numar natural si numarul fara ultima cifra, intoarse ca pereche `(fara_ultima, ultima)`. Ai nevoie de `//` si `%`. (Foloseste `divmod` doar dupa ce ai facut-o cu operatorii.)
""")
    c.ex("""
def desparte(n):
    pass  # TODO: intoarce (fara_ultima_cifra, ultima_cifra)
""", """
def desparte(n):
    return n // 10, n % 10
""")
    c.cod("""
verifica('desparte', desparte, [((4729,), (472, 9)), ((10,), (1, 0)), ((7,), (0, 7))],
         ascunse=[((1000,), (100, 0)), ((99999,), (9999, 9))],
         indiciu='intoarce doua valori: return a, b')
""")

    c.md("""
**Exercitiul 4.** Suma cifrelor unui numar cu exact trei cifre (fara bucle, cu ce ai vazut acum).
""")
    c.ex("""
def suma_cifre_3(n):
    pass  # TODO
""", """
def suma_cifre_3(n):
    return n // 100 + n // 10 % 10 + n % 10
""")
    c.cod("""
import random
verifica('suma_cifre_3', suma_cifre_3, [((123,), 6), ((999,), 27), ((100,), 1)],
         referinta=lambda n: sum(map(int, str(n))),
         generator=lambda: (random.randint(100, 999),))
""")

    c.md("""
**Exercitiul 5.** Interschimba doua valori si intoarce-le in noua ordine.
""")
    c.ex("""
def interschimba(a, b):
    pass  # TODO
""", """
def interschimba(a, b):
    a, b = b, a
    return a, b
""")
    c.cod("""
verifica('interschimba', interschimba, [((1, 2), (2, 1)), (('x', 'y'), ('y', 'x'))])
""")

    c.md("""
**Exercitiul 6.** Program ca la concurs: citeste doua numere intregi pe linii separate, afiseaza suma lor pe prima linie si produsul pe a doua. Aici `main` face exact ce ar face programul tau intreg.
""")
    c.ex("""
def main():
    pass  # TODO: citeste a si b, afiseaza suma, apoi produsul
""", """
def main():
    a = int(input())
    b = int(input())
    print(a + b)
    print(a * b)
""")
    c.cod("""
verifica_program('suma si produs', main,
                 [(['3', '4'], '7\\n12'), (['10', '-2'], '8\\n-20')],
                 ascunse=[(['0', '5'], '5\\n0')],
                 indiciu='citeste cu int(input()) de doua ori si foloseste doua print-uri')
""")

    c.md("""
**Exercitiul 7.** Cu ce ai vazut la `divmod`: transforma un numar de secunde in `(ore, minute, secunde)`. De ex. `3725` secunde sunt 1 ora, 2 minute, 5 secunde.
""")
    c.ex("""
def in_ore(total):
    pass  # TODO
""", """
def in_ore(total):
    ore, rest = divmod(total, 3600)
    minute, secunde = divmod(rest, 60)
    return ore, minute, secunde
""")
    c.cod("""
verifica('in_ore', in_ore, [((3725,), (1, 2, 5)), ((59,), (0, 0, 59)), ((3600,), (1, 0, 0))],
         ascunse=[((86399,), (23, 59, 59)), ((0,), (0, 0, 0))])
scor()
""")

    c.md("""
## Recapitulare

- Programul liniar se executa de sus in jos, fiecare linie o data.
- `input()` da **text**. `int()` / `float()` il transforma. `map(int, input().split())` citeste mai multe numere.
- `/` da float, `//` cat intreg, `%` rest. La numere negative Python rotunjeste spre minus infinit.
- Ultima cifra = `n % 10`, fara ultima cifra = `n // 10`.
- Nu pune nume de functii (`sum`, `max`, `list`) pe variabile. Nu compara `float` cu `==`.
- Eroarea: uita-te la ultima linie si la numarul liniei.

Tema (notebook-ul urmator) are mai multe exercitii, cu teste ascunse, ca la concurs.
""")
    c.salveaza('01-structuri-liniare-predare')


def tema():
    c = Carnet('Structuri liniare', 'tema')
    c.md("""
Aici sunt exercitiile de acasa. Testele vizibile iti arata daca ai inteles enuntul, cele **ascunse** verifica si cazurile limita (0, numere mari, negative). Poti rula o celula de verificare de cate ori vrei. La final, `scor()` aduna tot.

Daca te blochezi, inapoi la notebook-ul de predare, nu cauta solutii gata facute: aici conteaza sa gandesti tu.
""")

    c.md("""
### 1. Media aritmetica

Intoarce media a trei numere.
""")
    c.ex("""
def media3(a, b, c):
    pass  # TODO
""", """
def media3(a, b, c):
    return (a + b + c) / 3
""")
    c.cod("""
verifica('media3', media3, [((1, 2, 3), 2), ((10, 20, 30), 20), ((1, 1, 2), 4 / 3)],
         ascunse=[((-3, 3, 0), 0), ((7, 8, 9.5), 8.166666666666666)], puncte=1)
""")

    c.md("""
### 2. Ultimele doua cifre

Intoarce numarul format din ultimele doua cifre ale lui `n` (pentru `n < 10` intoarce `n`).
""")
    c.ex("""
def ultimele_doua(n):
    pass  # TODO
""", """
def ultimele_doua(n):
    return n % 100
""")
    c.cod("""
verifica('ultimele_doua', ultimele_doua, [((1234,), 34), ((7,), 7), ((100,), 0)],
         ascunse=[((99,), 99), ((123456789,), 89), ((5005,), 5)], puncte=1)
""")

    c.md("""
### 3. Cifra sutelor

Intoarce cifra sutelor unui numar (de ex. `4729 -> 7`, `85 -> 0`). Nu folosi `str`.
""")
    c.ex("""
def cifra_sutelor(n):
    pass  # TODO
""", """
def cifra_sutelor(n):
    return n // 100 % 10
""")
    c.cod("""
import random
verifica('cifra_sutelor', cifra_sutelor, [((4729,), 7), ((85,), 0), ((100,), 1)],
         referinta=lambda n: int(str(n).zfill(3)[-3]),
         generator=lambda: (random.randint(0, 10**7),), puncte=1)
""")

    c.md("""
### 4. Numarul rasturnat (3 cifre)

Pentru un numar cu exact trei cifre, intoarce numarul cu cifrele in ordine inversa (`123 -> 321`, `120 -> 21`, pentru ca `021` este `21`).
""")
    c.ex("""
def rasturnat3(n):
    pass  # TODO
""", """
def rasturnat3(n):
    return n % 10 * 100 + n // 10 % 10 * 10 + n // 100
""")
    c.cod("""
import random
verifica('rasturnat3', rasturnat3, [((123,), 321), ((120,), 21), ((505,), 505)],
         referinta=lambda n: int(str(n)[::-1]),
         generator=lambda: (random.randint(100, 999),), puncte=2)
""")

    c.md("""
### 5. Bancnote

Ai `suma` lei (numar natural). Intoarce cate bancnote de 100, 50, 10 si cate monede de 1 leu sunt necesare, luand mereu cat mai multe din cea mai mare valoare posibila: `(de_100, de_50, de_10, de_1)`. De ex. `278 -> (2, 1, 2, 8)`.

Ai nevoie doar de `//` si `%`, in lant: dupa fiecare pas ramai cu restul.
""")
    c.ex("""
def bancnote(suma):
    pass  # TODO
""", """
def bancnote(suma):
    de100, rest = divmod(suma, 100)
    de50, rest = divmod(rest, 50)
    de10, de1 = divmod(rest, 10)
    return de100, de50, de10, de1
""")
    c.cod("""
verifica('bancnote', bancnote, [((278,), (2, 1, 2, 8)), ((100,), (1, 0, 0, 0)), ((49,), (0, 0, 4, 9))],
         ascunse=[((0,), (0, 0, 0, 0)), ((999,), (9, 1, 4, 9)), ((60,), (0, 1, 1, 0))], puncte=2)
""")

    c.md("""
### 6. Repara codul

Functia de mai jos ar trebui sa intoarca **media aritmetica a cifrelor** unui numar cu exact doua cifre, dar da rezultate gresite. Gaseste greseala si repar-o. Ajuta-te de animatia din celula urmatoare.
""")
    c.cod("""
%%vezi
n = 47
c1 = n // 10
c2 = n % 10
media = c1 + c2 / 2
print(media)
""")
    c.ex("""
def media_cifre(n):
    c1 = n // 10
    c2 = n % 10
    media = c1 + c2 / 2
    return media
""", """
def media_cifre(n):
    c1 = n // 10
    c2 = n % 10
    media = (c1 + c2) / 2
    return media
""")
    c.cod("""
verifica('media_cifre', media_cifre, [((47,), 5.5), ((20,), 1), ((99,), 9)],
         ascunse=[((10,), 0.5), ((55,), 5)], indiciu='ordinea operatiilor: ce se imparte la 2?', puncte=1)
""")

    c.md("""
### 7. Program: bacsis

Citeste doua valori: `nota` de plata (numar cu zecimale) si `procent` bacsis (numar intreg). Afiseaza totalul de plata, cu **exact doua zecimale**. De ex. pentru `80` si `15` afiseaza `92.00`.
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    nota = float(input())
    procent = int(input())
    print(f'{nota + nota * procent / 100:.2f}')
""")
    c.cod("""
verifica_program('bacsis', main,
                 [(['80', '15'], '92.00'), (['100', '10'], '110.00'), (['33.5', '20'], '40.20')],
                 ascunse=[(['0', '10'], '0.00'), (['19.99', '5'], '20.99')], puncte=2)
""")

    c.md("""
### 8. Program: doua numere pe o linie

Pe o singura linie ai doua numere intregi, separate prin spatiu. Afiseaza pe o linie: **catul** si **restul** impartirii primului la al doilea, separate prin spatiu. Al doilea numar nu e 0.
""")
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    a, b = map(int, input().split())
    print(a // b, a % b)
""")
    c.cod("""
verifica_program('cat si rest', main,
                 [(['17 5'], '3 2'), (['10 2'], '5 0')],
                 ascunse=[(['-7 3'], '-3 2'), (['0 9'], '0 0'), (['1000000000 7'], '142857142 6')], puncte=2)
""")

    c.md("""
### 9. Provocare: distanta dintre doua puncte

Intoarce distanta dintre `(x1, y1)` si `(x2, y2)`. Formula o stii, iar `math` ti-a fost prezentat mai sus.
""")
    c.ex("""
import math


def distanta(x1, y1, x2, y2):
    pass  # TODO
""", """
import math


def distanta(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)
""")
    c.cod("""
verifica('distanta', distanta, [((0, 0, 3, 4), 5), ((1, 1, 1, 1), 0), ((-1, -1, 2, 3), 5)],
         ascunse=[((0, 0, 1, 1), 2 ** 0.5)], puncte=1)
""")

    c.md("""
### 10. Provocare: cifra de control

Pentru un numar cu exact 4 cifre, cifra de control este ultima cifra a sumei cifrelor. De ex. `4729`: `4+7+2+9 = 22`, cifra de control este `2`. Scrie functia **fara** `str` si **fara** `map`.
""")
    c.ex("""
def cifra_control(n):
    pass  # TODO
""", """
def cifra_control(n):
    s = n // 1000 + n // 100 % 10 + n // 10 % 10 + n % 10
    return s % 10
""")
    c.cod("""
import random
verifica('cifra_control', cifra_control, [((4729,), 2), ((1000,), 1), ((9999,), 6)],
         referinta=lambda n: sum(map(int, str(n))) % 10,
         generator=lambda: (random.randint(1000, 9999),), puncte=2)
scor()
""")
    c.salveaza('01-structuri-liniare-tema')


if __name__ == '__main__':
    predare()
    tema()
