from .elements import *


layout = html.Div(
    className='volcano_plot',
    children=[
        html.Div(
        id='gen', 
        children=[
            tab_title_gen,
            dropdown_genomics_x,
            dropdown_genomics_y,
            graph_genomics,
            table_genomics]),
        html.Div(
        id='prot',
        children=[
            tab_title_prot,
            dropdown_proteomics_x,
            dropdown_proteomics_y,
            graph_proteomics,
            table_proteomics
        ])
    ],
)
