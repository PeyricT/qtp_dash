from .elements import *


layout = html.Div(
    # className="",
    children=[
        tab_title,
        dropdown_genomics_x,
        dropdown_genomics_y,
        graph_genomics,
        table_genomics,
    ],
)
