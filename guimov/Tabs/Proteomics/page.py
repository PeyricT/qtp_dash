from .elements import *


layout = html.Div(
    # className="",
    children=[
        tab_title,
        dropdown_proteomics_x,
        dropdown_proteomics_y,
        graph_proteomics,
        table_proteomics,
    ],
)
