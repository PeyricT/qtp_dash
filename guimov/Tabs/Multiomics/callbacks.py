from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np
import plotly.express as px

from guimov._utils import tools as tl


@tl.app.callback(
    Output('dropdown_gen_fold', 'options'),
    Output('dropdown_prot_fold', 'options'),
    Output('dropdown_gen_pval', 'options'),
    Output('dropdown_prot_pval', 'options'),
    Input('text_genome', 'children'),
    Input('text_proteome', 'children'),
    prevent_initial_call=True,
)
def set_dropdrown_options(*_):
    if tl.genome is None or tl.proteome is None:
        raise PreventUpdate
    
    dgf = [col for col in tl.genome.columns if 'FC' in col]
    dgp = [col for col in tl.genome.columns if 'pval' in col]
    dpf = [col for col in tl.proteome.columns if 'Abundance Ratio' in col]
    dpp = [col for col in tl.proteome.columns if 'P-Value' in col]

    gen_temp = tl.genome.copy()
    prot_temp = tl.proteome.copy()

    gen_temp.index = gen_temp['gene_id']
    prot_temp.index = prot_temp['protein_id']

    gen_temp = gen_temp[~gen_temp.index.duplicated(keep='first')]
    prot_temp = prot_temp[~prot_temp.index.duplicated(keep='first')]

    index = list(set(gen_temp.index).intersection(set(prot_temp.index)))
    tl.multi = pd.DataFrame([], index=index)
    
    for col in ['gene_name', *dgf, *dgp]:
        tl.multi[col] = gen_temp[col]

    cols = list(set([*dpf, *dpp]))
    for col in ['Accession', cols]:
        tl.multi[col] = prot_temp[col]

    return dgf, dpf, dgp, dpp


@tl.app.callback(
    Output('graph_multi', 'figure'),
    Input('dropdown_gen_fold', 'value'),
    Input('dropdown_prot_fold', 'value'),
    Input('dropdown_gen_pval', 'value'),
    Input('dropdown_prot_pval', 'value'),
    Input('slider_pval', 'value'),
    prevent_initial_call=True,
)
def update_graph_multi(dgf, dpf, dgp, dpp, pval_cutoff):
    if dgf is None or dpf is None or dgp is None or dpp is None or tl.multi is None:
        raise PreventUpdate
    
    cut = np.exp(-pval_cutoff*np.log(10))
    cut_np = np.logical_and(
        tl.multi[dgp] < cut,
        tl.multi[dpp] < cut,
    )
    filtered = tl.multi[cut_np].copy()

    filtered['color'] = np.log10(filtered[dgp]/filtered[dpp])
    filtered['name'] = filtered['Accession']+' / '+filtered['gene_name']

    return px.scatter(filtered, x=dgf, y=dpf, color='color', hover_name='name', hover_data=[dgf, dgp, dpf, dpp])