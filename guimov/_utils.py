import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
import numpy as np
import dash
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
import scipy



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

    def venn_to_plotly(self,L_sets,L_labels=None,title=None):
        
        #get number of sets
        n_sets = len(L_sets)
        
        #choose and create matplotlib venn diagramm
        if n_sets == 2:
            if L_labels and len(L_labels) == n_sets:
                v = venn2(L_sets,L_labels)
            else:
                v = venn2(L_sets)
        elif n_sets == 3:
            if L_labels and len(L_labels) == n_sets:
                v = venn3(L_sets,L_labels)
            else:
                v = venn3(L_sets)
        #supress output of venn diagramm
        plt.close()
        
        #Create empty lists to hold shapes and annotations
        L_shapes = []
        L_annotation = []
        
        #Define color list for sets
        #check for other colors: https://css-tricks.com/snippets/css/named-colors-and-hex-equivalents/
        L_color = ['FireBrick','DodgerBlue','DimGrey'] 
        
        #Create empty list to make hold of min and max values of set shapes
        L_x_max = []
        L_y_max = []
        L_x_min = []
        L_y_min = []
        
        for i in range(0,n_sets):
            
            #create circle shape for current set
            
            shape = go.layout.Shape(
                    type="circle",
                    xref="x",
                    yref="y",
                    x0= v.centers[i][0] - v.radii[i],
                    y0=v.centers[i][1] - v.radii[i],
                    x1= v.centers[i][0] + v.radii[i],
                    y1= v.centers[i][1] + v.radii[i],
                    fillcolor=L_color[i],
                    line_color=L_color[i],
                    opacity = 0.75
                )
            
            L_shapes.append(shape)
            
            #create set label for current set
            
            anno_set_label = go.layout.Annotation(
                    xref="x",
                    yref="y",
                    x = v.set_labels[i].get_position()[0],
                    y = v.set_labels[i].get_position()[1],
                    text = v.set_labels[i].get_text(),
                    showarrow=False
            )
            
            L_annotation.append(anno_set_label)
            
            #get min and max values of current set shape
            L_x_max.append(v.centers[i][0] + v.radii[i])
            L_x_min.append(v.centers[i][0] - v.radii[i])
            L_y_max.append(v.centers[i][1] + v.radii[i])
            L_y_min.append(v.centers[i][1] - v.radii[i])
        
        #determine number of subsets
        n_subsets = sum([scipy.special.binom(n_sets,i+1) for i in range(0,n_sets)])
        
        for i in range(0,int(n_subsets)):
            
            #create subset label (number of common elements for current subset
            
            anno_subset_label = go.layout.Annotation(
                    xref="x",
                    yref="y",
                    x = v.subset_labels[i].get_position()[0],
                    y = v.subset_labels[i].get_position()[1],
                    text = v.subset_labels[i].get_text(),
                    showarrow=False
            )
            
            L_annotation.append(anno_subset_label)
            
            
        #define off_set for the figure range    
        off_set = 0.2
        
        #get min and max for x and y dimension to set the figure range
        x_max = max(L_x_max) + off_set
        x_min = min(L_x_min) - off_set
        y_max = max(L_y_max) + off_set
        y_min = min(L_y_min) - off_set
        
        #create plotly figure
        p_fig = go.Figure()
        
        #set xaxes range and hide ticks and ticklabels
        p_fig.update_xaxes(
            range=[x_min, x_max], 
            showticklabels=False, 
            ticklen=0
        )
        
        #set yaxes range and hide ticks and ticklabels
        p_fig.update_yaxes(
            range=[y_min, y_max], 
            scaleanchor="x", 
            scaleratio=1, 
            showticklabels=False, 
            ticklen=0
        )
        
        #set figure properties and add shapes and annotations
        p_fig.update_layout(
            plot_bgcolor='white', 
            margin = dict(b = 0, l = 10, pad = 0, r = 10, t = 40),
            width=800, 
            height=400,
            shapes= L_shapes, 
            annotations = L_annotation,
            title = dict(text = title, x=0.5, xanchor = 'center')
        )

        return p_fig

tools = Tools()
