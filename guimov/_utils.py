import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash



class Tools:
    """
    Tools contain all variables share in the differents callbacks of GUIMOV.
    When the App is launch the Settings.datasets_path is read to extract metadata about
    the datasets.
    """
    def __init__(self):
        # Dash main object
        self.app = dash.Dash('qtp')
        self.genome = None
        self.proteome = None

    def start_app(self, *args, **kwargs):
        self.app.run_server(*args, debug=True, **kwargs)

 
    @staticmethod
    def plot_sankey(df, source, target):
        """
        Get the observation from a datasets to convert categorical data for Sankey figure
        :param df:
        :param source:
        :param target:
        :return Sankey_plot:
        """
        label = list(df[source].cat.categories)
        label += list(df[target].cat.categories)

        nb1 = len(df[source].cat.categories)
        translate_source = {v: i for i, v in enumerate(df[source].cat.categories)}
        translate_target = {v: i + nb1 for i, v in enumerate(df[target].cat.categories)}

        counts = {}
        splice = df[[source, target]]
        for i in range(df.shape[0]):
            v = tuple(splice.iloc[i])
            counts[v] = counts.get(v, 0) + 1

        node_value = list(counts.values())
        node_source = [translate_source[cl[0]] for cl in counts.keys()]
        node_target = [translate_target[cl[1]] for cl in counts.keys()]

        fig = go.Figure(data=[go.Sankey(
            orientation="v",
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=label,
            ),
            link=dict(
                source=node_source,
                target=node_target,
                value=node_value,
            ))])

        return fig

    @staticmethod
    def full_heatmap(adata, rank_test, nb_genes):
        #
        #   CREATE SUBPLOT
        #

        from plotly.subplots import make_subplots
        fig = make_subplots(rows=10, cols=2, column_widths=[0.04, 0.96], vertical_spacing=0.02, horizontal_spacing=0.01,
                            specs=[
                                [{'rowspan': 9}, {'rowspan': 9}],
                                [None, None, ],
                                [None, None, ],
                                [None, None, ],
                                [None, None, ],
                                [None, None, ],
                                [None, None, ],
                                [None, None, ],
                                [None, None, ],
                                [{'rowspan': 1}, {'rowspan': 1}]
                            ])

        #
        #  HEATMAP
        #

        nb_cells = adata.shape[0]
        pslice = 5000 / nb_cells if nb_cells > 5000 else 0.99

        data = adata[
            np.random.choice([True, False], adata.shape[0], p=[pslice, 1 - pslice])
        ]
        # on trie les cellules par clusters pour une heatmap plus claire
        clusters = data.uns[rank_test]['params']['groupby']
        label = [f"{cl} ({round(k * (1 / pslice))})" for k, cl in
                enumerate(pd.Series.sort_values(data.obs[clusters]).values)]
        cells = pd.Series.sort_values(data.obs[clusters]).index
        sort_data = data[cells]

        genes_label = []
        genes = []
        genes_id = []
        i = 0
        for clust in sort_data.uns[rank_test]['names'].dtype.names:
            for gene in sort_data.uns[rank_test]['names'][clust][:nb_genes]:
                if gene not in genes:
                    genes_label.append(gene)
                    genes.append(gene)
                    genes_id.append(i)
                    i += 1
                else:
                    ind = genes.index(gene)
                    genes_id.append(genes_id[ind])
                    while gene in genes_label:
                        gene += ' '
                    genes_label.append(gene)

        df = pd.DataFrame([], index=sort_data.obs_names, columns=genes_label)
        array = sort_data[:, genes].X.toarray().transpose()
        for k in range(len(genes_label)):
            df[genes_label[k]] = array[genes_id[k]]

        heatmap = go.Heatmap(
            z=df.to_numpy(),
            x=df.columns,
            y=label,
            showlegend=False,
            type='heatmap',
            colorscale='Viridis')

        #
        #    CREATE LEFT COLOR LABEL BAR
        #

        clusters_col = adata.obs[clusters]
        nbcl = len(adata.obs[clusters].cat.categories)
        len_cl = []
        for cl in clusters_col.cat.categories:
            len_cl.append((clusters_col == cl).sum())

        x = [0, 1]
        y = [0]
        for size in len_cl:
            y.append(y[-1] + size)

        color = go.Heatmap(
            x=x,
            y=-np.sort(-np.array(y)),
            z=[[n] for n in range(len(clusters_col.cat.categories) - 1, -1, -1)],
            text=[[cl_name] for cl_name in list(clusters_col.cat.categories)[::-1]],
            texttemplate="%{text}",
            showscale=False,
            # showticklabels=False,
            colorscale=[[i / 23, px.colors.qualitative.Light24[i]] for i in range(24)],
        )

        #
        #    CREATE BOTTOM LABEL COLOR BAR
        #

        Z = []
        for i in range(nbcl):
            Z += [i] * nb_genes

        Text = []
        for i in range(nbcl):
            tmp = [clusters_col.cat.categories[i] if j == nb_genes // 2 else '' for j in range(nb_genes)]

            Text += tmp

        cl_heatmap = go.Heatmap(
            x=df.columns,
            y=['clusters'],
            z=[Z],
            text=[Text],
            texttemplate="%{text}",
            showscale=False,
            # showticklabels=False,
            colorscale=[[i / 23, px.colors.qualitative.Light24[i]] for i in range(24)]
        )

        #
        #    ADD TRACES
        #

        fig.add_trace(color, row=1, col=1)
        fig.add_trace(heatmap, row=1, col=2)
        fig.add_trace(cl_heatmap, row=10, col=2)
        fig.update_yaxes(title='y', visible=False, showticklabels=False)
        fig.update_xaxes(title='x', visible=False, showticklabels=False, row=1)
        fig.update_xaxes(title='x', visible=False, showticklabels=False, row=1, col=1)
        fig.update_xaxes(tickangle=0, row=10, col=10)

        return fig

    @staticmethod
    def low_heatmap(data, rank_test, nb_genes):

        # in order to be more efficient, we keep only 5000 cells max
        # they are choosen randomly so the results is representative
        nb_cells = data.shape[0]
        pslice = 5000/nb_cells if nb_cells > 5000 else 0.99

        sort_data = data[
            np.random.choice([True, False], data.shape[0], p=[pslice, 1-pslice])
        ]

        # the expression of top gene of each marker is gather in a DataFrame
        # 1 gene can be in top of multiples genes but Dataframe have unique column names
        # so we need to do some trick adding space after gene name
        # we also need to keep the old name of the gene to get his expression
        genes_label = []
        genes = []
        genes_id = []
        i = 0
        for clust in sort_data.uns[rank_test]['names'].dtype.names:
            for gene in sort_data.uns[rank_test]['names'][clust][:nb_genes]:
                if gene not in genes:
                    genes_label.append(gene)
                    genes.append(gene)
                    genes_id.append(i)
                    i += 1
                else:
                    ind = genes.index(gene)
                    genes_id.append(genes_id[ind])
                    while gene in genes:
                        gene += ' '
                    genes_label.append(gene)

        df = pd.DataFrame([], index=sort_data.obs_names, columns=genes_label)
        array = sort_data[:, genes].X.toarray().transpose()
        for k in range(len(genes_label)):
            df[genes_label[k]] = array[genes_id[k]]

        return px.imshow(df, aspect="auto", labels=dict(y='Clusters'))


tools = Tools()
