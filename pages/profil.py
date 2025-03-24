import dash
from dash import html

dash.register_page(__name__,path='/profil')

layout = html.Div(children=[
    html.Div([
        html.H1('Profil type', className='px-5 py-5'),
        html.Div([
            html.Article([
                html.Div([
                    html.Div(
                        html.I(className='bi bi-heart-pulse-fill pico-color-red-400'),
                        className='pico-background-red-100 p-2 rounded-3 profil-card'
                    ),
                    html.Span('Poids', className='fs-10')
                ], className='d-flex align-items-center gap-2'),
                html.Div([
                    '60-85',
                    html.Span('kg', className='fs-6')
                ], className='fs-3 mt-2 text-muted d-flex align-items-center gap-2')
            ], className='col-12 col-lg-4'),

            html.Article([
                html.Div([
                    html.Div(
                        html.I(className='bi bi-heart-pulse-fill pico-color-red-400'),
                        className='pico-background-red-100 p-2 rounded-3 profil-card'
                    ),
                    html.Span('Groupe   Sanguin', className='fs-10')
                ], className='d-flex align-items-center gap-2'),
                html.Div([
                    'O',
                    html.Span('rh-', className='fs-6')
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
                    '20-35',
                    html.Span('ans', className='fs-6')
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
                    '20-35',
                    html.Span('ans', className='fs-6')
                ], className='fs-3 mt-2 text-muted d-flex align-items-center gap-2')
            ], className='col-12 col-lg-4'),

            html.Article([
                html.Div([
                    html.Div(
                        html.I(className='bi bi-heart-pulse-fill pico-color-red-400'),
                        className='pico-background-red-100 p-2 rounded-3 profil-card'
                    ),
                    html.Span('Antecedent', className='fs-10')
                ], className='d-flex align-items-center gap-2'),
                html.Div([
                    'Non',
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
                    '20-35',
                    html.Span('ans', className='fs-6')
                ], className='fs-3 mt-2 text-muted d-flex align-items-center gap-2')
            ], className='col-12 col-lg-4'),
        ], className='row gap-5 px-5'),
        html.Div([
            html.Button([
                'Condition sante',
                html.I(className='bi bi-arrow-down-circle fs-5 ms-3')
            ], className='col pico-background-red-200 py-1 d-flex align-items-center rounded-0 text-light fw-bold'),
            html.Button([
                'Condition sante',
                html.I(className='bi bi-arrow-down-circle fs-5 ms-3')
            ], className='col pico-background-red-200 py-1 d-flex align-items-center rounded-0 text-light fw-bold'),
            html.Button([
                'Condition sante',
                html.I(className='bi bi-arrow-down-circle fs-5 ms-3')
            ], className='col pico-background-red-200 py-1 d-flex align-items-center rounded-0 text-light fw-bold'),
        ], className='row gap-3 mt-4 px-2')
    ], className='content'),

    html.Div([
        html.Img(src='/assets/front.svg', className='front'),
        html.Img(src='/assets/back.svg', className='back'),
    ], className='image')
], className='profil-container')