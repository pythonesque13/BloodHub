import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import json
import numpy as np
import plotly.graph_objects as go

dash.register_page(__name__, path='/')

#Donnees pour la construction de la carte 
cities_data = {
    'city': ['Yaoundé', 'Douala', 'Garoua', 'Bamenda', 'Maroua', 'Bafoussam', 'Ngaoundéré', 'Bertoua', 'Loum', 'Kumba', 'Edéa', 'Kumbo', 'Foumban', 'Mbouda', 'Dschang'],
    'lat': [3.8667, 4.0528, 9.3017, 5.9631, 10.5960, 5.4720, 7.3203, 4.5753, 4.7180, 4.6363, 3.8016, 6.2172, 5.7264, 5.6259, 5.4437],
    'lon': [11.5167, 9.7000, 13.3921, 10.1591, 14.3235, 10.4225, 13.5806, 13.6845, 9.7351, 9.4464, 10.1348, 10.6614, 10.9022, 10.2542, 10.0532],
    'population': [2765568, 2446945, 436899, 413538, 319941, 290768, 231357, 218111, 177429, 144413, 133652, 125486, 118738, 111328, 109270]
}

df_cities = pd.DataFrame(cities_data)

#Donnees pour le diagramme circulaire
data = {
    "Condition": ["Condition 1", "Condition 2", "Condition 3", "Condition N"],
    "Dons": [1726, 1380, 1204, 950]
}

df = pd.DataFrame(data)

#Construction du digramme en baton
categories = [str(i).zfill(2) for i in range(1, 13)]
values1 = [15, 10, 18, 12, 22, 25, 14, 9, 13, 11, 20, 23]
values2 = [10, 8, 12, 10, 14, 18, 9, 7, 10, 9, 13, 15]

fig = go.Figure()
fig.add_trace(go.Bar(x=categories, y=values1, marker_color='#CF5A5C'))
fig.add_trace(go.Bar(x=categories, y=values2, marker_color='lightgrey'))
fig.update_layout(
    barmode='group',
    title='',
    height=150,  
    width=600,  
    showlegend=False,  
    margin=dict(l=0, r=0, t=15, b=0)  
)

#Construction de la carte 
def create_cameroon_map():
    # Créer la bubble map
    fig = px.scatter_geo(
        df_cities, 
        lat='lat', 
        lon='lon',
        size='population',
        hover_name='city',
        hover_data={'population': True, 'lat': False, 'lon': False},
        title='',  
        size_max=45,
        projection='natural earth',
    )
    
    # Configuration de  la carte
    fig.update_geos(
        visible=True,
        resolution=50,
        scope='africa',
        showcountries=True,
        countrycolor='gray',
        showcoastlines=True,
        coastlinecolor='lightgray',
        showland=True,
        landcolor='lightgreen',
        showocean=True,
        oceancolor='lightblue',
        center=dict(lat=7.3697, lon=12.3547),
        lonaxis_range=[8, 17],
        lataxis_range=[2, 13],
    )
    
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0, pad=0),  
        autosize=True,                  
    )
    
    return fig

# Création du diagramme circulaire 
fig_pie = px.pie(
    data, 
    names="Condition", 
    values="Dons",
    color_discrete_sequence=["#FFC7C8", "#CF5A5C", "#ED8587", "#EFC94C"],  # Palette de couleurs
    hole=0.8,  # Style de Donut Chart
    title=""
)

# Ajout des labels au survol
fig_pie.update_traces(
    textinfo='none',  
    hoverinfo="label+value",  
    marker=dict(line=dict(color="white", width=1)),
)

# Personnalisation du layout
fig_pie.update_layout(
    showlegend=True,  
    legend=dict(
        x=1,  
        y=0.7, 
        xanchor='left',  
        yanchor='top',   
        font=dict(
            size=12,  
            family='Arial',  
        ),
        itemwidth=60,  
        itemsizing='constant',  
        traceorder='normal',  
        bgcolor='rgba(255,255,255,0.8)',  
    ),
    margin=dict(l=95, r=0, t=0, b=0),
    hoverlabel=dict(
        bgcolor="#DFA3A3",  
        font_size=20,
        font_family="Arial",
        bordercolor="black", 
        namelength=-1,
        
    ),
    width=420,
    height=210,
    
)



#Definintion de la page 
layout = html.Div([
    html.Div([
        
        html.Div([
            dcc.Graph(
                id="map-container",
                figure=create_cameroon_map(),
                config={
                    'displayModeBar': False,
                    'responsive': True,
                },
                className='map'
            )
        ]),

        html.Div([

            html.Div([
                html.Div([
                    html.P("Portions de dons suivant les conditions de santé", className="diagram-p"),
                    html.Span("From 1 Jan to 29 Dec 2019", className="diagram-span"),
                    dcc.Graph(figure=fig_pie)
                ], className="left-section"),
                    
            ], className="diagram-block"),


            html.Div([
                html.P("Participations", className="diagram-P"),
                html.Span("1920", className="diagram-Sp"),
                dcc.Graph(figure=fig, ),
                html.P("Donneurs", className="diagram-dp"),
                
                html.Div([
                    html.Div([
                        html.P("1000"),
                    ], className="Box-number"),
                    
                    html.Div([
                        html.P("920"),
                    ],className="Box-number"),
                    
                    html.Div([    
                        html.P("Condition de sante 1"),
                        html.I(className='bi bi-arrow-down-circle')      
                        
                    ], className="dropdown-menu")
                ], className='Box-stat'),

                html.Div([
                    html.P("Eligibles"),
                    html.P("Non-eligibles")

                ], className="Box-text"),

                html.Div([
                    dcc.Checklist(
                        className="checkbox-line",
                        options=[
                            {'label': ' Condition de sante 1', 'value': 'Condition de sante 1'},
                            {'label': ' Condition de sante 2', 'value': 'Condition de sante 2'},
                            {'label': ' Condition de sante 3', 'value': 'Condition de sante 3'}
                        ],
                        value=['opt1'],
                        inline=True
                    ),
                ], className="")
            ], className="diagram-block2")

        ], className="diagram-container")

    ], className="grid main-content")

], className="content-container")