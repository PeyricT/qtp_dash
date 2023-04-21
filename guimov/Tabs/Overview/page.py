from .elements import *


layout = html.Div(
    className='over',
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
)
