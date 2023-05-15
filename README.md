# QTP project

QTP is the new interface to visualize transcriptomics and proteomics data from your project. It allows to load and visualize your data thanks several different kind of plots. It is also possible to get the coverage between coding protein genes and proteins thanks a curated database. Some plots for multiomics comparaison allow you to visualize the data in common across your dataset.

# QTP Dash

The QTP app project had too many development layers to be accomplish during the project. Especially for the Frontend part, which requiere a deep understanding of typescript, javascript, VUE.js and D3.js. This is the reason why whe choose to develop a demo interface QTP_dash (this repo). QTP_dash is made thanks a python package, already known which allow a quick setup of the plots and an efficient way to handle the provided dataset.

##  Quick start

Clone this repository to your desired directory and install modules of requirements file, with pip install. 
Run this command and copy the link on Firefox to connect you to QTP.

```
python start.py
```

# Interface description

## Overview
You can loaded proteomics and transcriptomics data on the first tab : Overview. Files have to CSV format.
Some your file's metada are available in the table when the file is loaded. A coverage grah display on the bottom of the page.

## Volcano 
On the second tab Volcano, you can display a volcano plot of proteomics and transcriptomics data. 
For Genomics plot, choose **Log2FC** for X axis and **pval_adj** for Y axis. 
For Transcriptomics data, choose **Abundance Ratio (log2) : (T0) / (48h)** for X axis and **Abundance Ratio Adj.P-Value: (T0) / (T48h) for Y axis**. You can choose others exist conditions, to compare.
We advise to select **log10 Y axis**, to have log value for Y axis. 

## Multi-omics
On the third tab Multiomics, you can display the multiomics volcano plot. You have to choose genomics and proteomics foldchange and pvalue. Points display on the plot and represent all genes in common for desired condition. It is possible to change log(10) of the pvalue.


# QTP App

QTP Dash demo belong the QTP Application, firstly develop with javascript, python and redis. At the contrary of the demo, QTP app was made to handle a huge amount of request and can handle a lot of simultaneous connexion. That is why the project use a lot of heavy package, with a 3 layers architecture made to scale the project to a massive use.
The 3 differents layers use differents languages packages and each have a specific objective :

## QTP Services
QTP  Services is link to a custum database made with redis. It allow to handle all genes and proteins from genome and proteome in the database. QTP service is a bench of Flask python server made to interact between redis and the Nest Server. 

repos :
https://github.com/PeyricT/qtp-services
https://github.com/PeyricT/uniprot_redis

## QTP Nest
QTP Nest is a typescript server made with the Nest node js package. It allow to redirect get and post made from the website and link them to the QTP Services. It also use to check the input data and send html/json response. 

repo :
https://github.com/PeyricT/qtp-controller

## QTP Front

The frontend with Dash use CSS and HTML. CSS part is only one file where all classes and id selector are defided whereas HTML part is used by Dash fonction in Python files. 
The _page.py_ file contain the layout which describes what the platform looks like and is composed of a tree of **components** like ```html.Div``` in our file. 
And _elements.py_ file contain all the elements of the layout. 

repo:
https://github.com/PeyricT/qtp-front
