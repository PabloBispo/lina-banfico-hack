#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 13:57:26 2020

@author: bispo
"""

import pandas as pd
from datetime import datetime
from sklearn import preprocessing
from random import randint

months = {
   "jan":1,
   "fev":2,
   "mar":3,
   "abr":4,
   "mai":5,
   "jun":6,
   "jul":7,
   "ago":8,
   "set":9,
   "out":10,
   "nov":11,
   "dez":12
}


x_columns = [
    'valor_aplicado',
    'dias_aplicado',
    'class_risco',
    'rentabilidade_ano',
    'pior_mes',
    'meses_negativos',
    'id_user'
    ]


def format_date(args):  
    str_date = str(args)
    d, m, y, _h = str_date.split('/')
    H, M = _h.split(":")
    m_number = months[m]
    date = datetime.strptime(f'{d}/{m_number}/{y}/{H}:{M}', '%d/%m/%Y/%H:%M')    
    return date
    

def format_percents(args):
    str_val = str(args).replace(",", '.')
    return float(str_val)


def process_df(df, has_data=True, x_columns=x_columns):
    df = df.fillna(0)
    df.rentabilidade_ano= df.rentabilidade_ano.apply(format_percents)
    df.pior_mes = df.pior_mes.apply(format_percents)
    if has_data:
        df.data_resgate = df.data_resgate.apply(format_date)
        df.data_aplicacao = df.data_aplicacao.apply(format_date)
    
    return pd.get_dummies(df[x_columns])



def generate_users(df, n=10, n_invest = 10):
    temp_df = pd.DataFrame()
    for _ in range(n):
        _id = randint(1, n * 10)
        sample = df.sample(n_invest)
        sample["id_user"] = _id
        temp_df = temp_df.append(sample)
        
    return temp_df    
        

founds_df = pd.get_dummies(
    process_df(
        pd.read_csv('found_data.csv'),
        has_data=False,
        x_columns = [
            'valor_aplicado',
            'dias_aplicado',
            'class_risco',
            'rentabilidade_ano',
            'pior_mes',
            'meses_negativos'
            ]
        )
    )

mode = founds_df.dias_aplicado.mode()[0]

founds_df.dias_aplicado = founds_df.dias_aplicado.replace(0, mode)

sample = generate_users(founds_df, n=2)

df = pd.get_dummies(process_df(pd.read_csv('investment_data.csv'), has_data=False))

df = df.append(sample)
df.reset_index(inplace=True)




X = df.drop(['id_user', 'index'], axis=1)
y = df[['id_user']]


from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.tree import export_graphviz
from sklearn import tree
import matplotlib.pyplot as plt


clf = RandomForestClassifier(n_estimators=10)

cross_val_score(clf, X, y, cv=10)

clf.fit(X,y)

clf.predict(founds_df.head(10))


t_n = 1
fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=800)
tree.plot_tree(clf.estimators_[t_n],
               filled = True);
fig.savefig(f'tree_{t_n}.png')

