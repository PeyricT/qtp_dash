# QTP_TEMPLATE

QTP is the new interface to visualize transcriptomics et proteomics data of your project. 

## Usage

Clone this repository to your desired directory and install modules of requirements file, with pip install. 
Run this command and copy the link on Firefox to connect you to QTP.

```
python3 start.py
```

# Overview
You can loaded proteomics and transcriptomics data on the first tab : Overview. 
Some your file's metada are available in the table when the file is loaded. A coverage grah display on the bottom of the page.

# Volcano 
On the second tab Volcano, you can display a volcano plot of proteomics and transcriptomics data. 
For Genomics plot, choose **Log2FC** for X axis and **pval_adj** for Y axis. 
For Transcriptomics data, choose **Abundance Ratio (log2) : (T0) / (48h)** for X axis and **Abundance Ratio Adj.P-Value: (T0) / (T48h) for Y axis**. You can choose others exist conditions, to compare.
We advise to select **log10 Y axis**, to have log value for Y axis. 

# Multi-omics