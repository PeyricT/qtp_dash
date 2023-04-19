from dash import html, dcc, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc

from guimov._utils import tools as tl


tab_title = html.H2('Genomics')

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
    page_size=5,
    sort_action="native",
    sort_mode="multi",
)