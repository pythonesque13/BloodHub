import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


dash.register_page(__name__, path="/")


data_pie = pd.DataFrame({
    "Condition de santé": ["Condition 1", "Condition 2", "Condition 3"],
    "Dons": [40, 32, 28]
})

fig_pie = px.pie(data_pie, names="Condition de santé", values="Dons", hole=0.6)

layout = dbc.Container(
    [
  
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_pie), width=9),
            dbc.Col(html.Div("Carte interactive ici", 
                             className="d-flex align-items-center justify-content-center border p-4"), width=6),
        ], className="mb-4"),

      
        dbc.Row([
            html.H4("Participations : 1920", className="text-center"),
            html.P("Nombre de donneurs : 1000 | Non éligibles : 920", className="text-center"),
        ]),
    ],
    fluid=True
)
