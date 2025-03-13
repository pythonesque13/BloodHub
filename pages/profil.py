import dash
from dash import html
import dash_bootstrap_components as dbc

# Enregistrement de la page avec une route "/profil"
dash.register_page(__name__, path="/profil")

layout = dbc.Container(
    [
        html.H1("Profil type", className="text-center text-secondary"),
        
        dbc.Row([
            dbc.Col(dbc.Card([
                html.H5("Poids"),
                html.P("60-85 kg"),
            ], body=True, className="text-center"), width=3),

            dbc.Col(dbc.Card([
                html.H5("Groupe sanguin"),
                html.P("O rh-"),
            ], body=True, className="text-center"), width=3),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dbc.Card([
                html.H5("Âge"),
                html.P("20-35 ans"),
            ], body=True, className="text-center"), width=3),

            dbc.Col(dbc.Card([
                html.H5("Antécédents"),
                html.P("Non"),
            ], body=True, className="text-center"), width=3),
        ]),

        html.Br(),

        dbc.Row([
            dbc.Button("Conditions santé", color="danger", className="me-2"),
            dbc.Button("Conditions santé", color="danger", className="me-2"),
            dbc.Button("Conditions santé", color="danger"),
        ], className="d-flex justify-content-center"),
    ],
    fluid=True
)
