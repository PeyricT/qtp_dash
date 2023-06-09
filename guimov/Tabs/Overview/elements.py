from dash import html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc

from guimov._utils import tools as tl


tab_title = html.H2('Overview')

tab_title = html.H2('Load your data',
    id="title")

upload_genome = dcc.Upload(
    id='upload_genome',
    children=html.Div([
        html.H3('Transcriptomics data'),
        'Genome drag and drop or ',
        html.A('Select File'),
    ]),
)

upload_proteome = dcc.Upload(
    id='upload_proteome',
    className='up',
    children=html.Div([
        html.H3('Proteomics data'),
        'Proteome drag and drop or ',
        html.A('Select File'),
    ]),
)

text_genome = html.Div(
    id="text_genome",
    className='text',
)

text_proteome = html.Div(
    id="text_proteome",
    className='text',
)

venn_diagram = dcc.Graph(
    id="venn_diagram",
    className='VennHide',
)