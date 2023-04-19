from .elements import *


layout = html.Div(
    # className=None,
    children=[
        tab_title,
        upload_genome,
        upload_proteome,
        text_genome,
        text_proteome,
    ],
)
