"""Genereaza seturile pentru topicul 11 (valori lipsa). Deterministe, seed fix.

    python date_11_valori_lipsa.py

date/11_elevi_complet.csv   300 elevi (cu tinta `calificat`), NICIO valoare lipsa (adevarul cunoscut; elevii mascheaza singuri, cu masca lor)
date/11_concurs_lipsa.csv   200 elevi, cu valori sterse (mecanism MAR) la ore_studiu, nota_mate, nota_info
date/11_concurs_adevar.csv  aceiasi 200 de elevi, complet (folosit doar de celula de verificare din tema)

Structura (aceeasi la ambele): ore_studiu creste cu clasa, nota_mate si nota_info depind de un "talent" ascuns
(deci sunt corelate intre ele) si de ore_studiu. Asa strategiile de imputare au rezultate diferite.
"""
import os

import numpy as np
import pandas as pd

AICI = os.path.dirname(os.path.abspath(__file__))
DATE = os.path.normpath(os.path.join(AICI, '..', 'date'))


def complet(rng, n, cu_meditatii=True):
    clasa = rng.integers(9, 13, n)
    ore = np.clip(rng.gamma(4.0, 0.9 + 0.3 * (clasa - 9)), 0.5, 30).round(1)
    absente = np.clip(rng.poisson(6, n), 0, 40)
    talent = rng.normal(0, 1, n)
    nota_mate = np.clip(5.6 + 0.9 * talent + 0.05 * ore - 0.02 * absente + rng.normal(0, 0.5, n), 1, 10).round(2)
    nota_info = np.clip(5.2 + 0.9 * talent + 0.14 * ore - 0.03 * absente + rng.normal(0, 0.5, n), 1, 10).round(2)
    df = pd.DataFrame({'clasa': clasa, 'ore_studiu': ore, 'absente': absente, 'nota_mate': nota_mate,
                       'nota_info': nota_info})
    if cu_meditatii:
        df['meditatii'] = np.where(rng.random(n) < 0.35, 'da', 'nu')
    z = 1.6 * (nota_info - 5.7) + 0.25 * (ore - 5.2) - 0.05 * (absente - 6)
    df['calificat'] = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)
    df.insert(0, 'id', np.arange(1, n + 1))
    return df


def masca_concurs(df, rng):
    """Mecanism MAR: la clasa 12 lipsesc mai des orele, iar notele lipsesc mai des la cei cu multe absente."""
    n = len(df)
    out = df.copy()
    p_ore = np.where(df['clasa'] == 12, 0.35, 0.10)
    p_info = np.where(df['absente'] > 8, 0.35, 0.12)
    out.loc[rng.random(n) < p_ore, 'ore_studiu'] = np.nan
    out.loc[rng.random(n) < 0.12, 'nota_mate'] = np.nan
    out.loc[rng.random(n) < p_info, 'nota_info'] = np.nan
    return out


def main():
    os.makedirs(DATE, exist_ok=True)
    complet(np.random.default_rng(1101), 300).to_csv(os.path.join(DATE, '11_elevi_complet.csv'), index=False)
    adevar = complet(np.random.default_rng(1102), 200, cu_meditatii=False).drop(columns='calificat')
    lipsa = masca_concurs(adevar, np.random.default_rng(1103))
    lipsa.to_csv(os.path.join(DATE, '11_concurs_lipsa.csv'), index=False)
    adevar.to_csv(os.path.join(DATE, '11_concurs_adevar.csv'), index=False)
    for f in ('11_elevi_complet.csv', '11_concurs_lipsa.csv', '11_concurs_adevar.csv'):
        d = pd.read_csv(os.path.join(DATE, f))
        print(f, d.shape, 'lipsa:', {k: int(v) for k, v in d.isna().sum().items() if v})


if __name__ == '__main__':
    main()
