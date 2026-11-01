"""Genereaza date/10_magazin.csv (set murdar pentru sarcina "detectiv" din tema de EDA). Seed fix.

    python date_10_eda.py

Probleme plantate intentionat (le gasesc elevii, nu le repara in fisier):
  - 3 randuri duplicate exact
  - oras scris inconsistent ('Cluj', 'cluj', 'CLUJ ', 'Bucuresti ', ...)
  - 2 preturi negative, un discount de 250 (procent), o cantitate de 5000
  - rating numeric, dar cu textul 'fara nota' la 7 randuri (coloana ajunge de tip text)
  - coloana `tara` constanta (nu spune nimic)
  - ~5% valori lipsa la discount_pct
"""
import os

import numpy as np
import pandas as pd

AICI = os.path.dirname(os.path.abspath(__file__))
DATE = os.path.normpath(os.path.join(AICI, '..', 'date'))


def magazin(rng):
    n = 200
    oras = rng.choice(['Bucuresti', 'Cluj', 'Iasi', 'Brasov'], n, p=[0.4, 0.25, 0.2, 0.15]).astype(object)
    produs = rng.choice(['pix', 'caiet', 'rucsac', 'casti'], n, p=[0.35, 0.35, 0.15, 0.15])
    baza = pd.Series(produs).map({'pix': 3.0, 'caiet': 8.0, 'rucsac': 120.0, 'casti': 250.0}).to_numpy()
    cantitate = np.where(np.isin(produs, ['pix', 'caiet']), rng.integers(1, 21, n), rng.integers(1, 4, n))
    pret = (baza * rng.lognormal(0, 0.08, n)).round(1)
    discount = rng.choice([0, 0, 0, 5, 10, 15, 20, 30], n).astype(float)
    rating = rng.choice([1, 2, 3, 4, 5], n, p=[0.05, 0.1, 0.2, 0.35, 0.3]).astype(object)
    df = pd.DataFrame({'id_comanda': np.arange(1, n + 1), 'oras': oras, 'produs': produs, 'cantitate': cantitate,
                       'pret_unitar': pret, 'discount_pct': discount, 'rating': rating, 'tara': 'RO'})
    df.loc[[20, 77], 'pret_unitar'] = [-25.0, -3.5]
    df.loc[140, 'discount_pct'] = 250.0
    df.loc[33, 'cantitate'] = 5000
    df.loc[[5, 40, 65, 90, 120, 150, 185], 'rating'] = 'fara nota'
    df.loc[[8, 60, 130, 44], 'oras'] = ['cluj', 'CLUJ ', 'Bucuresti ', 'Cluj']
    df.loc[[150, 151], 'oras'] = 'Cluj'
    df.loc[rng.random(n) < 0.05, 'discount_pct'] = np.nan
    dup = df.sample(3, random_state=5)
    return pd.concat([df, dup], ignore_index=True)


def main():
    os.makedirs(DATE, exist_ok=True)
    df = magazin(np.random.default_rng(310))
    df.to_csv(os.path.join(DATE, '10_magazin.csv'), index=False)
    d = pd.read_csv(os.path.join(DATE, '10_magazin.csv'))
    print(d.shape, d.dtypes.to_dict())
    print('duplicate', d.duplicated().sum(), 'lipsa', d.isna().sum().to_dict())


if __name__ == '__main__':
    main()
