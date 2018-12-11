#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 07:39:48 2018

@author: root
"""

#displaying data on dash


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import folium
import pandas as pd
import datetime as dt
import random as rnd
import numpy as np
import plotly.graph_objs as go
import itertools


data = pd.read_csv('/home/diego/Desktop/JobSearch/BJS/crime.csv',encoding='latin1')
data.SHOOTING = data.SHOOTING.fillna('N')
coord_pd = pd.DataFrame(data=data[['Lat','Long']].values, columns=['Lat','Long'])
coord_pd=coord_pd.dropna()
lat = coord_pd['Lat'].values
lon = coord_pd['Long'].values
coords = np.vstack((lat,lon))
coords = coords.T


# Creating menus data
#---------------------------------------------------------------------
years = data.YEAR.unique()
options_data_year = [{'label':str(year),'value':year} for year in years]


months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
              'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month_number = list(range(1,13))
options_data_month =  [{'label':months[i-1],'value':i} for i in month_number]



days = np.asarray(['Wednesday', 'Thursday', 'Tuesday', 'Monday', 'Saturday', 'Sunday',
       'Friday'], dtype=object)
labels = np.asarray(['Wed', 'Thu', 'Tue', 'Mon', 'Sat', 'Sun',
       'Fri'], dtype=object)
days_number = list(range(1,8))
options_data_days = [{'label':labels[i-1],'value':days[i-1]} for i in days_number]

offenses = data.OFFENSE_DESCRIPTION.unique()
options_data_offense = [{'label':offense,'value':offense} for offense in offenses]
options_data_offense.append({'label': 'ALL', 'value': 'ALL'})

columns_name = data.columns.values
columns_name=np.append(columns_name,['ALL'])
columns_name_options = [{'label':i,'value':i} for i in columns_name]


#---------------------------------------------------------------------


#Boston Coordinates
BST_COORD = [42.3601, -71.0589]

# Sample (0.33% over 1.5 million) 
sample_coords = rnd.sample(list(coords),50)

# Build default map 
map_nyc = folium.Map(location=BST_COORD, zoom_start=12, 
tiles='cartodbpositron', width=640, height=480)

app = dash.Dash()
MAX = 10000

app.layout = html.Div([
        html.Div([html.H1('Boston Crime Report')],style = {'text-align': 'center'}),
#----------------------------------------------------------------------------         
        html.Hr(),
        html.Div([html.H2('Event Coordinates')],style = {'text-align': 'center'}), 
        html.Div(id = 'text-warning',children='''
        WARNING: The plot may time out if you select too many months and/or years without extra filtering options (MAX unique set to 10000).  
    ''',style = {'padding': 10,'text-align': 'center'}),        
        html.Div([
        html.Div([html.Label('Select Year'),
        dcc.Dropdown(
            id='dropdown-years',    
            options=options_data_year,
            value=['2018'],
            multi=True,
         #   style = {'width': '200','padding': 10, 'display': 'inline-block'}
                    )],style = {'width': '200','padding': 10, 'display': 'inline-block' }),

        html.Div([html.Label('Select Month'),        
        dcc.Dropdown(
            id='dropdown-months',    
            options=options_data_month,
            value=[2],
            multi=True,
         #   style = {'width': '200','padding': 10, 'display': 'inline-block' }
                    )],style = {'width': '200','padding': 10, 'display': 'inline-block' }),

        html.Div([html.Label('Select days'),        
        dcc.Dropdown(
            id='dropdown-days',    
            options=options_data_days,
            value=['Monday'],
            multi=True,
         #   style = {'width': '200','padding': 10, 'display': 'inline-block' }
                    )],style = {'width': '350','padding': 10, 'display': 'inline-block' }),

        html.Div([html.Label('Shooting'),        
        dcc.Dropdown(
            id='dropdown-shooting',    
            options=[{'label': 'With shooting', 'value': 'Y'},
                     {'label': 'No shooting', 'value': 'N'}
                     ],
            value=['N'],
            multi=True,
         #   style = {'width': '200','padding': 10, 'display': 'inline-block' }
                    )],style = {'width': '350','padding': 10, 'display': 'inline-block' }),

        html.Div([html.Label('Offense description'),        
        dcc.Dropdown(
            id='dropdown-OFFENSE_DESCRIPTION',    
            options=options_data_offense,
            value=['ALL'],
            multi=True,
         #   style = {'width': '200','padding': 10, 'display': 'inline-block' }
                    )],style = {'width': '350','padding': 10, 'display': 'inline-block' }),

        html.Div([html.Label('Select hours')],style = {'padding': 10}),
        html.Div([
        dcc.RangeSlider(
            id='my-hour-slider',
            min=0,
            max=23,
            step=1,
            value=[0, 23],
            marks={
                0: '12 am',
                1: '1 am',
                2: '2 am',
                3: '3 am',
                4: '4 am',
                5: '5 am',
                6: '6 am',
                7: '7 am',
                8: '8 am',
                9: '9 am',
                10: '10 am',
                11: '11 am',
                12: '12 pm',
                13: '1 pm',
                14: '2 pm',
                15: '3 pm',
                16: '4 pm',
                17: '5 pm',                
                18: '6 pm',
                19: '7 pm',
                20: '8 pm',
                21: '9 pm',
                22: '10 pm',
                23: '11 pm'               
                  }        
            )],style = {'padding': 20,'text-align': 'center','margin': '200', 'margin-top':'10', 'margin-bottom':'10'}),
            
        html.Div(id = 'text-0',children='''
        Total number of points: 0
    ''',style = {'padding': 10}),
                   ],style = {'text-align': 'center'}),
             
        html.Div([html.Button('Start Plotting',id='button-data')],style = {'padding': 10,'text-align': 'center'}),            
        html.Div([html.Iframe(id = 'map', srcDoc = map_nyc.get_root().render(), width = '640', height = '480')],style = {'text-align': 'center'}),
        html.Hr(),        
#----------------------------------------------------------------------------        
        html.Div([html.H2('Data Plots')],style = {'text-align': 'center'}),  
        
        html.Div([
    
        html.Div([html.Label('Select X Variable'),    dcc.Dropdown(
        id='dropdown-X',
        options=columns_name_options,
        value='close'
        )],style = {'width': '200','padding': 10, 'display': 'inline-block' }),

#     html.Div([html.Label('Select Y Variable'),    dcc.Dropdown(
#        id='dropdown-Y',
#        options=columns_name_options,
#        value='close'
#    )]),
    
         html.Div([html.Label('Select filter_value Variable'),    dcc.Dropdown(
            id='dropdown-filter_value',
            options=columns_name_options,
            value='close'
        )],style = {'width': '200','padding': 10, 'display': 'inline-block' })],style = {'text-align': 'center'}),
    
    #    html.Div([html.Div(id='output-graph')]),
        html.Div([ html.Button('plot data',id='button-3') ],style = {'text-align': 'center'}), 
        html.Div([html.Hr()]),   
        
        html.Div([html.Div(id='output-graph-column')],style = {'text-align': 'center','padding': 20}),          
        
        
        
        
        
        ])




@app.callback(
    Output('map', 'srcDoc'),
 #    Output('placeholder', 'children'),
    [Input('button-data', 'n_clicks'),
     Input('dropdown-years', 'value'), #past
     Input('dropdown-months', 'value'), #past  
     Input('dropdown-days', 'value'), #past 
     Input('my-hour-slider', 'value'), #past     
     Input('dropdown-shooting', 'value'),
     Input('dropdown-OFFENSE_DESCRIPTION', 'value'),     
     ])
def plot_coord(n_clicks,value_0,value_1,value_2,value_3,value_4,value_5):
    global map_nyc
    if n_clicks>0:
        
        if 'ALL' in value_5:
            hours = list(range(value_3[0],value_3[1]+1))
            crime_by_year_month = data.query("YEAR in {0} and MONTH in {1} and DAY_OF_WEEK in {2} and HOUR in {3} and SHOOTING in {4}".format(value_0,value_1,value_2,hours,value_4))
            coord_pd = pd.DataFrame(data=crime_by_year_month[['Lat','Long']].values, columns=['Lat','Long'])
            coord_pd=coord_pd.dropna()
          #  print(coord_pd.shape)
            coord_pd=coord_pd.drop_duplicates(['Lat','Long'])
          #  print(coord_pd.shape)
          #  print("############################################################")
            lat = coord_pd['Lat'].values
            lon = coord_pd['Long'].values
            coords = np.vstack((lat,lon))
            coords = coords.T
            
                
            
            map_nyc = folium.Map(location=BST_COORD, zoom_start=12, 
            tiles='cartodbpositron', width=640, height=480)
            if coords.shape[0] > MAX or coords.shape[1] > MAX:
                return map_nyc.get_root().render()
     #       sample_coords = rnd.sample(list(coords),value_1)
            sample_coords = coords
            [folium.CircleMarker(sample_coords[i], radius=1,
                    color='#0080bb', fill_color='#0080bb').add_to(map_nyc) 
                for i in range(len(sample_coords))]

        else:
            hours = list(range(value_3[0],value_3[1]+1))
            crime_by_year_month = data.query("YEAR in {0} and MONTH in {1} and DAY_OF_WEEK in {2} and HOUR in {3} and SHOOTING in {4} and OFFENSE_DESCRIPTION in {5}".format(value_0,value_1,value_2,hours,value_4,value_5))
            coord_pd = pd.DataFrame(data=crime_by_year_month[['Lat','Long']].values, columns=['Lat','Long'])
            coord_pd=coord_pd.dropna()
            print(coord_pd.shape)
            coord_pd=coord_pd.drop_duplicates(['Lat','Long'])
            print(coord_pd.shape)
            print("############################################################")
            lat = coord_pd['Lat'].values
            lon = coord_pd['Long'].values
            coords = np.vstack((lat,lon))
            coords = coords.T
            
            
            map_nyc = folium.Map(location=BST_COORD, zoom_start=12, 
            tiles='cartodbpositron', width=640, height=480)
            
     #       sample_coords = rnd.sample(list(coords),value_1)
            sample_coords = coords
            [folium.CircleMarker(sample_coords[i], radius=1,
                    color='#0080bb', fill_color='#0080bb').add_to(map_nyc) 
                for i in range(len(sample_coords))]            
            

        return map_nyc.get_root().render()
            
@app.callback(
    Output('text-0', 'children'),
 #    Output('placeholder', 'children'),
    [Input('dropdown-years', 'value'), #past
     Input('dropdown-months', 'value'), #past 
     Input('dropdown-days', 'value'), #past   
     Input('my-hour-slider', 'value'), #past  
     Input('dropdown-shooting', 'value'),
     Input('dropdown-OFFENSE_DESCRIPTION', 'value'),     
     ])
def num_points_year(value_0,value_1,value_2,value_3,value_4,value_5):
    global  data
    
    if 'ALL' in value_5:    
        hours = list(range(value_3[0],value_3[1]+1))
        crime_by_year_month = data.query("YEAR in {0} and MONTH in {1} and DAY_OF_WEEK in {2} and HOUR in {3} and SHOOTING in {4}".format(value_0,value_1,value_2,hours,value_4)) 
        crime_by_year_month.Lat = crime_by_year_month.Lat.dropna()
        crime_by_year_month.Long = crime_by_year_month.Long.dropna()
    else:
        hours = list(range(value_3[0],value_3[1]+1))
        crime_by_year_month = data.query("YEAR in {0} and MONTH in {1} and DAY_OF_WEEK in {2} and HOUR in {3} and SHOOTING in {4} and OFFENSE_DESCRIPTION in {5}".format(value_0,value_1,value_2,hours,value_4,value_5))
        crime_by_year_month.Lat = crime_by_year_month.Lat.dropna()
        crime_by_year_month.Long = crime_by_year_month.Long.dropna()        



    return "Total number of points: {0}. Number of unique locations: {1}".format(crime_by_year_month.shape[0],len(set(crime_by_year_month.Location.values))) 
    
@app.callback(
    Output('output-graph-column', 'children'),
    [Input('button-3', 'n_clicks'),
     Input('dropdown-X', 'value'),  
     Input('dropdown-filter_value', 'value'),     
     ])
def plot_graph_column(n_clicks,x_value,filter_value):
    global data
    if n_clicks > 0:
       
        if filter_value != 'ALL':    
            
            return  dcc.Graph(
                    id='life-exp-vs-gdp',
                    figure={
                        'data': [
                            go.Bar(
                                x=data.query("{1} == '{0}'".format(i,filter_value)).groupby(['{0}'.format(x_value)]).agg(['count']).OFFENSE_CODE.index.get_values(),
                                y=data.query("{1} == '{0}'".format(i,filter_value)).groupby(['{0}'.format(x_value)]).agg(['count']).OFFENSE_CODE.values.reshape([data.query("{1} == '{0}'".format(i,filter_value)).groupby(['{0}'.format(x_value)]).agg(['count']).OFFENSE_CODE.values.shape[0]]),
                               # text=df[df['continent'] == i]['country'],
                                marker={
                                    'line': {'width': 0.5, 'color': 'white'}
                                },
                                name=str(i)
                            ) for i in data['{0}'.format(filter_value)].unique()
                        ],
                        'layout': go.Layout(
                            title ='Crimes by {0} filteres by {1}'.format(x_value,filter_value),  
                            xaxis={'title': '{0}'.format(x_value)},
                            yaxis={'title': 'Crimes'},
                            margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                            legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
                    }
                )
        else:
            
            return dcc.Graph(
                    id='life-exp-vs-gdp',
                    figure={
                        'data': [
                            go.Bar(
                                x=data.groupby(['{0}'.format(x_value)]).agg(['count']).OFFENSE_CODE.index.get_values(),
                                y=data.groupby(['{0}'.format(x_value)]).agg(['count']).OFFENSE_CODE.values.reshape([data.groupby(['{0}'.format(x_value)]).agg(['count']).OFFENSE_CODE.values.shape[0]]),
                               # text=df[df['continent'] == i]['country'],
                                marker={
                                    'line': {'width': 0.5, 'color': 'white'}
                                },

                            ) 
                        ],
                        'layout': go.Layout(
                            title ='Crimes by {0}'.format(x_value),    
                            xaxis={'title': '{0}'.format(x_value)},
                            yaxis={'title': 'Crimes'},
                            margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                            legend={'x': 0, 'y': 1},
                            hovermode='closest'
                        )
                    }
                )            
















if __name__ == '__main__':
    app.run_server(debug=True,port=8042)