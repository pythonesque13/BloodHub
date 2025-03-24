import dash
from dash import html, dcc, callback, Input, Output, State
import requests
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px

dash.register_page(__name__, path='/ai')


layout = dbc.Container([
    html.H1("Prédiction d'éligibilité au don de sang", className="text-center mb-4"),
    
    dbc.Row([
        dbc.Col([
            # Basic Information
            dbc.Card([
                dbc.CardHeader(html.H3("Informations de base")),
                dbc.CardBody([
                    dbc.Select(
                        id='genre',
                        options=[
                            {'label': 'Homme', 'value': 'Homme'},
                            {'label': 'Femme', 'value': 'Femme'}
                        ],
                        placeholder="Genre"
                    ),
                    dbc.Input(
                        id='age',
                        type='number',
                        placeholder='Age',
                        min=18,
                        max=65,
                        className="mt-2"
                    ),
                    dbc.Select(
                        id='deja_donne',
                        options=[
                            {'label': 'Oui', 'value': 'Oui'},
                            {'label': 'Non', 'value': 'Non'}
                        ],
                        placeholder="Avez-vous déjà donné du sang?",
                        className="mt-2"
                    ),
                    dbc.Input(
                        id='taux_hemoglobine',
                        type='number',
                        placeholder="Taux d'hémoglobine",
                        step=0.1,
                        className="mt-2"
                    ),
                ])
            ], className="mb-4"),

            # Rest of your form components converted to dbc...
            # (Continue converting the other sections similarly)

            dbc.Card([
                dbc.CardHeader(html.H3("Conditions médicales")),
                dbc.CardBody([
                    *[dbc.Select(
                        id=field,
                        options=[
                            {'label': 'Oui', 'value': 'Oui'},
                            {'label': 'Non', 'value': 'Non'}
                        ],
                        placeholder=field.replace('_', ' ').title(),
                        className="mt-2"
                    ) for field in [
                        'sous_antibiotherapie', 'hemoglobine_bas', 'dernier_don_recent',
                        'ist_recente', 'antecedent_transfusion', 'porteur_virus',
                        'opere', 'drepanocytaire', 'diabetique', 'hypertendu',
                        'asthmatique', 'cardiaque', 'tatoue', 'scarifie'
                    ]]
                ])

            ], className="mb-4"),

            dbc.Card(id='female-conditions', style={'display': 'none'}, children=[
                dbc.CardHeader(html.H3("Conditions spécifiques aux femmes")),
                dbc.CardBody([
                    *[dbc.Select(
                        id=field,
                        options=[
                            {'label': 'Oui', 'value': 'Oui'},
                            {'label': 'Non', 'value': 'Non'}
                        ],
                        placeholder=field.replace('_', ' ').title(),
                        className="mt-2"
                    ) for field in [
                        'ddr_mauvais', 'allaitement', 'accouchement_recent',
                        'interruption_grossesse', 'enceinte'
                    ]]
                ])

            ], className="mb-4"),

            dbc.Button(
                "Prédire",
                id='predict-button',
                color="primary",
                className="mt-3 mb-4 w-100"
            ),
        ], width=12),

        # Results section
        dbc.Col([
            html.Div(id='prediction-results')
        ], width=12, className='mb-3')
    ])
], fluid=True, className='ai mx-3')

@callback(
    Output('female-conditions', 'style'),
    Input('genre', 'value')
)
def toggle_female_conditions(genre):
    if genre == 'Femme':
        return {'display': 'block'}
    return {'display': 'none'}

@callback(
    Output('prediction-results', 'children'),
    Input('predict-button', 'n_clicks'),
    [State(field, 'value') for field in [
        'genre', 'age', 'deja_donne', 'taux_hemoglobine',
        'sous_antibiotherapie', 'hemoglobine_bas', 'dernier_don_recent',
        'ist_recente', 'ddr_mauvais', 'allaitement', 'accouchement_recent',
        'interruption_grossesse', 'enceinte', 'antecedent_transfusion',
        'porteur_virus', 'opere', 'drepanocytaire', 'diabetique',
        'hypertendu', 'asthmatique', 'cardiaque', 'tatoue', 'scarifie'
    ]],
    prevent_initial_call=True
)
def predict_eligibility(n_clicks, *values):
    if not all(values[:4]):  # Check if required fields are filled
        return html.Div("Veuillez remplir tous les champs obligatoires", className="alert alert-warning")

    # Prepare data for API request
    data = {
        "genre": values[0],
        "age": values[1],
        "deja_donne": values[2],
        "taux_hemoglobine": values[3],
        "sous_antibiotherapie": values[4] or "Non",
        "hemoglobine_bas": values[5] or "Non",
        "dernier_don_recent": values[6] or "Non",
        "ist_recente": values[7] or "Non",
        "ddr_mauvais": values[8] or "Non",
        "allaitement": values[9] or "Non",
        "accouchement_recent": values[10] or "Non",
        "interruption_grossesse": values[11] or "Non",
        "enceinte": values[12] or "Non",
        "antecedent_transfusion": values[13] or "Non",
        "porteur_virus": values[14] or "Non",
        "opere": values[15] or "Non",
        "drepanocytaire": values[16] or "Non",
        "diabetique": values[17] or "Non",
        "hypertendu": values[18] or "Non",
        "asthmatique": values[19] or "Non",
        "cardiaque": values[20] or "Non",
        "tatoue": values[21] or "Non",
        "scarifie": values[22] or "Non"
    }

    try:
        response = requests.post('http://localhost:8000/predict', json=data)
        result = response.json()

        # Create probability graph
        fig = go.Figure(data=[
            go.Bar(
                x=list(result['probabilities'].keys()),
                y=list(result['probabilities'].values()),
                marker_color=['#2ecc71', '#e74c3c', '#f1c40f']
            )
        ])
        fig.update_layout(
            title="Probabilités par catégorie",
            yaxis_title="Probabilité",
            xaxis_title="Catégorie"
        )

        return html.Div([
            html.H4(f"Résultat: {result['status']}", 
                   className=f"alert {'alert-success' if result['status'] == 'Eligible' else 'alert-danger'}"),
            html.P(result['message'], className="lead"),
            dcc.Graph(figure=fig)
        ])

    except Exception as e:
        return html.Div(f"Erreur lors de la prédiction: {str(e)}", className="alert alert-danger")