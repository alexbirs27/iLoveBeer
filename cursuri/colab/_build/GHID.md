# Ghid de autor pentru colab-urile ONIA

Cum scriem un set (predare + tema) pentru un topic. Citeste tot, apoi citeste `gen_01_liniare.py` (modelul de stil) si
`onia.py` (unealta).

## Ce construim si de ce

Elevii (clasele 9-12, stiu putin C++) invata Python + procesarea datelor pentru Olimpiada Nationala de IA, direct in Google Colab.
Materialul concurent (programa.nitro-ai.org) explica corect, dar: nu are nicio animatie, exercitiile sunt doar linkuri externe (pbinfo),
nu are nicio verificare automata, nu invata debugging-ul, ignora capcanele (aliasing, `bool`, leakage la valori lipsa).
**Noi facem invers**: fiecare concept se vede in miscare, fiecare exercitiu se verifica pe loc, capcanele sunt tratate direct.

Doua notebook-uri per topic:

- **predare** - cel pe care il parcurge profesorul cu clasa. Ordine: concept -> animatie -> "din topor" (de mana) ->
  scurtatura/functia din librarie -> de ce e mai rapida -> capcane -> exercitii in clasa (5-8, cu `verifica`) -> recapitulare.
- **tema** - de acasa. 8-12 exercitii cu **teste ascunse**, obligatoriu: cel putin un "repara codul", cel putin un program in
  format concurs (`verifica_program`), cel putin o provocare. Puncte diferite (`puncte=`), `scor()` la final.

Fiecare topic mai are si un notebook cu solutii (generat automat, nu-l publicam pana dupa curs).

## Vocea (obligatoriu)

- Scrii ca si cum ai vorbi direct cu elevul: "tu", propozitii scurte, opinii, fara ton de manual. Paragrafe de 1-3 propozitii.
- **Din topor**: mai intai varianta de mana (bucla, formula), apoi scurtatura (functie, librarie, NumPy/Pandas), apoi *de ce* e
  scurtatura mai rapida (bucla in C in loc de bucla Python, memorie contigua...). Nu prezenta o functie ca pe o cutie neagra.
- Bibliotecile nu se memoreaza (la olimpiada ai documentatie): spune-le asta, dar cere sa poata scrie de mana ce face functia.
- Spune unde apare in ONIA / ML ("asta e exact ce face `train_test_split`", "asa se calculeaza `StandardScaler`").
- Complexitatea acolo unde conteaza (O(n) vs O(n^2), `x in lista` vs `x in set`). Fara exagerari teoretice.
- **Prezice inainte sa rulezi**: intrebare + `<details><summary>Raspuns</summary>...</details>` (se vede in Colab).
- **Capcane**: sectiune dedicata, fiecare capcana demonstrata (de preferinta cu `%%vezi`).
- **Cum citesti eroarea**: arata erorile tipice ale topicului in `%%vezi` (eroarea apare in animatie, nu crapa celula).
- Fara sarcasm inutil, fara "in concluzie", fara liste lungi de calitati. Fara replici gen "dupa cum vedem".
- **Doar ASCII**: fara diacritice, fara cratima lunga (foloseste `-`), fara emoji. Builderul (`nb.py`) da eroare daca gaseste
  caractere non-ASCII. Ortografie fara diacritice dar in forma moderna: `sunt`, `cand`, `gand`, `rand` (nu `sint`, `cind`).
- Cod: simplu, comentarii putine si scurte, fara docstring-uri lungi, fara "defensive coding" inutil.

## API-ul (in `onia.py`; nu-l modifica)

```python
%%vezi                      # prima linie a celulei: executa codul pas cu pas (animatie)
%%vezi 3 4                  # valorile pentru input() (separate prin spatii; foloseste ghilimele pentru spatii in valoare)
```
- In cod poti pune `#: text` la finalul unei linii: textul apare sub cod cand se executa acea linie (nota didactica). Nu apare in cod.
- Arata: linia curenta, memoria (variabile, liste, matrici 2D ca tabel, tupluri, seturi, dictionare, obiecte), stiva de apeluri
  (recursivitate!), ce afiseaza `print`, erorile (linia rosie). Containerele partajate primesc eticheta `@1` (aliasing vizibil).
  Ce se schimba la un pas clipeste.
- Variabilele NU raman in notebook dupa `%%vezi` (ruleaza intr-un spatiu separat). Cel mult ~60 de pasi (limita implicita 250):
  fa exemple scurte. Nu functioneaza cu fisiere reale si nu afiseaza DataFrame-uri (foloseste-l pe liste, dict, obiecte, array-uri
  NumPy mici, numere, text).
- `vezi(cod_string, inputs=['3'], max_pasi=400, note={linie: 'text'})` - varianta ca functie.

```python
verifica('nume', functie, [((arg1, arg2), asteptat), ...],
         ascunse=[...],            # teste extra, apar doar ca numar
         referinta=f_corecta, generator=lambda: (random.randint(1, 99),), n=20,   # teste aleatoare vs o functie corecta
         indiciu='text', puncte=1, timp=3, tol=1e-6, in_loc=False)   # in_loc: compara argumentul 1 modificat pe loc
verifica_program('nume', main, [(['3', '4'], '7'), ...], ascunse=[...])   # program cu input()/print(); main = functia care il ruleaza
verifica_egal('nume', valoare, asteptat)      # numar, lista, np.ndarray, DataFrame/Series (compara cu tolerante)
scor()                                        # tabel cu punctajul, la finalul temei
```
- Testele de tip lista/tuplu compara si tipul (`(1, 2)` != `[1, 2]`). Numerele: `tol` relativ. Erorile si buclele infinite sunt prinse
  (timp limita) si raportate, nu crapa celula.
- Numele exercitiilor sunt unice in notebook (rularea repetata suprascrie).
- `descarca('date/elevi.csv')` aduce un fisier langa notebook (din repo). Se pune automat in prima celula prin `Carnet(fisiere=...)`.

## Constructorul (`nb.py`) si fluxul de lucru

```python
from nb import Carnet
c = Carnet('Titlu', 'predare', fisiere=('date/elevi.csv', 'anim_liste.py'))   # 'predare' sau 'tema'
c.md('markdown')          # celula text
c.cod('cod')              # celula de cod (ruleaza la teste)
c.ex(stub, solutie)       # celula pe care o completeaza elevul (stub = cu # TODO), solutie = varianta corecta (pentru notebook-ul cu solutii)
c.salveaza('02-structuri-decizionale-predare')    # scrie ../02-....ipynb si ../solutii/02-...-solutii.ipynb
```
Pasi: 1) scrii `gen_NN_slug.py` cu functiile `predare()` si `tema()` (ca in `gen_01_liniare.py`); 2) `python gen_NN_slug.py`;
3) `python test_colab.py NN` - toate 4 notebook-urile (predare, tema, cele doua cu solutii) trebuie sa fie **OK**. Cele cu solutii
ruleaza `asigura_toate()` la final: pica daca vreo solutie nu trece testele; cele pentru elevi trebuie sa ruleze curat si cu stub-urile goale
(verificarile vor arata "mai ai de lucru", asta e normal). Poti vedea cum arata iesirile cu `python preview_outputs.py NN-...-tema.ipynb`
(apoi deschizi `_preview/iesiri.html`; pe Windows poti face screenshot cu Edge headless: `msedge --headless=new --screenshot=... file:///...`).

Reguli tehnice:
- **Nu apela `input()` real** in celule care se ruleaza (nbclient nu are tastatura). Foloseste `%%vezi` cu valori de intrare, sau pune
  `input()` doar in functii `main` care nu sunt apelate direct (le apeleaza `verifica_program`).
- Celulele de exemplu nu trebuie sa depinda de stub-urile elevului (altfel pica in notebook-ul pentru elevi).
- Fara acces la internet in afara de `descarca` (repo). Biblioteci permise: standard library, numpy, pandas, matplotlib, scikit-learn,
  scipy, Pillow. (Colab le are pe toate.) Seturile din scikit-learn (`load_wine`, `load_iris`, `load_digits`, `load_breast_cancer`,
  `load_sample_image('china.jpg')`) merg offline.
- Cod compatibil cu Python 3.10-3.12 si pandas 2.x / 3.x (fara API-uri depreciate, fara `inplace=True` pe slice-uri, fara `fillna(inplace=)`).
- Randomness in teste: ok cu `random`/`numpy`; testele aleatoare se compara cu o `referinta` corecta, deci nu depind de seed.
- Notebook-urile nu au output-uri salvate (nbstripout le sterge oricum).
- Nu modifica `onia.py`, `nb.py`, `test_colab.py`, `preview*.py`, `gen_01_liniare.py`, `date_comune.py`. Daca iti lipseste ceva din API,
  rezolva local (in modulul tau) si scrie in raportul final ce ai fi vrut.

## Animatii in plus (in afara de `%%vezi`)

`%%vezi` acopera executia codului. Pentru intuitie vizuala speciala (matrici parcurse, sortari, diagrame Venn, histograme, scalare...)
scrii un modul propriu `cursuri/colab/anim_<topic>.py` cu functii care intorc animatii `matplotlib`:

```python
from matplotlib import animation
import matplotlib.pyplot as plt
from IPython.display import HTML

def anim_ceva(date, ...):
    fig, ax = plt.subplots(figsize=(6, 4))
    ...
    ani = animation.FuncAnimation(fig, update, frames=n_cadre, interval=400)
    html = ani.to_jshtml()      # play/pauza/slider incluse
    plt.close(fig)
    return HTML(html)
```
- NU apela `matplotlib.use('Agg')` la nivel de modul (strica afisarea in Colab); `to_jshtml()` merge oricum si in backend inline si in Agg.
- Cel mult ~40-60 de cadre, `figsize` modest (embed-ul e trimis in notebook); `animation.embed_limit` implicit e destul.
- Datele animate trebuie sa vina **din codul scris de elev in notebook** (el calculeaza `scalat = ...` de mana si apoi
  `anim_scalare(brut, scalat)` arata transformarea), nu dintr-o cutie neagra. Asa animatia ilustreaza codul lui.
- Functii cu nume in romana si docstring de o linie. Modulul se aduce prin `Carnet(..., fisiere=('anim_topic.py',))` (importa automat `*`).
- Fiecare functie de animatie se testeaza local (ruleaza cel putin o data in notebook-ul de solutii).
- Poti folosi si `ipywidgets` (slider) pentru explorare, dar animatia deterministica e prioritara (testele nu pot apasa butoane).

Datele proprii: fisiere mici (<100 KB) in `cursuri/colab/date/`, prefixate cu numarul topicului (`09_note.csv`), generate deterministic de un
script `_build/date_<topic>.py` (seed fix). Seturile comune deja existente: `date/elevi.csv`, `date/case.csv` (vezi docstring-ul din
`date_comune.py` pentru problemele plantate in ele: nu le "repara" in fisier).

## Ce contine un predare bun (lista de control)

- 25-45 de celule fara exercitii; 8-15 animatii `%%vezi` sau `anim_*`; cel putin 3 blocuri "Prezice".
- Fiecare concept mare: text scurt -> animatie -> de mana -> scurtatura -> de ce e mai rapida (unde are sens).
- Sectiune "Capcane" cu cel putin 3 capcane reale si sectiune "Cum citesti eroarea" cu erorile tipice ale topicului.
- 5-8 exercitii in clasa, crescator ca dificultate, fiecare cu `verifica*` si `ascunse=`.
- Recapitulare cu liste scurte. Legatura cu ONIA/ML in 1-2 locuri.

Tema: 8-12 exercitii, puncte 1-3, teste ascunse la toate, un "repara codul", un program format concurs, o provocare, `scor()` la final.
