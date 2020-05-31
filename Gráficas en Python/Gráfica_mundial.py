# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 09:33:24 2020

@author: Bryan Piguave
"""
import pandas as pd
import numpy as np
import folium
import json

#Get data from url
url='https://covid.ourworldindata.org/data/ecdc/total_cases.csv'
df_cor=pd.read_csv(url)
df_corona=df_cor.transpose()
df_corona.columns = list(map(str, df_corona.columns))
df_corona.index   = list(map(str, df_corona.index))
df_corona.drop(labels=['date','World'],inplace=True)
df_corona['Countries']=list(df_corona.index)
df_corona.index=range(len(df_corona))
df_corona = df_corona.replace('United States','United States of America')
df_corona = df_corona.replace('Democratic Republic of Congo','Democratic Republic of the Congo')
df_corona.dropna(subset=["104"],axis=0,inplace=True)
df_corona['104'].astype(int)
df_corona = df_corona.sort_values(['104'],ascending=False)


#Create a plain world map
world_map = folium.Map(location=[0, 0], zoom_start=2, tiles='Mapbox Bright')
df_corona['log']=np.log10(df_corona['104'])

threshold_scale = np.linspace(df_corona['log'].min(),df_corona['log'].max(), num=6, dtype=int)
threshold_scale = threshold_scale.tolist() 
threshold_scale[-1] = threshold_scale[-1]*1.3 
bins = list(df_corona['log'].quantile([0, 0.25, 0.5, 0.75, 1]))

world_geo = r'world_countries.json'

folium.Choropleth(
    geo_data=world_geo,
    data=df_corona,
    columns=['Countries','log'],
    key_on='feature.properties.name',
    fill_color='YlGnBu', 
    fill_opacity=0.8, 
    line_opacity=0.3,
    threshold_scale =threshold_scale,
    line_weight=0.7,
    nan_fill_color='white',
    bins=bins,
    legend_name='Coronavirus cases (log_10 Scale)',
    reset=True
).add_to(world_map)

world_map.save('Coronavirus_new.html')







