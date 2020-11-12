#Import Libraries
import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go

#Get your own mapbox token
mapbox_access_token='put your mapbox token here'


#Read data and add a color column for crimes
df=pd.read_csv('c:\\users\\hp\\Documents\\Dashcsv\\Crime_data.csv')
df['Colors']='red'
df['Colors'][df['Category']=='BURGLARY']='blue'
df['Colors'][df['Category']=='LARCENY/THEFT']='green'
df['Colors'][df['Category']=='ROBBERY']='orange'
df['Colors'][df['Category']=='VEHICLE THEFT']='aqua'
blackbold={'color':'black','font-weight':'bold'}

app=dash.Dash(__name__)

#Dash component
app.layout=html.Div([
    html.Div([
        html.Div([           
           # Map-legend
            html.Ul([
                html.Li("ASSAULT", className='circle', style={'background': 'red','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("BURGLARY", className='circle', style={'background': 'blue','color':'black',
                    'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
                html.Li("LARCENY/THEFT", className='circle', style={'background': 'green','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("ROBBERY", className='circle', style={'background': 'orange','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("VEHICLE THEFT", className='circle',  style={'background': 'aqua','color':'black',
                    'list-style':'none','text-indent': '17px'}),
            ], style={'border-bottom': 'solid 3px', 'border-color':'#00FC87','padding-top': '6px'}
            ),  
            
            #Category_checklist
            html.Label(children=['Crime Category:'],style=blackbold),
            dcc.Checklist(id='category_name',
                          options=[{'label':str(b),'value':b} for b in sorted(df['Category'].unique())],
                          value=[b for b in sorted(df['Category'].unique())],
                
                ),
            
            #District_checklist
            html.Label(children=['Police District:'],style=blackbold),
            dcc.Checklist(id='district_name',
                          options=[{'label':str(b),'value':b} for b in sorted(df['PdDistrict'].unique())],
                          value=[b for b in sorted(df['PdDistrict'].unique())],
                
                ),
            
            ]),
        
        #Map
        html.Div([
            dcc.Graph(id='graph', config={'displayModeBar': False, 'scrollZoom': True},
                      style={'padding-bottom':'2px','padding-left':'2px','height':'100vh'} 
                )
            ]),
        
        ]),
     
    ])

#Callback 
@app.callback(Output('graph','figure'),
              [Input('category_name','value'),
               Input('district_name','value')]) 
def update_figure(chosen_cat,chosen_dist):
    dff=df[(df['Category'].isin(chosen_cat))&
           (df['PdDistrict'].isin(chosen_dist))]
    
    #create figure
    locations=[go.Scattermapbox(
                    lon = dff['X'],
                    lat = dff['Y'],
                    mode='markers',
                    marker={'color' : dff['Colors']},
                    unselected={'marker' : {'opacity':1}},
                    selected={'marker' : {'opacity':0.5, 'size':25}},
                    hoverinfo='text',
                    hovertext=dff['Category']
                    
                    )]
    
    return {
        'data': locations,
        'layout': go.Layout(
            uirevision= 'foo',
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=2,
            title=dict(text="San Francisco Crime Map",font=dict(size=40, color='teal')),
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=25,
                style='light',
                center=dict(
                    lat=37.7745986,
                    lon=-122.4258917
                ),
                pitch=30,
                zoom=11
            ),
        )
    }


if __name__ == '__main__':
    app.run_server()