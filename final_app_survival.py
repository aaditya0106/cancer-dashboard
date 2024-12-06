import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats
from lifelines import KaplanMeierFitter
from PIL import Image

#st.set_page_config(page_title="Breast Cancer Dashboard", layout="wide")

min_year, max_year = 1975, 2021

age_group_options = [
    '5-14 yrs',
    '15-24 yrs',
    '25-34 yrs',
    '35-44 yrs',
    '45-54 yrs',
    '55-64 yrs',
    '65-74 yrs',
    '75-84 yrs'
    ]

tumor_site_options = [
    'Axillary tail',
    'Breast, NOS',
    'Central portion',
    'Lower-inner quadrant',
    'Lower-outer quadrant',
    'Nipple',
    'Overlapping lesion',
    'Upper-inner quadrant',
    'Upper-outer quadrant'
    ]

stage_options= ['I', 'II', 'III', 'IV', 'Unknown']

#@st.cache()
def load_data(path):
    return pd.read_csv(path+'.csv')

def col_filter_options(df, col, remove = set()):
    remove = remove.union({'Unknown'})
    return ['All'] + sorted(list(set(df[col]) - remove))

#img = Image.open("ribbon.png")

def survival_dashboard():
    # Sidebar filters
    if st.sidebar.button('Home'):
        st.session_state.page = 'Home'
        st.experimental_rerun()
    st.sidebar.title("Filters")
    year_range = st.sidebar.slider("Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))
    age_groups_selected = st.sidebar.multiselect("Age Groups", age_group_options)
    tumor_sites_selected = st.sidebar.multiselect("Tumor Site", tumor_site_options)
    stage_selected = st.sidebar.multiselect("Stage", stage_options)

    # Apply filters
    def filter_df(df):
        print(df.head())
        print(year_range)
        if 'year_of_diagnosis' in df.columns:
            df = df[
                (df["year_of_diagnosis"] >= year_range[0]) &
                (df["year_of_diagnosis"] <= year_range[1])
            ]
        print(df.shape)
        if 'age_group' in df.columns and age_groups_selected:
            df = df[df["age_group"].isin(age_groups_selected)]
        print(age_groups_selected)
        print(df.shape)
        if 'tumor_site' in df.columns and tumor_sites_selected:
            df = df[df["tumor_site"].isin(tumor_sites_selected)]
        print(tumor_sites_selected)
        print(df.shape)
        if 'adjusted_ajcc_6th_stage' in df.columns and stage_selected:
            df = df[df["adjusted_ajcc_6th_stage"].isin(stage_selected)]
        print(stage_selected)
        print(df.shape)
        return df

    # filter all dfs
    demographics_df = load_data('patients by year and age')
    demographics_df.year_of_diagnosis = demographics_df.year_of_diagnosis.astype(int)
    demographics_df.age_group = demographics_df.age_group.astype(str)
    demographics_df = filter_df(demographics_df)

    alluvial_data = load_data('laterality vs tumor site alluvial')
    alluvial_data = filter_df(alluvial_data)

    radar_data = load_data('age vs site radar data')
    radar_data = radar_data.melt(id_vars='age_group', var_name='tumor_site', value_name='count')
    radar_data = filter_df(radar_data)

    # Create Tabs
    st.markdown("<div style='margin-top: 0px;'></div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Demographics", "Tumor Characteristics", "Survival Analysis"])

    with tab1:
        st.subheader("Number of Patients by Year and Age Group")
        print(demographics_df.head())
        df1 = demographics_df.groupby(['year_of_diagnosis', 'age_group'])['Age'].sum().reset_index()
        print(df1.head())
        print(df1.shape)
        df1 = df1.rename(columns = {'Age' : 'Number of Patients', 'year_of_diagnosis' : 'Year of Diagnosis', 'age_group' : 'Age Group'})
        if not df1.empty:
            fig1 = px.line(
                df1,
                x='Year of Diagnosis',
                y='Number of Patients',
                color='Age Group',
                title='',
                color_discrete_sequence=px.colors.qualitative.T10,
                height=600
            )
            fig1.update_layout(yaxis=dict(tickmode='auto',  nticks=15))
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.write("No data available for the selected filters.")

    with tab2:
        st.subheader("Laterality vs Tumor Site")
        if not alluvial_data.empty:
            labels = list(alluvial_data.laterality.unique()) + list(alluvial_data.tumor_site.unique())
            source = alluvial_data.laterality.apply(lambda x: list(alluvial_data.laterality.unique()).index(x))

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
                    target=alluvial_data['tumor_site'].apply(lambda x: len(alluvial_data.laterality.unique()) + list(alluvial_data.tumor_site.unique()).index(x)),
                    value=alluvial_data['count'],
                    color=[px.colors.qualitative.Pastel[i % len(px.colors.qualitative.Pastel)] for i in source],
                )
            )])
            lateralityfig.update_layout(
                title='',
                font_size=14,
                title_font_size=20,
                #height=600,
                plot_bgcolor='white',
                margin=dict(l=60, r=60, t=30, b=30),
            )
            st.plotly_chart(lateralityfig, use_container_width=True)
        else:
            st.write("No data available for the selected filters.")
        
        st.subheader("Tumor Sites Across Age Groups")
        if not radar_data.empty:
            agefig = px.line_polar(
                radar_data,
                r='count',
                theta='tumor_site',
                color='age_group',
                line_close=True,
                title="",
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
            st.plotly_chart(agefig, use_container_width=True)
        else:
            st.write("No data available for the selected filters.")
        

    with tab3:
        st.subheader("Kaplan-Meier Survival Curves")
        col_map = {
            'Race/Ethnicity' : 'race',
            'Marital Status' : 'marital_status_at_diagnosis',
            'Stage' : 'adjusted_ajcc_6th_stage',
            'Laterality' : 'laterality',
            'Tumor Site' : 'tumor_site',
            'Tumor Size' : 'adjusted_ajcc_6th_t',
            'ER Status' : 'er_status',
            'PR Status' : 'pr_status',
        }

        gap, _ = st.columns([0.4, 0.6])
        with gap:
            chart_col = st.selectbox(
                "Survial Curve by:",
                ['Time (months)', 'Race/Ethnicity', 'Marital Status', 'Stage', 'Laterality', 'Tumor Site', 
                'Tumor Size', 'ER Status', 'PR Status'],
                help=""
            )
        survival_df = load_data('survival df')
        survival_df = survival_df.dropna()
        sdf = filter_df(survival_df)
        sdf.survival_months = sdf.survival_months.astype(int)

        # If there's no survival data after filtering, just skip
        if sdf.empty:
            st.write("No survival data available with current filters.")
        else:
            kmf = KaplanMeierFitter()
            if chart_col == 'Time (months)':
                kmf.fit(sdf.survival_months, event_observed=(sdf.vital_status == 'Dead'))
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=kmf.survival_function_.index,
                    y=kmf.survival_function_['KM_estimate'],
                    mode='lines',
                    name='Survival Probability'
                ))
            else:
                fig = go.Figure()
                col = col_map[chart_col]
                for val in set(sdf[col].unique()) - {'Unknown', 'unknown'}:
                    x = sdf[sdf[col] == val]
                    kmf.fit(
                        x.survival_months, 
                        event_observed=(x.vital_status == 'Dead')
                    )
                    fig.add_trace(go.Scatter(
                        x=kmf.survival_function_.index,
                        y=kmf.survival_function_['KM_estimate'],
                        mode='lines',
                        name=val,
                        line=dict(width=2)
                    ))
                    fig.add_trace(go.Scatter(
                        x=list(kmf.confidence_interval_.index) + list(kmf.confidence_interval_.index[::-1]),
                        y=list(kmf.confidence_interval_['KM_estimate_lower_0.95']) + 
                        list(kmf.confidence_interval_['KM_estimate_upper_0.95'][::-1]),
                        fill='toself',
                        fillcolor='rgba(0,100,250,0.07)',
                        line=dict(width=0),
                        hoverinfo="skip",
                        showlegend=False,
                    ))

            fig.update_layout(
                title='Kaplan-Meier Survival Curve by ' + chart_col,
                xaxis_title='Survival Time (Months)',
                yaxis_title='Survival Probability',
                template='plotly_white',
                hovermode='x unified',
                legend_title=chart_col,
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
