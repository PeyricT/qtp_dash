from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np

from guimov._utils import tools as tl
import plotly.express as px


@tl.app.callback(
    Output('dropdown_proteomics_x', 'options'),
    Output('dropdown_proteomics_y', 'options'),
    Input('text_proteome', 'children'),
    prevent_initial_call=True,
)
def update_dropdown_proteomics(_):
    if tl.proteome is None:
        raise PreventUpdate
    
    return tl.proteome.columns, tl.proteome.columns


@tl.app.callback(
    Output('graph_proteomics', 'figure'),
    Input('dropdown_proteomics_x', 'value'),
    Input('dropdown_proteomics_y', 'value'),
    prevent_initial_call=True,
)
def update_graph_proteomics(x, y):
    if x is None or y is None:
        raise PreventUpdate
     
    return px.scatter(
        tl.proteome,
        x = x,
        y = y,
        hover_name = 'Accession',
    )


@tl.app.callback(
    Output('table_proteomics', 'data'),
    Input('graph_proteomics', 'selectedData'),
    prevent_initial_call=True,
)
def update_table_proteomics(selected_data):
    if selected_data is None:
        return []
    
    index_sel = [point['pointIndex'] for point in selected_data['points']]
    data = tl.proteome.loc[index_sel]
    return data.to_dict('records')