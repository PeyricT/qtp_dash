from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np
from dash import html, dcc

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
    
    cols = [
        x for x in tl.genome.columns
            if tl.genome[x].dtype == int or tl.genome[x].dtype == float
    ]
    return cols, cols


@tl.app.callback(
    Output('graph_genomics', 'figure'),
    Input('dropdown_genomics_x', 'value'),
    Input('dropdown_genomics_y', 'value'),
    Input('switch_log_genome', 'on'),
    prevent_initial_call=True,
)
def update_graph_genomics(x, y, logy):
    if x is None or y is None:
        raise PreventUpdate
    
    if logy:
        tl.genome['temp'] = -np.log10(tl.genome[y])
        y = 'temp'

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
    
    index_sel_gen = [point['pointIndex'] for point in selected_data['points']]
    data_gen = tl.genome.loc[index_sel_gen]
    return data_gen.to_dict('records')


##########################################PROTEO PART#################################################

@tl.app.callback(
    Output('dropdown_proteomics_x', 'options'),
    Output('dropdown_proteomics_y', 'options'),
    Input('text_proteome', 'children'),
    prevent_initial_call=True,
)
def update_dropdown_proteomics(_):
    if tl.proteome is None:
        raise PreventUpdate
    
    cols = [
        x for x in tl.proteome.columns
            if tl.proteome[x].dtype == int or tl.proteome[x].dtype == float
    ]
    return cols, cols


@tl.app.callback(
    Output('graph_proteomics', 'figure'),
    Input('dropdown_proteomics_x', 'value'),
    Input('dropdown_proteomics_y', 'value'),
    Input('switch_log_proteome', 'on'),
    prevent_initial_call=True,
)
def update_graph_proteomics(x, y, logy):
    if x is None or y is None:
        raise PreventUpdate
    
    if logy:
        tl.proteome['temp'] = -np.log10(tl.proteome[y])
        y = 'temp'

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
    
    index_sel_prot = [point['pointIndex'] for point in selected_data['points']]
    data_prot = tl.proteome.loc[index_sel_prot]
    return data_prot.to_dict('records')