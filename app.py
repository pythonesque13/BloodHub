import dash
from dash import html, dcc, Output, Input
import plotly.express as px
import pandas as pd


app = dash.Dash(__name__, external_stylesheets=[], use_pages=True)

data_pie = pd.DataFrame({
    "Condition de santé": ["Condition 1", "Condition 2", "Condition 3"],
    "Dons": [40, 32, 28]
})

fig_pie = px.pie(data_pie, names="Condition de santé", values="Dons", hole=0.6)

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div([
       html.Div ([
            html.H1([
                # image,
                'BloodHub'
            ], className='pico-color-orange-500'),
            html.Span('Views'),
            html.Nav([
                html.Ul([
                    html.Li(
                        html.A(href='/', children=[
                            html.I(className='bi bi-house-heart'),
                            'Home'
                        ]),
                        id='home-item'
                    ),
                    html.Li(
                        html.A(href='/profil', children=[
                            html.I(className='bi bi-person-bounding-box'),
                            'Profil'
                        ]),
                        id='profil-item'
                    ),
                    html.Li(
                        html.A(href='/ai', children=[
                            html.I(className='bi bi-bar-chart-line-fill'),
                            'IA'
                        ]),
                        id='ia-item'
                    )   
                ])
            ], className='nav'),
       ], className='side-bar'),
        dash.page_container
    ], className='wrapper'),
], )

@app.callback(
    [
        Output('home-item', 'className'),
        Output('profil-item', 'className'),
        Output('ia-item', 'className'),
    ],
    Input('url', 'pathname')
)
def update_active_links(pathname):
    if pathname == '/':
        return 'active', '', ''
    elif pathname == '/profil':
        return '', 'active', ''
    elif pathname == '/ai':
        return '', '', 'active'
    return '', '', ''


app.index_string = '''
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <title>Dash + Pico CSS</title>
    {%metas%}
    {%favicon%}
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    {%css%}
</head>
<body>
    {%app_entry%}
    {%config%}
    {%scripts%}
    {%renderer%}
</body>
</html>
'''

if __name__ == "__main__":
    app.run_server(debug=True)
