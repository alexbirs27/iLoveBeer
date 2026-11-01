"""Genereaza 11-valori-lipsa-predare.ipynb si 11-valori-lipsa-tema.ipynb (+ variantele cu solutii).

Valorile asteptate din teste (inclusiv cele ascunse) sunt calculate aici, de solutiile de referinta, si scrise ca numere in notebook.
"""
import os
import random

import numpy as np
import pandas as pd

from nb import Carnet, COLAB

DATE = os.path.join(COLAB, 'date')
ELEVI = pd.read_csv(os.path.join(DATE, 'elevi.csv'))
CASE = pd.read_csv(os.path.join(DATE, 'case.csv'))
CONCURS = pd.read_csv(os.path.join(DATE, '11_concurs_lipsa.csv'))
COMPLET = pd.read_csv(os.path.join(DATE, '11_elevi_complet.csv'))

# Setul de lucru din predare: stergem noi valori din setul complet, cu o masca cu seed fix (adevarul ramane cunoscut)
SETUP = """
complet = pd.read_csv('date/11_elevi_complet.csv')

rng = np.random.default_rng(42)
masca_ore = rng.random(len(complet)) < 0.20
masca_info = rng.random(len(complet)) < 0.20

lipsa = complet.copy()
lipsa.loc[masca_ore, 'ore_studiu'] = np.nan
lipsa.loc[masca_info, 'nota_info'] = np.nan

adevar_ore = complet.loc[masca_ore, 'ore_studiu'].to_numpy()
adevar_info = complet.loc[masca_info, 'nota_info'].to_numpy()
print('goluri la ore_studiu:', masca_ore.sum(), '| la nota_info:', masca_info.sum())
"""

NS = {'np': np, 'pd': pd, 'elevi': ELEVI, 'case': CASE, 'concurs': CONCURS, 'complet': COMPLET,
      'read_csv_original': pd.read_csv}
exec(SETUP.replace("'date/11_elevi_complet.csv'", repr(os.path.join(DATE, '11_elevi_complet.csv'))), NS)
NS['train'] = ELEVI.iloc[:180]
NS['test'] = ELEVI.iloc[180:]


def py(x):
    if isinstance(x, dict):
        return {py(k): py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return type(x)(py(v) for v in x)
    if isinstance(x, np.generic):
        return x.item()
    return x


def R(x):
    return repr(py(x))


def T(nume, f, vis, asc=(), pre='', extra=''):
    """Celula de verificare cu asteptatul calculat de solutia din NS (vezi gen_10_eda.py)."""
    if pre:
        exec(pre, NS)

    def cazuri(lst):
        return '[' + ', '.join('((%s,), %s)' % (a, R(eval('%s(%s)' % (f, a), NS))) for a in lst) + ']'

    cod = (pre.strip() + '\n\n' if pre else '') + "verifica('%s', %s, %s" % (nume, f, cazuri(vis))
    if asc:
        cod += ',\n         ascunse=%s' % cazuri(asc)
    if extra:
        cod += ',\n         ' + extra
    return cod + ')'


def E(nume, var, expr, extra=''):
    cod = "verifica_egal('%s', %s, %s" % (nume, var, R(eval(expr, NS)))
    return cod + (', ' + extra if extra else '') + ')'


# ---------------------------------------------------------------------------
# PREDARE
# ---------------------------------------------------------------------------

def predare():
    c = Carnet('Completarea valorilor lipsa', 'predare',
               fisiere=('date/elevi.csv', 'date/11_elevi_complet.csv', 'anim_valori_lipsa.py'))

    c.md("""
## De ce conteaza golurile

Aproape orice set de date real are goluri: un senzor s-a oprit, cineva nu a completat un camp, un fisier a fost lipit prost. Ai doua probleme.

**Prima:** majoritatea modelelor din `scikit-learn` nu accepta deloc valori lipsa. Le dai un `NaN` si se opresc cu eroare.

**A doua, mai grava:** poti "repara" golurile in zece feluri, iar unele te lasa cu un model care pare mai bun decat e (**data leakage**), sau cu date mai "curate" decat realitatea. Iar pana acum nimeni nu iti spune cum afli daca o metoda a ajutat. Aici o afli, cu numere.

Notebook-ul urmeaza aceeasi cale: cum vezi golurile, de ce lipsesc (conteaza!), metodele de umplere (mai intai de mana, apoi cu pandas / scikit-learn), scurgerea de informatie, si cum **masori** o imputare. Nu memora functiile: la olimpiada ai documentatia. Trebuie sa stii ce face fiecare metoda si ce strica.

**Cum lucram.** Celulele `%%vezi` ruleaza cod Python simplu pas cu pas (liste, bucle, dictionare). Tabelele pandas nu se pot afisa acolo, asa ca pentru ele folosim grafice si animatii facute pe valorile tale.
""")

    c.md("""
## 1. Ce inseamna "lipsa"

In pandas o valoare lipsa e `NaN` (Not a Number), un `float` special. In Python simplu o reprezentam de obicei cu `None`. Un `NaN` are o particularitate care te va musca: **nu e egal cu nimic, nici cu el insusi**.
""")
    c.cod("""
%%vezi
x = float('nan')
egal = x == x             #: NaN nu e egal nici cu el insusi!
este_nan = x != x         #: asa il recunosti "de mana": singurul care difera de sine
lista = [4, None, 7, None, 9]
lipsa = 0
for v in lista:
    if v is None:         #: None se verifica cu 'is', nu cu ==
        lipsa += 1
""")
    c.md("""
Atentie la golurile **deghizate**: nu toate apar ca `NaN`. `-1`, `999`, `0`, `'n/a'`, `'necunoscut'` sau un sir gol pot insemna "nu stim", dar pandas nu le vede ca lipsa. Le gasesti la EDA (`describe`, `value_counts`) si le inlocuiesti tu cu `NaN`.
""")
    c.cod("""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x = pd.Series([1, None, np.nan, '', 'n/a', -1, 0])
print(x.isna().tolist())      # doar None si nan sunt "lipsa" pentru pandas
""")

    c.md("""
## 2. Detectarea golurilor

De mana, numeri `None`-urile pe coloane. Cu pandas, `isna()` da o masca `True`/`False` cu forma tabelului, iar `sum()` o aduna pe coloane (`True` = 1).
""")
    c.cod("""
%%vezi
randuri = [
    {'nota': 7, 'ore': None},
    {'nota': None, 'ore': 5.5},
    {'nota': 9, 'ore': None},
]
lipsa = {'nota': 0, 'ore': 0}
for r in randuri:
    for col in r:
        if r[col] is None:
            lipsa[col] += 1        #: numaram golurile pe fiecare coloana
""")
    c.cod("""
elevi = pd.read_csv('date/elevi.csv')

nr_lipsa = elevi.isna().sum()
procent = (elevi.isna().mean() * 100).round(1)        # media unei coloane True/False = procentul de True
print(pd.DataFrame({'lipsa': nr_lipsa, 'procent': procent}))
""")
    c.md("""
Un **"heatmap" al golurilor** (negru = lipseste) arata dintr-o privire ce lipseste si daca golurile vin **impreuna** (pe acelasi rand) sau separat:
""")
    c.cod("""
fig, ax = plt.subplots(figsize=(6, 4))
ax.imshow(elevi.isna().astype(int).to_numpy(), aspect='auto', cmap='Greys', interpolation='nearest')
ax.set_xticks(range(elevi.shape[1]), elevi.columns, rotation=45, ha='right')
ax.set_ylabel('randuri')
ax.set_title('negru = valoare lipsa')
plt.tight_layout()
plt.show()
""")
    c.md("""
**Prezice:** in `elevi` lipsesc 8% din `nota_info`, 10% din `ore_studiu` si 5% din `meditatii`. Daca stergi orice rand care are **cel putin un gol**, cam ce procent din randuri pierzi? (Gandeste-te: sunt trei coloane, fiecare cu propriile goluri.)

<details><summary>Raspuns</summary>

Aproape 23% (56 din 245). Golurile din coloane diferite nu se suprapun, deci pierderile se aduna: 8% + 10% + 5% ~ 23%. Cu 20 de coloane cu cate 5% goluri ai ramane, in medie, cu numai 36% din randuri. **Asta e costul lui `dropna`.**
</details>
""")
    c.cod("""
print('randuri cu cel putin un gol:', elevi.isna().any(axis=1).sum(), 'din', len(elevi))
print('dupa dropna:', elevi.dropna().shape)
""")

    c.md("""
## 3. De ce lipsesc: MCAR, MAR, MNAR

Inainte sa alegi o metoda te intrebi **de ce** lipseste valoarea. Sunt trei situatii, iar cea in care te afli decide cat de periculoasa e o metoda simpla.

| mecanism | ce inseamna | exemplu | media a ce a ramas |
|---|---|---|---|
| **MCAR** (complet aleator) | golul nu depinde de nimic | un senzor pierde la intamplare cate un pachet | e corecta (doar ai mai putine date) |
| **MAR** (aleator, dat de alta coloana) | golul depinde de o coloana pe care O AI | `ore_studiu` lipseste mai des la clasa a 12-a | e deformata, dar o poti corecta folosind acea coloana |
| **MNAR** (nealeator) | golul depinde de **valoarea lipsa** | cei care invata mult nu vor sa spuna cat | e deformata si nu o poti repara din aceste date |

Sa le vedem. Luam `ore_studiu` dintr-un set **complet** (stim adevarul!) si stergem valori in cele trei feluri:
""")
    c.cod("""
complet = pd.read_csv('date/11_elevi_complet.csv')
ore = complet['ore_studiu'].to_numpy()
clasa = complet['clasa'].to_numpy()

rng = np.random.default_rng(1)
mcar = rng.random(len(ore)) < 0.30                              # oricine, cu aceeasi sansa
mar = rng.random(len(ore)) < np.where(clasa == 12, 0.70, 0.10)  # depinde de ALTA coloana (clasa)
mnar = rng.random(len(ore)) < np.where(ore > 6.5, 0.60, 0.10)   # depinde de valoarea INSASI

print('media reala:', round(ore.mean(), 3))
for nume, m in [('MCAR', mcar), ('MAR', mar), ('MNAR', mnar)]:
    print(f'{nume}: lipsesc {m.mean():.0%}, media a ce a ramas = {ore[~m].mean():.3f}')
""")
    c.md("""
**Prezice** inainte sa te uiti la animatie: la care din cele trei ramane media aproape de cea reala, si la care se muta si in ce directie?

<details><summary>Raspuns</summary>

La MCAR ramane aproape (mica abatere e intamplare). La MAR si MNAR se muta **in jos**, pentru ca lipsesc tocmai valorile mari: elevii de clasa a 12-a (care invata mai mult) si, respectiv, valorile mari direct.
</details>
""")
    c.cod("""
anim_mecanisme(ore, {'MCAR': mcar, 'MAR': mar, 'MNAR': mnar}, eticheta='ore_studiu')
""")
    c.md("""
La **MAR** stii de ce lipsesc valorile, si acel "de ce" e o coloana pe care o ai (`clasa`). Deci poti corecta: faci media pe fiecare clasa, din ce a ramas, apoi le ponderezi cu cati elevi sunt REAL in fiecare clasa (clasa nu lipseste nimanui). Asta e ideea din spatele imputarii pe grupuri, pe care o vezi mai jos.
""")
    c.cod("""
pe_clasa = pd.Series(ore[~mar]).groupby(clasa[~mar]).mean()      # media pe clasa, din ce a ramas
greutati = pd.Series(clasa).value_counts(normalize=True)          # ponderea reala a fiecarei clase
print('media naiva (ce a ramas)   :', round(ore[~mar].mean(), 3))
print('media corectata pe clasa   :', round((pe_clasa * greutati).sum(), 3))
print('media reala                :', round(ore.mean(), 3))
""")
    c.md("""
La **MNAR** nu ai cum sa corectezi din date: informatia lipseste chiar acolo unde ar fi trebuit sa o gasesti. Poti doar sa ai o ipoteza (din afara datelor) si sa o folosesti cu grija.

**Si datele noastre reale?** In `elevi.csv`, `ore_studiu` lipseste mult mai des la clasa a 12-a (~29% fata de 2-7%). E semnul unui **MAR**: golul depinde de `clasa`, pe care o avem. Nu poti *demonstra* niciodata ca ceva e MCAR sau MNAR doar din date (MNAR se vede doar din informatii de afara), dar poti gasi indicii de MAR ca acesta:
""")
    c.cod("""
print(elevi['ore_studiu'].isna().groupby(elevi['clasa']).mean().round(3))
""")

    c.md("""
## 4. Setul nostru de lucru

De aici incolo lucram pe un set **cu adevarul cunoscut**: luam `11_elevi_complet.csv` (nicio valoare lipsa) si stergem noi cateva valori, cu o masca cu seed fix. Asa, dupa ce completam golurile, putem compara cu ce am sters si sa **masuram** cat de bine am nimerit. La datele reale nu ai adevarul, dar vei vedea la final cum se simuleaza.

Stergem 20% din `ore_studiu` si 20% din `nota_info`, la intamplare (MCAR).
""")
    c.cod(SETUP)

    c.md("""
## 5. Metoda 1: stergi randurile sau coloanele

Cea mai simpla: scoti tot ce are goluri. De mana:
""")
    c.cod("""
%%vezi
randuri = [[7, 5.5], [None, 6.0], [8, None], [9, 7.0]]    # [nota, ore]
pastrate = []
for r in randuri:
    if None not in r:              #: pastram randul doar daca nu are niciun gol
        pastrate.append(r)
""")
    c.md("""
In pandas: `dropna()`. Are variante utile: `subset=` (conteaza doar anumite coloane), `thresh=` (cate valori minim trebuie sa aiba randul), `axis=1` (scoate coloane).

Costul: pierzi date (23% din randuri la `elevi`) si, daca golurile sunt **MAR**, ceea ce ramane nu mai seamana cu tot setul. Vezi ce se intampla cu proportia claselor:
""")
    c.cod("""
print(elevi.shape, '->', elevi.dropna().shape)
print('clase inainte:', elevi['clasa'].value_counts(normalize=True).sort_index().round(3).to_dict())
print('clase dupa   :', elevi.dropna()['clasa'].value_counts(normalize=True).sort_index().round(3).to_dict())

print(elevi.dropna(subset=['nota_info']).shape)   # scoate doar randurile fara nota_info
print(elevi.dropna(thresh=8).shape)                # pastreaza randul daca are cel putin 8 din 9 valori
print(elevi.dropna(axis=1).shape)                  # scoate COLOANELE cu goluri (pierzi feature-uri intregi)
""")
    c.md("""
Clasa a 12-a scade de la 22% la ~19%: ai scos tocmai elevii la care `ore_studiu` lipsea cel mai des. **Regula de bun simt:** scoti randuri cand sunt putine si golurile par MCAR; scoti o coloana cand lipseste mai mult de jumatate din ea; in rest, completezi.
""")

    c.md("""
## 6. Metoda 2: o constanta

Pui aceeasi valoare peste tot (0, -1, `'necunoscut'`). Pentru **categorii** e chiar bine: "necunoscut" e o categorie sincera. Pentru numere, aproape niciodata: `0` ore de studiu e o valoare reala, iar constanta deformeaza tot.
""")
    c.cod("""
ore_lipsa = lipsa['ore_studiu']
ore_zero = ore_lipsa.fillna(0)               # fillna intoarce un rezultat NOU, nu modifica ore_lipsa
print('media reala   :', round(complet['ore_studiu'].mean(), 3))
print('dupa fillna(0):', round(ore_zero.mean(), 3))
print(elevi.fillna({'ore_studiu': 0, 'meditatii': 'necunoscut'}).isna().sum().sum(), 'goluri au ramas (dupa ce am completat 2 coloane)')
""")

    c.md("""
## 7. Metoda 3: media, mediana, modul

Cea mai folosita metoda: pui in gol o valoare "tipica" calculata din ce ai. Trei variante:

- **media** pentru numere aproximativ simetrice;
- **mediana** pentru numere cu coada lunga sau outlieri (media ar fi trasa de ei, ai vazut la EDA);
- **modul** (valoarea cea mai frecventa) pentru categorii.

De mana, cu liste:
""")
    c.cod("""
%%vezi
ore = [4.0, None, 6.0, 5.0, None, 30.0]
cunoscute = []
for x in ore:
    if x is not None:
        cunoscute.append(x)                        #: strangem doar ce stim
media = sum(cunoscute) / len(cunoscute)
cu_zero = [0 if x is None else x for x in ore]              #: umplere cu constanta
cu_media = [media if x is None else x for x in ore]         #: umplere cu media
""")
    c.md("""
**Prezice:** ai `[1, 2, 2, 3, 50, gol]`. Cu ce ai completa golul, cu media sau cu mediana? Cat iese fiecare?

<details><summary>Raspuns</summary>

Media celor cunoscute e `58 / 5 = 11.6`, mediana e `2`. Un elev "tipic" din lista are 2, nu 11.6: media e trasa de `50`. Pentru date asimetrice, mediana e alegerea sigura.
</details>
""")
    c.md("""
Modul pentru categorii, de mana (un dictionar de frecvente, ca la EDA, si apoi cel mai frecvent):
""")
    c.cod("""
%%vezi
cat = ['nu', 'da', None, 'nu', 'nu', None, 'da']
frecv = {}
for x in cat:
    if x is not None:
        frecv[x] = frecv.get(x, 0) + 1      #: numaram fiecare categorie
mod = None
for x in frecv:
    if mod is None or frecv[x] > frecv[mod]:
        mod = x                              #: modul = cel mai frecvent
completat = [mod if x is None else x for x in cat]
""")
    c.md("""
In pandas: `fillna(valoare)`. Valoarea o calculezi tu inainte. Atentie: `mode()` intoarce un **`Series`** (pot fi mai multe valori la egalitate), de aceea iei primul element cu `[0]`.
""")
    c.cod("""
ore = lipsa['ore_studiu']
print('media:', round(ore.mean(), 3), '| mediana:', ore.median(), '| skew:', round(ore.skew(), 2))
ore_media = ore.fillna(ore.mean())
ore_mediana = ore.fillna(ore.median())

med = elevi['meditatii'].str.strip().str.lower()
print(med.mode()[0], '<- modul din meditatii (dupa curatare)')
med_completat = med.fillna(med.mode()[0])
print(med_completat.isna().sum(), 'goluri au ramas')
""")

    c.md("""
## 8. Ce strica media: varianta se micsoreaza

Umplerea cu media pare inofensiva. Dar toate valorile puse au **aceeasi** valoare, exact media. Fiecare adauga 0 la suma patratelor abaterilor (distanta la medie e 0), dar creste `n`. Rezultat: varianta scade, iar in histograma apare un **varf artificial** exact la medie.

Animatia primeste valorile tale (cu goluri), masca si trei umpleri calculate de tine:
""")
    c.cod("""
valori = lipsa['ore_studiu'].to_numpy()
anim_imputare(valori, masca_ore,
              {'constanta 0': ore_zero.to_numpy(), 'media': ore_media.to_numpy(), 'mediana': ore_mediana.to_numpy()},
              eticheta='ore_studiu')
""")
    c.md("""
**Prezice:** dupa umplerea cu media, deviatia standard a coloanei: creste, scade sau ramane la fel? Dar corelatia cu `nota_info`?

<details><summary>Raspuns</summary>

Deviatia scade, iar corelatia cu alte coloane **slabeste**: punctele umplute stau pe o linie orizontala, fara legatura cu `nota_info`. Un model care se bazeaza pe varianta sau pe relatii nu are cum sa nu fie afectat.
</details>
""")
    c.cod("""
print('std adevarat            :', round(complet['ore_studiu'].std(), 3))
print('std dupa umplere (medie):', round(ore_media.std(), 3))

corela_reala = complet['ore_studiu'].corr(complet['nota_info'])
corela_medie = ore_media.corr(lipsa['nota_info'])
print('corelatie ore-nota_info reala        :', round(corela_reala, 3))
print('corelatie dupa umplere cu media      :', round(corela_medie, 3))
""")

    c.md("""
## 9. Metoda 4: valoarea vecina (`ffill` / `bfill`)

Cand randurile au **ordine** (timp: temperatura la fiecare ora), valoarea de langa gol e o estimare buna. `ffill` = copiaza ultima valoare cunoscuta ("forward fill"), `bfill` = o ia pe urmatoarea ("backward fill"). De mana:
""")
    c.cod("""
%%vezi
temp = [12, None, None, 15, None, 14]
rez = []
ultima = None
for t in temp:
    if t is None:
        rez.append(ultima)        #: copiem ultima valoare cunoscuta
    else:
        rez.append(t)
        ultima = t                #: retinem valoarea noua
""")
    c.md("""
Observa: daca **primul** element lipseste, `ultima` e `None` si golul ramane gol. Pentru asta exista `bfill`. Iar `interpolate()` face mai bine cand seria e neteda: traseaza o linie dreapta intre vecini.
""")
    c.cod("""
t = np.arange(48)
adevar_temp = 14 + 6 * np.sin(t / 48 * 4 * np.pi)          # temperatura reala pe 48 de ore
gol = np.random.default_rng(3).random(48) < 0.30
gol[0] = False
temp = pd.Series(np.where(gol, np.nan, adevar_temp))

f = temp.ffill()
i = temp.interpolate()
for nume, s in [('ffill', f), ('interpolate', i)]:
    print(nume, 'RMSE =', round(float(np.sqrt(np.mean((s[gol] - adevar_temp[gol]) ** 2))), 3))

plt.figure(figsize=(8, 3))
plt.plot(t, adevar_temp, color='#cbd5e1', lw=6, label='adevar')
plt.plot(t, f, color='#ea580c', drawstyle='steps-post', label='ffill')
plt.plot(t, i, color='#15803d', ls='--', label='interpolate')
plt.plot(t[~gol], temp[~gol], 'o', color='#2563eb', ms=4, label='cunoscute')
plt.legend(ncol=4, fontsize=8)
plt.show()
""")
    c.md("""
**Cand NU:** daca randurile nu au ordine. Randurile din `elevi` sunt in ordinea `id`, care nu spune nimic. `ffill` ar copia nota_info a elevului de dinainte, ceea ce e complet fara sens. Regula: `ffill` / `bfill` / `interpolate` doar pe serii ordonate (timp, pozitie).
""")

    c.md("""
## 10. Metoda 5: pe grupuri

Daca stii ca valoarea depinde de o categorie (orele cresc cu clasa), completezi cu media **grupului**. Asta e exact corectia pe care am facut-o la MAR. De mana, cu doua dictionare (sume si numarari):
""")
    c.cod("""
%%vezi
clasa = [9, 9, 12, 12, 12, 9]
ore = [3.0, None, 7.0, 8.0, None, 4.0]
sume = {}
nr = {}
for c, o in zip(clasa, ore):
    if o is not None:
        sume[c] = sume.get(c, 0) + o
        nr[c] = nr.get(c, 0) + 1
medii = {}
for c in sume:
    medii[c] = sume[c] / nr[c]                        #: media fiecarei clase
completat = [medii[c] if o is None else o for c, o in zip(clasa, ore)]
""")
    c.md("""
In pandas: `groupby(...).transform('mean')` intoarce o coloana **de aceeasi lungime** cu tabelul, avand pe fiecare rand media grupului lui. Apoi o folosesti la `fillna`. (`fillna` cu o coloana aliniaza dupa index.)
""")
    c.cod("""
medii_clasa = lipsa.groupby('clasa')['ore_studiu'].transform('mean')
ore_grup = lipsa['ore_studiu'].fillna(medii_clasa)

print(pd.DataFrame({'clasa': lipsa['clasa'], 'ore': lipsa['ore_studiu'], 'media clasei': medii_clasa.round(2),
                    'completat': ore_grup})[masca_ore].head(5))
print(lipsa.groupby('clasa')['ore_studiu'].mean().round(2).to_dict(), '<- media orelor pe clasa')
""")
    c.cod("""
anim_imputare(valori, masca_ore, {'media globala': ore_media.to_numpy(), 'media pe clasa': ore_grup.to_numpy()},
              eticheta='ore_studiu')
""")
    c.md("""
Varfurile sunt acum patru mai mici (unul pe clasa), nu unul mare. Nu e o imputare perfecta, dar respecta mai bine faptul ca in clasa a 12-a se invata mai mult.
""")

    c.md("""
## 11. Metoda 6: un indicator de "lipsa"

Uneori **faptul ca lipseste** e informatie: cine nu raspunde la o intrebare poate fi diferit de cei care raspund. Pastrezi golul completat si adaugi o coloana `0/1` care spune "asta a fost completat":
""")
    c.cod("""
cu_indicator = lipsa.assign(ore_lipsa=lipsa['ore_studiu'].isna().astype(int),
                            ore_studiu=ore_grup)
print(cu_indicator[['clasa', 'ore_studiu', 'ore_lipsa']].head(4))

# si pe datele reale: exista o legatura intre "lipseste" si tinta?
print(elevi.groupby(elevi['ore_studiu'].isna())['calificat'].mean().round(3).to_dict(), '<- rata de calificare (False=exista, True=lipseste)')
""")
    c.md("""
Costa o coloana in plus si nu repara un MNAR, dar lasa modelul sa invete singur daca lipsa conteaza. Se combina cu orice alta metoda.
""")

    c.md("""
## 12. Metoda 7: vecinii cei mai apropiati (KNN)

Ideea: un elev cu nota la mate foarte apropiata de a ta probabil are si o nota la info apropiata. Completezi golul cu media valorilor de la cei `k` vecini cei mai apropiati (dupa celelalte coloane). Intai varianta cu **o singura coloana**, de mana:
""")
    c.cod("""
%%vezi
x = [1.0, 2.0, 3.0, 8.0, 9.0]        # nota_mate (nu lipseste)
y = [2.0, 3.0, None, 9.0, 8.0]       # nota_info (lipseste la al treilea)
k = 2
i = 2
dist = []
for j in range(len(x)):
    if y[j] is not None:
        dist.append((abs(x[j] - x[i]), y[j]))     #: cat de departe e fiecare rand cunoscut, si valoarea lui y
dist.sort()                                       #: cei mai apropiati primii
vecini = dist[:k]
total = 0
for d, val in vecini:
    total += val
y[i] = total / k                                  #: media lui y la cei k vecini
""")
    c.md("""
Acelasi lucru pentru un tablou intreg, cu NumPy. Pentru fiecare gol: distantele la toate randurile cunoscute, iau primii `k`, fac media.
""")
    c.cod("""
def knn_1d(x, y, k=5):
    y = y.copy()
    cunoscut = ~np.isnan(y)
    for i in np.where(~cunoscut)[0]:
        dist = np.abs(x[cunoscut] - x[i])
        vecini = np.argsort(dist, kind='stable')[:k]
        y[i] = y[cunoscut][vecini].mean()
    return y


nota_info_knn = knn_1d(lipsa['nota_mate'].to_numpy(), lipsa['nota_info'].to_numpy(), k=5)
print(nota_info_knn[masca_info][:5].round(2), '<- primele 5 valori imputate')
print(adevar_info[:5], '<- adevarul')
""")
    c.md("""
Scikit-learn are toate acestea gata facute. Tiparul e mereu acelasi: **`fit`** = invata statistica din date (mediana fiecarei coloane, vecinii), **`transform`** = o aplica (completeaza golurile). `fit_transform` le face pe amandoua. Ele intorc un `ndarray`, il pui inapoi in tabel.
""")
    c.cod("""
from sklearn.impute import SimpleImputer, KNNImputer

cols = ['clasa', 'ore_studiu', 'absente', 'nota_mate', 'nota_info']
X = lipsa[cols]

simplu = SimpleImputer(strategy='median').fit(X)
print('medianele invatate:', simplu.statistics_.round(2))
X_med = pd.DataFrame(simplu.transform(X), columns=cols, index=X.index)

X_knn = pd.DataFrame(KNNImputer(n_neighbors=5).fit_transform(X), columns=cols, index=X.index)
print(X_knn[masca_info].head(3).round(2))
""")
    c.md("""
`KNNImputer` masoara distantele pe **toate** coloanele deodata. Daca o coloana are numere mult mai mari decat celelalte (`pret_eur` langa `camere`), ea domina distanta si vecinii nu mai sunt vecini "buni". De aceea, inainte de KNN se **scaleaza** datele (topicul de normalizare).
""")

    c.md("""
## 13. Scurgerea de informatie (data leakage)

Ai un set de antrenare (`train`) si unul de testare (`test`). Testul simuleaza datele **noi**, pe care modelul nu le-a vazut niciodata. Regula de aur:

> **Tot ce "inveti" din date (media, mediana, vecinii, scalarea) se invata DOAR din train.** Testul doar primeste ce s-a invatat.

Daca calculezi mediana pe tot setul si abia apoi imparti, testul a "contribuit" la mediana, deci informatie din test s-a scurs in antrenare. In productie nu ai testul dinainte.

Impartirea de mana (asta face `train_test_split`, plus amestecarea):
""")
    c.cod("""
rng = np.random.default_rng(0)
perm = rng.permutation(len(lipsa))              # o ordine aleatoare a randurilor
n_train = int(0.8 * len(lipsa))
train = lipsa.iloc[perm[:n_train]]
test = lipsa.iloc[perm[n_train:]]

print('media pe TOT setul (gresit) :', round(lipsa['ore_studiu'].mean(), 4))
print('media doar din train (corect):', round(train['ore_studiu'].mean(), 4))
""")
    c.md("""
Diferenta e mica, si e adevarat: **la media simpla scurgerea e aproape neglijabila**. Tocmai de aceea e periculoasa: pare inofensiva, iar obiceiul ramane. Cu statistici mai "puternice" (KNN, regresie, scalare, tot ce foloseste tinta) scurgerea devine mare. Forma corecta, cu `fit` pe train si `transform` pe ambele:
""")
    c.cod("""
imp = SimpleImputer(strategy='median')
imp.fit(train[['ore_studiu']])                     # mediana se invata DOAR din train
train_f = imp.transform(train[['ore_studiu']])
test_f = imp.transform(test[['ore_studiu']])       # testul primeste mediana din train
print('mediana din train:', imp.statistics_, '| goluri ramase in test:', np.isnan(test_f).sum())
""")
    c.md("""
Sa vedem cat de rau poate fi. Scenariu: prezicem `calificat` din `nota_info`, care are 30% goluri. Comparam trei variante pe acelasi train/test:

1. **corect**: completam cu media din train;
2. **cu scurgere**: completam golurile cu media notei *din aceeasi clasa de `calificat`*, calculata pe TOATE randurile (deci am folosit tinta, inclusiv a testului);
3. **date complete** (fara goluri): plafonul realist.

**Prezice:** care are cea mai mare acuratete pe test? Poate fi varianta 2 mai buna decat varianta 3 (date complete)?

<details><summary>Raspuns</summary>

Varianta 2 iese cea mai buna, **chiar peste datele complete**. Asta e imposibil pentru o metoda cinstita: nu poti sti mai mult decat datele complete. E semnul clasic de scurgere: cand scorul cu goluri completate intrece scorul cu date complete, ceva "se uita" la raspuns.
</details>
""")
    c.cod("""
from sklearn.linear_model import LogisticRegression


def acuratete(seed):
    rng = np.random.default_rng(seed)
    x_complet = complet['nota_info'].to_numpy()
    y = complet['calificat'].to_numpy()
    x = x_complet.copy()
    x[rng.random(len(x)) < 0.30] = np.nan               # 30% goluri
    perm = rng.permutation(len(x))
    tr, te = perm[:200], perm[200:]

    def scor_pe(v):                                     # antreneaza pe train, masoara pe test
        m = LogisticRegression().fit(v[tr].reshape(-1, 1), y[tr])
        return m.score(v[te].reshape(-1, 1), y[te])

    corect = np.where(np.isnan(x), np.nanmean(x[tr]), x)        # media doar din train
    scurs = x.copy()
    for clasa_y in (0, 1):
        scurs[np.isnan(x) & (y == clasa_y)] = np.nanmean(x[y == clasa_y])   # foloseste tinta lui y, inclusiv la test
    return scor_pe(corect), scor_pe(scurs), scor_pe(x_complet)


rez = np.array([acuratete(s) for s in range(30)]).mean(axis=0)
print(f'corect: {rez[0]:.3f} | cu scurgere: {rez[1]:.3f} | date complete: {rez[2]:.3f}')
""")
    c.md("""
Ai vazut cum arata un scor umflat artificial. **In practica nu-ti scrii tu impartirea de mana**: pui imputarea intr-un `Pipeline`, iar `cross_val_score` face `fit` pe partea de train a fiecarui fold si `transform` pe cea de test, corect, fara sa te gandesti.
""")
    c.cod("""
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score

model = make_pipeline(SimpleImputer(strategy='median'), LogisticRegression())
scoruri = cross_val_score(model, lipsa[['ore_studiu', 'nota_info', 'absente']], lipsa['calificat'], cv=5)
print('acuratete pe 5 folduri (imputare corecta, in interiorul fiecarui fold):', scoruri.round(3), scoruri.mean().round(3))
""")

    c.md("""
## 14. Cum afli daca imputarea a ajutat

Intrebarea cea mai importanta din notebook. La datele reale nu stii valorile lipsa (de aia lipsesc). Solutia: **simulezi**.

1. Iei un set (sau partea lui) unde **stii totul**.
2. Stergi cateva valori cu o masca cu seed fix, si pastrezi adevarul separat.
3. Completezi cu fiecare metoda.
4. Compari ce ai pus cu adevarul.

Compararea se face cu o **eroare**. Doua populare, de mana:

- **MAE** (eroarea absoluta medie): media lui `|adevar - imputat|`
- **RMSE** (radacina erorii patratice medii): patratul pedepseste mai tare erorile mari
""")
    c.cod("""
%%vezi
adevar = [5.0, 7.0, 6.0]
imputat = [6.0, 6.0, 9.0]
abs_tot = 0
patrat_tot = 0
for a, b in zip(adevar, imputat):
    abs_tot += abs(a - b)               #: MAE aduna distantele
    patrat_tot += (a - b) ** 2          #: RMSE aduna patratele distantelor
mae = abs_tot / len(adevar)
rmse = (patrat_tot / len(adevar)) ** 0.5
""")
    c.md("""
Aceleasi formule, vectorizate (bucla in C, de ce e mai rapid stii de la EDA). Apoi mini-benchmark-ul: toate metodele pe golurile din `lipsa`, comparate cu `adevar_ore` si `adevar_info`.
""")
    c.cod("""
def mae(adevar, imputat):
    return float(np.mean(np.abs(np.asarray(adevar) - np.asarray(imputat))))


def rmse(adevar, imputat):
    return float(np.sqrt(np.mean((np.asarray(adevar) - np.asarray(imputat)) ** 2)))


# valorile puse in goluri, pentru fiecare metoda (doar pozitiile din masca)
ore_cunoscute = lipsa.loc[~masca_ore, 'ore_studiu']
info_cunoscute = lipsa.loc[~masca_info, 'nota_info']
pred_ore = {
    'constanta 0': np.zeros(masca_ore.sum()),
    'media': np.full(masca_ore.sum(), ore_cunoscute.mean()),
    'mediana': np.full(masca_ore.sum(), ore_cunoscute.median()),
    'media pe clasa': ore_grup[masca_ore].to_numpy(),
    'KNNImputer (5 coloane)': X_knn.loc[masca_ore, 'ore_studiu'].to_numpy(),
}
pred_info = {
    'constanta 0': np.zeros(masca_info.sum()),
    'media': np.full(masca_info.sum(), info_cunoscute.mean()),
    'mediana': np.full(masca_info.sum(), info_cunoscute.median()),
    'KNN pe nota_mate (de mana)': nota_info_knn[masca_info],
    'KNNImputer (5 coloane)': X_knn.loc[masca_info, 'nota_info'].to_numpy(),
}

tabel = pd.DataFrame({
    'ore RMSE': {n: rmse(adevar_ore, p) for n, p in pred_ore.items()},
    'ore MAE': {n: mae(adevar_ore, p) for n, p in pred_ore.items()},
    'info RMSE': {n: rmse(adevar_info, p) for n, p in pred_info.items()},
    'info MAE': {n: mae(adevar_info, p) for n, p in pred_info.items()},
})
print(tabel.round(3))
""")
    c.md("""
Ce se vede: **`constanta 0`** e de departe cea mai proasta. **Nicio metoda nu e cea mai buna la tot.** La `ore_studiu` merge bine media pe clasa (orele depind de clasa). La `nota_info` cistiga metodele care folosesc `nota_mate` (KNN), pentru ca cele doua note merg impreuna, iar media sau mediana nu folosesc nimic din asta. Iar la `ore_studiu` (asimetrica) `mediana` bate media la MAE, dar pierde la RMSE: fiecare eroare "prefera" alta valoare.

Ce spun punctele? Fiecare scatter arata un gol imputat (portocaliu) langa adevarul lui (cerc verde):
""")
    c.cod("""
def completeaza(baza, masca, valori):
    out = baza.copy()
    out[masca] = valori
    return out


nota_mate = lipsa['nota_mate'].to_numpy()
nota_info = lipsa['nota_info'].to_numpy()
anim_scatter_imputare(nota_mate, nota_info, masca_info,
                      {'media': completeaza(nota_info, masca_info, pred_info['media']),
                       'KNN pe nota_mate': completeaza(nota_info, masca_info, pred_info['KNN pe nota_mate (de mana)'])},
                      adevar=adevar_info, eticheta_x='nota_mate', eticheta_y='nota_info')
""")
    c.md("""
**O singura masca e norocul, nu o concluzie.** Repeta cu mai multe masti (seed-uri) si uita-te la medie si la imprastiere:
""")
    c.cod("""
def rmse_ore(seed):
    rng = np.random.default_rng(seed)
    m = rng.random(len(complet)) < 0.20
    ad = complet.loc[m, 'ore_studiu'].to_numpy()
    ramase = complet.loc[~m]
    pe_clasa = ramase.groupby('clasa')['ore_studiu'].mean()
    return {'constanta 0': rmse(ad, 0), 'media': rmse(ad, ramase['ore_studiu'].mean()),
            'mediana': rmse(ad, ramase['ore_studiu'].median()),
            'media pe clasa': rmse(ad, complet.loc[m, 'clasa'].map(pe_clasa))}


rez = pd.DataFrame([rmse_ore(s) for s in range(20)])
print(rez.agg(['mean', 'std']).round(3))
""")
    c.md("""
Doua avertismente. **Primul:** cea mai buna metoda dupa RMSE nu e neaparat cea mai buna pentru model: media are RMSE bun, dar strica varianta si corelatiile (sectiunea 8). Cel mai sigur criteriu final este **scorul modelului tau**, evaluat corect (imputare in interiorul `Pipeline`, fit pe train). **Al doilea:** pe date reale mimezi acelasi lucru: iei valorile pe care le ai, "ascunzi" 20% din ele si vezi ce metoda le ghiceste mai bine.
""")
    c.cod("""
cunoscute = elevi['ore_studiu'].dropna().to_numpy()          # datele reale, doar ce stim
rng = np.random.default_rng(0)
ascunse = rng.random(len(cunoscute)) < 0.20                  # ascundem 20% dintre ele
ramase = cunoscute[~ascunse]
print('RMSE media  :', round(rmse(cunoscute[ascunse], ramase.mean()), 3))
print('RMSE mediana:', round(rmse(cunoscute[ascunse], np.median(ramase)), 3))
""")

    c.md("""
## 15. Capcane

**Capcana 1: imputarea inainte de impartire (leakage).** Vazuta mai sus. Regula: `fit` pe train, `transform` pe train si test. In cod: imputezi *dupa* `train_test_split`, sau in `Pipeline`.

**Capcana 2: `fillna` nu modifica, intoarce.** Daca nu pastrezi rezultatul, ai facut treaba degeaba:
""")
    c.cod("""
x = pd.Series([1.0, None, 3.0])
x.fillna(0)                  # rezultatul se pierde
print(x.tolist())
x = x.fillna(0)              # asa il pastrezi
print(x.tolist())
""")
    c.md("""
(`fillna(0, inplace=True)` pe o coloana luata din tabel e si mai rau: modifica o copie temporara sau e interzis in pandas nou. Nu-l folosi, pastreaza rezultatul cu `=`.)

**Capcana 3: golurile deghizate.** Un `-999` pus de senzor nu e `NaN`, deci `mean()` il ia in calcul:
""")
    c.cod("""
temp = pd.Series([21.0, 19.5, -999.0, 22.0, -999.0])
print('media cu -999:', round(temp.mean(), 1), '| minim:', temp.min())
temp = temp.replace(-999, np.nan)                    # ii transformi in NaN adevarat
print('media dupa replace:', round(temp.mean(), 2))
""")
    c.md("""
**Capcana 4: `mode()` intoarce o `Series`.** Iar `NaN` nu se compara cu `==`:
""")
    c.cod("""
cat = pd.Series(['nu', 'da', 'nu', None])
print(cat.mode())                          # o Series cu un element, nu o valoare
print(cat.fillna(cat.mode()[0]).tolist())

print(elevi[elevi['ore_studiu'] == np.nan].shape, '<- comparatia cu NaN nu prinde nimic; foloseste isna()')
""")
    c.md("""
**Capcana 5: completezi coloana-tinta.** Nu imputa niciodata ce vrei sa prezici pe setul de test. Randurile fara tinta se scot (sau se prezic la final), nu se "completeaza".

**Capcana 6: completezi si uiti.** O coloana completata are alta distributie decat cea reala (varful la medie, varianta mica). Daca golurile erau multe (peste ~40%), gandeste-te serios la alta strategie sau la un indicator de lipsa.
""")

    c.md("""
### Cum citesti erorile
""")
    c.cod("""
%%vezi
ore = [4.0, None, 6.0]
total = sum(ore)         #: TypeError: nu poti aduna un numar cu None
""")
    c.cod("""
from sklearn.linear_model import LogisticRegression
try:
    LogisticRegression().fit(lipsa[['ore_studiu']], lipsa['calificat'])
except ValueError as e:
    print('ValueError:', str(e)[:90])

try:
    SimpleImputer(strategy='mean').fit_transform(elevi[['meditatii']])
except ValueError as e:
    print('ValueError:', str(e)[:90])
""")
    c.md("""
| eroare | de obicei inseamna |
|---|---|
| `ValueError: Input X contains NaN` | modelul nu accepta goluri: imputeaza (in Pipeline) inainte de `fit` |
| `TypeError: unsupported operand ... 'NoneType'` | ai un `None` intr-o lista pe care faci calcule |
| `ValueError: could not convert string to float` | ai dat lui `SimpleImputer(strategy='mean')` o coloana text: foloseste `most_frequent` |
| `KeyError` la `fillna(dict)` | numele coloanei din dictionar nu exista |
| `ValueError: X has N features, but ... expected M` | ai facut `transform` pe alte coloane decat la `fit` |
""")

    c.md("""
## Exercitii

Le rezolvi pe rand. Pe cele cu date lucrezi pe `elevi` (cu tot cu problemele lui) sau pe `lipsa` din sectiunea 4 (masca cu seed 42, o ai deja in memorie).

**Exercitiul 1.** Cate valori lipsesc in fiecare coloana din `elevi`, ca dictionar `{coloana: numar}` (doar coloanele care au goluri), si pe cate randuri lipseste cel putin o valoare.
""")
    c.ex("""
lipsa_pe_coloana = None    # TODO: dictionar
randuri_incomplete = None  # TODO: numar
""", """
nr = elevi.isna().sum()
lipsa_pe_coloana = nr[nr > 0].to_dict()
randuri_incomplete = elevi.isna().any(axis=1).sum()
""")
    c.cod(E('lipsa pe coloana', 'lipsa_pe_coloana', "elevi.isna().sum()[elevi.isna().sum() > 0].to_dict()") + '\n' +
          E('randuri incomplete', 'randuri_incomplete', 'elevi.isna().any(axis=1).sum()'))

    c.md("""
**Exercitiul 2.** De mana: `imputa_mediana(lista)` primeste o lista cu numere si `None`, si intoarce lista cu fiecare `None` inlocuit cu mediana valorilor cunoscute. Fara `numpy` sau `pandas`. Mediana la numar par de valori = media celor doua din mijloc.
""")
    c.ex("""
def imputa_mediana(lista):
    pass  # TODO
""", """
def imputa_mediana(lista):
    cunoscute = sorted(x for x in lista if x is not None)
    n = len(cunoscute)
    if n % 2:
        med = cunoscute[n // 2]
    else:
        med = (cunoscute[n // 2 - 1] + cunoscute[n // 2]) / 2
    return [med if x is None else x for x in lista]
""")
    c.cod("""
import random


def ref_med(v):
    k = [x for x in v if x is not None]
    m = float(np.median(k))
    return [m if x is None else x for x in v]


def gen_lista():
    v = [random.choice([None, round(random.uniform(0, 30), 1)]) for _ in range(random.randint(2, 12))]
    v[0] = round(random.uniform(0, 30), 1)
    return (v,)


verifica('imputa_mediana', imputa_mediana,
         [(([4, None, 6, 5, None, 30],), [4, 5.5, 6, 5, 5.5, 30]), (([1, 2, None],), [1, 2, 1.5])],
         ascunse=[(([7.5, None],), [7.5, 7.5])],
         referinta=ref_med, generator=gen_lista,
         indiciu='sorteaza valorile cunoscute; mediana = elementul din mijloc (sau media celor doua)')
""")

    c.md("""
**Exercitiul 3.** Media sau mediana? Completeaza `ore_studiu` din `elevi` cu **mediana** coloanei si salveaza media noii coloane in `media_dupa_mediana`. Apoi in `alegere` scrie `'mediana'` sau `'media'`, dupa regula: daca `abs(skew) > 0.5`, coloana e asimetrica, deci `'mediana'`.
""")
    c.ex("""
media_dupa_mediana = None   # TODO
alegere = None              # TODO: 'mediana' sau 'media'
""", """
ore_m = elevi['ore_studiu'].fillna(elevi['ore_studiu'].median())
media_dupa_mediana = ore_m.mean()
alegere = 'mediana' if abs(elevi['ore_studiu'].skew()) > 0.5 else 'media'
""")
    c.cod(E('media dupa mediana', 'media_dupa_mediana', "elevi['ore_studiu'].fillna(elevi['ore_studiu'].median()).mean()") + '\n' +
          E('alegere', 'alegere', "'mediana' if abs(elevi['ore_studiu'].skew()) > 0.5 else 'media'"))

    c.md("""
**Exercitiul 4.** Pe grupuri: completeaza `ore_studiu` din `elevi` cu **media clasei** (`groupby` + `transform`) si intoarce **suma** coloanei complete in `suma_ore_pe_clasa`.
""")
    c.ex("""
suma_ore_pe_clasa = None   # TODO
""", """
ore_g = elevi['ore_studiu'].fillna(elevi.groupby('clasa')['ore_studiu'].transform('mean'))
suma_ore_pe_clasa = ore_g.sum()
""")
    c.cod(E('suma pe clasa', 'suma_ore_pe_clasa', "elevi['ore_studiu'].fillna(elevi.groupby('clasa')['ore_studiu'].transform('mean')).sum()",
            "indiciu='transform(\\'mean\\') da o coloana de aceeasi lungime; fillna o foloseste ca valori'"))

    c.md("""
**Exercitiul 5.** Fara scurgere. Am impartit `elevi` in `train` (primele 180 de randuri) si `test` (restul). Calculeaza mediana lui `ore_studiu` **doar din `train`** (`mediana_train`), apoi completeaza golurile din `test` cu ea si intoarce suma coloanei din test dupa completare (`suma_test_completat`).
""")
    c.cod("""
train = elevi.iloc[:180]
test = elevi.iloc[180:]
""")
    c.ex("""
mediana_train = None        # TODO
suma_test_completat = None  # TODO
""", """
mediana_train = train['ore_studiu'].median()
suma_test_completat = test['ore_studiu'].fillna(mediana_train).sum()
""")
    c.cod(E('mediana din train', 'mediana_train', "train['ore_studiu'].median()") + '\n' +
          E('test completat', 'suma_test_completat', "test['ore_studiu'].fillna(train['ore_studiu'].median()).sum()",
            "indiciu='fillna pe test, dar cu valoarea calculata din train'"))

    c.md("""
**Exercitiul 6.** RMSE de mana, fara `numpy`: `rmse_manual(adevar, imputat)` intoarce radacina mediei patratelor diferentelor.
""")
    c.ex("""
def rmse_manual(adevar, imputat):
    pass  # TODO
""", """
def rmse_manual(adevar, imputat):
    s = 0
    for a, b in zip(adevar, imputat):
        s += (a - b) ** 2
    return (s / len(adevar)) ** 0.5
""")
    c.cod("""
import random
verifica('rmse_manual', rmse_manual, [(([5.0, 7.0, 6.0], [6.0, 6.0, 9.0]), 1.9148542155126762), (([1, 2], [1, 2]), 0.0)],
         referinta=lambda a, b: float(np.sqrt(np.mean((np.array(a) - np.array(b)) ** 2))),
         generator=lambda: tuple(zip(*[(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(random.randint(1, 15))])))
""")

    c.md("""
**Exercitiul 7.** Mini-benchmark pe `ore_studiu`. Ai in memorie `lipsa`, `masca_ore` si `adevar_ore` (adevarul de la goluri). Calculeaza, pe pozitiile din `masca_ore`, RMSE pentru trei metode si pune-le in dictionarul `rmse_ore`, cu cheile `'media'`, `'mediana'`, `'pe_clasa'`:

- `media` / `mediana`: media / mediana valorilor **cunoscute** din `lipsa['ore_studiu']`;
- `pe_clasa`: media clasei fiecarui rand cu gol, calculata din valorile cunoscute.

Apoi `cea_mai_buna` = numele metodei cu RMSE minim.
""")
    c.ex("""
rmse_ore = None     # TODO: {'media': ..., 'mediana': ..., 'pe_clasa': ...}
cea_mai_buna = None  # TODO
""", """
def _rmse(a, b):
    return float(np.sqrt(np.mean((np.asarray(a) - np.asarray(b)) ** 2)))

cunoscute = lipsa['ore_studiu'].dropna()
medii = lipsa.groupby('clasa')['ore_studiu'].mean()          # groupby ignora NaN
rmse_ore = {
    'media': _rmse(adevar_ore, cunoscute.mean()),
    'mediana': _rmse(adevar_ore, cunoscute.median()),
    'pe_clasa': _rmse(adevar_ore, lipsa.loc[masca_ore, 'clasa'].map(medii)),
}
cea_mai_buna = min(rmse_ore, key=rmse_ore.get)
""")
    NS['_rmse'] = lambda a, b: float(np.sqrt(np.mean((np.asarray(a) - np.asarray(b)) ** 2)))
    _cun = NS['lipsa']['ore_studiu'].dropna()
    _med = NS['lipsa'].groupby('clasa')['ore_studiu'].mean()
    NS['rmse_ore'] = {
        'media': NS['_rmse'](NS['adevar_ore'], _cun.mean()),
        'mediana': NS['_rmse'](NS['adevar_ore'], _cun.median()),
        'pe_clasa': NS['_rmse'](NS['adevar_ore'], NS['lipsa'].loc[NS['masca_ore'], 'clasa'].map(_med)),
    }
    NS['cea_mai_buna'] = min(NS['rmse_ore'], key=NS['rmse_ore'].get)
    c.cod(E('rmse pe metode', 'rmse_ore', 'rmse_ore', 'tol=1e-4') + '\n' +
          E('cea mai buna', 'cea_mai_buna', 'cea_mai_buna') + '\nscor()')

    c.md("""
## Recapitulare

- Goluri: `NaN` (pandas) sau `None`. `NaN != NaN`, deci il cauti cu `isna()`. Cauta si golurile deghizate (`-1`, `999`, `'n/a'`).
- Detectie: `isna().sum()`, `isna().mean()`, un heatmap al golurilor. Vezi daca golurile vin pe acelasi rand.
- **Mecanisme:** MCAR (la intamplare), MAR (depinde de alta coloana, o poti corecta), MNAR (depinde de valoarea insasi, nu se poate corecta din date). La MAR si MNAR media ramasa e deformata.
- **Metode:** stergere (pierzi date; distorsioneaza la MAR), constanta (bine la categorii, prost la numere), medie / mediana (mediana la date asimetrice) / mod, `ffill` / `bfill` / `interpolate` (doar serii ordonate), pe grupuri (`groupby().transform`), indicator de lipsa, KNN (vecini, dupa scalare).
- Media strica: **varianta scade**, apare un varf artificial la medie, corelatiile slabesc.
- **Leakage:** statisticile de umplere se invata doar din `train`. `fit` pe train, `transform` pe train si test, sau `Pipeline`. Semnal de alarma: scor cu goluri completate mai bun decat cu date complete.
- **Evaluare:** stergi valori cunoscute cu masca cu seed fix, imputezi, compari cu adevarul (MAE / RMSE), pe mai multe seed-uri. Criteriul final e scorul modelului, evaluat corect.

Legatura cu ONIA: sarcinile cu CSV au aproape mereu goluri. Un competitor care completeaza corect (in interiorul unui `Pipeline`) si poate arata *de ce* a ales metoda are un avantaj real fata de unul care scrie `fillna(0)` peste tot. Tema are un exercitiu de repara-codul (leakage), un program in format concurs si o imputare evaluata pe un adevar ascuns.
""")
    c.salveaza('11-valori-lipsa-predare')


# ---------------------------------------------------------------------------
# TEMA
# ---------------------------------------------------------------------------

def tema():
    c = Carnet('Completarea valorilor lipsa', 'tema',
               fisiere=('date/elevi.csv', 'date/case.csv', 'date/11_concurs_lipsa.csv', 'date/11_elevi_complet.csv'))

    c.md("""
Tema: functii generale pe DataFrame-uri (testele vizibile pe `elevi.csv`, cele **ascunse** pe alte seturi), un cod de reparat (scurgere de informatie), un program in format concurs, o imputare evaluata pe un **adevar ascuns** si o provocare. La final, `scor()`.

Nu memora pandas: cauta in documentatie. Nu cauta solutii gata facute, aici conteaza sa gandesti tu.
""")
    c.cod("""
import numpy as np
import pandas as pd

elevi = pd.read_csv('date/elevi.csv')
case = pd.read_csv('date/case.csv')
concurs = pd.read_csv('date/11_concurs_lipsa.csv')       # 200 de elevi, cu goluri (folosit mai jos)
""")

    # 1
    c.md("""
### 1. Procentul de goluri pe coloane

`procent_lipsa_pe_coloana(df)` intoarce un dictionar `{coloana: procent}` (0-100) pentru **toate** coloanele.
""")
    sol = """
def procent_lipsa_pe_coloana(df):
    return (df.isna().mean() * 100).to_dict()
"""
    exec(sol, NS)
    c.ex("""
def procent_lipsa_pe_coloana(df):
    pass  # TODO
""", sol)
    c.cod(T('procent_lipsa_pe_coloana', 'procent_lipsa_pe_coloana', ['elevi'], ['case', 'concurs', 'elevi.head(40)', 'elevi.dropna()']))

    # 2
    c.md("""
### 2. Completeaza cu mediana

`completeaza_mediana(serie)` intoarce seria cu golurile inlocuite cu mediana valorilor cunoscute. (Verificarea se uita la suma seriei tale si la cate goluri au ramas.)
""")
    sol = """
def completeaza_mediana(serie):
    return serie.fillna(serie.median())
"""
    exec(sol, NS)
    c.ex("""
def completeaza_mediana(serie):
    pass  # TODO
""", sol)
    pre = """
def _rez_mediana(df, col):
    s = completeaza_mediana(df[col])
    return float(s.sum()), int(s.isna().sum())
"""
    c.cod(T('completeaza_mediana', '_rez_mediana', ["elevi, 'ore_studiu'", "elevi, 'nota_info'"],
            ["case, 'an_constructie'", "case, 'etaj'", "concurs, 'nota_mate'", "elevi, 'absente'"], pre=pre))

    # 3
    c.md("""
### 3. Completeaza cu modul

`completeaza_mod(serie)` completeaza golurile unei coloane categorice cu valoarea cea mai frecventa. (Atentie la ce intoarce `mode()`. Nu vom da teste cu egalitati.)
""")
    sol = """
def completeaza_mod(serie):
    return serie.fillna(serie.mode()[0])
"""
    exec(sol, NS)
    c.ex("""
def completeaza_mod(serie):
    pass  # TODO
""", sol)
    pre = """
def _frecv(serie):
    return completeaza_mod(serie).value_counts().to_dict()
"""
    c.cod(T('completeaza_mod', '_frecv', ["elevi['meditatii'].str.strip().str.lower()"],
            ["case['oras']", "pd.Series(['a', 'b', 'b', None, None])", "pd.Series([3.0, 3.0, 1.0, None])",
             "elevi['meditatii'].str.strip().str.lower().head(50)"], pre=pre))

    # 4
    c.md("""
### 4. Completeaza pe grupuri (2 puncte)

`completeaza_pe_grup(df, col, grup)` completeaza golurile lui `col` cu **mediana grupului** din care face parte randul (grupul = valoarea din coloana `grup`). Intoarce seria completata. Ai nevoie de `groupby` si `transform`.
""")
    sol = """
def completeaza_pe_grup(df, col, grup):
    return df[col].fillna(df.groupby(grup)[col].transform('median'))
"""
    exec(sol, NS)
    c.ex("""
def completeaza_pe_grup(df, col, grup):
    pass  # TODO
""", sol)
    pre = """
def _rez_grup(df, col, grup):
    s = completeaza_pe_grup(df, col, grup)
    return float(s.sum()), int(s.isna().sum())
"""
    c.cod(T('completeaza_pe_grup', '_rez_grup', ["elevi, 'ore_studiu', 'clasa'", "concurs, 'ore_studiu', 'clasa'"],
            ["concurs, 'nota_info', 'clasa'", "case, 'an_constructie', 'oras'", "case, 'etaj', 'camere'", "elevi, 'nota_info', 'clasa'"],
            pre=pre, extra="puncte=2, indiciu=\"df.groupby(grup)[col].transform('median') da mediana grupului pe fiecare rand\""))

    # 5
    c.md("""
### 5. `ffill` de mana

`ffill_manual(lista)`: primeste o lista cu numere si `None` si intoarce o lista in care fiecare `None` e inlocuit cu ultima valoare cunoscuta dinainte. Daca nu exista nicio valoare inainte (gol la inceput), ramane `None`. Fara pandas.
""")
    sol = """
def ffill_manual(lista):
    rez = []
    ultima = None
    for x in lista:
        if x is None:
            rez.append(ultima)
        else:
            rez.append(x)
            ultima = x
    return rez
"""
    exec(sol, NS)
    c.ex("""
def ffill_manual(lista):
    pass  # TODO
""", sol)
    c.cod(T('ffill_manual', 'ffill_manual', ['[3, None, None, 5, None]', '[1, 2, 3]'],
            ['[None, 2, None]', '[None, None]', '[]', '[7.5, None, 8, None, None, 9.5]', '[None, 4, None, None, 1]']))

    # 6 repara
    c.md("""
### 6. Repara codul: scurgerea de informatie (2 puncte)

Functia trebuie sa imparta `df` in `train` (primele `n_train` randuri) si `test` (restul) si sa completeze golurile din `col` cu **mediana coloanei**. Ce face gresit? Cand compari cu ce ar trebui sa iasa, valorile din `test` difera. Gaseste de ce si repara: mediana trebuie invatata doar din `train`.
""")
    sol = """
def completeaza_train_test(df, col, n_train):
    train = df.iloc[:n_train].copy()
    test = df.iloc[n_train:].copy()
    mediana = train[col].median()
    train[col] = train[col].fillna(mediana)
    test[col] = test[col].fillna(mediana)
    return train, test
"""
    exec(sol, NS)
    c.ex("""
def completeaza_train_test(df, col, n_train):
    mediana = df[col].median()
    train = df.iloc[:n_train].copy()
    test = df.iloc[n_train:].copy()
    train[col] = train[col].fillna(mediana)
    test[col] = test[col].fillna(mediana)
    return train, test
""", sol)
    pre = """
def _rez_split(df, col, n_train):
    train, test = completeaza_train_test(df, col, n_train)
    return float(train[col].sum()), float(test[col].sum())
"""
    c.cod(T('completeaza_train_test', '_rez_split', ["elevi, 'ore_studiu', 180", "concurs, 'ore_studiu', 150"],
            ["concurs, 'nota_info', 100", "case, 'an_constructie', 200", "elevi, 'nota_info', 60", "elevi, 'ore_studiu', 30"],
            pre=pre, extra="puncte=2, indiciu='pe ce randuri se calculeaza mediana? Ar trebui sa vada testul?'"))

    # 7
    c.md("""
### 7. Care metoda a fost cea mai buna? (2 puncte)

Ai valorile adevarate de la goluri (`adevar`) si, pentru fiecare metoda, ce a completat ea in acele goluri (`candidati`, un dictionar `{nume: lista_valori}`). `alege_metoda(adevar, candidati)` intoarce perechea `(nume_cea_mai_buna, rmse_ei)`. Cea mai buna = RMSE minim.
""")
    sol = """
def alege_metoda(adevar, candidati):
    scoruri = {}
    for nume, imp in candidati.items():
        scoruri[nume] = float(np.sqrt(np.mean((np.asarray(adevar) - np.asarray(imp)) ** 2)))
    nume = min(scoruri, key=scoruri.get)
    return nume, scoruri[nume]
"""
    exec(sol, NS)
    c.ex("""
def alege_metoda(adevar, candidati):
    pass  # TODO
""", sol)
    rnd = random.Random(7)
    cazuri = []
    for _ in range(5):
        n = rnd.randint(4, 12)
        ad = [round(rnd.uniform(0, 10), 2) for _ in range(n)]
        cand = {nm: [round(v + rnd.gauss(0, s), 2) for v in ad] for nm, s in [('media', 1.5), ('mediana', 1.3), ('knn', 0.6)]}
        cazuri.append('%r, %r' % (ad, cand))
    c.cod(T('alege_metoda', 'alege_metoda',
            ["[5.0, 7.0, 6.0], {'a': [6.0, 6.0, 9.0], 'b': [5.5, 7.5, 6.5]}", "[1, 2, 3], {'unic': [1, 2, 4]}"],
            cazuri, extra="puncte=2"))

    # 8
    c.md("""
### 8. Indicatori de lipsa

`adauga_indicatori(df)` intoarce o **copie** a lui `df` la care, pentru fiecare coloana care are goluri, adaugi o coloana noua `<nume>_lipsa` cu `1` unde valoarea lipsea si `0` altfel. Coloanele fara goluri nu primesc indicator. `df` nu se modifica.
""")
    sol = """
def adauga_indicatori(df):
    d = df.copy()
    for col in df.columns[df.isna().any()]:
        d[col + '_lipsa'] = df[col].isna().astype(int)
    return d
"""
    exec(sol, NS)
    c.ex("""
def adauga_indicatori(df):
    pass  # TODO
""", sol)
    pre = """
def _rez_ind(df):
    d = adauga_indicatori(df)
    noi = sorted(set(d.columns) - set(df.columns))
    return noi, {n: int(d[n].sum()) for n in noi}
"""
    c.cod(T('adauga_indicatori', '_rez_ind', ['elevi'], ['case', 'concurs', 'elevi.dropna()', 'elevi.head(20)'], pre=pre))

    # 9 program
    c.md("""
### 9. Program in format concurs: umplere cu mediana

Pe prima linie primesti `n`, pe a doua `n` valori separate prin spatiu; o valoare lipsa e scrisa `?`. Afiseaza pe o linie cele `n` valori, cu **doua zecimale**, separate prin spatiu, in care fiecare `?` e inlocuit cu **mediana valorilor cunoscute** (la numar par de valori cunoscute, media celor doua din mijloc). Exista cel putin o valoare cunoscuta.

Exemplu: `5` si `4 ? 6 ? 30` -> valorile cunoscute sunt 4, 6, 30 (mediana 6) si iese `4.00 6.00 6.00 6.00 30.00`.
""")

    def ref_prog(inp):
        tok = inp[1].split()
        cun = sorted(float(t) for t in tok if t != '?')
        m = len(cun)
        med = cun[m // 2] if m % 2 else (cun[m // 2 - 1] + cun[m // 2]) / 2
        return ' '.join('%.2f' % (med if t == '?' else float(t)) for t in tok)

    rnd = random.Random(23)
    cazuri = []
    for _ in range(7):
        n = rnd.randint(1, 15)
        tok = [str(round(rnd.uniform(0, 40), rnd.choice([0, 1, 2]))) if rnd.random() > 0.35 else '?' for _ in range(n)]
        if all(t == '?' for t in tok):
            tok[0] = '12.5'
        inp = [str(n), ' '.join(tok)]
        cazuri.append((inp, ref_prog(inp)))
    vis = [(['5', '4 ? 6 ? 30'], '4.00 6.00 6.00 6.00 30.00'), (['3', '1 2 ?'], '1.00 2.00 1.50')]
    c.ex("""
def main():
    pass  # TODO
""", """
def main():
    n = int(input())
    tok = input().split()
    cunoscute = sorted(float(t) for t in tok if t != '?')
    m = len(cunoscute)
    if m % 2:
        med = cunoscute[m // 2]
    else:
        med = (cunoscute[m // 2 - 1] + cunoscute[m // 2]) / 2
    rez = []
    for t in tok:
        rez.append(med if t == '?' else float(t))
    print(' '.join(f'{v:.2f}' for v in rez))
""")
    c.cod("verifica_program('umplere cu mediana', main,\n                 %s,\n                 ascunse=%s, puncte=2)" % (R(vis), R(cazuri)))

    # 10 concurs
    c.md("""
### 10. Imputare pe un adevar ascuns (4 puncte)

`concurs` are 200 de elevi si goluri la `ore_studiu`, `nota_mate` si `nota_info`. Golurile nu sunt aleatoare (**MAR**): `ore_studiu` lipseste mai des la clasa a 12-a, notele mai des la cine are multe absente. Scrie `imputeaza(df)`: primeste tabelul cu goluri si intoarce **acelasi tabel** (aceleasi coloane, in aceeasi ordine, aceleasi randuri) fara niciun gol.

Cum e notat: la fel ca la olimpiada, comparam ce ai completat cu adevarul (pe care tu nu-l vezi) prin **RMSE normalizat**: pentru fiecare coloana cu goluri, RMSE-ul la golurile ei impartit la deviatia standard a coloanei, apoi media pe coloane. Treci daca ai cel putin cu **3%** mai bine decat completarea cu media coloanei. Valorile deja cunoscute nu au voie sa se schimbe. Testul se ruleaza pe tabelul de mai sus, plus **doua tabele ascunse** (aceeasi structura, alta masca), deci nu merge sa "invatzi" valorile pe de rost.

Ce ai la dispozitie: tot ce ai vazut. Media/mediana globala nu ajunge. Idei: mediana pe clasa pentru `ore_studiu`; `KNNImputer` (coloanele `clasa`, `ore_studiu`, `absente`, `nota_mate`, `nota_info`, nu si `id`); regresie pe celelalte coloane.
""".replace('invatzi', 'inveti'))
    c.ex("""
def imputeaza(df):
    d = df.copy()
    # TODO: completeaza golurile din d (nu modifica id si nu schimba valorile cunoscute)
    return d
""", """
from sklearn.impute import KNNImputer


def imputeaza(df):
    d = df.copy()
    cols = ['clasa', 'ore_studiu', 'absente', 'nota_mate', 'nota_info']
    d[cols] = KNNImputer(n_neighbors=5).fit_transform(d[cols])
    return d
""")
    c.cod("""
descarca('date/11_concurs_adevar.csv')
adevar = pd.read_csv('date/11_concurs_adevar.csv')             # adevarul: ce se ascunde la olimpiada. Nu-l deschide inainte sa termini.
baza_completa = pd.read_csv('date/11_elevi_complet.csv').drop(columns=['meditatii', 'calificat'])


def sterge(df, seed):                                           # aceeasi structura MAR ca in `concurs`, alta masca
    rng = np.random.default_rng(seed)
    n = len(df)
    out = df.copy()
    out.loc[rng.random(n) < np.where(df['clasa'] == 12, 0.35, 0.10), 'ore_studiu'] = np.nan
    out.loc[rng.random(n) < 0.12, 'nota_mate'] = np.nan
    out.loc[rng.random(n) < np.where(df['absente'] > 8, 0.35, 0.12), 'nota_info'] = np.nan
    return out


SETURI = [(concurs, adevar), (sterge(baza_completa, 5), baza_completa), (sterge(baza_completa, 6), baza_completa)]
SCORURI = []


def nrmse(imputat, adevar, lipsa):
    masca = lipsa.isna()
    coloane = [c for c in lipsa.columns if masca[c].any()]
    total = 0
    for c in coloane:
        m = masca[c]
        total += np.sqrt(((imputat.loc[m, c] - adevar.loc[m, c]) ** 2).mean()) / adevar[c].std()
    return total / len(coloane)


def _evalueaza(i):
    lipsa, adevar = SETURI[i]
    iesire = imputeaza(lipsa.copy())
    if not isinstance(iesire, pd.DataFrame) or list(iesire.columns) != list(lipsa.columns) or len(iesire) != len(lipsa):
        return False
    coloane = [c for c in lipsa.columns if lipsa[c].isna().any()]
    if iesire[coloane].isna().any().any():
        return False
    for c in coloane:                                           # valorile cunoscute nu se schimba
        cunoscut = lipsa[c].notna()
        if not np.allclose(iesire.loc[cunoscut, c].astype(float), lipsa.loc[cunoscut, c]):
            return False
    baza = nrmse(lipsa.fillna(lipsa.mean()), adevar, lipsa)
    al_tau = nrmse(iesire, adevar, lipsa)
    SCORURI.append((baza, al_tau))
    return bool(al_tau <= 0.97 * baza)


verifica('imputare concurs', _evalueaza, [((0,), True)], ascunse=[((1,), True), ((2,), True)], puncte=4,
         indiciu='foloseste si celelalte coloane (nota_mate si nota_info merg impreuna), nu doar media')
if SCORURI:
    print(f'pe tabelul vizibil: RMSE normalizat = {SCORURI[0][1]:.3f} | completare cu media = {SCORURI[0][0]:.3f} | prag = {0.97 * SCORURI[0][0]:.3f}')
""")

    # 11 provocare
    c.md("""
### 11. Provocare: regresie liniara "de mana" ca imputare (3 puncte)

Cand doua coloane merg impreuna (`nota_mate` si `nota_info`), o dreapta `y = a * x + b` prinsa prin punctele cunoscute prezice golurile mult mai bine decat media. `imputare_regresie(x, y)` primeste doua array-uri NumPy de aceeasi lungime: `x` complet, `y` cu `NaN` in unele pozitii. Intoarce `y` cu golurile completate cu `a * x + b`, unde dreapta e ajustata **doar pe perechile in care `y` e cunoscut**, prin formulele metodei celor mai mici patrate:

`a = suma((x - mx) * (y - my)) / suma((x - mx)^2)`, `b = my - a * mx`

(`mx`, `my` = mediile calculate pe perechile cunoscute). Fara `np.polyfit`. Valorile cunoscute raman neschimbate.
""")
    c.ex("""
def imputare_regresie(x, y):
    pass  # TODO
""", """
def imputare_regresie(x, y):
    cunoscut = ~np.isnan(y)
    xc, yc = x[cunoscut], y[cunoscut]
    mx, my = xc.mean(), yc.mean()
    a = ((xc - mx) * (yc - my)).sum() / ((xc - mx) ** 2).sum()
    b = my - a * mx
    rez = y.copy()
    rez[~cunoscut] = a * x[~cunoscut] + b
    return rez
""")
    c.cod("""
import random


def ref_regresie(x, y):
    cunoscut = ~np.isnan(y)
    a, b = np.polyfit(x[cunoscut], y[cunoscut], 1)
    rez = y.copy()
    rez[~cunoscut] = a * x[~cunoscut] + b
    return rez


def gen_reg():
    n = random.randint(5, 25)
    x = np.array([random.uniform(0, 10) for _ in range(n)])
    y = 2 * x + 1 + np.array([random.gauss(0, 1) for _ in range(n)])
    y[random.sample(range(n), random.randint(1, n // 3))] = np.nan
    return x, y


verifica('imputare_regresie', imputare_regresie,
         [((np.array([1.0, 2.0, 3.0, 4.0]), np.array([3.0, 5.0, np.nan, 9.0])), np.array([3.0, 5.0, 7.0, 9.0]))],
         referinta=ref_regresie, generator=gen_reg, puncte=3,
         indiciu='intai pastrezi doar perechile unde y nu e NaN, apoi mx, my, a, b')
scor()
""")
    c.salveaza('11-valori-lipsa-tema')


if __name__ == '__main__':
    predare()
    tema()
