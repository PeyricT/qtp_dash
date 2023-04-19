from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np

from guimov._utils import tools as tl
import plotly.express as px


@tl.app.callback(
    Output('dropdown_genomics_x', 'options'),
    Output('dropdown_genomics_y', 'options'),
    Input('text_genome', 'children'),
    prevent_initial_call=True,
)
def update_dropdown_genomics(_):
    if tl.genome is None:
        raise PreventUpdate
    
    return tl.genome.columns, tl.genome.columns


@tl.app.callback(
    Output('graph_genomics', 'figure'),
    Input('dropdown_genomics_x', 'value'),
    Input('dropdown_genomics_y', 'value'),
    prevent_initial_call=True,
)
def update_graph_genomics(x, y):
    if x is None or y is None:
        raise PreventUpdate
     
    return px.scatter(
        tl.genome,
        x = x,
        y = y,
        hover_name = 'gene_name',
    )


@tl.app.callback(
    Output('table_genomics', 'data'),
    Input('graph_genomics', 'selectedData'),
    prevent_initial_call=True,
)
def update_table_genomics(selected_data):
    if selected_data is None:
        return []
    
    index_sel = [point['pointIndex'] for point in selected_data['points']]
    data = tl.genome.loc[index_sel]
    return data.to_dict('records')