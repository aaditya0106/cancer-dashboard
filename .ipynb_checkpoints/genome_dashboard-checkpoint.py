# load packages
import pandas as pd
import plotly.express as px
import numpy as np
import requests
from io import StringIO
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

#load data
response = requests.get('https://raw.githubusercontent.com/aaditya0106/cancer-dashboard/data-processing/geneClinicalCleanStageGeneUpdate.csv')
df = pd.read_csv(StringIO(response.text), sep=',')
df = df.drop(columns = ['Unnamed: 0'])
df_drop = df.drop(columns = ['treatment_or_therapy', 'treatment_type'])
df_drop_Clean = df_drop.drop_duplicates()
heatmap_data = df_drop_Clean.pivot_table(
    index='Case',
    columns='Gene',
    values='Expression',
    aggfunc='mean'
)

# Add Cancer Stage as hover information
custom_hover_data = df_drop_Clean.set_index(['Case', 'Gene'])['Cancer Stage']

# Create the heatmap
fig = px.imshow(
    heatmap_data.values,
    labels=dict(x="Gene", y="Case", color="Expression Level"),
    x=heatmap_data.columns,
    y=heatmap_data.index,
    color_continuous_scale="Blues",
    range_color=(-2, 30),
    title="Heatmap of Gene Expression Levels"
)

# Customize hover with Cancer Stage
fig.update_traces(
    hovertemplate=(
        "Gene: %{x}<br>"
        "Case: %{y}<br>"
        "Expression: %{z:.2f}<br>"
        "Cancer Stage: %{customdata}"
    ),
    customdata=custom_hover_data.reset_index().pivot(index='Case', columns='Gene')['Cancer Stage'].values
)

# Update figure size
fig.update_layout(
    width=800,  # Set the width
    height=570,  # Set the height
)

st.plotly_chart(fig)

# filter by a list of genes and cases
case_list = [
    'TCGA-AC-A2QJ', 'TCGA-FA-A7DS', 'TCGA-A2-A4S1', 'TCGA-AR-A5QQ',
    'TCGA-E9-A5FL', 'TCGA-E2-A1LL', 'TCGA-E2-A572', 'TCGA-A7-A56D',
    'TCGA-E2-A1LS', 'TCGA-AC-A2QH'
]

gene_list = [
    'TP53INP1', 'CDH1', 'ALDH1A1', 'CD44', 'CCND1', 'CCND2', 'TOP2A',
    'DUSP4', 'ERBB2', 'ERBB3', 'CDK6', 'LAMP5'
]

# Filter the dataframe based on 'Case' and 'Gene' columns
filtered_df = df_drop_Clean[df_drop_Clean['Case'].isin(case_list) & df_drop_Clean['Gene'].isin(gene_list)]

# Group data and calculate mean expression
aggregated_data = filtered_df.groupby(
    ['Case', 'Cancer Stage', 'ajcc_pathologic_n', 'ajcc_pathologic_m', 'ajcc_pathologic_t', 'ajcc_pathologic_stage'], as_index=False
).agg({'Expression': 'mean'})

# Filter out "Unknown" values for the 'ajcc_pathologic_stage' column in the aggregated_data
filtered_data = aggregated_data[aggregated_data['ajcc_pathologic_stage'] != "Unknown"]

# Ensure 'Cancer Stage' is ordered correctly
sorted_stages = ['Stage I', 'Stage II', 'Stage III']
filtered_data['Cancer Stage'] = pd.Categorical(filtered_data['Cancer Stage'], categories=sorted_stages, ordered=True)

# Count cases by stage
stage_counts = filtered_data['Cancer Stage'].value_counts().sort_index()

# Create a DataFrame for Plotly
plot_data = stage_counts.reset_index()
plot_data.columns = ['Cancer Stage', 'Number of Cases']

# Create a bar plot using Plotly
fig_stage = px.bar(
    plot_data,
    x='Cancer Stage',
    y='Number of Cases',
    text='Number of Cases',
    title='Distribution of Cases by AJCC Pathologic Stage',
    labels={'Cancer Stage': 'AJCC Pathologic Stage', 'Number of Cases': 'Number of Cases'},
)

# Customize plot appearance
fig_stage.update_traces(textposition='outside', marker_color='lightblue', marker_line_color='black', marker_line_width=1)
fig_stage.update_layout(xaxis_title='AJCC Pathologic Stage', yaxis_title='Number of Cases', xaxis_tickangle=45)

# Display the plot
st.plotly_chart(fig_stage)
