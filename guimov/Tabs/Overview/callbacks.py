from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import base64
import io
from dash import html, dcc

import pandas as pd
import numpy as np

from guimov._utils import tools as tl


@tl.app.callback(
    Output('text_genome', 'children'),
    Input('upload_genome', 'contents'),
    State('upload_genome', 'filename'),
    prevent_initial_call=True,
)
def load_genome(content,filename):
    if content is None:
        raise PreventUpdate
    
    decoded = base64.b64decode(content.split(',')[1])

    tl.genome = pd.read_csv(io.StringIO(decoded.decode('UTF-8')), index_col=None, header=0, sep='\t', decimal=',', engine='python')
    # file=io.StringIO(decoded.decode('UTF-8'))
    # file_name=file.read()
    return html.Div([
        html.H4(('Metadata'), style={'text-decoration': 'underline'}),
        html.Table([
            html.Tr([html.Th('Name'),html.Td(filename)]),
            html.Tr([html.Th('Genes'),html.Td(tl.genome.shape[0])]),
            html.Tr([html.Th('Columns'),html.Td(tl.genome.shape[1])])
        ]),
    ])

@tl.app.callback(
    Output('text_proteome', 'children'),
    Input('upload_proteome', 'contents'),
    State('upload_proteome','filename'),
    prevent_initial_call=True,
)
def load_proteome(content,filename):
    if content is None:
        raise PreventUpdate
    
    decoded = base64.b64decode(content.split(',')[1])
    tl.proteome = pd.read_csv(io.StringIO(decoded.decode('UTF-8')), index_col=None, header=0, sep='\t', decimal=',', engine='python')
    return html.Div([
        html.H4(('Metadata'), style={'text-decoration': 'underline'}),
        html.Table([
            html.Tr([html.Th('Name'),html.Td(filename)]),
            html.Tr([html.Th('Proteins'),html.Td(tl.proteome.shape[0])]),
            html.Tr([html.Th('Colomns'),html.Td(tl.proteome.shape[1])]),
            html.Tr([html.Th('Mean coverage'),html.Td((tl.proteome['Coverage [%]'].mean()),"%")])
        ])
    ])