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
import numpy as np
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
                html.Button("Toggle Metric", id="toggle_metric", n_clicks=0),  # Add Toggle Button - Mathias
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
        html.Label('Chose what to compare:'),
        html.H4('On the X-axis:'),
        dcc.Dropdown(
            id='corona_map',
            options=[
                {'label': 'Before Covid-19', 'value': 'Before Covid-19'},
                {'label': 'After Covid-19', 'value': 'After Covid-19'},
                {'label': 'During Covid-19', 'value': 'During Covid-19'}
                ],
            value='Before Covid-19',
            clearable= False),
        html.H4('On the Y-axis:'),
        dcc.Dropdown(
            id='corona_map_2',
            options=[
                {'label': 'Before Covid-19', 'value': 'Before Covid-19'},
                {'label': 'After Covid-19', 'value': 'After Covid-19'},
                {'label': 'During Covid-19', 'value': 'During Covid-19'}
                ],
            value='After Covid-19',
            clearable= False),
        dcc.Graph(id='scatterplot_corona')
        ]),
    
    html.Div(id='bottom_info', children=[
        dcc.Graph(id='sanky_teaching'),
        dcc.Graph(id='distribution')
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
    [Input(component_id='time_slider', component_property='value'),
     Input(component_id='map_category', component_property='value'),
     Input(component_id='toggle_metric', component_property='n_clicks'),
     Input(component_id='map_chart', component_property='clickData')]  # New input
)
def update_bar(year_range, map_category, n_clicks, clickData):
    selected_kommune = None
    if clickData and 'points' in clickData:
        selected_kommune = clickData['points'][0]['hovertext']

    # Filter based on year, map_category and Municipality
    df_filtered = data.df_visit[
        (data.df_visit['Year'] >= year_range[0]) &
        (data.df_visit['Year'] <= year_range[1])
    ]
    
    if map_category != "All museums":
        df_filtered = df_filtered[df_filtered['Category'] == map_category]
    if selected_kommune:  # Filter further if a kommune is clicked
        df_filtered = df_filtered[df_filtered['Kommune'] == selected_kommune]

    # Toggle between two metrics
    y_column = 'Visit_Exhibition' if n_clicks % 2 == 0 else 'Visitors_Exhibition_per_opening_hour'
    y_title = 'Visit Exhibition' if n_clicks % 2 == 0 else 'Visitors per Opening Hour'
    df_agg = df_filtered.groupby('Year', as_index=False)[y_column].sum()
    # Create the barplot
    fig = go.Figure(
        data=[go.Bar(
            x=df_agg['Year'], 
            y=df_agg[y_column],
            hovertext=df_agg[y_column]
        )]
    )
    
    fig.update_traces(marker_color='rgb(89,0,43)', 
                      marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5) 
    
    fig.update_layout(
        title_text=f'Yearly {y_title} for {map_category}',
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        plot_bgcolor='#efefef',
        paper_bgcolor='#efefef',
    )
    
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
       # colors = colors - 0.2
        
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
        #colors = colors - 0.2

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
    [Input(component_id='corona_map', component_property='value'),
     Input(component_id='corona_map_2', component_property='value')]
)
def update_corona(x_axis, y_axis):
    
    df = util.corona_data(data.df_visit)
    
    
    max_limit = max(df[x_axis].max(), df[y_axis].max())

    # Create scatter plot
    fig = go.Figure(
        data=[
            go.Scatter(
                x=df[x_axis].values,
                y=df[y_axis].values,
                mode='markers',
                hovertext=df['Name'],
                marker=dict(
                    color='rgb(46,54,144)',
                    size=df['scale'].values,
                    showscale=False
                ) ,
                hovertemplate=(
                "<b>Name:</b> %{hovertext}<br>" +  
                f"<b>{x_axis}:</b>"+" %{x}<br>" +       
                f"<b>{y_axis}:</b>"+" %{y}<br>" +       
                "<extra></extra>"                
                )
            )
        ]
    )

    
    fig.update_layout(
        title_text=f'Attendance: {x_axis} vs {y_axis}',
        shapes = [
    {
        'type': 'line',      
        'yref': 'paper',    
        'xref': 'paper',    
        'y0': 0,             
        'y1': 1,             
        'x0': 0,             
        'x1': 1,            
        'layer': 'below',    
        'opacity': 0.2       
    }
],
        xaxis=dict(
            title=x_axis,
            range=[0, max_limit * 1.1],  
            constrain="domain"           
        ),
        yaxis=dict(
            title=y_axis,
            range=[0, max_limit * 1.1],  
            constrain="domain"           
        ),
        margin={"r": 10, "t": 50, "l": 30, "b": 10},
        plot_bgcolor='#efefef',
        paper_bgcolor='#efefef'
    )

    
   

    return [fig]


@app.callback(
    [Output(component_id="sanky_teaching", component_property="figure")],
    [Input(component_id='time_slider', component_property='value')]
)
def update_sankey(time_slider):
    
    df = util.teaching_data(data.df_teaching, ['Teaching', 'Category'], 'Amount')
    
    fig = go.Figure(
        data=[
            go.Sankey(
                node = dict(
                    pad = 15,
                    thickness = 20,
                    line = dict(color = "black", width = 0.5),
                    label = df[0],
                    color = ['green', 'blue', 'pink', 'orange', 'yellow', 'grey', 'violet']
                    ),
                link = dict(
                    source = df[2] + [6, 6], # indices correspond to labels, eg A1, A2, A1, B1, ...
                    target = df[1] + [0, 1],
                    value = df[3] + [84347, 11168],
                    color = ['rgba(0, 255, 0, 0.6)', 'rgba(0, 255, 0, 0.6)', 'rgba(0, 255, 0, 0.6)', 'rgba(0, 255, 0, 0.6)', 'rgba(0, 255, 0, 0.6)', 'rgba(0, 0, 255, 0.6)', 'rgba(0, 0, 255, 0.6)', 'rgba(0, 0, 255, 0.6)', 'rgba(0, 0, 255, 0.6)', 'rgba(0, 0, 255, 0.6)', 'rgb(255, 0, 0, 1)', 'rgba(255, 0, 0, 1)']
                    
        ))])
    
    fig.update_layout(
                  title_text='Teaching and No Teaching groups undrer 18 years',
                  margin={"r": 0, "t": 0, "l": 0, "b": 0},
                  font_size=10,
                  plot_bgcolor='#efefef',
                  paper_bgcolor = '#efefef'
                 )

    return [fig]


@app.callback(
    [Output(component_id="distribution", component_property="figure")],
    [Input(component_id='time_slider', component_property='value')]
)
def update_dist(time_slider):
    
    df = util.name_agg(data.df_visit, 'Visit_Exhibition', [2018, 2023])

# produce histogram data wiht numpy
    count, index = np.histogram(df['Visit_Exhibition'], bins=100)
    fig = go.Figure(
        data=[
            go.Scatter(
                x=index, 
                y=count,
                line=dict(width = 1.5, shape='hvh'))])
    
    fig.update_yaxes(
    showgrid=True,
    ticks="inside",
    tickson="boundaries",
    ticklen=0,
    showline=False,
    #linewidth=1,
    #linecolor='black',
    mirror=True,
    zeroline=False)

    fig.update_xaxes(
    showgrid=True,
    ticks="inside",
    tickson="boundaries",
    ticklen=0,
    showline=False,
    #linewidth=1,
    #linecolor='black',
    mirror=True,
    zeroline=False)

    
    fig.update_layout(
        title_text='Some Distribution',
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        plot_bgcolor='#efefef',
        paper_bgcolor = '#efefef')

    return [fig]


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
                        
