import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    # html.Article([
    #     html.H1('Hello World', className='pico-color-pink-500')
    # ])
])