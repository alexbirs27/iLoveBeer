# ML pentru Olimpiada

Cursul e organizat carte. Textul de prezentare (de ce fac cursul asta,
ce vreau sa acopar) e in `preface.tex`, iar cuprinsul intreg pleaca din
`main.tex`.

Compilare (are nevoie de o distributie LaTeX cu `pdflatex` si de
pygments pentru minted: `pip install pygments`):

```
pdflatex -shell-escape main.tex
```
(ruleaza de 2-3 ori, pana se stabilizeaza TOC-ul si referintele)

## Deschide notebook-urile in Colab

Fiecare notebook are un badge "Open in Colab". Elevul apasa pe el, apoi
Copy to Drive, si lucreaza pe propria copie - nu poate scrie inapoi in
repo. Link-ul se construieste asa: iei URL-ul de GitHub al notebook-ului
si inlocuiesti `github.com` cu `colab.research.google.com/github`.

Repo-ul are filtrul `nbstripout` instalat, deci output-urile se sterg
automat la commit.

Notebook-uri cu badge, deocamdata:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alexbirs27/iLoveBeer/blob/main/cursuri/python-intro/notebooks/curs-python-intro.ipynb) `python-intro/notebooks/curs-python-intro.ipynb` - notebook-ul de curs, cu explicatii si exemple rezolvate

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alexbirs27/iLoveBeer/blob/main/cursuri/python-intro/notebooks/exercitii-python-intro.ipynb) `python-intro/notebooks/exercitii-python-intro.ipynb` - playground, exercitii goale pentru elevi

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alexbirs27/iLoveBeer/blob/main/cursuri/playground-test/salut-colab.ipynb) `playground-test/salut-colab.ipynb` - notebook de test, cat am verificat fluxul

Pe masura ce pun badge si pe restul notebook-urilor (`fundamentals/`,
exercitiile individuale din `python-intro/`), o le adaug aici.

## Structura

```
main.tex                          orchestratorul, vezi mai jos
preface.tex                       de ce fac cursul, ce vreau sa acopar
preamble.sty                      setari LaTeX comune

python-intro.tex                  "parte" - Curs 0
python-intro/
  intro.tex                       teorie: de ce Python, sintaxa vs C++
  exercitii.tex                   exercitii, cu link spre notebook + surse
  notebooks/*.ipynb               rulabil, interactiv

fundamentals.tex                  "parte" - Curs 1: NumPy si Pandas
fundamentals/
  numpy-pandas.tex
  exercitii-numpy-pandas.tex
  notebooks/*.ipynb

src/<capitol>/<slug>.py           codul sursa complet, acelasi ca in notebook,
                                   dar ca fisier .py simplu (pentru apendice)

appendix.tex                      "parte" - apendice, colecteaza codul complet
appendix/
  python-intro.tex                 \inputminted pe fiecare .py din src/python-intro
  fundamentals.tex                 \inputminted pe fiecare .py din src/fundamentals
```

Tiparul, ca la carte: in corpul unui capitol, un exercitiu are doar un
link `notebook` (interactiv) si un link `surse` (`\hyperref[code:slug]`)
care duce la apendice, unde codul complet e printat cu `\inputminted`.
Codul propriu-zis traieste o singura data, in `src/<capitol>/<slug>.py`.

Un capitol nou = un `<capitol>.tex` nou in radacina (doar `\import`-uri,
ca `fundamentals.tex`) + un folder `<capitol>/` cu teorie + exercitii +
`notebooks/` + un `src/<capitol>/` cu sursele + o intrare noua in
`appendix.tex`.

## Referinte

- [Programa oficiala a Olimpiadei Nationale de Inteligenta Artificiala](https://platform.olimpiada-ai.ro/ro/roadmap/programa)
- [Problemele ale Olimpiadei Nationale de Inteligenta Artificiala](https://platform.olimpiada-ai.ro/ro/problems)
- [Feature Engineering pe Kagle](https://www.kaggle.com/learn/feature-engineering)
- [Introduction to NumPy, Pandas and Matplotlib](https://www.kaggle.com/code/chats351/introduction-to-numpy-pandas-and-matplotlib)
- [A very good tutorial for Pandas](https://www.kaggle.com/learn/pandas)
- [Cool stuf](https://www.kaggle.com/learn)
## Plan

O sa rezolv toate problemele de pe platforma, pe rand, si o sa le
documentez: ce vor ei sa obtina cu fiecare, ce le scapa, ce ar trebui sa
stie elevii pe langa ce cere problema explicit. Ideea e sa predau
lucrurile de baza stiind deja ce ii asteapta mai departe, ca sa ii
pregatesc atat pentru problemele in sine cat si pentru ce vine dupa ele.
