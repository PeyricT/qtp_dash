from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import base64
import io

import pandas as pd
import numpy as np

from guimov._utils import tools as tl


@tl.app.callback(
    Output('text_genome', 'children'),
    Input('upload_genome', 'contents'),
    prevent_initial_call=True,
)
def load_genome(content):
    if content is None:
        raise PreventUpdate
    
    decoded = base64.b64decode(content.split(',')[1])

    tl.genome = pd.read_csv(io.StringIO(decoded.decode('UTF-8')), index_col=None, header=0, sep='\t', decimal=',', engine='python')
    return f"{tl.genome.shape[0]} genes with {tl.genome.shape[1]} columns"

@tl.app.callback(
    Output('text_proteome', 'children'),
    Input('upload_proteome', 'contents'),
    prevent_initial_call=True,
)
def load_proteome(content):
    if content is None:
        raise PreventUpdate
    
    decoded = base64.b64decode(content.split(',')[1])
    tl.proteome = pd.read_csv(io.StringIO(decoded.decode('UTF-8')), index_col=None, header=0, sep='\t', decimal=',', engine='python')
    return f"{tl.proteome.shape[0]} proteins with {tl.proteome.shape[1]} columns"

