from dash import html, dcc, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc

from guimov._utils import tools as tl


tab_title = html.H2('Multiomics')

graph_multi = dcc.Graph(
    id='graph_multi',
)

dropdown_gen_fold = dcc.Dropdown(
        id='dropdown_gen_fold',
        placeholder='genomics foldchange',
)

dropdown_prot_fold = dcc.Dropdown(
        id='dropdown_prot_fold',
        placeholder='proteomics foldchange',
)

dropdown_gen_pval = dcc.Dropdown(
        id='dropdown_gen_pval',
        placeholder='genomics pvalue',
)

dropdown_prot_pval = dcc.Dropdown(
        id='dropdown_prot_pval',
        placeholder='proteomics pvalue',
)

slider_pval = dcc.Slider(
    0, 10,
    step = 1,
    value = 1,
    id = 'slider_pval'
)