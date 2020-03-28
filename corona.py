# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 10:59:08 2020

@author: Bryan Piguave
"""

import pandas as pd
path=r'C:\Users\usuario\Dropbox\PythonEnhanced\COVID19\corona.csv'
df = pd.read_csv(path,sep=';')

Headers =df.columns
df_1 =df[['nombre_pro Mbvincia','casos_confirmados']]
df_grp = df_1.groupby(['nombre_pro Mbvincia'], as_index=False).max()

