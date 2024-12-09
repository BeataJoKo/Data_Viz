# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 13:35:51 2024

@author: BeButton
"""

#%%

import data_wrangling as data
import data_utils as util
import dash
from dash import Dash, dcc, html
# import dash_bootstrap_components as dbc
#import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from collections import Counter
import math
import pandas as pd
#from dash_bootstrap_templates import load_figure_template

#%% create Dash app

app = dash.Dash()

#%% import data

mintime = min(data.df_visit['Year'])
maxtime = max(data.df_visit['Year'])

#%% define Dash app layout 

app.layout = html.Div([

    html.Div(id='title', children=[
        html.H1("Museums' Visitors"),
        html.H4(f"Total visitors on exhibitions: {round(data.df_visit['Visit_Exhibition'].sum())}", 
                         id='total_exhibition'),
        html.H6(f"Total visitors on museum locations: {round(data.df_visit['Visit_Place'].sum())}", 
                         id='total_place')
       
        ]),
    
    html.Div(id='top_info', children=[
        html.Div(id='map_container', children=[
            html.Label('Choose map type:'),
            html.Label('Choose museum category:'),
            dcc.Dropdown(
                id='map_type',
                options=[
                         {'label': 'Visitors on Exhibition in Museum', 'value': 'exhibition'},
                         #{'label': 'Visitors of the Museum Location', 'value': 'location'},
                         #{'label': 'Visitors on Exhibition in Municipality', 'value': 'kommune_ex'},
                         {'label': 'Visitors of the Museum Location in Municipality', 'value': 'kommune_loc'}
                         ],
                value='exhibition',
                clearable= False
                ),
            dcc.Dropdown(
                id='map_category',
                options= data.map_cat,
                value='All museums',
                #multi=True,
                clearable= False
                ),
            dcc.Graph(id='map_chart')
            ]),
        html.Div(id='bar_container', children=[
            #html.Div(id='mus_info', children=[
                html.H3(f"Here comes museum name {'...'}"),
                html.H5(f"..and some more informations {'...'}"),
                html.Button("Reset", id = "reset_all"),
           # ]),
            dcc.Graph(id='bar_visit'),
            dcc.RangeSlider(
                id='time_slider',
                min=mintime,
                max=maxtime,
                step=1,
                value=[mintime, maxtime],
                marks={i: str(i) for i in range(mintime, maxtime+1, 1)})
            ]),
        ]),
    
    html.Div(id='midd_info', children=[
        dcc.Graph(id='pop_graph'),
        dcc.Graph(id='scatterplot_corona')
        ]),
    
    html.Div(id='bottom_info', children=[
        dcc.Graph(id='sanky_teaching'),
        dcc.Graph(id='art_consumption')
        ]),
    
    html.Div(id='footer', children=[
        ])

    ])
                     

@app.callback(
    [Output(component_id="map_chart", component_property="figure")],
    [Input(component_id='map_type', component_property='value'),
     Input(component_id='map_category', component_property='value')],
    [State(component_id='map_chart', component_property='figure')]
)
def update_map(selected_map, map_category, current_map_state):
    
    df = data.df_visit
    df_agg_loc = util.kommune_agg(data.df_visit, 'Visit_Place', data.dt_mun)
    #df_agg_ex = util.kommune_agg(data.df_visit, 'Visit_Exhibition', data.dt_mun)
    
    initial_zoom = 5.6
    initial_center = {'lat': 56.30205043365613, 'lon': 11.153154691145753}
    
    if current_map_state:
        current_zoom = current_map_state['layout']['mapbox']['zoom']
        current_center = current_map_state['layout']['mapbox']['center']
        fig = current_map_state
    else:
        current_zoom = initial_zoom
        current_center = initial_center
        fig = go.Figure() # create a new figure
        

        
    if selected_map == 'exhibition':
        df_agg_year = util.name_agg(df, 'Visit_Exhibition', [2018, 2023])
        limits = util.quantile_lim(df_agg_year, 'Visit_Exhibition')
        
        for lim in limits:
            df_agg_year.loc[(df_agg_year['Visit_Exhibition'] >= lim[0]) & (df_agg_year['Visit_Exhibition']<= lim[1]), "type"] = str(lim[0]) + ' - ' + str(lim[1])        
        #colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
    

        fig = px.scatter_mapbox(df_agg_year,
                                lat="lat",
                                lon="lon",
                                hover_data=['Name', 'Category', 'Visit_Exhibition'],
                                mapbox_style="carto-positron",
                                #color='Visit_Exhibition',
                                color="type", 
                                size='scale',
                                #size_max=30,
                                zoom=current_zoom,
                                center=current_center,
                                #color_continuous_scale=color_scale,
                                )

        #fig.update_traces(selector=dict(mode='markers'))
        
        fig.update_traces(customdata=df[['Name', 'Category', 'Visit_Exhibition']], 
                        hovertemplate='<b>Name:</b> %{customdata[0]}<br>'
                                        '<b>Category:</b> %{customdata[1]}<br>'
                                        '<b>Visit Exhibition:</b> %{customdata[2]}<br>'
                                        '<extra></extra>')
        fig.update_layout(
            title_text = 'Visitors on Exhibitions',
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            plot_bgcolor='#efefef',
            paper_bgcolor = '#efefef'
        )
        fig.update_coloraxes(colorbar_title='Visitors')

    else:
        min_value = 0
        max_value = max(df_agg_loc['VisitCount'])

        fig = px.choropleth_mapbox(df_agg_loc,
                                    geojson=data.kommune_geojson,
                                    color='VisitCount',
                                    hover_name='Kommune',
                                    locations='Location',
                                    featureidkey='properties.kode',
                                    center=current_center,
                                    mapbox_style="carto-positron",
                                    zoom=current_zoom,
                                    #color_continuous_scale=color_scale,
                                    range_color=[min_value, max_value]
                                    )
        fig.update_layout(
                        title_text = 'Visitors at Museums\' Location',
                        margin={"r": 0, "t": 0, "l": 0, "b": 0},
                        plot_bgcolor='#efefef',
                        paper_bgcolor = '#efefef'
                        )
        fig.update_coloraxes(colorbar_title='Visitors')

    return [fig]


@app.callback(
    [Output(component_id="bar_visit", component_property="figure")],
    [Input(component_id='time_slider', component_property='value')]
)
def update_bar(year_range):  

    df, colors = util.year_agg(data.df_visit, year_range)
    
    fig = go.Figure(
        data=[go.Bar(
            x=df['Year'], 
            y=df['Visit_Exhibition'],
            hovertext=df['Visit_Exhibition']
            )])
    
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df['Year'], 
            y=df['Visit_Exhibition'],
            hovertext=df['Visit_Exhibition'],
            marker={'opacity': colors}
            ))
    
    fig.update_traces(marker_color='rgb(89,0,43)', 
                      marker_line_color='rgb(8,48,107)',
                      #opacity=0.9,
                      marker_line_width=1.5) 
    
    #fig.data[0].marker.color = ('red','red','red', 'red')
    
    fig.update_layout(
        title_text='Yearly Visitors on Expositions in Museums',
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        plot_bgcolor='#efefef',
        paper_bgcolor = '#efefef')
    
    return [fig]


@app.callback(
    [Output(component_id="pop_graph", component_property="figure")],
    [Input(component_id='time_slider', component_property='value')]
)
def update_pop(year_range):  
    
    man, woman = util.gender_data(data.df_cat, year_range)
    colors = 1.0
    
    fig = go.Figure()
    for col in man.columns[1:]:
        fig.add_trace(
            go.Bar(x=-man[col],
                   y =man['Age'],
                   orientation='h',
                   name= 'Male: '+col,
                   marker={
                       'opacity': colors,
                       'color': 'rgb(99,110,250)'
                           },
                   legendgroup="Male",
                   showlegend = col == 'Kunstmuseum',
                   customdata=man[col],
                   hovertemplate = "%{y}: %{customdata}"))
        colors = colors - 0.2
        
    colors = 1.0
    for col in woman.columns[1:]:
        fig.add_trace(
            go.Bar(x= woman[col].values,
                   y=woman['Age'],
                   orientation='h',
                   name='Female: '+col,
                   marker={
                       'opacity': colors,
                       'color': 'rgb(239,86,64)'
                           },
                   legendgroup="Female",
                   showlegend = col == 'Kunstmuseum',
                   hovertemplate="%{y}: %{x}"))    
        colors = colors - 0.2

    fig.update_layout(barmode='relative', 
                  yaxis_autorange='reversed',
                  height=400, 
                  width=700, 
                  legend_orientation ='h',
                  bargap=0.01,
                  legend_x=-0.05, 
                  legend_y=1.1,
                  title_text='Population Graph',
                  margin={"r": 0, "t": 0, "l": 0, "b": 0},
                  plot_bgcolor='#efefef',
                  paper_bgcolor = '#efefef'
                 )
    
    return [fig]
        
@app.callback(
    [Output(component_id="scatterplot_corona", component_property="figure")],
    [Input(component_id='map_category', component_property='value')]
)
def update_corona(map_cat):
    
    df = util.corona_data(data.df_visit)
    
    fig = go.Figure(
        data=[
            go.Scatter(
                x=df['After'].values,
                y=df['Before'].values,
                mode='markers',
                hovertext=df['Name'],
                marker=dict(
                    color='rgb(46,54,144)',
                    size=df['scale'].values,
                    showscale=True
                    )
            )])  
    
    fig.add_trace(
        go.Scatter(
            x=[1315418],
            y=[1512747],
            mode='markers',
            hovertext=['Louisiana Museum Of Modern Art'],
            marker=dict(
                color='rgb(250,175,67)',
                size=[30],
                showscale=True
                )))

    fig.update_layout(
                  title_text='Museums Visitors Before and After Corona',
                  margin={"r": 0, "t": 0, "l": 0, "b": 0},
                  plot_bgcolor='#efefef',
                  paper_bgcolor = '#efefef'
                 )
    
    return [fig]


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
                        