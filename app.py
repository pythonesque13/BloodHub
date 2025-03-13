import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

data_pie = pd.DataFrame({
    "Condition de santé": ["Condition 1", "Condition 2", "Condition 3"],
    "Dons": [40, 32, 28]
})

fig_pie = px.pie(data_pie, names="Condition de santé", values="Dons", hole=0.6)


app.layout = dbc.Container([
    
    dcc.Location(id="url"),

    dbc.Row([
       
        dbc.Col([
            html.H2("IndabaX", className="text-center text-primary"),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Accueil", href="/", active="exact"),
                    dbc.NavLink("Profil Type", href="/profil", active="exact"),
                    dbc.NavLink("Profil", href="/profil-type", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ], width=2, className="bg-light"),

      
        dbc.Col([
            dash.page_container  
        ], width=10),
    ]),
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
