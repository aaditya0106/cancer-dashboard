#!/usr/bin/env python
# coding: utf-8

# In[6]:


import streamlit as st
from streamlit_lottie import st_lottie
import json

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# In[8]:


st.set_page_config(page_title="Breast Cancer Dashboard", layout="wide")


# In[5]:


# Display lottie animation on the landing page
with open('lottie.json', "r") as f:
    lottie_animation = json.load(f)

_, col, _ = st.columns([1,4,1])
with col:
    st_lottie(lottie_animation, height=550, width=900)
    st.write("Explore data-driven insights and visualizations to understand breast cancer better.")


# In[ ]:


# year vs no of patients with age when diagnosed
df1 = pd.read_csv('patients by year and age.csv')
fig = px.line(
        df1,
        x='Year of Diagnosis',
        y='Number of Patients',
        color='Age Group', 
        title='Number of Patients by Year and Age Group',
        labels={'Number of Patients': 'Number of Patients', 'Year': 'Year'},
        color_discrete_sequence=px.colors.qualitative.T10,
        height=600,
        width=800
    )
fig.update_layout(yaxis=dict(tickmode='auto',  nticks=15))

st.title("Journey Begins")
_, col, _ = st.columns([1,4,1])
with col:
    st.plotly_chart(fig)


# In[ ]:


st.title('Age Range Slider')


# In[ ]:


# select agr group range
age_range = st.slider(
    "Select Age Group Range:",
    min_value=0,
    max_value=100,
    value=(20, 50),  # Default range
    step=1
)


# In[ ]:


st.subheader('Tumor Sites Analysis')
age_groups = st.multiselect(
    "Select an Age Group:", 
    options =[f'{i}-{i+9} yrs' for i in range(5, 85, 10)], 
    default = '55-64 yrs'
)


# In[ ]:


alluvial_data = pd.read_csv('laterality vs tumor site alluvial.csv')
al_data = alluvial_data[alluvial_data.age_group.isin(age_groups)].drop(columns = ['age_group'])


# In[ ]:


labels = list(al_data.laterality.unique()) + list(al_data.tumor_site.unique())
source = al_data.laterality.apply(lambda x: list(al_data.laterality.unique()).index(x))

lateralityfig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color='rgba(200,200,200,0.8)'
    ),
    link=dict(
        source=source,
        target=al_data['tumor_site'].apply(lambda x: len(al_data.laterality.unique()) + list(al_data.tumor_site.unique()).index(x)),
        value=al_data['count'],
        color=[px.colors.qualitative.Pastel[i % len(px.colors.qualitative.Pastel)] for i in source],
    )
)])
lateralityfig.update_layout(
    title_text="Laterality vs Tumor Site",
    font_size=14,
    title_font_size=20,
    #height=600,
    plot_bgcolor='white',
    margin=dict(l=60, r=60, t=30, b=30),
)


# In[ ]:


radar_data = pd.read_csv('age vs site radar data.csv')
radar_data_melted = radar_data.melt(id_vars='age_group', var_name='tumor_site', value_name='count')


# In[ ]:


filtered_radar_data = radar_data_melted[radar_data_melted.age_group.isin(age_groups)]
agefig = px.line_polar(
    filtered_radar_data,
    r='count',
    theta='tumor_site',
    color='age_group',
    line_close=True,
    title="Tumor Sites Across Age Groups",
    #height=600,
    #width=600
)
agefig.update_traces(fill='toself')
agefig.update_layout(
    margin=dict(l=50, r=50, t=50, b=50),
    polar=dict(
        angularaxis=dict(tickfont=dict(size=10))
    )
)


# In[ ]:


col1, col2 = st.columns(2, gap = 'medium')
with col1:
    st.plotly_chart(lateralityfig, use_container_width=False)
with col2:
    st.plotly_chart(agefig, use_container_width=False)

