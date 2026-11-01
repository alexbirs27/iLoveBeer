"""Genereaza 14-mini-olimpiada.ipynb (+ varianta cu solutii). Datele: python date_14_mini.py"""
from nb import Carnet

FISIERE = ('date/14_train.csv', 'date/14_test.csv', 'date/14_test_etichete.csv')


def tema():
    c = Carnet('Mini-olimpiada', 'tema', fisiere=FISIERE)

    c.md("""
## Enuntul

Ai date despre elevi (clasa, note, ore de studiu, absente, varsta, meditatii). In `date/14_train.csv` stii si rezultatul: `calificat` (1 = a trecut mai departe, 0 = nu). In `date/14_test.csv` sunt **80 de elevi noi, fara** `calificat`.

Trebuie sa prezici `calificat` pentru fiecare elev din test si sa scrii fisierul `submission.csv`, in formatul de la olimpiada:

```
subtaskID,datapointID,answer
1,17,0
1,23,1
...
```

`subtaskID` este mereu `1`, `datapointID` este `id`-ul elevului, `answer` este `0` sau `1`. **Scorul** este acuratetea pe test. Functia `evalueaza` (mai jos) iti spune scorul si un verdict: *sub baseline*, *ok* sau *bun*.

Regulile jocului:

- toti cei 80 de elevi din test trebuie sa primeasca un raspuns: **nu ai voie sa scoti randuri din test**, oricat de stricate ar fi
- orice statistica (mediana, media, abaterea standard) se calculeaza **doar din train**
- datele au aceleasi probleme ca in notebook-urile de EDA si valori lipsa: lipsuri, duplicate, `meditatii` scris in mai multe feluri, varsta imposibila, absente extreme

Pasii sunt ghidati (fiecare cu verificare), la final ii lipesti si trimiti. Fisierul `14_test_etichete.csv` contine raspunsurile si il foloseste doar functia de scor. Nu te uita in el, altfel nu inveti nimic.
""")
    c.cod("""
import os
import random
import tempfile
import numpy as np
import pandas as pd
from IPython.display import HTML, display
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

train = pd.read_csv('date/14_train.csv')
test = pd.read_csv('date/14_test.csv')
CARACT = ['clasa', 'nota_mate', 'nota_info', 'ore_studiu', 'absente', 'varsta', 'meditatii']   # coloanele modelului
print('train:', train.shape, ' test:', test.shape)
train.head()
""")
    c.cod("""
print(train['meditatii'].value_counts(dropna=False).to_dict())
print(train[['varsta', 'absente']].describe().loc[['min', 'max']])
print('duplicate in train:', train.duplicated().sum(), ' valori lipsa in test:', test.isna().sum()[lambda s: s > 0].to_dict())
""")

    c.md("""
## Functia de scor

Aceasta celula o rulezi si o lasi asa. Citeste `submission.csv`, verifica formatul (coloanele, `id`-urile, valorile 0/1), calculeaza acuratetea si o compara cu **baseline-ul**: cat ar lua un program care raspunde mereu cu clasa cea mai frecventa. Da si un loc estimat printre 20 de participanti inchipuiti.
""")
    c.cod("""
PARTICIPANTI = [0.575, 0.6, 0.6, 0.625, 0.6625, 0.6625, 0.675, 0.6875, 0.7, 0.7, 0.7125, 0.725, 0.725,
                0.7375, 0.75, 0.7625, 0.775, 0.8, 0.8125, 0.825]


def evalueaza(cale):
    def card(culoare, titlu, linii):
        corp = ''.join(f'<div style="font-size:13px;margin:2px 0">{x}</div>' for x in linii)
        display(HTML(f'<div style="border-left:5px solid {culoare};background:#f6f8fa;color:#1f2933;padding:6px 10px;'
                     f'border-radius:6px;font-family:system-ui,sans-serif"><b style="color:{culoare}">{titlu}</b>{corp}</div>'))

    eticheta = pd.read_csv('date/14_test_etichete.csv').set_index('id')['calificat']
    if not os.path.exists(cale):
        card('#b42318', 'submission invalid', [f'fisierul {os.path.basename(cale)} nu exista (inca)'])
        return {'verdict': 'lipsa'}
    sub = pd.read_csv(cale)
    if list(sub.columns) != ['subtaskID', 'datapointID', 'answer']:
        card('#b42318', 'submission invalid', ['coloanele trebuie sa fie exact: subtaskID, datapointID, answer'])
        return {'verdict': 'invalid'}
    if sorted(sub['datapointID']) != sorted(eticheta.index) or not sub['answer'].isin([0, 1]).all():
        card('#b42318', 'submission invalid', ['trebuie sa ai exact un raspuns (0 sau 1) pentru fiecare id din test'])
        return {'verdict': 'invalid'}
    y = eticheta.loc[sub['datapointID']].to_numpy()
    p = sub['answer'].to_numpy()
    acc = float((y == p).mean())
    baseline = float(max(y.mean(), 1 - y.mean()))
    verdict = 'sub baseline' if acc <= baseline else ('ok' if acc < 0.75 else 'bun')
    tp = int(((p == 1) & (y == 1)).sum())
    recall = tp / max(1, int((y == 1).sum()))
    precizie = tp / max(1, int((p == 1).sum()))
    loc = 1 + sum(1 for s in PARTICIPANTI if s > acc)
    culoare = {'sub baseline': '#b42318', 'ok': '#b54708', 'bun': '#1b7f3b'}[verdict]
    card(culoare, f'verdict: {verdict}',
         [f'acuratete: {acc:.4f}   (baseline, raspunsul cel mai frecvent: {baseline:.4f})',
          f'pentru clasa 1 (calificat): recall {recall:.2f}, precizie {precizie:.2f}',
          f'loc estimat: {loc} din {len(PARTICIPANTI) + 1}'])
    return {'verdict': verdict, 'acc': acc, 'baseline': baseline}
""")

    c.md("""
## Capcana: raspunsul cel mai frecvent

Cea mai proasta solutie care "arata bine": un program care nu se uita la date si raspunde mereu cu clasa majoritara din train.

**Prezice:** ce acuratete ia, si ce verdict?

<details><summary>Raspuns</summary>

Circa 0.66 (cati elevi din test nu sunt calificati), deci exact baseline-ul: verdict *sub baseline*. Si are `recall 0` pe clasa 1: nu gaseste niciun elev calificat. Un scor bun de acuratete pe date dezechilibrate poate ascunde un model inutil. Tu trebuie sa il bati.
</details>
""")
    c.cod("""
majoritar = int(train['calificat'].mean() >= 0.5)
gol = pd.DataFrame({'subtaskID': 1, 'datapointID': test['id'], 'answer': majoritar})
cale_maj = os.path.join(tempfile.mkdtemp(), 'submission.csv')
gol.to_csv(cale_maj, index=False)
_ = evalueaza(cale_maj)
""")

    c.md("""
## Pasul 1: curata datele

Scrie `curata(df)`: intoarce o **copie** a lui `df` in care:

1. `meditatii` este numar: taie spatiile, litere mici, `'da'` devine `1`, `'nu'` devine `0` (o valoare lipsa ramane `NaN`)
2. `varsta` in afara intervalului `[12, 20]` devine `NaN`
3. `absente` mai mare decat 40 devine `NaN`

Nu scoate randuri (in test nu ai voie). O sa o aplici si pe train, si pe test.
""")
    c.ex("""
def curata(df):
    df = df.copy()
    # TODO: meditatii -> 1/0, varsta imposibila -> NaN, absente > 40 -> NaN
    return df
""", """
def curata(df):
    df = df.copy()
    df['meditatii'] = df['meditatii'].str.strip().str.lower().map({'da': 1, 'nu': 0})
    df['varsta'] = df['varsta'].where((df['varsta'] >= 12) & (df['varsta'] <= 20))
    df['absente'] = df['absente'].where(df['absente'] <= 40)
    return df
""")
    c.cod("""
def _ref_curata(df):
    df = df.copy()
    df['meditatii'] = df['meditatii'].str.strip().str.lower().map({'da': 1, 'nu': 0})
    df['varsta'] = df['varsta'].where((df['varsta'] >= 12) & (df['varsta'] <= 20))
    df['absente'] = df['absente'].where(df['absente'] <= 40)
    return df

mic = pd.DataFrame({'id': [1, 2, 3, 4], 'meditatii': ['Da', ' nu', 'DA ', np.nan],
                    'varsta': [15, 150, 2, 18], 'absente': [3, 87, 40, 41]})
asteptat = pd.DataFrame({'id': [1, 2, 3, 4], 'meditatii': [1.0, 0.0, 1.0, np.nan],
                         'varsta': [15.0, np.nan, np.nan, 18.0], 'absente': [3.0, np.nan, 40.0, np.nan]})
verifica('curata', curata, [((mic,), asteptat)],
         ascunse=[((train,), _ref_curata(train)), ((test,), _ref_curata(test))],
         indiciu='df[col].str.strip().str.lower().map({...}); df[col].where(conditie) pune NaN unde conditia e falsa', puncte=2)
""")

    c.md("""
## Pasul 2: repara codul (valorile lipsa)

Dupa curatare raman valori lipsa (unele erau din start, altele le-ai creat tu la pasul 1). Le umplem cu **mediana din train**. Functia de mai jos are exact greseala din notebook-ul despre scalare, in alta forma: din care set se ia mediana pentru test?

Repar-o: `imputa(train, test, coloane)` intoarce `(train_completat, test_completat)`, cu mediana calculata din train pentru ambele.
""")
    c.ex("""
def imputa(train, test, coloane):
    train, test = train.copy(), test.copy()
    for col in coloane:
        train[col] = train[col].fillna(train[col].median())
        test[col] = test[col].fillna(test[col].median())
    return train, test
""", """
def imputa(train, test, coloane):
    train, test = train.copy(), test.copy()
    for col in coloane:
        m = train[col].median()
        train[col] = train[col].fillna(m)
        test[col] = test[col].fillna(m)
    return train, test
""")
    c.cod("""
def _ref_imputa(tr, te, coloane):
    tr, te = tr.copy(), te.copy()
    for col in coloane:
        m = tr[col].median()
        tr[col], te[col] = tr[col].fillna(m), te[col].fillna(m)
    return tr, te

tr_m = pd.DataFrame({'a': [1.0, 2.0, np.nan, 4.0], 'b': [np.nan, 10.0, 20.0, 30.0]})
te_m = pd.DataFrame({'a': [np.nan, 100.0], 'b': [5.0, np.nan]})
tr_c = _ref_curata(train.drop_duplicates())
te_c = _ref_curata(test)
verifica('imputa', imputa,
         [((tr_m, te_m, ['a', 'b']),
           (pd.DataFrame({'a': [1.0, 2.0, 2.0, 4.0], 'b': [20.0, 10.0, 20.0, 30.0]}),
            pd.DataFrame({'a': [2.0, 100.0], 'b': [5.0, 20.0]})))],
         ascunse=[((tr_c, te_c, CARACT), _ref_imputa(tr_c, te_c, CARACT))],
         indiciu='mediana trebuie calculata o singura data, din train, si folosita pe ambele', puncte=2)
""")

    c.md("""
## Pasul 3: modelul

Scrie `construieste_model()`: intoarce un `Pipeline` **cu `StandardScaler` ca prim pas**, urmat de un clasificator la alegerea ta (`LogisticRegression` sau `KNeighborsClassifier`, de exemplu). Verificarea il antreneaza pe datele curate si cere o acuratete de validare incrucisata peste 0.6.
""")
    c.ex("""
def construieste_model():
    pass  # TODO
""", """
def construieste_model():
    return make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
""")
    c.cod("""
tr_i, te_i = _ref_imputa(tr_c, te_c, CARACT)


def _verif_model():
    m = construieste_model()
    primul = type(m.steps[0][1]).__name__
    return primul, bool(cross_val_score(m, tr_i[CARACT], tr_i['calificat'], cv=5).mean() > 0.6)

verifica('construieste_model', _verif_model, [((), ('StandardScaler', True))],
         indiciu='make_pipeline(StandardScaler(), model). Scaler-ul in pipeline = fara scurgere in validare', puncte=2)
""")

    c.md("""
## Pasul 4: scrie `submission.csv`

`scrie_submission(model, df_test, coloane, cale)`: cu modelul deja antrenat, prezice pentru `df_test[coloane]` si scrie fisierul la `cale`, cu coloanele `subtaskID` (mereu 1), `datapointID` (coloana `id` din `df_test`) si `answer` (predictia, 0 sau 1), fara indexul pandas.
""")
    c.ex("""
def scrie_submission(model, df_test, coloane, cale):
    pass  # TODO
""", """
def scrie_submission(model, df_test, coloane, cale):
    sub = pd.DataFrame({'subtaskID': 1, 'datapointID': df_test['id'].to_numpy(),
                        'answer': model.predict(df_test[coloane]).astype(int)})
    sub.to_csv(cale, index=False)
""")
    c.cod("""
class _MicModel:
    def predict(self, X):
        return np.array([1, 0, 1])


def _verif_scrie():
    cale = os.path.join(tempfile.mkdtemp(), 's.csv')
    scrie_submission(_MicModel(), pd.DataFrame({'id': [7, 8, 9], 'f': [0.0, 1.0, 2.0]}), ['f'], cale)
    return pd.read_csv(cale)

verifica('scrie_submission', _verif_scrie,
         [((), pd.DataFrame({'subtaskID': [1, 1, 1], 'datapointID': [7, 8, 9], 'answer': [1, 0, 1]}))],
         indiciu='pd.DataFrame({...}).to_csv(cale, index=False); coloanele in ordinea din enunt', puncte=2)
""")

    c.md("""
## Pasul 5: totul impreuna

Aici lipesti pasii in ordinea corecta:

1. scoate duplicatele din **train** (din test nu: fiecare elev trebuie sa primeasca un raspuns)
2. `curata` pe train si pe test
3. `imputa` cu mediana din train
4. model, cu scor de validare incrucisata pe train (ca sa stii cum stai *inainte* sa trimiti)
5. antreneaza pe tot train-ul si scrie `submission.csv` la `CALE_SUB`

`CALE_SUB` este locul unde se scrie fisierul. Poti alege alte coloane decat `CARACT`, poti incerca alt model. Nu te opri la primul verdict: ai voie sa incerci de cate ori vrei.
""")
    c.ex("""
CALE_SUB = 'submission.csv'
""", """
CALE_SUB = os.path.join(tempfile.mkdtemp(), 'submission.csv')
""")
    c.ex("""
# TODO: pasii 1-5 de mai sus, in ordine
""", """
tr = curata(train.drop_duplicates())
te = curata(test)
tr, te = imputa(tr, te, CARACT)
model = construieste_model()
print('validare incrucisata pe train:', round(cross_val_score(model, tr[CARACT], tr['calificat'], cv=5).mean(), 3))
model.fit(tr[CARACT], tr['calificat'])
scrie_submission(model, te, CARACT, CALE_SUB)
""")

    c.md("""
## Scorul

Se evalueaza fisierul tau. Pentru punctaj: o solutie *peste baseline* (nu raspunde doar cu clasa majoritara) si o solutie *buna* (acuratete cel putin 0.75; datele au si zgomot, un elev cu note bune poate sa nu treaca si invers, deci nu te astepta la 100%).
""")
    c.cod("""
rez = evalueaza(CALE_SUB)
verifica_egal('submission peste baseline', rez['verdict'] in ('ok', 'bun'), True, puncte=3,
              indiciu='ai scris fisierul si l-ai completat cu predictii reale, nu doar clasa majoritara?')
verifica_egal('submission bun', rez['verdict'] == 'bun', True, puncte=3,
              indiciu='verifica pasii: valori lipsa completate din train, StandardScaler, modelul potrivit')
scor()
""")

    c.md("""
## Ce ai facut

- ai curatat date murdare in test fara sa scoti randuri (nu ai voie sa "pierzi" un raspuns)
- ai completat valorile lipsa cu statistici **doar din train**
- ai pus scalarea intr-un `Pipeline`, ca sa nu se strecoare nimic din test
- ai scris fisierul in formatul cerut si l-ai verificat cu un scor local

Exact asta se cere la ONIA: un fisier `submission.csv` bine format, facut fara scurgeri de informatie. Data viitoare incearca alt model, alte coloane, alt `k`: si compara cu baseline-ul, nu doar cu acuratetea.
""")
    c.salveaza('14-mini-olimpiada')


if __name__ == '__main__':
    tema()
