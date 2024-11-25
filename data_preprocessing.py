# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 08:21:06 2024

@author: BeButton
"""

#%%
import pandas as pd
import numpy as np

#%%

# Base data


#%%
df_18 = pd.read_excel('museer/2018.xlsx')
df_19 = pd.read_excel('museer/2019.xlsx')
df_20 = pd.read_excel('museer/2020.xlsx')
df_21 = pd.read_excel('museer/2021.xlsx')
df_22 = pd.read_excel('museer/2022.xlsx')
df_23 = pd.read_excel('museer/2023.xlsx')

#%%
print(df_22.columns)
print(df_23.columns)

#%%
data = [df_18, df_19, df_20, df_21, df_22, df_23]

#%%
for d in data:
    d.rename(
        columns={'Museumsnavn': 'Name', 
                 'Museumstype': 'Type', 
                 'Museumskategori': 'Category', 
                 'Besøgende, i udstillingen': 'Visit_Exhibition', 
                 'Udstilling': 'Visit_Exhibition', 
                 'Besøgende, Udstilling i alt': 'Visit_Exhibition', 
                 'Besøgende, på besøgsstedet': 'Visit_Place',
                 'Besøgssted': 'Visit_Place',
                 'Besøgende, Besøgssted': 'Visit_Place', 
                 'Antal åbningstimer': 'Opening_Time', 
                 'Åbningstimer': 'Opening_Time', 
                 'Børn og unge under 18 år, undervisning' : 'Under_18_NO_teaching', 
                 'Besøgende u. 18 år, ej undervisning': 'Under_18_NO_teaching', 
                 'Børn og unge under 18 år, ikke undervisning': 'Under_18_Teaching',
                 'Besøgende u. 18 år, undervisning': 'Under_18_Teaching', 
                 'Landsdel': 'Region',
                 'Museer og museums-afdelinger': 'Department',
                 'Museer og Besøgssteder': 'Department', 
                 'Udstillings-steder': 'Place',
                 'Hovedmuseum': 'Place', 
                 'Besøgende 18 år og derover, fuld pris': 'Under_18_Full_Price', 
                 'Besøgende 18 år og derover, reduceret pris (inkl. årskort)': 'Under_18_Reduced_Price',
                 'Besøgende 18 år og derover, gratis': 'Under_18_Gratis', 
                 'Antal arrangementer': 'Arrangements', 
                 'Deltagere til arrangementer i alt': 'Participate_Arrangement',
                 'Deltagere u. 18 år, ej undervisning': 'Under_18_Arrangement_NO_teaching',
                 'Deltagere u. 18 år, undervisning': 'Under_18_Arrangement_Teaching', 
                 'Deltagere, 18 år og derover eller uspecificeret': 'Over_18_Arrangement', 
                 'Antal online arrangementer (livestream)': 'Livestream',
                 'Deltagere til online arrangementer': 'Participate_Livestream', 
                 'Bemærkning': 'Remark', 
                 'Besøgende, uspecificeret': 'Visit_Unspecific'},
        inplace=True)
    
#%%
df_23['Year'] = 2023
df_22['Year'] = 2022
df_21['Year'] = 2021
df_20['Year'] = 2020
df_19['Year'] = 2019
df_18['Year'] = 2018

#%%
df_19.dropna(subset=['Visit_Exhibition', 'Visit_Place'], axis=0,  inplace=True)
df_20.dropna(subset=['Visit_Exhibition', 'Visit_Place'], axis=0,  inplace=True)
df_22.dropna(subset=['Visit_Exhibition', 'Visit_Place'], axis=0,  inplace=True)
df_23.dropna(subset=['Visit_Exhibition', 'Visit_Place'], axis=0,  inplace=True)
   
#%%
df = pd.concat([df_18, df_19, df_20, df_21, df_22, df_23], axis=0)

#%%
df.drop(['Remark', 'Column28'], axis=1,  inplace=True)

#%%
print(df.Name.unique())

#%%
print(df.Name.nunique())

#%%
print(df[['Name']].value_counts())

#%%
dd = df[['Name']].value_counts()
dd = pd.DataFrame(dd)
dd = dd.reset_index()

#%%
df.loc[df["Type"] == "Statsanerkendte i henhold til museumsloven", "Type"] = 'Statsanerkendt i henhold til museumsloven'
df.loc[df["Type"] == "Statsanderkendt i henhold til museumsloven", "Type"] = 'Statsanerkendt i henhold til museumsloven'
df.loc[df["Region"] == "Byen københavn", "Region"] = 'Byen København'
df.loc[df["Region"] == "København", "Region"] = 'Byen København'
df.loc[df["Department"] == "Museumsafdeling", "Department"] = 'Afdeling'
# df.loc[df["Department"] == "Besøgssted", "Department"] = 'Afdeling'
df.loc[df["Place"] == "De Kulturhistoriske Museer i Holstebro Kommune", "Place"] = 'De Kulturhistoriske Museer i Holstebro'
df.loc[df["Place"] == "Historie & Kunst", "Place"] = 'Kunst og Historie'
df['Place'] = df['Place'].str.replace('  ', ' ')
df['Place'] = df['Place'].str.title()

#%%
df['Name'] = df['Name'].str.strip()
df['Name'] = df['Name'].str.replace(',', '')
df['Name'] = df['Name'].str.replace('VIII"s', 'VIIIs')
df['Name'] = df['Name'].str.replace('  ', ' ')
df['Name'] = df['Name'].str.replace(' ¿ ', ' ')
df['Name'] = df['Name'].str.replace('Danmark Borgcenter', 'Danmarks Borgcenter')
df['Name'] = df['Name'].str.replace('J.F. ', 'J. F. ')
df['Name'] = df['Name'].str.title()
df['Name'] = df['Name'].str.replace(' Viiis ', ' VIIIs ')
df['Name'] = df['Name'].str.replace(' C/O ', ' c/o ')

#%%
df.loc[df["Name"] == "Carl Nielsen Barndomshjem", "Name"] = 'Carl Nielsens Barndomshjem'
df.loc[df["Name"] == "Den Gamle By Danmarks Købstadmuseum", "Name"] = 'Den Gamle By Danmarks Købstadsmuseum'
df.loc[df["Name"] == "Holmegaard Væk", "Name"] = 'Holmegaard Værk'
df.loc[df["Name"] == "Kunsten - Museum Of Modern Art Aalborg", "Name"] = 'Kunsten Museum Of Modern Art Aalborg'
df.loc[df["Name"] == "Kunstmuseet I Tønder/Kulturhistorie Tønder", "Name"] = 'Kunstmuseet I Tønder Kulturhistorie Tønder'
df.loc[df["Name"] == "Louisiana Museum For Moderne Kunst", "Name"] = 'Louisiana Museum Of Modern Art'
df.loc[df["Name"] == "Moesgaard Museum", "Name"] = 'Moesgård Museum'
df.loc[df["Name"] == "Ringkøbing- Skjern Museum", "Name"] = 'Ringkøbing-Skjern Museum'
df.loc[df["Name"] == "Vendsyssels Historiske Museum", "Name"] = 'Vendsyssel Historiske Museum'

df.loc[df["Name"] == "Kvindemuseet I Danmark", "Name"] = 'Køn'
df.loc[df["Name"] == "Museum Lolland Falster", "Name"] = 'Museum Obscurum Falsters Minder'
df.loc[df["Name"] == "Reventlow-Museet Pederstrup", "Name"] = 'Reventlow-Museet'
df.loc[df["Name"] == "Kulturmuseum Øst", "Name"] = 'Den Selvejende Institution Østsjællands Museum'
df.loc[df["Name"] == "Østsjællands Museum", "Name"] = 'Den Selvejende Institution Østsjællands Museum'
df.loc[df["Name"] == "Gram Lergrav - Palæontologi", "Name"] = 'Naturhistorie Og Palæontologi'
df.loc[df["Name"] == "Naturhistorie Og Palæontologi Gram Lergrav - Palæontologi", "Name"] = 'Naturhistorie Og Palæontologi'
df.loc[df["Name"] == "Museet På Koldinghus", "Name"] = 'Koldingshus'
df.loc[df["Name"] == "Panser Og Artillerimuseum", "Name"] = 'Varde Artillerimuseum'
df.loc[df["Name"] == "Krigsmuseet (Tidl.Tøjhusmuseet)", "Name"] = 'Tøjhusmuseet'
df.loc[df["Name"] == "Billund Museum", "Name"] = 'Mark Billund Kommunes Museer'
df.loc[df["Name"] == "Frederikssund Museum", "Name"] = 'Frederikssund Museum Færgegården'
df.loc[df["Name"] == "Museum Give", "Name"] = 'Give-Egnens Museum'
df.loc[df["Name"] == "Industrimuseet Frederiks Værk & Knud Rasmussens Hus", "Name"] = 'Industrimuseet Frederiks Værk'
df.loc[df["Name"] == "Museerne Helsingør", "Name"] = 'Helsingør Kommunes Museer'
df.loc[df["Name"] == "Skibshallerne", "Name"] = 'Det Gamle Hus/Skibshallerne'
df.loc[df["Name"] == "Museum Østjylland", "Name"] = 'Museum Østjylland Randers'
df.loc[df["Name"] == "Spøttrup Borg", "Name"] = 'Spøttrup Middelalderborg'
df.loc[df["Name"] == "Nordjyske Museer S/I", "Name"] = 'Nordjyllands Historiske Museum'
df.loc[df["Name"] == "Kystmuseet Skagen", "Name"] = 'Skagen By- Og Egnsmuseum'
df.loc[df["Name"] == "Skagens Kunstmuseer S/I", "Name"] = 'Skagens Kunstmuseer'
df.loc[df["Name"] == "Lützhøfs Købmandsgård Og Håndværksmuseum", "Name"] = 'Lützhøfs Købmandsgård'
#df.loc[df["Name"] == "Ringkøbing-Skjern Museum", "Name"] = 'Skjern Reberbane'
df.loc[df["Name"] == "Kystmuseet Bangsbo Fort", "Name"] = 'Bangsbomuseet'

#%%
dd = pd.DataFrame(df.groupby('Year')[['Name']].value_counts().reset_index(name='Counts'))

#%%
print(dd['Counts'].unique())

#%%

# Audience data


#%%
df_art_23 = pd.read_csv('museer/consumption_of_graphic_art_23.csv', sep=';', encoding="utf8")
df_art = pd.read_csv('museer/consumption_of_graphic_art.csv', sep=';', encoding="utf8")
df_type_23 = pd.read_csv('museer/visit_to_mus_type_23.csv', sep=';', encoding="utf8")
df_type = pd.read_csv('museer/visit_to_mus_type.csv', sep=';', encoding="utf8")
df_area_23 = pd.read_csv('museer/visit_to_ex_area_23.csv', sep=';', encoding="utf8")
df_area = pd.read_csv('museer/visit_to_ex_area.csv', sep=';', encoding="utf8")
df_purp_23 = pd.read_csv('museer/visit_to_ex_purpose_23.csv', sep=';', encoding="utf8")
df_purp = pd.read_csv('museer/visit_to_ex_purpose.csv', sep=';', encoding="utf8")

#%%
df_art.columns = ['Age', 'Sex', 'Category', 2018, 2019, 2020, 2021, 2022]
df_art_23.columns = ['var', 'Category', 'Q1', 'Q2', 'Q3', 'Q4']
df_type.columns = ['Age', 'Sex', 'Category', 2018, 2019, 2020, 2021, 2022]
df_type_23.columns = ['Category', 'var', 'Q1', 'Q2', 'Q3', 'Q4']
df_area.columns = ['Sex', 'Category', 'Age', 2018, 2019, 2020, 2021, 2022]
df_area_23.columns = ['Category', 'var', 'Q1', 'Q2', 'Q3', 'Q4']
df_purp.columns = ['Sex', 'Category', 'Age', 2018, 2019, 2020, 2021, 2022]
df_purp_23.columns = ['Category', 'var', 'Q1', 'Q2', 'Q3', 'Q4']

#%%
df_art.dropna(subset=[2018, 2019, 2020, 2021, 2022], axis=0,  inplace=True)
df_art_23.dropna(subset=['Q1', 'Q2', 'Q3', 'Q4'], axis=0,  inplace=True)
df_type.dropna(subset=[2018, 2019, 2020, 2021, 2022], axis=0,  inplace=True)
df_type_23.dropna(subset=['Q1', 'Q2', 'Q3', 'Q4'], axis=0,  inplace=True)
df_area.dropna(subset=[2018, 2019, 2020, 2021, 2022], axis=0,  inplace=True)
df_area_23.dropna(subset=['Q1', 'Q2', 'Q3', 'Q4'], axis=0,  inplace=True)
df_purp.dropna(subset=[2018, 2019, 2020, 2021, 2022], axis=0,  inplace=True)
df_purp_23.dropna(subset=['Q1', 'Q2', 'Q3', 'Q4'], axis=0,  inplace=True)

#%%
for d in [df_area, df_art, df_type, df_purp]:
    d['Age'] = d['Age'].str.replace(' years', '')
    d.loc[d["Age"] == "75 and over", "Age"] = '+75'
    
for d in [df_area_23, df_art_23, df_type_23, df_purp_23]:
    d['var'] = d['var'].str.replace(' years', '')
    d.loc[d["var"] == "75 and over", "var"] = '+75'
    
for d in [df_area, df_area_23]:
    d['Category'] = d['Category'].str.replace(r'[\(].*?[\)]', '', regex=True)
    d['Category'] = d['Category'].str.replace(' etc.', '')
    d['Category'] = d['Category'].str.replace(' e.g. during vacation', '')
    d['Category'] = d['Category'].str.strip()
    
for d in [df_art, df_art_23]:
    d.loc[d["Category"] == "Other types", "Category"] = 'Other'
    d.loc[d["Category"] == "I have not consumed graphic art within the last three months", "Category"] = 'None'
    d['Category'] = d['Category'].str.strip()
    
for d in [df_purp, df_purp_23]:
    d.loc[d["Category"] == "Other purpose", "Category"] = 'Other'
    d.loc[d["Category"] == "Cafe or restaurant visit", "Category"] = 'Cafe or restaurant'
    d['Category'] = d['Category'].str.strip()
    
for d in [df_type, df_type_23]:
    d.loc[d["Category"] == "Cultural history museum", "Category"] = 'Kulturhistorisk museum'
    d.loc[d["Category"] == "Art Museum", "Category"] = 'Kunstmuseum'
    d.loc[d["Category"] == "Natural history or science museum", "Category"] = 'Naturhistorisk museum'
    d.loc[d["Category"] == "Other types of museums", "Category"] = 'Museumslignende institution'
    d.loc[d["Category"] == "Visited a museum etc.", "Category"] = 'Yes'
    d.loc[d["Category"] == "Cultural heritage site or monument", "Category"] = 'Blandet'
    d.loc[d["Category"] == "Have not visited a museum", "Category"] = 'No'
    d['Category'] = d['Category'].str.strip()
    
#%%
for c in [2019, 2020, 2021, 2022]:
    df_type.loc[df_type[c] == "..", c] = 0
    df_type[c] = df_type[c].astype('int')
    
for c in ['Q1', 'Q2', 'Q3', 'Q4']:
    df_type_23.loc[df_type_23[c] == "..", c] = 0
    df_type_23[c] = df_type_23[c].astype('int')
    
#%%
cat = ['Concert', 'Lecture', 'Conference', 'Private event']
a = df_purp_23[df_purp_23['Category'] == cat[0]].reset_index()
b = df_purp_23[df_purp_23['Category'] == cat[1]].reset_index()
c = df_purp_23[df_purp_23['Category'] == cat[2]].reset_index()
d = df_purp_23[df_purp_23['Category'] == cat[3]].reset_index()
df_purp_23 = df_purp_23[~df_purp_23['Category'].isin(cat)].reset_index()

#%%
a.drop(['index'], axis=1, inplace=True)
b.drop(['index'], axis=1, inplace=True)
c.drop(['index'], axis=1, inplace=True)
d.drop(['index'], axis=1, inplace=True)
df_purp_23.drop(['index'], axis=1, inplace=True)

#%%
for q in ['Q1', 'Q2', 'Q3', 'Q4']:
    a[q] = a[q] + b[q]
    a['Category'] = 'Lecture or concert'

    c[q] = c[q] + d[q]
    c['Category'] = 'Conference or private event'

#%%
df_purp_23 = pd.concat([df_purp_23, a, c], axis=0)

#%%
for d in [df_art_23, df_area_23, df_purp_23, df_type_23]:
    d[2023] = d[['Q1', 'Q2', 'Q3', 'Q4']].mean(axis=1).round()
    d.drop(['Q1', 'Q2', 'Q3', 'Q4'], axis=1,  inplace=True)

#%%
def calculate_prop(data_set_23, data_set):
    m = data_set_23[data_set_23['var'] == 'Men'].reset_index()
    f = data_set_23[data_set_23['var'] == 'Women'].reset_index()
    t = data_set_23[~data_set_23['var'].isin(['Men','Women'])].reset_index()
    m.drop(['index'], axis=1, inplace=True)
    f.drop(['index'], axis=1, inplace=True)
    t.drop(['index'], axis=1, inplace=True)
    f['%'] = f[2023] / ((m[2023] + f[2023]) / 2)
    m['%'] = m[2023] / ((m[2023] + f[2023]) / 2)
    for c in t.Category.unique():
        t.loc[t["Category"] == c, "Women"] = round(t[2023] * f.loc[f['Category'] == c]['%'].values[0])
        t.loc[t["Category"] == c, "Men"] = round(t[2023] * m.loc[m['Category'] == c]['%'].values[0])
    t.rename(columns={'var': 'Age', 2023: 'Total'}, inplace=True)
    p = pd.melt(t, id_vars=['Age','Category'], value_vars=['Men', 'Women'], var_name='Sex', value_name=2023, ignore_index=True)
    p = pd.merge(data_set, p, how="left", on=['Age', 'Sex', 'Category'])
    return p

#%%
df_art = calculate_prop(df_art_23, df_art)
df_area = calculate_prop(df_area_23, df_area)
df_type = calculate_prop(df_type_23, df_type)
df_purp = calculate_prop(df_purp_23, df_purp)

#%%
df_type[2023] = df_type[2023].fillna(0)
df_purp[2023] = df_purp[2023].fillna(0)

#%%
df.to_csv('base_data_2018_2023.csv', index=False)
df_art.to_csv('graphic_art_2018_2023.csv', index=False, encoding='utf8')
df_area.to_csv('visit_area_2018_2023.csv', index=False, encoding='utf8')
df_type.to_csv('museum_category_2018_2023.csv', index=False, encoding='utf8')
df_purp.to_csv('visit_reason_2018_2023.csv', index=False, encoding='utf8')

#%%

# coordinates


#%%
import re
import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim
from thefuzz import process
from thefuzz import fuzz

#%%
ctx = ssl._create_unverified_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
locator = Nominatim(scheme='https', user_agent="Test", timeout=5)

#%%
count = pd.DataFrame(df[['Name']].value_counts().reset_index(name='Counts'))

#%%
empty = []
count['lat'] = ''
count['lon'] = ''
count['address'] = ''
count['country'] = ''
count['new_name'] = ''

#%%  Finding geocoordinates
for i, row in count.iterrows():
    try:
        city = row['Name']
        location = locator.geocode(city)
        if location.address.split(', ')[-1] == 'Danmark':
            count.loc[i, 'lat'] = location.latitude
            count.loc[i, 'lon'] = location.longitude
            count.loc[i, 'new_name'] = location.raw['name']
            count.loc[i, 'address'] = location.address
            count.loc[i, 'country'] = location.address.split(', ')[-1]
    except AttributeError:
        empty.append(city)

#%%
print(count['lat'].isna().sum())
print(count['lat'].eq('').sum())
print(count['address'].eq('').sum())
print(count['country'].unique())

#%%

#%%
count.loc[count["Name"] == "Museum Vestfyn", "address"] = 'Nordre Havnevej 19, 5610 Assens'
count.loc[count["Name"] == "Museum Vestfyn", "new_name"] = 'Museum Vestfyn - Toldboden'
count.loc[count["Name"] == "Museum Mors", "address"] = 'Dueholmgade 9, 7900 Nykøbing'
count.loc[count["Name"] == "Den Gamle By Danmarks Købstadsmuseum", "address"] = 'Viborgvej 2, 8000 Aarhus'
count.loc[count["Name"] == "Den Gamle By Danmarks Købstadsmuseum", "new_name"] = 'Den Gamle By'
count.loc[count["Name"] == "Koldingshus", "address"] = 'Koldinghus 1, 6000 Kolding'
count.loc[count["Name"] == "Randers Kunstmuseum", "address"] = 'Stemannsgade 2, 8900 Randers'
count.loc[count["Name"] == "Furesø Museer", "address"] = 'Stavnsholtvej 3, 3520 Farum'
count.loc[count["Name"] == "Svendborg Museum", "address"] = 'Grubbemøllevej 13, 5700 Svendborg'
count.loc[count["Name"] == "Svendborg Museum", "new_name"] = 'Danmarks Forsorgsmuseum'
count.loc[count["Name"] == "Rudersdal Museer", "address"] = 'Biblioteksalleen 5, 2850 Nærum'
count.loc[count["Name"] == "Museerne I Fredericia", "address"] = 'Jernbanegade 10, 7000 Fredericia'
count.loc[count["Name"] == "Prinsens Palais", "address"] = 'Ny Vestergade 10, 1471 København'
count.loc[count["Name"] == "Prinsens Palais", "new_name"] = 'Prinsens Palæ'
count.loc[count["Name"] == "Industrimuseet Frederiks Værk", "address"] = 'Torvet 1, 3300 Frederiksværk'
count.loc[count["Name"] == "Ribe Domkirkemuseum", "address"] = 'Torvet 19, 6760 Ribe'
count.loc[count["Name"] == "Ribe Domkirkemuseum", "new_name"] = 'Ribe Domkirke'
count.loc[count["Name"] == "Horsens Historiske Museum", "address"] = 'Sundvej 1A, 8700 Horsens'
count.loc[count["Name"] == "Jens Søndergårds Museum", "address"] = 'Transvej 4, 7620 Lemvig'
count.loc[count["Name"] == "Jens Søndergårds Museum", "new_name"] = 'Jens Søndergaards Museum'
count.loc[count["Name"] == "Hovedgården", "address"] = 'Hovedgårdsvej 7, 8600 Silkeborg'
count.loc[count["Name"] == "Papirmuseet Bikuben", "address"] = 'Papirfabrikken 78, 8600 Silkeborg'
count.loc[count["Name"] == "Papirmuseet Bikuben", "new_name"] = 'Papirmuseet'
count.loc[count["Name"] == "Museum Frello", "address"] = 'Kirkepladsen 1, 6800 Varde'
count.loc[count["Name"] == "Museet På Gl. Rye Mølle", "address"] = 'Møllestien 5, 8680 Ry'
count.loc[count["Name"] == "Naturama", "address"] = 'Dronningemaen 30, 5700 Svendborg'
count.loc[count["Name"] == "Landskabs- Og Landsbrugsmuseet Mosbjerg", "address"] = 'Jerupvej 613, Mosbjerg 9870 Sindal'
count.loc[count["Name"] == "Landbrugsmuseet På Melstedgård", "address"] = 'Melstedvej 25, 3760 Gudhjem'
count.loc[count["Name"] == "Landbrugsmuseet På Melstedgård", "new_name"] = 'Landbrugsmuseet Melstedgaard'
count.loc[count["Name"] == "Kunstmuseet I Tønder Kulturhistorie Tønder", "address"] = 'Wegners plads 1, 6270 Tønder'
count.loc[count["Name"] == "Kulturhistorisk Museum Rønne", "address"] = 'Sankt Mortens Gade 29, Rønne, Bornholm 3700 Danmark'
count.loc[count["Name"] == "Kulturhistorisk Museum Rønne", "new_name"] = 'Bornholms Museum'
count.loc[count["Name"] == "Rosenborgsamlingen", "address"] = 'Øster Voldgade 4A, 1350 København'
count.loc[count["Name"] == "Rosenborgsamlingen", "new_name"] = 'Rosenborg Slot'
count.loc[count["Name"] == "Varde Artillerimuseum", "address"] = 'Industrivej 18, 6840 Oksbøl'
count.loc[count["Name"] == "Varde Artillerimuseum", "new_name"] = 'Panser- & Artillerimuseum'
count.loc[count["Name"] == "Cathrineminde Teglværk", "address"] = 'Illerstrandvej 7, 6310 Broager'
count.loc[count["Name"] == "Cathrineminde Teglværk", "new_name"] = 'Cathrinesminde Teglværk'
count.loc[count["Name"] == "Cirkusmuseet Rold", "address"] = 'Østerled 1, 9510 Arden'
count.loc[count["Name"] == "Danmarks Rockmuseum", "address"] = 'Rabalderstræde 16, 4000 Roskilde'
count.loc[count["Name"] == "Danmarks Rockmuseum", "new_name"] = 'Ragnarock'
count.loc[count["Name"] == "Det Gamle Hus/Skibshallerne", "address"] = 'Gilleleje Hovedgade 49, 3250 Gilleleje'
count.loc[count["Name"] == "Det Gamle Hus/Skibshallerne", "new_name"] = 'Skibshallerne Og Det Gamle Hus'
count.loc[count["Name"] == "Det Gamle Rådhus I Ribe", "address"] = 'Von Støckens Plads 1, 6760 Ribe'
count.loc[count["Name"] == "E Bindstouw I Lysgård", "address"] = 'Blichersvej 40, 8800 Viborg'
count.loc[count["Name"] == "Ølgod Museum", "address"] = 'Vestergade 5, 6870 Ølgod'
count.loc[count["Name"] == "Ølgod Museum", "new_name"] = 'Dit Museum Ølgod'
count.loc[count["Name"] == "Amalienborg Museet Christian VIIIs Palæ", "address"] = 'Amalienborg Slotsplads 7, 1257 København'
count.loc[count["Name"] == "Amalienborg Museet Christian VIIIs Palæ", "new_name"] = 'Amalienborg'
count.loc[count["Name"] == "Apotekersamlingen Jens Bangs Stenhus", "address"] = 'Østerågade 9, 9000 Aalborg'
count.loc[count["Name"] == "Arkæologi Haderslev", "address"] = 'Dalgade 7, 6100 Haderslev'
count.loc[count["Name"] == "Æbelholt Kloster Museum", "address"] = 'Æbelholt 4, 3400 Hillerød'
count.loc[count["Name"] == "Blicheregnens Museum", "address"] = 'Blichersvej 30, 8620 Kjellerup'
count.loc[count["Name"] == "Vikingeborgentrelleborg", "address"] = 'Trelleborg Alle 4, 4200 Slagelse'
count.loc[count["Name"] == "Vikingeborgentrelleborg", "new_name"] = 'Vikingeborgen Trelleborg'
count.loc[count["Name"] == "Hjorths Fabrik Bornholms Keramikmuseum", "address"] = 'Krystalgade 5, 3700 Rønne'
count.loc[count["Name"] == "Spøttrup Middelalderborg", "address"] = 'Borgen 6a, 7860 Spøttrup'
count.loc[count["Name"] == "Helligåndshuset Næstved Museum", "address"] = 'Ringstedgade 4, 4700 Næstved'
count.loc[count["Name"] == "Slagelse Museum", "address"] = 'Bredegade 11A, 4200 Slagelse'
count.loc[count["Name"] == "Skjoldborgs Barndomshjem", "address"] = 'Skippergade 6, 7742 Vesløs'
count.loc[count["Name"] == "Skjoldborgs Barndomshjem", "new_name"] = 'Johan Skjoldborgs Hus'
count.loc[count["Name"] == "Hals Museum Hals Skanse", "address"] = 'Skansen 1, 9370 Hals'
count.loc[count["Name"] == "Hals Museum Hals Skanse", "new_name"] = 'Hals Museum og Skanse'
count.loc[count["Name"] == "Helsingør Kommunes Museer", "address"] = 'Allegade 2, 3000 Helsingør'
count.loc[count["Name"] == "Graabrødrekloster Museum", "address"] = 'Algade 19, 9000 Aalborg'
count.loc[count["Name"] == "Heltborg Museum Og Sydthy Kunst-Og Kulturcenter", "address"] = 'Skårhøjvej 15, 7760 Hurup Thy'
count.loc[count["Name"] == "Heltborg Museum Og Sydthy Kunst-Og Kulturcenter", "new_name"] = 'Heltborg Museum'
count.loc[count["Name"] == "Hjerl Hedes Frilandsmuseum", "address"] = 'Hjerlhedevej 14, 7830 Vinderup'
count.loc[count["Name"] == "Fiskerhuset I Agger", "address"] = 'Toftevej 9, 7770 Vestervig'
count.loc[count["Name"] == "Stenaldercentret Ertebølle", "address"] = 'Gammel Møllevej 8, 9640 Farsø'
count.loc[count["Name"] == "Stenaldercentret Ertebølle", "new_name"] = 'Stenaldercenter Ertebølle'
count.loc[count["Name"] == "Frøslevlejrens Museum", "address"] = 'Lejrvejen 83, 6330 Padborg'
count.loc[count["Name"] == "Fængselsmuseet", "address"] = 'Fussingsvej 8 8700 Horsens'
count.loc[count["Name"] == "Skagens Kunstmuseer", "address"] = 'Brøndumsvej 4, 9990 Skagen'
count.loc[count["Name"] == "Thorvaldsen-Samlingen På Nysø", "address"] = 'Nysøvej 1, 4720 Præstø'
count.loc[count["Name"] == "Fiskeri- Og Søfartsmuseet / Saltvandsakvariet", "address"] = 'Tarphagevej 2, 6710 Esbjerg'
count.loc[count["Name"] == "Hex!", "address"] = 'Sortebrødregade 1, 6760 Ribe'
count.loc[count["Name"] == "Hex!", "new_name"] = 'Hex! Museum of Witch Hunt'
count.loc[count["Name"] == "Den Selvejende Institution Østsjællands Museum", "address"] = 'Rådhusvej 2, 4640 Faxe'
count.loc[count["Name"] == "Skibene På Holmen", "address"] = 'Elefanten 2, 1439 København K'
count.loc[count["Name"] == "Christiansfeld Centret c/o Søstrehuset", "address"] = 'Nørregade 14, 6070 Christiansfeld'
count.loc[count["Name"] == "Skovgaard Museet I Viborg", "address"] = 'Domkirkestræde 2-4, 8800 Viborg'
count.loc[count["Name"] == "Odsherreds Kunstmuseum Hvide Hus", "address"] = 'Rødhøj 11, 4550 Asnæs'
count.loc[count["Name"] == "Kunstmuseum Brandts", "address"] = 'Amfipladsen 7, 5000 Odense'
count.loc[count["Name"] == "Folkemuseet I Hillerød", "address"] = 'Helsingørsgade 65, 3400 Hillerød'
count.loc[count["Name"] == "Folkemuseet I Hillerød", "new_name"] = 'Frederiksborg Slot'
count.loc[count["Name"] == "Fyrhistorisk Museum", "address"] = 'Fyrvejen 25A, 3250 Gilleleje'
count.loc[count["Name"] == "Museum Nordsjælland Hørsholm", "address"] = 'Søndre Jagtvej 2, 2970 Hørsholm'
count.loc[count["Name"] == "Blichermuseum På Herningsholm", "address"] = 'Herregårdsparken 1, 7400 Herning'
count.loc[count["Name"] == "Blichermuseum På Herningsholm", "new_name"] = 'Herningsholm Museum'
count.loc[count["Name"] == "Lützhøfs Købmandsgård", "address"] = 'Ringstedgade 6-8, 4000 Roskilde'
count.loc[count["Name"] == "Museum Amager", "address"] = 'Strandlinien 4, 2791 Dragør'

count.loc[count["Name"] == "Bangsbomuseet", "address"] = 'Dronning Margrethes Vej 6, 9900 Frederikshavn'
count.loc[count["Name"] == "Bangsbomuseet", "new_name"] = 'Kystmuseet Bangsbo Fort'

count.loc[count["Name"] == "Haldladen - De Fem Halder", "address"] = 'Ravnsbjergvej 71, Viborg'
count.loc[count["Name"] == "Haderup Museum", "address"] = 'Jens Jensensvej 1, 7540 Haderup'
count.loc[count["Name"] == "Museum Vestsjælland", "address"] = 'Oldvejen 25, 4300 Holbæk'
count.loc[count["Name"] == "Museum Lolland-Falster", "address"] = 'Frisegade 40, 4800 Nykøbing F'
count.loc[count["Name"] == "Hattemagerhuset I Tarm", "address"] = 'Foersumvej 1, 6880 Tarm'
count.loc[count["Name"] == "Vildmosemuseet", "address"] = 'Nørregade 35, 9700 Brønderslev'
count.loc[count["Name"] == "Tøjhusmuseet", "address"] = 'Tøjhusgade 3, 1220 København'
count.loc[count["Name"] == "Tøjhusmuseet", "new_name"] = 'Krigsmuseet'
count.loc[count["Name"] == "Nordjyllands Historiske Museum", "address"] = 'Algade 48, 9000 Aalborg'
count.loc[count["Name"] == "Gåsemandens Gaard", "address"] = 'Galgebjergevej 20, 6893 Hemmet'
count.loc[count["Name"] == "Museum Obscurum Falsters Minder", "address"] = 'Færgestræde 1a, 4800 Nykøbing Falster'
count.loc[count["Name"] == "Sæby Museum Og Sæbygård Slot", "address"] = 'Sæbygårdvej 49, 9300 Sæby'
count.loc[count["Name"] == "Kystmuseet Sæby", "address"] = 'Søndergade 1B, 9300 Sæby'
count.loc[count["Name"] == "Jagt- Og Skovbrugsmuseet På Dorf", "address"] = 'Folehavevej 17, 2970 Hørsholm'
count.loc[count["Name"] == "Jagt- Og Skovbrugsmuseet På Dorf", "new_name"] = 'Dansk Jagt- og Skovbrugsmuseum'
count.loc[count["Name"] == "Naturhistorisk Museum", "address"] = 'Øster Voldgade 5-7, 1350 København'
count.loc[count["Name"] == "Vikingemuseet Fyrkat", "address"] = 'Fyrkatvej 37B, 9500 Hobro'
count.loc[count["Name"] == "De Gamle Huse Frilandsmuseet", "address"] = 'Meinckes Vej 5, 4930 Maribo'
count.loc[count["Name"] == "Provstgaards Jagthus", "address"] = 'Langkærvej 10, 6900 Skjern'
count.loc[count["Name"] == "Mark Billund Kommunes Museer", "address"] = 'Morsbølvej 101, 7200 Grindsted'
count.loc[count["Name"] == "Museumsgården Kjeldbylille", "address"] = 'Skullebjergvej 15 - Keldbylille, 4780 Stege'
count.loc[count["Name"] == "Sankt Laurentius", "address"] = 'Munkebro 2, 4000 Roskilde'
count.loc[count["Name"] == "Hjedding Mejerimuseum", "address"] = 'Hjeddingvej 2, 6870 Ølgod'
count.loc[count["Name"] == "Janusbygningen", "address"] = 'Lærkevej 25, 6862 Tistrup'
count.loc[count["Name"] == "Janusbygningen", "new_name"] = 'JANUS'
count.loc[count["Name"] == "Vikingemuseet Lindholm Høje", "address"] = 'Vendilavej 11, 9400 Nørresundby'
count.loc[count["Name"] == "Hodde Skolemuseum", "address"] = 'Letbækvej 15, 6862 Tistrup'
count.loc[count["Name"] == "Arresten", "address"] = 'Jernbanegade 21, 4000 Roskilde'
count.loc[count["Name"] == "Besættelsesudstillingen", "address"] = 'Morsbølvej 102, 7200 Grindsted'
count.loc[count["Name"] == "De Kulturhistoriske Museer I Holstebro Kommune", "address"] = 'Museumsvej 2B, 7500 Holstebro'
count.loc[count["Name"] == "Vardemuseerne", "address"] = 'Lundvej 4, 6800 Varde'
count.loc[count["Name"] == "Skibene I Holbæk", "address"] = 'Kanalstræde 23, 4300 Holbæk'
count.loc[count["Name"] == "Museum Sydøstdanmark", "address"] = 'Slotsruinen 1, 4760 Vordingborg'
count.loc[count["Name"] == "Museum Thy", "address"] = 'Jernbanegade 11, 7700 Thisted'
count.loc[count["Name"] == "Museum Thy", "new_name"] = 'Thisted Museum'
count.loc[count["Name"] == "Museum Thy S/I", "address"] = 'Jernbanegade 4, 7700 Thisted'
count.loc[count["Name"] == "Museum Midtjylland", "address"] = 'Vestergade 20, 7400 Herning'

count.loc[count["Name"] == "Muserum", "address"] = ''

count.loc[count["Name"] == "Museerne I Brønderslev Kommune", "address"] = 'Merkurvej 11, 9700 Brønderslev'
count.loc[count["Name"] == "Møns Museum Empiregården", "address"] = 'Storegade 75, 4780 Stege'
count.loc[count["Name"] == "Odense Bys Museer", "address"] = 'Overgade 48, 5000 Odense'
count.loc[count["Name"] == "Ordrupgårdsamlingen", "address"] = 'Vilvordevej 110, 2920 Charlottenlund'
count.loc[count["Name"] == "Ordrupgårdsamlingen", "new_name"] = 'Ordrupgaard'
count.loc[count["Name"] == "Romu", "address"] = 'Sankt Ols Stræde 3, 4000 Roskilde'
count.loc[count["Name"] == "Romu", "new_name"] = 'Den Selvejende Institution Romu'
count.loc[count["Name"] == "Historie & Kunst (Thorvaldsens Museum)", "address"] = 'Bertel Thorvaldsens Plads 2, 1213 København K'
count.loc[count["Name"] == "Historie & Kunst (Thorvaldsens Museum)", "new_name"] = 'Thorvaldsens Museum'
count.loc[count["Name"] == "Museum Nordsjælland S/I", "address"] = 'Frederiksgade 9, 3400 Hillerød'
count.loc[count["Name"] == "H.C. Andersens Hus / Barndomshjem", "address"] = 'Munkemøllestræde 3, 5000 Odense'
count.loc[count["Name"] == "Stiftmuseet Maribo", "address"] = 'Banegårdspladsen 11, 4930 Maribo'
count.loc[count["Name"] == "Strandfogedgården Rubjerg", "address"] = 'Langelinie 2, 9480 Løkken'
count.loc[count["Name"] == "Frederiksbergmuseerne", "address"] = 'Andebakkesti 5, 2000 Frederiksberg'
count.loc[count["Name"] == "Sydvestjyske Museer", "address"] = 'Tangevej 6B, 6760 Ribe'

#%%
dd = df.loc[df['Name'] == 'Muserum']
print(df.loc[df['Name'] == 'Muserum'])

#%%
dd = count.loc[count['lat'] == '']
empty = []

#%%

#%%  Finding geocoordinates - secound round
for i, row in dd.iterrows():
    try:
        city = row['address']
        location = locator.geocode(city)
        if location.address.split(', ')[-1] == 'Danmark':
            count.loc[i, 'lat'] = location.latitude
            count.loc[i, 'lon'] = location.longitude
            count.loc[i, 'new_name'] = location.raw['name']
            count.loc[i, 'address'] = location.address
            count.loc[i, 'country'] = location.address.split(', ')[-1]
    except AttributeError:
        empty.append(row['Name'])

#%%
print(count['lat'].isna().sum())
print(count['lat'].eq('').sum())
print(count['address'].eq('').sum())
print(count['new_name'].eq('').sum())
print(count['country'].unique())

#%%
fix = []
counter = 0
for group, data in count.groupby(['lat', 'lon']):
    if data.shape[0] > 1:
        print(data['Name'], data['Counts'])
        counter += 1
        fix.append((data.iloc[0, 0], data.iloc[0, 1], data.iloc[1, 0], data.iloc[1, 1]))
print(counter)

#%%
empty = []
count['Kommune'] = ''
count['Region'] = ''
count['ZipCode'] = ''

#%%
for i, row in count.iterrows():
    try:
        parts = row['address'].split(', ')
        kom = [p for p in parts if 'Kommune' in p]
        reg = [p for p in parts if 'Region' in p]
        cod = parts[-2]
        print(i, kom[0], reg[0], cod)
        count.loc[i, 'Kommune'] = kom[0]
        count.loc[i, 'Region'] = reg[0]
        count.loc[i, 'ZipCode'] = cod
    except IndexError:
        empty.append((i, row['address']))

#%%
for i, a in empty:
    try:
        parts = a.split(', ')
        kom = [p for p in parts if 'Regionskommune' in p]
        reg = [p for p in parts if 'Region ' in p]
        cod = parts[-2]
        if '37' not in cod:
            cod = ''
        print(i, kom[0], reg[0], cod)
        count.loc[i, 'Kommune'] = kom[0]
        count.loc[i, 'Region'] = reg[0]
        count.loc[i, 'ZipCode'] = cod
    except IndexError:
        print(i, a)
        
#%%
empty = count.loc[count["Region"] == count['ZipCode']]

#%%
for i, row in empty.iterrows():
    try:
        city = row['Kommune']
        location = locator.geocode(city)
        cod = location.address.split(', ')
        count.loc[i, 'ZipCode'] = cod[-2]
        print(i, cod)
    except AttributeError:
        count.loc[i, 'ZipCode'] = ''
        print(i, cod)

#%%
count.loc[count["Region"] == count['ZipCode'], 'ZipCode'] = ''

#%%
count.loc[5, 'ZipCode'] = '9940'
count.loc[21, 'ZipCode'] = '7130'
count.loc[39, 'ZipCode'] = '6000'
count.loc[40, 'ZipCode'] = '3760'
count.loc[74, 'ZipCode'] = '6792'
count.loc[78, 'ZipCode'] = '4791'
count.loc[79, 'ZipCode'] = '6760'
count.loc[84, 'ZipCode'] = '6960'
count.loc[94, 'ZipCode'] = '6990'
count.loc[98, 'ZipCode'] = '7700'
count.loc[105, 'ZipCode'] = '7700'
count.loc[118, 'ZipCode'] = '6830'
count.loc[120, 'ZipCode'] = '6990'
count.loc[146, 'ZipCode'] = '9610'
count.loc[150, 'ZipCode'] = '7870'
count.loc[152, 'ZipCode'] = '1801'
count.loc[157, 'ZipCode'] = '5792'
count.loc[171, 'ZipCode'] = '8850'
count.loc[173, 'ZipCode'] = '9560'
count.loc[195, 'ZipCode'] = '9560'
count.loc[213, 'ZipCode'] = '7000'
count.loc[227, 'ZipCode'] = '9400'
count.loc[245, 'ZipCode'] = '6720'
count.loc[265, 'ZipCode'] = '4780'
count.loc[268, 'ZipCode'] = '6900'
count.loc[284, 'ZipCode'] = '5985'
count.loc[289, 'ZipCode'] = '9520'
count.loc[308, 'ZipCode'] = '7800'

#%%
print(count['lat'].eq('').sum())
print(count['address'].eq('').sum())
print(count['Kommune'].eq('').sum())
print(count['Region'].eq('').sum())
print(count['ZipCode'].eq('').sum())
print(count['country'].eq('').sum())
print(count['country'].unique())

#%%
count.to_csv('mus_address.csv', index=False)

#%%
print(df['Category'].unique())
print(df_area['Category'].unique())
print(df_art['Category'].unique())
print(df_purp['Category'].unique())
print(df_type['Category'].unique())

#%%


