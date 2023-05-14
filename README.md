# QTP_TEMPLATE

QTP is the new interface to visualize transcriptomics et proteomics data of your project. It allows to load and visualize plots of your transcriptomics and proteomics data. It is possible to get coverage between genes of data and visualize scatter plot fot multiomics comparaison. 

# Usage

Clone this repository to your desired directory and install modules of requirements file, with pip install. 
Run this command and copy the link on Firefox to connect you to QTP.

```
python3 start.py
```

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


# Development
At the begining, we don't use this platform but an existing platform which has more complete. For the backend, it was two parts **Services** and **Nest Server** which exchange informations between them. It is developed with Python and TypeScrit and used Flask, Redis Server and Nest. For the fronted, it is developed with JavaScript and TypeScrip and used Vue and D3. We worked with this plateform for five weeks and we decided it is not a good idea to continue with JavaScript. We didn't know this language and we couldn't get a good project's final. 
We choose Dash which is a Python package for the demo of the frontend. It isn't for production usage but it is a good template to show what is we can do. 

## Backend



## Frontend
The frontend with Dash use CSS and HTML. CSS part is only one file where all classes and id selector are defided whereas HTML part is used by Dash fonction in Python files. 
The _page.py_ file contain the layout which describes what the platform looks like and is composed of a tree of **components** like ```html.Div``` in our file. 
And _elements.py_ file contain all the elements of the layout. 
