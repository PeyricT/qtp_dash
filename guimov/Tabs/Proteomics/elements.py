from dash import html, dcc, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc

from guimov._utils import tools as tl


tab_title = html.H2('Proteomics')

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
    page_size=5,
    sort_action="native",
    sort_mode="multi",
)