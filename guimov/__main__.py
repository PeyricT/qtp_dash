from dash import html, dcc
from guimov._utils import tools
import logging

from .Tabs.Overview.page import layout as ov_layout
from .Tabs.Volcano.page import layout as vo_layout
from .Tabs.Multiomics.page import layout as mu_layout

from .Tabs.Overview.callbacks import *
from .Tabs.Volcano.callbacks import *
from .Tabs.Multiomics.callbacks import *

def start(*args, **kwargs):
    """Start the interface

    :param str host: IP to access the interface .Default '0.0.0.0'
    :param str port: Port to access the interface. Default '8585'
    :param bool debug: Launch the interface with debug mode. Default False
    :param args: Parameters pass to Dash.app.run_server
    :param kwargs: Parameters pass to Dash.app.run_server
    :return:
    """

    # Main layout
    tools.app.layout = html.Div(
        # className="guimov_main",
        children=[
            html.Div(
                'QTP Template',
                className='guimov_H1',
            ),
            dcc.Tabs(
                # className="guimov_tabs",
                # parent_className="guimov_parent_tabs",
                # content_className="guimov_content_tabs",
                value='Overview_tab',
                children=[
                    dcc.Tab(id='Overview_tab', label='Overview', value='Overview_tab', children=ov_layout),
                    dcc.Tab(id='Volcano_tab', label='Volcano', value='Volcano_tab', children=vo_layout),
                    dcc.Tab(id='Multiomics_tab', label='Multiomics', value='Multiomics_tab', children=mu_layout),
                ],
                vertical=False,
            )
        ]
    )
    # start the fonction which check users activities
    tools.start_app(*args, **kwargs)


if __name__ == '__main__':
    start(host='0.0.0.0', port='8050')
