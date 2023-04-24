from dash import html, dcc, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_daq as daq

from guimov._utils import tools as tl


tab_title_gen = html.H2('Genomics')

graph_genomics = dcc.Graph(
    id='graph_genomics',
)

dropdown_genomics_x = dcc.Dropdown(
        id='dropdown_genomics_x',
        placeholder='X axis',
)

dropdown_genomics_y = dcc.Dropdown(
        id='dropdown_genomics_y',
        placeholder='Y axis',
)

table_genomics = dash_table.DataTable(
    id = 'table_genomics',
    style_cell={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0
    },
    page_size=5,
    sort_action="native",
    sort_mode="multi",
)


tab_title_prot = html.H2('Proteomics')

graph_proteomics = dcc.Graph(
    id='graph_proteomics',
)

dropdown_proteomics_x = dcc.Dropdown(
        id='dropdown_proteomics_x',
        placeholder='X axis',
)

dropdown_proteomics_y = dcc.Dropdown(
        id='dropdown_proteomics_y',
        placeholder='Y axis',
)

table_proteomics = dash_table.DataTable(
    id = 'table_proteomics',
    style_cell={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0
    },
    page_size=5,
    sort_action="native",
    sort_mode="multi",
)

switch_log_genome = daq.BooleanSwitch(
    id='switch_log_genome',
    on=True,
    label='log10 Y axis',
)

switch_log_proteome = daq.BooleanSwitch(
    id='switch_log_proteome',
    on=True,
    label='log10 Y axis',
)