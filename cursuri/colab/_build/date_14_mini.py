"""Genereaza datele pentru mini-olimpiada (14): imparte date/elevi.csv in train / test, deterministic.

    python date_14_mini.py

- date/14_train.csv          elevi.csv fara elevii de test (cu problemele plantate: lipsuri, duplicate, valori imposibile)
- date/14_test.csv           elevii de test, FARA coloana calificat (aceleasi probleme; nu ai voie sa-i elimini)
- date/14_test_etichete.csv  id, calificat: folosit doar de functia de scor
"""
import os

import numpy as np
import pandas as pd

AICI = os.path.dirname(os.path.abspath(__file__))
DATE = os.path.normpath(os.path.join(AICI, '..', 'date'))
SEED = 29
N_TEST = 80


def main():
    full = pd.read_csv(os.path.join(DATE, 'elevi.csv'))
    ids = full['id'].unique()
    test_ids = np.random.default_rng(SEED).choice(ids, N_TEST, replace=False)
    in_test = full['id'].isin(test_ids)
    train = full[~in_test]
    test = full[in_test].drop_duplicates()
    train.to_csv(os.path.join(DATE, '14_train.csv'), index=False)
    test.drop(columns='calificat').to_csv(os.path.join(DATE, '14_test.csv'), index=False)
    test[['id', 'calificat']].to_csv(os.path.join(DATE, '14_test_etichete.csv'), index=False)
    print('train', train.shape, 'test', test.shape, 'rata de 1 in test:', round(test['calificat'].mean(), 3))


if __name__ == '__main__':
    main()
