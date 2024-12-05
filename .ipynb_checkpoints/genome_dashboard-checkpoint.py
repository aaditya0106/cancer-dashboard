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