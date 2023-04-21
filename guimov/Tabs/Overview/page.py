from .elements import *


layout = html.Div(
    id='over',
    children=[
        tab_title,
        html.Div(
        id='upload',
        children=[
            upload_genome,
            upload_proteome
        ]),
        html.Div(
        id='text',
        children=[
            text_genome,
            text_proteome
        ])
    ],
    style={'display':'flex', 'flex-direction': 'row', 'justify-content': 'space-between','flex-wrap':'wrap'}
)
