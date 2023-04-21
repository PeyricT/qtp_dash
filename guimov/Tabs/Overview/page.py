from .elements import *


layout = html.Div(
    id='over',
    children=[
        tab_title,
        upload_genome,
        upload_proteome,
        text_genome,
        text_proteome,
    ],
    style={'display':'flex', 'flex-direction': 'row', 'justify-content': 'space-between','flex-wrap':'wrap'}
)

genome = html.Div(
    id='genome',
    children=[
        upload_genome,
        text_genome
    ]
)

proteome = html.Div(
    id='proteome',
    children=[
        upload_proteome,
        text_proteome
    ]
)