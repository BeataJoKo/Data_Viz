# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 14:35:44 2024

@author: BeButton
"""

#%%
import math
import numpy as np 
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

#%%
def kommune_agg(df, column_name, mun):
    kommune = list(mun['label_dk'].unique())
    df_agg = []
    
    for k in kommune:
        if k in list(df['Kommune']):
            #rows = len(df[df['Kommune'] == k])
            visit = sum(df[df['Kommune'] == k][column_name])
            #visit = round(visit / 10000)
            codes = list(df[df['Kommune'] == k]['ZipCode'].unique())
            codes = [str(round(x)) for x in codes]
            codes = (', ').join(codes)
            loc = df[df['Kommune'] == k]['GeoCode'].values[0]
            df_agg.append(('0'+str(loc), k, visit, codes))
        else:
            loc = mun[mun['label_dk'] == k]['lau_1'].values[0]
            df_agg.append(('0'+str(loc), k, 0, ''))            
            
    df_agg = pd.DataFrame(df_agg, columns=['Location', 'Kommune', 'VisitCount', 'ZipCode'])
    df_agg = df_agg.reset_index(drop=True)
    #df_agg['VisitCount'] = df_agg['VisitCount'].astype('int')
    df_agg['VisitCount'] = [round(num) for num in df_agg['VisitCount']]
    
    return df_agg 

#%%
#dd = kommune_agg(df_visit, 'Visit_Exhibition', dt_mun)

#%%
def quantile_lim(df, column_name):
    dd = list(df[column_name].quantile([0.0, 0.2, 0.4, 0.6, 0.8, 1]))
    lim = [(round(dd[i-1]), round(dd[i])-1) if i < len(dd)-1 else (round(dd[i-1]), math.ceil(dd[i])) for i in range(1, len(dd))]
    return lim

#%%
#dd = quantile_lim(df_visit, 'Visit_Exhibition')

#%%
def name_agg(df, cloumn_name, year_range):
    dd = df.loc[(df['Year'] >= min(year_range)) & (df['Year'] <= max(year_range))]
    dd = dd.groupby(['Name', 'Category', 'lat', 'lon', 'Kommune'])[['Visit_Exhibition', 'Visit_Place', 'Opening_Time']].sum().reset_index()
    scaler = MinMaxScaler(feature_range=(3,50))
    dd['scale'] = scaler.fit_transform(dd[cloumn_name].values.reshape(-1, 1))
    dd['scale'] = [math.ceil(x) for x in dd['scale']]
    return dd
        
#%%   
#dd = name_agg(df_visit, 'Visit_Exhibition', [2018, 2023])

#%%
def year_agg(df, year_range):
    #dd = df.loc[(df['Year'] >= min(year_range)) & (df['Year'] <= max(year_range))]
    dd = df.groupby(['Year'])[['Visit_Exhibition', 'Visit_Place', 'Opening_Time','Visitors_Exhibition_per_opening_hour']].sum().reset_index()
    mintime = min(year_range)
    maxtime = max(year_range)
    time = list(dd['Year'].unique())
    time.sort()
    color = [0.9 if (year >= mintime) & (year <= maxtime) else 0.3 for year in time]
    return dd, color

#%%
#dd = year_agg(df_visit, [2018, 2021])

#%%
def reshape_cat(df, sex):
    dd = df[df['Sex'] == sex].drop(['Sex'], axis=1)
    dd = dd.pivot(index=['Year', 'Age'], columns=['Category']).reset_index()
    idx = [dd.columns.get_level_values(0)[i]+dd.columns.get_level_values(1)[i] for i in range(len(dd.columns))]
    dd.columns = [i.replace('Percent_', '') for i in idx]
    dd = round(dd.groupby(['Age'])[['Kunstmuseum', 'Kulturhistorisk museum', 'Naturhistorisk museum', 'Blandet', 'Museumslignende institution']].mean().reset_index(), 1)
    dd = pd.concat([dd.iloc[1:], dd.iloc[:1]])
    return dd

def gender_data(df, year_range):
    df = pd.melt(df, id_vars=['Age','Sex', 'Category'], var_name='Year', value_name='Percent_', ignore_index=True) 
    man = reshape_cat(df, 'Men')
    woman = reshape_cat(df, 'Women')     
    return man, woman

#%%
#dd, ddd = gender_data(df_cat, [2018, 2021])
#dd = pd.concat([dd, ddd.iloc[:, 1:]], axis=1)

#%%
def corona_data(df):
    dd = df.loc[:, ['Name', 'Category', 'Year', 'Visit_Exhibition']]
    dd = dd.pivot(index=['Name', 'Category'], columns=['Year']).reset_index()
    idx = [dd.columns.get_level_values(0)[i]+'_'+str(dd.columns.get_level_values(1)[i]) for i in range(len(dd.columns))]
    dd.columns = idx
    dd = dd.fillna(0)
    data = dd[['Name_', 'Category_']]
    data['Before Covid-19'] = dd['Visit_Exhibition_2018'] + dd['Visit_Exhibition_2019']
    data['During Covid-19'] = dd['Visit_Exhibition_2020'] + dd['Visit_Exhibition_2021']
    data['After Covid-19'] = dd['Visit_Exhibition_2022'] + dd['Visit_Exhibition_2023']
    data['Before Covid-19'] = data['Before Covid-19'].astype('int')
    data['During Covid-19'] = data['During Covid-19'].astype('int')
    data['After Covid-19'] = data['After Covid-19'].astype('int')
    data.columns = ['Name', 'Category','Before Covid-19', 'During Covid-19', 'After Covid-19']
    scaler = MinMaxScaler(feature_range=(3, 30))
    data['scale'] = scaler.fit_transform(data[['Before Covid-19', 'During Covid-19', 'After Covid-19']].mean(axis=1).values.reshape(-1,1))
    data['scale'] = [math.ceil(x) for x in data['scale']]

    return data


#%%
#dd = corona_data(df_visit)

#%%
# https://plotly.com/blog/sankey-diagrams/

def teaching_data(df: pd.DataFrame, columns: list, sankey_link_weight: str):

    # list of list: each list are the set of nodes in each tier/column
    column_values = [df[col] for col in columns]

    # this generates the labels for the sankey by taking all the unique values
    labels = sum([list(node_values.unique()) for node_values in column_values],[])

    # initializes a dict of dicts (one dict per tier) 
    link_mappings = {col: {} for col in columns}

    # each dict maps a node to unique number value (same node in different tiers
    # will have different nubmer values
    i = 0
    for col, nodes in zip(columns, column_values):
        for node in nodes.unique():
            link_mappings[col][node] = i
            i = i + 1

    # specifying which coluns are serving as sources and which as sources
    # ie: given 3 df columns (col1 is a source to col2, col2 is target to col1 and 
    # a source to col 3 and col3 is a target to col2
    source_nodes = column_values[: len(columns) - 1]
    target_nodes = column_values[1:]
    source_cols = columns[: len(columns) - 1]
    target_cols = columns[1:]
    links = []

    # loop to create a list of links in the format [((src,tgt),wt),(),()...]
    for source, target, source_col, target_col in zip(source_nodes, target_nodes, source_cols, target_cols):
        for val1, val2, link_weight in zip(source, target, df[sankey_link_weight]):
            links.append(
                (
                    (
                        link_mappings[source_col][val1],
                        link_mappings[target_col][val2]
       ),
       link_weight,
    )
             )

    # creating a dataframe with 2 columns: for the links (src, tgt) and weights
    df_links = pd.DataFrame(links, columns=["link", "weight"])

    # aggregating the same links into a single link (by weight)
    df_links = df_links.groupby(by=["link"], as_index=False).agg({"weight": sum})

    # generating three lists needed for the sankey visual
    sources = [val[0] for val in df_links["link"]]
    targets = [val[1] for val in df_links["link"]]
    weights = [round(x) for x in list(df_links["weight"])]

    return labels, sources, targets, weights

#%%

#dd = teaching_data(df_teaching, ['Teaching', 'Category'], 'Amount')

#%%
#print(dd[2] + [1, 1])

#%%
#ddd = dd.loc[192]
#print(ddd)


