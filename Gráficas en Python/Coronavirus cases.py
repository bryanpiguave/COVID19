# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 21:30:22 2020

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
#df_corona = df_corona.head(10)


#Create a plain world map
world_map=folium.Map(zoom_start=2,tiles='Mapbox Bright')
world_geo = r'world_countries.json'
file=open('world_countries.json')
data =json.load(file)
file.close()
pais_json = []
for i in range(len(data['features'])):
    pais_json.append(data['features'][i]['properties']['name'])
threshold_scale = np.linspace(df_corona['104'].min(),df_corona['104'].max(), num=10, dtype=int)
threshold_scale = threshold_scale.tolist() 
threshold_scale[-1] = threshold_scale[-1] + 10 


bins = list(df_corona['104'].quantile([0, 0.25, 0.5, 0.75, 1]))

folium.Choropleth(
    geo_data=world_geo,
    data=df_corona,
    columns=['Countries','104'],
    key_on='feature.properties.name',
    threshold_scale = threshold_scale,
    fill_color='YlGnBu', 
    fill_opacity=0.9, 
    line_opacity=0.4,
    line_weight=0.7,
    nan_fill_color='white',
    bins=bins,
    legend_name='Coronavirus cases',
    reset=True
).add_to(world_map)

world_map.save('Coronavirus.html')

unicos = pd.unique(pais_json + list(df_corona['Countries'])).tolist()
unicos.sort()




