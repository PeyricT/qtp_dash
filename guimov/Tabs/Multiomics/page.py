from .elements import *


layout = html.Div(
    className="",
    children=[
        tab_title,
        dropdown_gen_fold,
        dropdown_prot_fold,
        dropdown_gen_pval,
        dropdown_prot_pval,
        graph_multi,
        slider_pval,
    ],
)
