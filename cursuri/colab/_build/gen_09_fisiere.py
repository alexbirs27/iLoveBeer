"""Genereaza 09-fisiere-predare.ipynb si 09-fisiere-tema.ipynb (+ variantele cu solutii).

Fisierele pe care le scriu celulele se creeaza in foldere temporare (nu ramane nimic langa notebook).
"""
from nb import Carnet

FISIERE = ('date/elevi.csv', 'date/09_forme.png', 'date/09_mic.png', 'anim_imagini.py')

# ajutor pentru testele exercitiilor: creeaza un fisier temporar, apeleaza functia elevului, sterge folderul
AJUTOR = r"""
import os, tempfile

def pe_fisier(f, continut, *alte, nume='a.txt'):
    # scrie 'continut' intr-un fisier temporar, apeleaza f(cale, *alte), sterge fisierul
    with tempfile.TemporaryDirectory() as d:
        cale = os.path.join(d, nume)
        with open(cale, 'w', encoding='utf-8', newline='') as g:
            g.write(continut)
        return f(cale, *alte)
"""


def predare():
    c = Carnet('Fisiere: text, CSV, imagini', 'predare', fisiere=FISIERE)

    c.md(r"""
## De ce fisiere

Pana acum datele veneau din `input()` sau din liste scrise de mana. La olimpiada (si in orice proiect de ML) datele stau in **fisiere**: un `train.csv` cu exemple, poze pentru un clasificator, iar raspunsul tau pleaca tot intr-un fisier, `submission.csv`. Cine nu stie sa citeasca si sa scrie fisiere nu poate nici macar sa-si trimita solutia.

Trei lucruri in acest notebook: **text**, **CSV** si **imagini**. Toate sunt, pana la urma, numere si siruri de caractere puse pe un disc.

Ca sa nu umplem folderul cu fisiere de test, scriem tot intr-un folder temporar. `ACASA` retine folderul cu datele cursului (`date/elevi.csv`, imaginile).
""")
    c.cod(r"""
import os, tempfile

ACASA = os.getcwd()                    # aici sunt date/elevi.csv si imaginile
os.chdir(tempfile.mkdtemp())           # de acum scriem intr-un folder temporar
print('lucram in', os.getcwd())
""")

    c.md(r"""
## 1. Fisiere text

Un fisier text e un sir lung de caractere, cu `\n` intre randuri. Ai nevoie de trei pasi: **deschizi**, **lucrezi**, **inchizi**. Instructiunea `with` inchide singura fisierul la sfarsit, chiar daca apare o eroare pe drum, deci o scrii mereu.

| mod | ce face |
|---|---|
| `'r'` | citeste (implicit); eroare daca fisierul nu exista |
| `'w'` | scrie; **sterge tot** ce era in fisier (il creeaza daca nu exista) |
| `'a'` | adauga la sfarsit, fara sa stearga |

**Prezice:** rulam de doua ori `open('x.txt', 'w')` si scriem de fiecare data `'a\n'`. Cate linii are fisierul?

<details><summary>Raspuns</summary>

Una singura. Modul `'w'` goleste fisierul cand il deschide, deci a doua rulare il ia de la zero. Pentru a adauga se foloseste `'a'`.
</details>
""")
    c.cod(r"""
with open('note.txt', 'w', encoding='utf-8') as f:
    f.write('Ana 9\n')                # write NU pune singur \n
    f.write('Dan 7\n')
    print('Eva 10', file=f)           # print scrie in fisier si pune el \n

with open('note.txt', 'a', encoding='utf-8') as f:
    f.write('Ion 8\n')                # 'a' = la sfarsit

with open('note.txt', encoding='utf-8') as f:
    print(f.read())
""")
    c.md(r"""
`print(..., file=f)` si `f.write(...)` fac aproape acelasi lucru. Diferenta: `print` pune singur `\n` si transforma orice in text, `write` primeste doar text si scrie exact ce ii dai.

Citirea. Cea mai folosita forma e bucla pe fisier: `for linie in f`. Fiecare `linie` vine **cu `\n` la capat**, de aceea urmeaza aproape mereu `.strip()` (taie spatiile si `\n` de la capete) sau `.split()` (taie dupa spatii).
""")
    c.cod(r"""
%%vezi
suma = 0
with open('note.txt', encoding='utf-8') as f:
    for linie in f:                       #: f se parcurge linie cu linie; linia are \n la capat
        nume, nota = linie.split()        #: split() fara argument taie dupa spatii si scapa si de \n
        suma += int(nota)
""")
    c.md(r"""
Celelalte metode de citire, ca sa le recunosti:
""")
    c.cod(r"""
with open('note.txt', encoding='utf-8') as f:
    tot = f.read()                    # tot fisierul, un singur string
print(repr(tot))

with open('note.txt', encoding='utf-8') as f:
    print(repr(f.readline()))         # o singura linie
    print(repr(f.readline()))         # urmatoarea: fisierul isi tine minte pozitia
    print(f.readlines())              # restul, ca lista de linii

with open('note.txt', encoding='utf-8') as f:
    print([l.strip() for l in f])     # cel mai des: bucla, cu strip
""")
    c.md(r"""
**De ce bucla si nu `read()`?** `read()` aduce tot fisierul in memorie deodata. La un fisier de cativa GB, programul moare. Bucla tine in memorie **o singura linie** la un moment dat. Masuram cu `tracemalloc` (memoria maxima ocupata) pe un fisier cu 300.000 de linii:
""")
    c.cod(r"""
import tracemalloc

with open('mare.txt', 'w') as f:
    for i in range(300_000):
        f.write(f'{i}\n')

def suma_cu_read():
    with open('mare.txt') as f:
        return sum(int(x) for x in f.read().split())    # tot fisierul in memorie

def suma_pe_linii():
    with open('mare.txt') as f:
        return sum(int(l) for l in f)                   # o linie odata

for fct in (suma_cu_read, suma_pe_linii):
    tracemalloc.start()
    rez = fct()
    _, varf = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f'{fct.__name__:15} suma={rez}  memorie maxima ~ {varf / 1e6:.2f} MB')
""")
    c.md(r"""
### Diacritice: `encoding`

Un fisier tine octeti, nu litere. `encoding` spune cum se transforma literele in octeti si invers. Standardul de azi e `'utf-8'`. Daca deschizi un fisier cu alt encoding decat cel in care a fost scris, obtii litere stricate sau eroare. Pe Windows `open` fara `encoding` foloseste altceva decat utf-8, deci codul care merge in Colab poate crapa pe calculatorul de acasa. **Scrie mereu `encoding='utf-8'`.**

Ca sa avem litere romanesti fara sa le tastam, le scriem cu escape-uri (`\u0103` este `a` cu semn, `\u0219` este `s` cu virgula):
""")
    c.cod(r"""
text = 'Ana are mere \u0219i pere, iar \u021b\u0103ranul are \u00eenv\u0103\u021b\u0103tor'
with open('ro.txt', 'w', encoding='utf-8') as f:
    f.write(text + '\n')

with open('ro.txt', encoding='utf-8') as f:
    print(f.read().strip())               # citit corect
with open('ro.txt', encoding='latin-1') as f:
    print(f.read().strip())               # citit cu alt encoding: litere stricate
""")
    c.md(r"""
### Cai si fisiere care nu exista

`open('note.txt')` cauta fisierul relativ la **folderul curent** al programului (`os.getcwd()`). `os.path.exists` iti spune daca exista, `os.path.join` lipeste cai corect pe orice sistem, iar o cale scrisa complet (absoluta) merge de oriunde.
""")
    c.cod(r"""
print(os.path.exists('note.txt'), os.path.exists('nu_exista.txt'))
print(sorted(os.listdir('.')))                    # ce fisiere sunt in folderul curent
cale_elevi = os.path.join(ACASA, 'date', 'elevi.csv')
print(os.path.exists(cale_elevi))
""")
    c.md(r"""
Un fisier lipsa nu trebuie sa-ti dea programul peste cap: prinzi `FileNotFoundError` cu `try/except`.
""")
    c.cod(r"""
%%vezi
def citeste(cale):
    try:
        with open(cale, encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None                       #: nu exista: intoarcem None in loc sa crape programul

a = citeste('note.txt')
b = citeste('nu_exista.txt')
""")

    c.md(r"""
## 2. CSV

CSV (comma separated values) e un fisier text in care fiecare linie e un rand de tabel, iar valorile sunt separate prin virgula. De obicei prima linie e antetul (numele coloanelor). Aproape toate seturile de date de ML vin asa.

**Din topor**, un CSV se citeste cu ce stii deja: `split(',')`. Sa vedem unde se rupe. Fisierul de mai jos are trei feluri de linii: normala, cu o celula lipsa, si cu o virgula **in interiorul** unui nume:
""")
    c.cod(r"""
with open('mini.csv', 'w', encoding='utf-8') as f:
    f.write('nume,nota,clasa\n')
    f.write('Ana,9,10\n')
    f.write('Dan,,11\n')                     # nota lipseste
    f.write('"Popescu, Ion",8,12\n')         # virgula intre ghilimele face parte din nume
""")
    c.md(r"""
**Prezice:** cate campuri iese pentru fiecare linie, daca o tai cu `.split(',')`?

<details><summary>Raspuns</summary>

3, 3, 3 si... **4** pentru ultima. `split(',')` nu stie de ghilimele, taie si virgula din `"Popescu, Ion"`. Celula lipsa nu e o problema (da un sir gol, `''`), dar virgula din text strica tot.
</details>
""")
    c.cod(r"""
%%vezi
linii = ['Ana,9,10', 'Dan,,11', '"Popescu, Ion",8,12']
for linie in linii:
    campuri = linie.split(',')        #: taie la fiecare virgula, si la cea din ghilimele
    print(len(campuri), campuri)
""")
    c.md(r"""
Modulul `csv` din biblioteca standard stie regulile (ghilimele, virgule in text). `csv.reader` da fiecare rand ca lista de siruri. **Deschide fisierul cu `newline=''`**: modulul `csv` isi gestioneaza singur capetele de linie, iar fara asta pe Windows apar randuri goale intre randuri.
""")
    c.cod(r"""
import csv

with open('mini.csv', encoding='utf-8', newline='') as f:
    for rand in csv.reader(f):
        print(rand)
""")
    c.md(r"""
`csv.DictReader` foloseste prima linie ca nume de coloane si da fiecare rand ca dictionar. Codul se citeste mai bine (`r['nota']` in loc de `r[1]`) si nu se strica daca cineva schimba ordinea coloanelor.

**Atentie:** `csv` da mereu **siruri**. Celula lipsa e `''`, nu `0` si nu `None`. Conversia o faci tu, si trebuie sa prevezi celulele proaste:
""")
    c.cod(r"""
with open('mini.csv', encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        print(r['nume'], '->', repr(r['nota']))
""")
    c.cod(r"""
%%vezi
note = ['9', '', '8', 'absent']
bune = []
for t in note:
    try:
        bune.append(float(t))             #: float('') si float('absent') ridica ValueError
    except ValueError:
        pass                              #: celula proasta: o sarim
media = sum(bune) / len(bune)             #: media doar pe ce am putut citi
""")
    c.md(r"""
Acum pe un fisier real, `date/elevi.csv` (aproape 250 de elevi). Media notei la informatica, **de mana**, sarind peste celulele goale:
""")
    c.cod(r"""
suma, cate = 0, 0
with open(cale_elevi, encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        try:
            suma += float(r['nota_info'])
            cate += 1
        except ValueError:
            pass                          # celula goala
media_mana = suma / cate
print(cate, 'note valide; media =', round(media_mana, 4))
""")
    c.md(r"""
### Prima privire la pandas

Tot ce ai scris mai sus (deschis, `DictReader`, `try/except`, suma, numarat) e **o singura linie** in pandas. Il inveti pe larg in notebook-urile 10 si 11; aici vezi doar de ce il vei prefera:
""")
    c.cod(r"""
import pandas as pd

df = pd.read_csv(cale_elevi)
print(df.shape)
print(df['nota_info'].mean())             # mean() sare singur peste celulele lipsa (NaN)
verifica_egal('media de mana = pandas', media_mana, float(df['nota_info'].mean()))
""")
    c.md(r"""
Pandas ghiceste singur tipurile (coloana cu celule goale devine `float` cu `NaN`), sare peste valorile lipsa la statistici si e **mult mai rapid**: citirea e scrisa in C, nu in bucla de Python. Masuram pe un fisier cu 200.000 de randuri:
""")
    c.cod(r"""
import time
import numpy as np

x = np.random.default_rng(0).random(200_000).round(4)
with open('mare.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['id', 'x'])
    w.writerows(zip(range(len(x)), x))

def media_de_mana(cale):
    suma, n = 0, 0
    with open(cale, encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f):
            suma += float(r['x'])
            n += 1
    return suma / n

t = time.perf_counter(); m1 = media_de_mana('mare.csv'); t1 = time.perf_counter() - t
t = time.perf_counter(); m2 = pd.read_csv('mare.csv')['x'].mean(); t2 = time.perf_counter() - t
print(f'de mana: {m1:.5f} in {t1:.3f}s | pandas: {m2:.5f} in {t2:.3f}s | ~{t1 / t2:.0f}x mai repede')
""")
    c.md(r"""
Scrierea unui CSV: `csv.writer` (cu `newline=''` si aici). Vezi ca pune singur ghilimele cand valoarea contine virgula. Asa nu mai scrii tu `','.join(...)`, care ar strica exact cazul de mai sus.
""")
    c.cod(r"""
with open('rezultate.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['nume', 'nota'])
    w.writerow(['Popescu, Ion', 9])       # virgula in text: writer pune ghilimele
    w.writerows([['Ana', 10], ['Dan', 7]])

with open('rezultate.csv', encoding='utf-8') as f:
    print(f.read())
""")

    c.md(r"""
## 3. Cum iti trimiti raspunsul: `submission.csv`

La olimpiada nu afisezi raspunsul pe ecran. Programul tau scrie un fisier CSV cu trei coloane, iar judgele il citeste si iti da punctele:

| subtaskID | datapointID | answer |
|---|---|---|
| 1 | 1 | pisica |
| 1 | 2 | caine |

Cate un rand pentru fiecare exemplu de test, in aceasta forma exacta (numele coloanelor conteaza, la fel si numarul de randuri). In enuntul fiecarei probleme verifici detaliile: cate subtask-uri sunt, ce fel de valori se cer in `answer`.
""")
    c.cod(r"""
predictii = ['pisica', 'caine', 'pisica']         # raspunsurile modelului, in ordinea exemplelor

with open('submission.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['subtaskID', 'datapointID', 'answer'])
    for i, raspuns in enumerate(predictii, start=1):
        w.writerow([1, i, raspuns])

with open('submission.csv', encoding='utf-8') as f:
    print(f.read())
""")
    c.md(r"""
Cu pandas iese mai scurt, dar are o capcana: `to_csv` scrie implicit si indexul randurilor, adica o **coloana in plus** pe care judgele nu o asteapta. Adauga mereu `index=False`:
""")
    c.cod(r"""
sub = pd.DataFrame({'subtaskID': 1, 'datapointID': range(1, 4), 'answer': predictii})
print(sub.to_csv(index=False))                    # corect: fara cale, intoarce textul, ca sa vezi ce s-ar scrie
print(sub.to_csv())                               # gresit: prima coloana (indexul) n-are ce cauta aici
""")
    c.md(r"""
Inainte sa trimiti: citeste fisierul inapoi si verifica-l (numele coloanelor, numarul de randuri, ca nu lipseste niciun `datapointID`). Cateva secunde de verificare fac diferenta dintre 0 si punctajul real.
""")
    c.cod(r"""
verif = pd.read_csv('submission.csv')
print(list(verif.columns))
print(len(verif), 'randuri;', 'datapointID de la', verif['datapointID'].min(), 'la', verif['datapointID'].max())
""")

    c.md(r"""
## 4. Imagini

O imagine este o **matrice de numere**. Fiecare numar e un pixel.

- imagine in **tonuri de gri**: matrice `H x W`, valori `0` (negru) ... `255` (alb);
- imagine **color**: `H x W x 3`, cele trei numere din fiecare pixel sunt intensitatile de rosu, verde si albastru (**RGB**).

Tipul e `uint8` (intreg fara semn pe 8 biti, 0-255). Il retii, pentru ca de el se leaga o capcana mai jos.

Citim imaginea cu Pillow (`PIL`) si o transformam in tablou NumPy. Urmareste cum zoom-ul coboara de la imaginea intreaga pana la 64 de numere:
""")
    c.cod(r"""
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

mic = np.array(Image.open(os.path.join(ACASA, 'date', '09_mic.png')))
print(mic.shape, mic.dtype)
anim_pixeli(mic, 7, 13, 8)            # patratul 8 x 8 care incepe la randul 7, coloana 13
""")
    c.md(r"""
Acum una color. `.convert('RGB')` e un obicei bun: unele PNG-uri vin cu un canal in plus (transparenta) sau cu paleta, iar el le aduce mereu la 3 canale.
""")
    c.cod(r"""
forme = np.array(Image.open(os.path.join(ACASA, 'date', '09_forme.png')).convert('RGB'))
print(forme.shape, forme.dtype, forme.min(), forme.max())
print(forme[10, 10])                  # un pixel: [R, G, B]
print(forme[10, 10, 0])               # doar canalul rosu al pixelului
fig, ax = plt.subplots(1, 4, figsize=(10, 2.8))
ax[0].imshow(forme)
ax[0].set_title('RGB')
for i, nume in enumerate('RGB'):
    ax[i + 1].imshow(forme[:, :, i], cmap='gray', vmin=0, vmax=255)     # un canal = o matrice 2D
    ax[i + 1].set_title('canalul ' + nume)
for a in ax:
    a.axis('off')
plt.show()
""")
    c.md(r"""
Observa: patratul rosu e **luminos** in canalul R si intunecat in G si B. Cercul verde, invers.

Din faptul ca imaginea e un tablou, vine gratis tot ce stii de la slicing. Pe o matrice mica se vede clar:
""")
    c.cod(r"""
%%vezi
import numpy as np
img = np.array([[10, 20, 30, 40],
                [50, 60, 70, 80],
                [90, 100, 110, 120]])
sus_jos = img[::-1]               #: randurile in ordine inversa: oglindire pe verticala
stanga_dreapta = img[:, ::-1]     #: coloanele inversate: oglindire pe orizontala
bucata = img[0:2, 1:3]            #: decupaj: randurile 0-1, coloanele 1-2
""")
    c.md(r"""
**Capcana: decupajul nu e copie.** `img[0:2, 1:3]` e o "fereastra" catre aceeasi memorie. Daca modifici bucata, se schimba si imaginea originala. Pentru o copie adevarata: `.copy()`.
""")
    c.cod(r"""
%%vezi
import numpy as np
img = np.array([[10, 20, 30], [40, 50, 60]])
bucata = img[:, 0:2]
bucata[0, 0] = 999                #: bucata e o fereastra spre img: se schimba si img
copie = img[:, 0:2].copy()        #: .copy() da un tablou separat
copie[0, 1] = -1                  #: img ramane neatins
""")
    c.cod(r"""
fig, ax = plt.subplots(1, 4, figsize=(10, 2.8))
poze = [forme, forme[:, ::-1], forme[::-1], forme[8:28, 8:28]]
titluri = ['original', 'forme[:, ::-1]', 'forme[::-1]', 'forme[8:28, 8:28]']
for a, p, t in zip(ax, poze, titluri):
    a.imshow(p)
    a.set_title(t, fontsize=9)
    a.axis('off')
plt.show()
""")

    c.md(r"""
### Din color in tonuri de gri

Ochiul e mai sensibil la verde decat la rosu, iar la albastru cel mai putin. Formula uzuala pentru luminozitatea unui pixel:

`gri = 0.299 * R + 0.587 * G + 0.114 * B`

Un pixel, apoi o imagine 2 x 2, **din topor** (doua bucle):
""")
    c.cod(r"""
%%vezi
r, g, b = 205, 40, 40                        #: un pixel rosu
gri = 0.299 * r + 0.587 * g + 0.114 * b      #: verdele conteaza cel mai mult
""")
    c.cod(r"""
%%vezi
img = [[(255, 0, 0), (0, 255, 0)],
       [(0, 0, 255), (255, 255, 255)]]
gri = [[0, 0], [0, 0]]
for i in range(2):
    for j in range(2):
        r, g, b = img[i][j]                  #: despachetam pixelul (i, j)
        gri[i][j] = round(0.299 * r + 0.587 * g + 0.114 * b)
""")
    c.md(r"""
Aceeasi bucla pe imaginea `forme`, apoi varianta NumPy (inmultesti canalele cu ponderile si aduni pe axa 2), apoi cea din Pillow (`.convert('L')`, "L" vine de la luminance). Toate trei trebuie sa dea aproape acelasi lucru (Pillow rotunjeste la intregi):
""")
    c.cod(r"""
import time

def gri_bucle(img):
    h, w = img.shape[:2]
    gri = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            r, g, b = img[i, j]
            gri[i, j] = 0.299 * r + 0.587 * g + 0.114 * b
    return gri

def gri_numpy(img):
    return (img * np.array([0.299, 0.587, 0.114])).sum(axis=2)

gri = gri_bucle(forme)
verifica_egal('bucle = NumPy', gri, gri_numpy(forme))
gri_pil = np.array(Image.fromarray(forme).convert('L'))
verifica_egal('de mana = Pillow (+-1)', gri, gri_pil.astype(float), tol=1)

# si viteza, pe o bucata mai mare din fotografia din scikit-learn
from sklearn.datasets import load_sample_image
china = load_sample_image('china.jpg')[:200, :200]
t = time.perf_counter(); gri_bucle(china); t1 = time.perf_counter() - t
t = time.perf_counter(); gri_numpy(china); t2 = time.perf_counter() - t
print(f'{china.shape}: bucle {t1:.3f}s, NumPy {t2:.5f}s (~{t1 / t2:.0f}x)')
""")
    c.md(r"""
NumPy castiga de zeci sau sute de ori din acelasi motiv ca in orice alt loc: bucla ruleaza in C, pe memorie continua, in loc sa treaca prin interpretorul Python pentru fiecare din cele 40.000 de pixeli.

Ramai cu ideea, nu cu functia: **o operatie pe toata imaginea deodata e mai rapida si mai scurta decat bucla**. `.convert('L')` e cel mai scurt, dar acum stii ce face.
""")
    c.cod(r"""
gri_u8 = np.round(gri).astype(np.uint8)          # inapoi la intregi 0-255
fig, ax = plt.subplots(1, 2, figsize=(6, 3))
ax[0].imshow(forme)
ax[1].imshow(gri_u8, cmap='gray', vmin=0, vmax=255)      # vmin/vmax: altfel matplotlib "intinde" contrastul
for a in ax:
    a.axis('off')
plt.show()

Image.fromarray(gri_u8).save('gri.png')                  # salvare: din tablou uint8 inapoi in fisier
print(np.array(Image.open('gri.png')).shape)
""")

    c.md(r"""
### Luminozitate: capcana `uint8`

Sa luminam o imagine inseamna sa adunam un numar la fiecare pixel. Numai ca un `uint8` nu poate trece de 255: cand depaseste, **se rostogoleste** de la 0 (ca odometrul).

**Prezice:** ce iese la `250 + 10` daca `250` e un `uint8`?

<details><summary>Raspuns</summary>

`4`. `260` nu incape in 0-255, deci ramane `260 - 256 = 4`. Un pixel aproape alb devine aproape negru. Pe tablouri NumPy nu apare nicio eroare, doar imaginea iese cu pete ciudate.
</details>
""")
    c.cod(r"""
%%vezi
import numpy as np
a = np.array([100, 200, 250], dtype=np.uint8)
gresit = a + 10                                             #: 250 + 10 nu incape in uint8: se rostogoleste la 4
corect = np.clip(a.astype(int) + 10, 0, 255).astype(np.uint8)   #: trecem la int, taiem la 255, ne intoarcem la uint8
""")
    c.cod(r"""
gresit = gri_u8 + 60                                                    # uint8 + 60: pixelii albi ies negri
corect = np.clip(gri_u8.astype(int) + 60, 0, 255).astype(np.uint8)      # clip taie la 255

fig, ax = plt.subplots(1, 3, figsize=(9, 3))
for a, p, t in zip(ax, [gri_u8, gresit, corect], ['original', '+ 60 gresit', '+ 60 cu clip']):
    a.imshow(p, cmap='gray', vmin=0, vmax=255)
    a.set_title(t)
    a.axis('off')
plt.show()
""")
    c.md(r"""
(Pe un scalar NumPy, `np.uint8(250) + 10` da acelasi `4`, dar cu un avertisment, in functie de versiune. Bug-ul cel mai des apare pe tablouri, si acolo e mut.)

O mentiune, doar ca sa nu te ia prin surprindere: biblioteca **OpenCV** (`cv2`) incarca imaginile color in ordinea **BGR**, nu RGB. Daca o afisezi cu matplotlib fara sa inversezi canalele, rosul si albastrul sunt schimbate. Pillow si scikit-learn folosesc RGB.
""")

    c.md(r"""
### Prag alb / negru si histograma

**Pragul** transforma o imagine gri in alb-negru: pixelul e alb daca depaseste un prag, altfel negru. Comparatia se face pe toata matricea deodata si da o matrice de `True`/`False`:
""")
    c.cod(r"""
%%vezi
import numpy as np
g = np.array([[10, 200, 130], [90, 250, 40]])
masca = g > 128                   #: comparatia se face pe fiecare pixel; rezulta True/False
albe = masca.sum()                #: True conteaza 1, deci suma numara pixelii albi
bw = masca * 255                  #: True -> 255, False -> 0: imagine alb-negru
""")
    c.md(r"""
Care prag e bun? Depinde de imagine. Animatia de mai jos e facuta cu `gri_u8`, matricea pe care ai calculat-o tu mai sus. Uita-te la histograma din dreapta (cati pixeli au fiecare valoare 0-255): pragul potrivit e in "valea" dintre cele doua grupuri de valori.
""")
    c.cod(r"""
anim_prag(gri_u8)
""")
    c.md(r"""
Histograma se calculeaza usor de mana: un contor pentru fiecare valoare posibila.
""")
    c.cod(r"""
%%vezi
pixeli = [3, 0, 3, 1, 3]
h = [0, 0, 0, 0]                  #: cate un contor pentru fiecare valoare posibila 0..3
for v in pixeli:
    h[v] += 1                     #: valoarea pixelului e chiar pozitia contorului
""")
    c.cod(r"""
h = [0] * 256
for v in gri_u8.ravel():                      # ravel(): matricea desfacuta intr-un sir de pixeli
    h[v] += 1
h_np = np.bincount(gri_u8.ravel(), minlength=256)         # aceeasi idee, scrisa in C
verifica_egal('histograma de mana = bincount', np.array(h), h_np)

plt.bar(range(256), h_np, width=1.0, color='gray')
plt.xlabel('valoarea pixelului')
plt.ylabel('cati pixeli')
plt.show()
""")

    c.md(r"""
## 5. Capcane

**Capcana 1: `'w'` sterge.** Ai vazut-o la inceput. Daca vrei sa adaugi la un fisier (un jurnal, rezultate pe parcurs), foloseste `'a'`.
""")
    c.cod(r"""
for _ in range(2):
    with open('jurnal.txt', 'w') as f:
        f.write('pornit\n')
with open('jurnal.txt') as f:
    print(len(f.readlines()), 'linie (dupa doua rulari cu w)')
""")
    c.md(r"""
**Capcana 2: CSV da doar text.** Un `'9'` citit din fisier nu e numarul 9. Adunarea lipeste, iar sortarea e alfabetica:
""")
    c.cod(r"""
%%vezi
valori = ['10', '9', '8']
lipite = valori[0] + valori[1]            #: + intre texte inseamna lipire
sortate = sorted(valori)                  #: '10' vine inaintea lui '8': comparatie caracter cu caracter
bune = sorted(int(v) for v in valori)     #: dupa conversie, ordinea e cea numerica
""")
    c.md(r"""
**Capcana 3: `\n` la capatul liniei.** Linia citita din fisier nu e egala cu textul din spatele ei. Compara doar dupa `strip()`:
""")
    c.cod(r"""
%%vezi
with open('note.txt', encoding='utf-8') as f:
    prima = f.readline()                  #: 'Ana 9\n'
egal = prima == 'Ana 9'                   #: False: \n conteaza
egal_strip = prima.strip() == 'Ana 9'     #: True
""")
    c.md(r"""
**Capcana 4: imaginea nu are mereu 3 canale.** Un PNG cu transparenta se incarca cu 4 canale (RGBA), si formula gri cu `img[..., 2]` merge in continuare, dar ai citit alt lucru decat credeai. Verifica `shape` si converteste:
""")
    c.cod(r"""
rgba = Image.new('RGBA', (2, 2), (255, 0, 0, 128))
print(np.array(rgba).shape)                       # (2, 2, 4): al patrulea canal e transparenta
print(np.array(rgba.convert('RGB')).shape)        # (2, 2, 3)
""")

    c.md(r"""
## 6. Cum citesti eroarea

Cu fisiere apar erori pe care nu le-ai vazut pana acum. Le vezi in animatii, cu linia rosie exact la cauza.

**`FileNotFoundError`** - calea e gresita, fisierul nu e in folderul curent, sau ai uitat sa-l aduci. Verifica `os.getcwd()` si `os.path.exists(cale)`.
""")
    c.cod(r"""
%%vezi
with open('nu_exista.txt') as f:
    text = f.read()
""")
    c.md(r"""
**`UnicodeDecodeError`** - ai deschis fisierul cu alt encoding decat cel in care a fost scris (aici, `ascii` pentru un fisier cu litere romanesti). Solutia: `encoding='utf-8'`.
""")
    c.cod(r"""
%%vezi
with open('ro.txt', encoding='ascii') as f:
    text = f.read()
""")
    c.md(r"""
**`ValueError: I/O operation on closed file`** - ai folosit fisierul dupa ce s-a terminat blocul `with` (care l-a inchis).
""")
    c.cod(r"""
%%vezi
with open('note.txt', encoding='utf-8') as f:
    prima = f.readline()
continut = f.read()
""")
    c.md(r"""
**`ValueError: could not convert string to float: ''`** - o celula goala din CSV. Prinzi eroarea sau verifici `if celula:` inainte de conversie.
""")
    c.cod(r"""
%%vezi
celula = ''
nota = float(celula)
""")
    c.md(r"""
**`KeyError: 'Nota'`** - numele coloanei din `DictReader` nu se potriveste (mare / mica conteaza, la fel si spatiile din antet).
""")
    c.cod(r"""
%%vezi
import csv
import io
f = io.StringIO('nume,nota\nAna,9\n')
for r in csv.DictReader(f):
    valoare = r['Nota']
""")
    c.md(r"""
**`ValueError: operands could not be broadcast together`** - formele nu se potrivesc: aici ai inmultit o imagine `(H, W, 3)` cu ponderi pentru doar doua canale. Verifica mereu `.shape` inainte de operatii pe imagini.
""")
    c.cod(r"""
%%vezi
import numpy as np
img = np.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [9, 9, 9]]])
gri = (img * np.array([0.299, 0.587])).sum(axis=2)
""")
    c.md(r"""
| eroare | de obicei inseamna |
|---|---|
| `FileNotFoundError` | cale gresita sau fisier neadus |
| `UnicodeDecodeError` | encoding gresit: foloseste `utf-8` |
| `ValueError: I/O operation on closed file` | ai folosit `f` dupa blocul `with` |
| `ValueError: could not convert string to float` | celula goala sau text in coloana numerica |
| `KeyError` la `DictReader` | numele coloanei nu se potriveste cu antetul |
| `ValueError: operands could not be broadcast` | formele (`shape`) tablourilor nu se potrivesc |
| `IndexError` la o linie | linie goala (de obicei ultima) sau rand prea scurt |
""")

    c.md(r"""
## Exercitiile de clasa

Verificarile de mai jos creeaza singure fisiere temporare (functia `pe_fisier`), apeleaza functia ta pe ele si le sterg. Tu scrii doar functia care primeste **calea** fisierului. Celula urmatoare defineste `pe_fisier`: ruleaz-o o data.
""")
    c.cod(AJUTOR + r"""
import numpy as np
""")

    c.md(r"""
**Exercitiul 1.** `linii_cuvinte(cale)`: intoarce perechea `(numar_de_linii, numar_de_cuvinte)` a fisierului. O linie goala conteaza ca linie; cuvintele sunt separate prin spatii.
""")
    c.ex(r"""
def linii_cuvinte(cale):
    pass  # TODO
""", r"""
def linii_cuvinte(cale):
    linii = cuvinte = 0
    with open(cale, encoding='utf-8') as f:
        for linie in f:
            linii += 1
            cuvinte += len(linie.split())
    return linii, cuvinte
""")
    c.cod(r"""
verifica('linii_cuvinte', lambda text: pe_fisier(linii_cuvinte, text),
         [(('ana are mere\nsi pere\n',), (2, 5)), (('a\n\nb',), (3, 2))],
         ascunse=[(('',), (0, 0)), (('un cuvant',), (1, 2)), (('\n\n',), (2, 0)), (('  a   b  \nc\n',), (2, 3))],
         indiciu='for linie in f: numeri linia, apoi len(linie.split()) cuvinte')
""")

    c.md(r"""
**Exercitiul 2.** `suma_din_fisier(cale)`: fisierul are cate un numar intreg pe linie (pot fi si linii goale, pe care le ignori). Intoarce suma lor.
""")
    c.ex(r"""
def suma_din_fisier(cale):
    pass  # TODO
""", r"""
def suma_din_fisier(cale):
    s = 0
    with open(cale, encoding='utf-8') as f:
        for linie in f:
            if linie.strip():
                s += int(linie)
    return s
""")
    c.cod(r"""
verifica('suma_din_fisier', lambda text: pe_fisier(suma_din_fisier, text),
         [(('1\n2\n3\n',), 6), (('10\n\n-4\n',), 6)],
         ascunse=[(('',), 0), ((' 5 \n7',), 12), (('-1\n-2\n',), -3), (('1000000\n2000000\n',), 3000000)],
         indiciu='sari peste liniile goale: if linie.strip(): ...; int() accepta si \\n la capat')
""")

    c.md(r"""
**Exercitiul 3.** `media_coloana(cale, coloana)`: fisierul e CSV cu antet. Intoarce media valorilor din coloana `coloana`, **sarind celulele care nu sunt numere** (goale, text, sau randuri prea scurte). Daca nu exista nicio valoare buna, intoarce `None`. Foloseste `csv.DictReader` (numele pot contine virgule, intre ghilimele).
""")
    c.ex(r"""
import csv


def media_coloana(cale, coloana):
    pass  # TODO
""", r"""
import csv


def media_coloana(cale, coloana):
    suma, cate = 0, 0
    with open(cale, encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f):
            try:
                suma += float(r[coloana])
                cate += 1
            except (ValueError, TypeError):
                pass
    return suma / cate if cate else None
""")
    c.cod(r"""
verifica('media_coloana', lambda text, col: pe_fisier(media_coloana, text, col, nume='a.csv'),
         [(('nume,nota\nAna,9\nDan,\nEva,7\n', 'nota'), 8.0),
          (('nume,nota\n"Popescu, Ion",10\nAna,8\n', 'nota'), 9.0)],
         ascunse=[(('nume,nota\nAna,absent\nDan,6\n', 'nota'), 6.0), (('nume,nota\nAna,\nDan,\n', 'nota'), None),
                  (('nume,nota,clasa\nAna,9,10\nDan\nEva,7,11\n', 'nota'), 8.0), (('a,b\n1,2\n3,4\n', 'b'), 3.0),
                  (('a,b\n1.5,2\n2.5,4\n', 'a'), 2.0)],
         indiciu='try: float(r[coloana]) ... except (ValueError, TypeError): o celula lipsa poate fi \'\' sau None')
""")

    c.md(r"""
**Exercitiul 4.** `scrie_submission(cale, subtask, raspunsuri)`: scrie un CSV in formatul judge-ului. Antetul `subtaskID,datapointID,answer`, apoi cate un rand pentru fiecare raspuns din lista: `subtask`, numarul de ordine al exemplului (de la 1) si raspunsul. Foloseste `csv.writer`.
""")
    c.ex(r"""
import csv


def scrie_submission(cale, subtask, raspunsuri):
    pass  # TODO
""", r"""
import csv


def scrie_submission(cale, subtask, raspunsuri):
    with open(cale, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['subtaskID', 'datapointID', 'answer'])
        for i, r in enumerate(raspunsuri, start=1):
            w.writerow([subtask, i, r])
""")
    c.cod(r"""
def t_scrie(subtask, raspunsuri):
    with tempfile.TemporaryDirectory() as d:
        cale = os.path.join(d, 's.csv')
        scrie_submission(cale, subtask, raspunsuri)
        with open(cale, encoding='utf-8') as f:
            return f.read().splitlines()

H = 'subtaskID,datapointID,answer'
verifica('scrie_submission', t_scrie,
         [((1, ['a', 'b']), [H, '1,1,a', '1,2,b']), ((2, [0, 1, 1]), [H, '2,1,0', '2,2,1', '2,3,1'])],
         ascunse=[((1, []), [H]), ((3, ['x,y']), [H, '3,1,"x,y"']), ((1, [7]), [H, '1,1,7'])],
         indiciu='csv.writer, open(..., \'w\', newline=\'\'), enumerate(raspunsuri, start=1); un raspuns cu virgula are nevoie de ghilimele')
""")

    c.md(r"""
**Exercitiul 5.** `gri_de_mana(img)`: primeste o imagine color (`H x W x 3`) si intoarce matricea `H x W` de tip `float` cu formula `0.299 * R + 0.587 * G + 0.114 * B`, **fara rotunjire**. Poti face bucle sau NumPy.
""")
    c.ex(r"""
def gri_de_mana(img):
    pass  # TODO
""", r"""
def gri_de_mana(img):
    h, w = img.shape[:2]
    gri = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            r, g, b = img[i, j]
            gri[i, j] = 0.299 * r + 0.587 * g + 0.114 * b
    return gri
""")
    c.cod(r"""
rgb_mic = np.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 255]]], dtype=np.uint8)
asteptat = np.array([[0.299 * 255, 0.587 * 255], [0.114 * 255, 255.0]])
verifica('gri_de_mana', gri_de_mana, [((rgb_mic,), asteptat)],
         referinta=lambda im: (im * np.array([0.299, 0.587, 0.114])).sum(axis=2),
         generator=lambda: (np.random.randint(0, 256, (np.random.randint(1, 6), np.random.randint(1, 6), 3)).astype(np.uint8),),
         indiciu='r, g, b = img[i, j] si apoi formula; rezultatul e o matrice de float H x W')

# aceeasi verificare, dar pe imaginea reala si fata de Pillow (care rotunjeste, de aceea tol=1)
forme_ex = np.array(Image.open(os.path.join(ACASA, 'date', '09_forme.png')).convert('RGB'))
gri_pil_ex = np.array(Image.fromarray(forme_ex).convert('L')).astype(float)
verifica('gri_de_mana vs Pillow', gri_de_mana, [((forme_ex,), gri_pil_ex)], tol=1)
""")

    c.md(r"""
**Exercitiul 6.** `oglinda_si_centru(img)`: intoarce o pereche `(oglinda, centru)`. `oglinda` e imaginea oglindita stanga-dreapta. `centru` e bucata din mijloc: randurile de la `H // 4` la `3 * H // 4` (exclusiv), coloanele de la `W // 4` la `3 * W // 4` (exclusiv). Merge la fel pentru imagini gri si color: doar slicing, fara bucle.
""")
    c.ex(r"""
def oglinda_si_centru(img):
    pass  # TODO
""", r"""
def oglinda_si_centru(img):
    h, w = img.shape[:2]
    return img[:, ::-1], img[h // 4:3 * h // 4, w // 4:3 * w // 4]
""")
    c.cod(r"""
def ref_oglinda(img):
    h, w = img.shape[:2]
    return img[:, ::-1].copy(), img[h // 4:3 * h // 4, w // 4:3 * w // 4].copy()

def gen_oglinda():
    forma = (np.random.randint(4, 11), np.random.randint(4, 11)) + ((3,) if np.random.rand() < 0.5 else ())
    return (np.random.randint(0, 256, forma).astype(np.uint8),)

mica = np.arange(16, dtype=np.uint8).reshape(4, 4)
verifica('oglinda_si_centru', oglinda_si_centru, [((mica,), (mica[:, ::-1], mica[1:3, 1:3]))],
         referinta=ref_oglinda, generator=gen_oglinda,
         indiciu='oglinda: img[:, ::-1]; centru: img[h // 4:3 * h // 4, w // 4:3 * w // 4]')
""")

    c.md(r"""
**Exercitiul 7.** `pixeli_peste(img, prag)`: cati pixeli dintr-o imagine gri au valoarea **strict mai mare** decat `prag`. Fara bucle: `(img > prag).sum()`.
""")
    c.ex(r"""
def pixeli_peste(img, prag):
    pass  # TODO
""", r"""
def pixeli_peste(img, prag):
    return int((img > prag).sum())
""")
    c.cod(r"""
g1 = np.array([[10, 200, 130], [90, 250, 40]], dtype=np.uint8)
verifica('pixeli_peste', pixeli_peste, [((g1, 128), 3), ((g1, 250), 0), ((g1, 0), 6)],
         ascunse=[((g1, 255), 0), ((g1, 39), 5), ((np.zeros((3, 3), dtype=np.uint8), 0), 0)],
         referinta=lambda im, p: int(np.sum(im.ravel() > p)),
         generator=lambda: (np.random.randint(0, 256, (5, 7)).astype(np.uint8), np.random.randint(0, 256)),
         indiciu='comparatia (img > prag) da o matrice de True/False; sum() le numara')
""")

    c.md(r"""
## Recapitulare

- **Text:** `with open(cale, mod, encoding='utf-8') as f`. Moduri: `r` (citeste), `w` (scrie si **sterge**), `a` (adauga). Bucla `for linie in f` + `.strip()` / `.split()`. Nu `read()` pe fisiere mari.
- `write` nu pune `\n`, `print(..., file=f)` il pune. Linia citita are `\n` la capat.
- Fisier lipsa: `os.path.exists`, `try/except FileNotFoundError`.
- **CSV:** `csv.reader` / `csv.DictReader` / `csv.writer`, cu `newline=''`. Totul vine ca **text**: conversie cu `try/except`. Pandas (`read_csv`) face totul intr-o linie, mai rapid.
- **submission.csv** = `subtaskID,datapointID,answer`, cate un rand pe exemplu. Cu pandas: `to_csv(index=False)`.
- **Imagini:** matrice de numere (`H x W` gri, `H x W x 3` RGB), `uint8`. `Image.open` -> `np.array`; oglindire si decupaj cu slicing (decupajul e view, nu copie); gri = `0.299 R + 0.587 G + 0.114 B`; prag = comparatie pe toata matricea; histograma = contor pe valoare.
- Capcana `uint8`: `250 + 10` face `4`. Trece la `int`, aplica `np.clip(..., 0, 255)`, intoarce-te la `uint8`.
- OpenCV foloseste BGR, nu RGB.

Tema (notebook-ul urmator): mai multe exercitii pe text si CSV, un program in format concurs, un jurnal de reparat, iluminare cu clip, histograma si un blur 3 x 3 pe care il scrii singur.
""")
    c.salveaza('09-fisiere-predare')


def tema():
    c = Carnet('Fisiere: text, CSV, imagini', 'tema', fisiere=FISIERE)
    c.md(r"""
Exercitiile de acasa. Testele vizibile iti arata daca ai inteles enuntul, cele **ascunse** verifica si cazurile limita. La final, `scor()` aduna tot.

Testele creeaza singure fisiere temporare (`pe_fisier`, definita in celula de mai jos), apeleaza functia ta pe ele si le sterg. Tu scrii doar functia care primeste **calea**. Ruleaz-o o data.
""")
    c.cod(AJUTOR + r"""
import numpy as np
""")

    c.md(r"""
### 1. Filtreaza linii

`linii_cu(cale, cuvant)`: intoarce lista liniilor din fisier care **contin** textul `cuvant` (cautare exacta, litere mari si mici conteaza), in ordinea din fisier si **fara** `\n` la capat.
""")
    c.ex(r"""
def linii_cu(cale, cuvant):
    pass  # TODO
""", r"""
def linii_cu(cale, cuvant):
    rez = []
    with open(cale, encoding='utf-8') as f:
        for linie in f:
            if cuvant in linie:
                rez.append(linie.strip('\n'))
    return rez
""")
    c.cod(r"""
verifica('linii_cu', lambda text, cuv: pe_fisier(linii_cu, text, cuv),
         [(('mere rosii\npere\nmere verzi\n', 'mere'), ['mere rosii', 'mere verzi']), (('a\nb\n', 'c'), [])],
         ascunse=[(('Mere\nmere\n', 'mere'), ['mere']), (('', 'x'), []), (('ab\nba\n\nb', 'b'), ['ab', 'ba', 'b']),
                  (('  x  \ny\n', 'x'), ['  x  '])],
         puncte=1, indiciu='append pe linie.strip(\'\\n\') (nu strip() simplu: nu vrei sa pierzi spatiile de la capete)')
""")

    c.md(r"""
### 2. Diacritice

Fisierul e scris in `utf-8` si contine text romanesc. `numara_diacritice(cale)` intoarce de cate ori apar in el literele cu semne diacritice romanesti, mici sau mari: `a` cu semn (`\u0103`, `\u00e2`), `i` cu semn (`\u00ee`), `s` cu virgula (`\u0219`), `t` cu virgula (`\u021b`) si majusculele lor (`\u0102`, `\u00c2`, `\u00ce`, `\u0218`, `\u021a`). Ca sa ramana codul in ASCII, scrie literele in program tot cu escape-uri, ca in enunt.
""")
    c.ex(r"""
def numara_diacritice(cale):
    pass  # TODO: deschide cu encoding='utf-8'
""", r"""
def numara_diacritice(cale):
    diacritice = '\u0103\u00e2\u00ee\u0219\u021b\u0102\u00c2\u00ce\u0218\u021a'
    total = 0
    with open(cale, encoding='utf-8') as f:
        for linie in f:
            total += sum(1 for ch in linie if ch in diacritice)
    return total
""")
    c.cod(r"""
verifica('numara_diacritice', lambda text: pe_fisier(numara_diacritice, text),
         [(('Ana are mere \u0219i pere\n',), 1), (('\u021b\u0103ranul \u00eenv\u0103\u021b\u0103tor\n',), 6)],
         ascunse=[(('',), 0), (('fara diacritice\n',), 0), (('\u0102\u00c2\u00ce\u0218\u021a\n\u0103\u00e2\u00ee\u0219\u021b',), 10)],
         puncte=1, indiciu='open(cale, encoding=\'utf-8\'); ch in \'...\' pentru fiecare caracter')
""")

    c.md(r"""
### 3. Valori lipsa pe coloane

`lipsuri_pe_coloana(cale)`: fisierul e CSV cu antet. Intoarce un dictionar `{nume_coloana: cate celule sunt goale}` (o celula goala e sirul vid, sau lipseste pentru ca randul e prea scurt). Dupa testele mici, verifica rezultatul si pe `date/elevi.csv`, comparat cu `pandas`.
""")
    c.ex(r"""
import csv


def lipsuri_pe_coloana(cale):
    pass  # TODO
""", r"""
import csv


def lipsuri_pe_coloana(cale):
    with open(cale, encoding='utf-8', newline='') as f:
        citit = csv.DictReader(f)
        lipsa = {col: 0 for col in citit.fieldnames}
        for r in citit:
            for col in lipsa:
                if not (r[col] or '').strip():
                    lipsa[col] += 1
    return lipsa
""")
    c.cod(r"""
import pandas as pd

verifica('lipsuri_pe_coloana', lambda text: pe_fisier(lipsuri_pe_coloana, text, nume='a.csv'),
         [(('a,b,c\n1,,3\n,,\n4,5,\n',), {'a': 1, 'b': 2, 'c': 2}), (('x\n1\n2\n',), {'x': 0})],
         ascunse=[(('a,b\n',), {'a': 0, 'b': 0}), (('a,b\n1\n,2\n',), {'a': 1, 'b': 1}), (('a,b\n"x, y",\n',), {'a': 0, 'b': 1})],
         puncte=2, indiciu='DictReader da None pentru celulele care lipsesc complet: (r[col] or \'\')')

de_pandas = {k: int(v) for k, v in pd.read_csv('date/elevi.csv').isna().sum().items()}
verifica('lipsuri pe date/elevi.csv', lipsuri_pe_coloana, [(('date/elevi.csv',), de_pandas)], puncte=1)
""")

    c.md(r"""
### 4. Repara codul: numarul de note

`suma_note(cale)` trebuie sa adune notele dintr-un fisier cu linii de forma `nume,nota`. Pe fisiere care se termina cu `\n` (adica aproape toate) crapa. Animatia de mai jos arata problema pe un text; repara functia.
""")
    c.cod(r"""
%%vezi
text = 'Ana,9\nDan,7\n'
suma = 0
for linie in text.split('\n'):            #: split('\n') pastreaza un element gol dupa ultimul \n
    suma += int(linie.split(',')[1])
""")
    c.ex(r"""
def suma_note(cale):
    with open(cale, encoding='utf-8') as f:
        continut = f.read()
    suma = 0
    for linie in continut.split('\n'):
        suma += int(linie.split(',')[1])
    return suma
""", r"""
def suma_note(cale):
    with open(cale, encoding='utf-8') as f:
        continut = f.read()
    suma = 0
    for linie in continut.splitlines():
        suma += int(linie.split(',')[1])
    return suma
""")
    c.cod(r"""
verifica('suma_note', lambda text: pe_fisier(suma_note, text),
         [(('Ana,9\nDan,7\n',), 16), (('Eva,10',), 10)],
         ascunse=[(('',), 0), (('a,1\nb,2\nc,3\n',), 6), (('x,5\n',), 5)],
         puncte=1, indiciu='"a\\nb\\n".split("\\n") are 3 elemente, ultimul gol. Ce metoda nu lasa element gol?')
""")

    c.md(r"""
### 5. Repara codul: jurnalul

`adauga_in_jurnal(cale, mesaj)` trebuie sa adauge `mesaj` pe o linie noua la sfarsitul fisierului, fara sa piarda ce era deja acolo. Acum pierde tot si nici nu trece la linie noua. Sunt doua greseli.
""")
    c.ex(r"""
def adauga_in_jurnal(cale, mesaj):
    with open(cale, 'w', encoding='utf-8') as f:
        f.write(mesaj)
""", r"""
def adauga_in_jurnal(cale, mesaj):
    with open(cale, 'a', encoding='utf-8') as f:
        f.write(mesaj + '\n')
""")
    c.cod(r"""
def t_jurnal(mesaje):
    with tempfile.TemporaryDirectory() as d:
        cale = os.path.join(d, 'jurnal.txt')
        for m in mesaje:
            adauga_in_jurnal(cale, m)
        with open(cale, encoding='utf-8') as f:
            return f.read().splitlines()

verifica('adauga_in_jurnal', t_jurnal, [((['pornit', 'oprit'],), ['pornit', 'oprit']), ((['a'],), ['a'])],
         ascunse=[((['1', '2', '3'],), ['1', '2', '3']), ((['x', 'x'],), ['x', 'x'])],
         puncte=1, indiciu='ce mod de deschidere nu sterge fisierul? si write nu pune singur \\n')
""")

    c.md(r"""
### 6. Program: notele clasei

Program ca la concurs. Prima linie: `n`. Urmeaza `n` linii CSV de forma `nume,nota`. Numele poate contine virgula, caz in care apare intre ghilimele (`"Popescu, Ion",9`), iar nota poate lipsi (`Dan,`). Afiseaza pe prima linie media notelor care exista, cu **doua zecimale**, iar pe a doua numele elevului cu nota cea mai mare (la egalitate, primul din lista). Se garanteaza ca exista cel putin o nota.

Sfat: `csv.reader([linie])` citeste o singura linie deja in memorie, cu regulile CSV.
""")
    c.ex(r"""
import csv


def main():
    pass  # TODO
""", r"""
import csv


def main():
    n = int(input())
    note = []
    for _ in range(n):
        nume, nota = next(csv.reader([input()]))
        if nota.strip():
            note.append((float(nota), nume))
    print(f'{sum(v for v, _ in note) / len(note):.2f}')
    print(max(note, key=lambda t: t[0])[1])
""")
    c.cod(r"""
verifica_program('note clasa', main,
                 [(['3', 'Ana,9', 'Dan,', 'Eva,7'], '8.00\nAna'),
                  (['2', '"Popescu, Ion",10', 'Ana,8'], '9.00\nPopescu, Ion')],
                 ascunse=[(['1', 'X,5'], '5.00\nX'), (['4', 'a,7', 'b,9', 'c,', 'd,9'], '8.33\nb'),
                          (['2', 'Ana,', 'Dan,6.5'], '6.50\nDan')],
                 puncte=2, indiciu='next(csv.reader([linie])) da lista [nume, nota]; max cu key= intoarce primul la egalitate')
""")

    c.md(r"""
### 7. Valideaza un submission

Inainte sa trimiti, verifici. `valideaza_submission(cale, n)` intoarce `True` doar daca fisierul are exact: antetul `subtaskID,datapointID,answer`; `n` randuri de date; pe fiecare rand exact 3 campuri, `datapointID` egal cu numarul de ordine al randului (1, 2, ..., n) si `answer` nevid. Altfel `False`.
""")
    c.ex(r"""
import csv


def valideaza_submission(cale, n):
    pass  # TODO
""", r"""
import csv


def valideaza_submission(cale, n):
    with open(cale, encoding='utf-8', newline='') as f:
        randuri = list(csv.reader(f))
    if not randuri or randuri[0] != ['subtaskID', 'datapointID', 'answer']:
        return False
    date = randuri[1:]
    if len(date) != n:
        return False
    for i, r in enumerate(date, start=1):
        if len(r) != 3 or r[1] != str(i) or not r[2].strip():
            return False
    return True
""")
    c.cod(r"""
H = 'subtaskID,datapointID,answer\n'
verifica('valideaza_submission', lambda text, n: pe_fisier(valideaza_submission, text, n, nume='s.csv'),
         [((H + '1,1,a\n1,2,b\n', 2), True), ((H + '1,1,a\n', 2), False)],
         ascunse=[(('id,datapointID,answer\n1,1,a\n', 1), False), ((H + '1,1,a\n1,3,b\n', 2), False),
                  ((',' + H + '0,1,1,a\n', 1), False), ((H + '1,1,\n', 1), False), ((H, 0), True),
                  ((H + '1,1,a\n1,2,b\n1,3,c\n', 2), False), (('', 0), False)],
         puncte=2, indiciu='citeste tot cu csv.reader, apoi verifica pe rand: antetul, len(randuri), fiecare rand')
""")

    c.md(r"""
### 8. Luminozitate cu clip

`lumineaza(img, delta)`: primeste o imagine `uint8` (gri sau color) si un intreg `delta` (pozitiv sau negativ). Intoarce imaginea cu `delta` adunat la fiecare pixel, **taiat la intervalul 0-255**, tot de tip `uint8`. Atentie la capcana din predare.
""")
    c.ex(r"""
def lumineaza(img, delta):
    pass  # TODO
""", r"""
def lumineaza(img, delta):
    return np.clip(img.astype(int) + delta, 0, 255).astype(np.uint8)
""")
    c.cod(r"""
def t_lumineaza(img, delta):
    r = lumineaza(img, delta)
    return r.tolist(), str(r.dtype)

def ref_lumineaza(img, delta):
    r = np.clip(img.astype(int) + delta, 0, 255).astype(np.uint8)
    return r.tolist(), 'uint8'

a = np.array([[100, 200, 250]], dtype=np.uint8)
verifica('lumineaza', t_lumineaza,
         [((a, 10), ([[110, 210, 255]], 'uint8')), ((a, -150), ([[0, 50, 100]], 'uint8'))],
         ascunse=[((a, 0), ([[100, 200, 250]], 'uint8')), ((a, 1000), ([[255, 255, 255]], 'uint8'))],
         referinta=ref_lumineaza,
         generator=lambda: (np.random.randint(0, 256, (3, 4)).astype(np.uint8), np.random.randint(-300, 300)),
         puncte=2, indiciu='uint8 + numar se rostogoleste: converteste la int, np.clip(..., 0, 255), apoi .astype(np.uint8)')
""")

    c.md(r"""
### 9. Histograma de mana

`histograma(img)`: pentru o imagine gri `uint8`, intoarce o **lista** cu 256 de numere: cate pixeli au valoarea `0`, cati au `1`, ..., cati au `255`. Scrie tu bucla (un contor pe valoare), fara `np.bincount`.
""")
    c.ex(r"""
def histograma(img):
    pass  # TODO
""", r"""
def histograma(img):
    h = [0] * 256
    for v in img.ravel():
        h[v] += 1
    return h
""")
    c.cod(r"""
def ref_hist(img):
    return np.bincount(img.ravel(), minlength=256).tolist()

g = np.array([[0, 255, 0], [7, 7, 7]], dtype=np.uint8)
asteptat = [0] * 256
asteptat[0], asteptat[255], asteptat[7] = 2, 1, 3
verifica('histograma', histograma, [((g,), asteptat)],
         ascunse=[((np.zeros((2, 2), dtype=np.uint8),), [4] + [0] * 255)],
         referinta=ref_hist, generator=lambda: (np.random.randint(0, 256, (np.random.randint(1, 9), np.random.randint(1, 9))).astype(np.uint8),),
         puncte=2, indiciu='h = [0] * 256; for v in img.ravel(): h[v] += 1')
""")

    c.md(r"""
### 10. Alb-negru

`alb_negru(img, prag)`: pentru o imagine gri, intoarce o matrice `uint8` de aceeasi forma cu `255` unde pixelul e **strict** mai mare decat `prag` si `0` in rest. (Asta e imaginea din animatia `anim_prag`.)
""")
    c.ex(r"""
def alb_negru(img, prag):
    pass  # TODO
""", r"""
def alb_negru(img, prag):
    return ((img > prag) * 255).astype(np.uint8)
""")
    c.cod(r"""
def t_alb_negru(img, prag):
    r = alb_negru(img, prag)
    return r.tolist(), str(r.dtype)

g = np.array([[10, 200, 130], [90, 250, 40]], dtype=np.uint8)
verifica('alb_negru', t_alb_negru,
         [((g, 128), ([[0, 255, 255], [0, 255, 0]], 'uint8')), ((g, 255), ([[0, 0, 0], [0, 0, 0]], 'uint8'))],
         ascunse=[((g, 0), ([[255, 255, 255], [255, 255, 255]], 'uint8')), ((g, 40), ([[0, 255, 255], [255, 255, 0]], 'uint8'))],
         puncte=1, indiciu='(img > prag) e True/False; inmultit cu 255 devine 255/0; la final .astype(np.uint8)')
""")

    c.md(r"""
### 11. Provocare: blur 3 x 3

Un **blur** (estompare) inlocuieste fiecare pixel cu media vecinilor lui. Scrie `blur3(img)` pentru o matrice 2D (cel putin `3 x 3`): fiecare pixel **interior** devine media celor 9 valori din patratul `3 x 3` centrat pe el (pixelul insusi inclus); pixelii de pe margine raman neschimbati. Intoarce o matrice `float` noua, fara sa modifici `img`. Important: media se calculeaza pe valorile **originale**, nu pe cele deja estompate.

Poti face patru bucle (`i`, `j`, apoi vecinii) sau folosi slicing: suma celor 9 decupaje deplasate, impartita la 9.
""")
    c.ex(r"""
def blur3(img):
    pass  # TODO
""", r"""
def blur3(img):
    a = np.asarray(img, dtype=float)
    rez = a.copy()
    h, w = a.shape
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            rez[i, j] = a[i - 1:i + 2, j - 1:j + 2].mean()
    return rez
""")
    c.cod(r"""
def ref_blur(img):
    a = np.asarray(img, dtype=float)
    r = a.copy()
    h, w = a.shape
    r[1:-1, 1:-1] = sum(a[i:h - 2 + i, j:w - 2 + j] for i in range(3) for j in range(3)) / 9
    return r

m = np.array([[0, 0, 0, 0], [0, 9, 0, 0], [0, 0, 0, 0]], dtype=float)
verifica('blur3', blur3, [((m,), np.array([[0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]], dtype=float))],
         ascunse=[((np.arange(9).reshape(3, 3),), np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]], dtype=float))],
         referinta=ref_blur,
         generator=lambda: (np.random.randint(0, 256, (np.random.randint(3, 8), np.random.randint(3, 8))),),
         puncte=3, indiciu='rezultatul se scrie in alt tablou (o copie), altfel vecinii urmatori vad valori deja estompate')
scor()
""")
    c.salveaza('09-fisiere-tema')


if __name__ == '__main__':
    predare()
    tema()
