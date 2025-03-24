import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

FILE_PATH = 'data/dataset.xlsx'
SHEET_NAME = 'Donneurs 2019'

dash.register_page(__name__,path='/profil')
donneurs = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)

bins = [18, 25, 35, 45, 55, 65, 100]
labels = ["18-25", "26-35", "36-45", "46-55", "56-65", "66+"]
donneurs["Groupe d'Age"] = pd.cut(donneurs['Age '], bins=bins, labels=labels, right=False)

@callback(
    Output('donation-chart', 'figure'),
    [Input('age-dropdown', 'value'),
    Input('blood-group-dropdown', 'value')]
)
def update_chart(selected_age, selected_bg):
    df_filtered = donneurs[(donneurs["Groupe d'Age"] == selected_age) & (donneurs['Groupe Sanguin ABO / Rhesus '] == selected_bg)]

    fig = px.bar(df_filtered, x="Type de donation ", color='Sexe', title='Répartition par type de donation et sexe')
    return fig


layout = html.Div(children=[
    html.Div([
        html.H1('Profil type', className='px-5 py-4'),
        html.Div([
            html.Article([
                html.Div([
                    html.Div(
                        html.I(className='bi bi-heart-pulse-fill pico-color-red-400'),
                        className='pico-background-red-100 p-2 rounded-3 profil-card'
                    ),
                    html.Span('Groupe   Sanguin', className='fs-10')
                ], className='d-flex align-items-center gap-2'),
                html.Div([
                    donneurs['Groupe Sanguin ABO / Rhesus '].mode(dropna=True)[0],
                    html.Span('', className='fs-6')
                ], className='fs-3 mt-2 text-muted d-flex align-items-center gap-2')
            ], className='col-12 col-lg-4'),

            html.Article([
                html.Div([
                    html.Div(
                        html.I(className='bi bi-heart-pulse-fill pico-color-red-400'),
                        className='pico-background-red-100 p-2 rounded-3 profil-card'
                    ),
                    html.Span('Age', className='fs-10')
                ], className='d-flex align-items-center gap-2'),
                html.Div([
                    f'{donneurs['Age '].mean():.0f}',
                    html.Span('ans', className='fs-6')
                ], className='fs-3 mt-2 text-muted d-flex align-items-center gap-2')
            ], className='col-12 col-lg-4'),

            html.Article([
                html.Div([
                    html.Div(
                        html.I(className='bi bi-heart-pulse-fill pico-color-red-400'),
                        className='pico-background-red-100 p-2 rounded-3 profil-card'
                    ),
                    html.Span('Sexe', className='fs-10')
                ], className='d-flex align-items-center gap-2'),
                html.Div([
                    'Homme' if  donneurs['Sexe'].mode(dropna=True)[0] == 'M' else 'Femme',
                    html.Span('', className='fs-6')
                ], className='fs-3 mt-2 text-muted d-flex align-items-center gap-2')
            ], className='col-12 col-lg-4'),

            html.Article([
                html.Div([
                    html.Div(
                        html.I(className='bi bi-heart-pulse-fill pico-color-red-400'),
                        className='pico-background-red-100 p-2 rounded-3 profil-card'
                    ),
                    html.Span('Type de donation', className='fs-10')
                ], className='d-flex align-items-center gap-2'),
                html.Div([
                    donneurs['Type de donation '].mode(dropna=True)[0],
                    html.Span('', className='fs-6')
                ], className='fs-3 mt-2 text-muted d-flex align-items-center gap-2')
            ], className='col-12 col-lg-4'),
        ], className='row gap-1 px-5'),

        html.Div([
            html.Div([
                html.Div([
                    html.Label('Age',  className='fs-10'),
                    dcc.Dropdown(
                        id='age-dropdown',
                        options=[{'label': age, 'value': age} for age in labels],
                        value='18-25',
                        clearable=False,
                    )
                ], className='col-12 col-lg-5'),

                html.Div([
                    html.Label('Group sanguin', className='fs-10'),
                    dcc.Dropdown(
                        id='blood-group-dropdown',
                        options=[{'label': bg, 'value': bg} for bg in donneurs['Groupe Sanguin ABO / Rhesus '].unique()],
                        value=donneurs['Groupe Sanguin ABO / Rhesus '].unique()[0],
                        clearable=False
                    )
                ], className='col-12 col-lg-5')
            ], className='row gap-4'),

            html.Div(
                dcc.Graph(id='donation-chart'),
            )

        ], className='mt-2')
       
    ], className='content'),

    html.Div([
        html.Img(src='/assets/front.svg', className='front'),
        html.Img(src='/assets/back.svg', className='back'),
    ], className='image')
], className='profil-container')