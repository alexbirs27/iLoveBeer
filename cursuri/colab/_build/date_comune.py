"""Genereaza seturile de date comune (deterministe, seed fix): date/elevi.csv si date/case.csv.

    python date_comune.py

Probleme plantate INTENTIONAT (le gasesc elevii la EDA / valori lipsa; nu le rezolva aici):

elevi.csv (aprox. 245 randuri)
  - ~8% lipsa la nota_info, ~10% la ore_studiu (mai des la clasa a 12-a: lipsa NU e complet aleatoare), ~5% la meditatii
  - absente: doua valori extreme (87 si 120)
  - varsta: o valoare imposibila (150) si una (2)
  - meditatii scris inconsistent: 'da', 'nu', 'Da', 'DA ', ' nu'
  - 5 randuri duplicate exact
  - calificat (0/1) = a trecut mai departe, depinde de nota_info, ore_studiu si absente

case.csv (300 randuri)
  - pret_eur are ordine de marime 10^5, suprafata_mp 10^1-10^2, camere 1-5: scari foarte diferite (pentru normalizare/scalare)
  - 3 preturi extreme; ~12% lipsa la an_constructie, ~6% la etaj
"""
import os

import numpy as np
import pandas as pd

AICI = os.path.dirname(os.path.abspath(__file__))
DATE = os.path.normpath(os.path.join(AICI, '..', 'date'))


def elevi(rng):
    n = 240
    clasa = rng.integers(9, 13, n)
    ore = np.clip(rng.gamma(4.0, 1.6, n), 0, 30).round(1)
    absente = np.clip(rng.poisson(6, n), 0, 40)
    talent = rng.normal(0, 1, n)
    nota_info = np.clip(5.2 + 0.9 * talent + 0.12 * ore - 0.03 * absente + rng.normal(0, 0.6, n), 1, 10).round(2)
    nota_mate = np.clip(5.5 + 0.7 * talent + 0.08 * ore - 0.02 * absente + rng.normal(0, 0.9, n), 1, 10).round(2)
    varsta = clasa + 5 + rng.integers(0, 2, n) + (rng.random(n) < 0.05)
    meditatii = np.where(rng.random(n) < 0.35, 'da', 'nu').astype(object)
    z = -6.2 + 0.9 * nota_info + 0.12 * ore - 0.06 * absente
    calificat = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)
    df = pd.DataFrame({'id': np.arange(1, n + 1), 'clasa': clasa, 'nota_mate': nota_mate, 'nota_info': nota_info,
                       'ore_studiu': ore, 'absente': absente, 'varsta': varsta, 'meditatii': meditatii,
                       'calificat': calificat})
    # probleme plantate
    df.loc[[17, 130], 'absente'] = [87, 120]
    df.loc[[42, 200], 'varsta'] = [150, 2]
    df.loc[[3, 55, 91, 160], 'meditatii'] = ['Da', 'DA ', ' nu', 'Da']
    lipsa_info = rng.random(n) < 0.08
    p_ore = np.where(df['clasa'] == 12, 0.22, 0.05)
    lipsa_ore = rng.random(n) < p_ore
    lipsa_med = rng.random(n) < 0.05
    df.loc[lipsa_info, 'nota_info'] = np.nan
    df.loc[lipsa_ore, 'ore_studiu'] = np.nan
    df.loc[lipsa_med, 'meditatii'] = np.nan
    dup = df.sample(5, random_state=3)
    return pd.concat([df, dup], ignore_index=True)


def case(rng):
    n = 300
    oras = rng.choice(['Bucuresti', 'Cluj', 'Iasi', 'Timisoara'], n, p=[0.4, 0.25, 0.2, 0.15])
    factor = pd.Series(oras).map({'Bucuresti': 1.0, 'Cluj': 1.05, 'Iasi': 0.8, 'Timisoara': 0.85}).to_numpy()
    mp = np.clip(rng.lognormal(4.2, 0.4, n), 25, 220).round(0)
    camere = np.clip((mp / 28 + rng.normal(0, 0.6, n)).round(), 1, 6).astype(int)
    etaj = rng.integers(0, 11, n).astype(float)
    an = rng.integers(1950, 2024, n).astype(float)
    dist = np.clip(rng.gamma(2.0, 2.2, n), 0.3, 25).round(1)
    pret = (1250 * mp * factor * (1 - 0.018 * dist) * (1 + (an - 1950) / 400) + rng.normal(0, 9000, n)).round(-2)
    df = pd.DataFrame({'suprafata_mp': mp, 'camere': camere, 'etaj': etaj, 'an_constructie': an,
                       'distanta_centru_km': dist, 'oras': oras, 'pret_eur': pret})
    df.loc[[11, 120, 250], 'pret_eur'] = [1450000, 1900000, 2600000]
    df.loc[rng.random(n) < 0.12, 'an_constructie'] = np.nan
    df.loc[rng.random(n) < 0.06, 'etaj'] = np.nan
    return df


def main():
    os.makedirs(DATE, exist_ok=True)
    elevi(np.random.default_rng(2026)).to_csv(os.path.join(DATE, 'elevi.csv'), index=False)
    case(np.random.default_rng(7)).to_csv(os.path.join(DATE, 'case.csv'), index=False)
    for f in ('elevi.csv', 'case.csv'):
        d = pd.read_csv(os.path.join(DATE, f))
        print(f, d.shape, 'lipsa:', dict(d.isna().sum()[d.isna().sum() > 0]))


if __name__ == '__main__':
    main()
