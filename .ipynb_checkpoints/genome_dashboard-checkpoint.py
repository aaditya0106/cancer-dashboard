# import pandas as pd
# import plotly.express as px
# import requests
# from io import StringIO
# import streamlit as st

# # Load data
# response = requests.get('https://raw.githubusercontent.com/aaditya0106/cancer-dashboard/data-processing/geneClinicalCleanStageGeneUpdate.csv')
# df = pd.read_csv(StringIO(response.text), sep=',')
# df = df.drop(columns = ['Unnamed: 0'])
# df_drop = df.drop(columns = ['treatment_or_therapy', 'treatment_type'])
# df_drop_Clean = df_drop.drop_duplicates()

# # Prepare heatmap data
# heatmap_data = df_drop_Clean.pivot_table(
#     index='Case',
#     columns='Gene',
#     values='Expression',
#     aggfunc='mean'
# )

# # Add Cancer Stage as hover information
# custom_hover_data = df_drop_Clean.set_index(['Case', 'Gene'])['Cancer Stage']

# # Create the heatmap
# fig = px.imshow(
#     heatmap_data.values,
#     labels=dict(x="Gene", y="Case", color="Expression Level"),
#     x=heatmap_data.columns,
#     y=heatmap_data.index,
#     color_continuous_scale="Blues",
#     range_color=(-2, 30),
#     title="Heatmap of Gene Expression Levels"
# )

# # Customize hover with Cancer Stage
# fig.update_traces(
#     hovertemplate=(
#         "Gene: %{x}<br>"
#         "Case: %{y}<br>"
#         "Expression: %{z:.2f}<br>"
#         "Cancer Stage: %{customdata}"
#     ),
#     customdata=custom_hover_data.reset_index().pivot(index='Case', columns='Gene')['Cancer Stage'].values
# )

# # Update figure size
# fig.update_layout(
#     width=800,  # Set the width
#     height=570,  # Set the height
# )

# # Display the heatmap with interactive selection
# selected_data = st.plotly_chart(fig, use_container_width=True)

# # Always display the bar plot with all cases initially
# def get_bar_plot(df_drop_Clean):
#     # Group data and calculate mean expression
#     aggregated_data = df_drop_Clean.groupby(
#         ['Case', 'Cancer Stage', 'ajcc_pathologic_n', 'ajcc_pathologic_m', 'ajcc_pathologic_t', 'ajcc_pathologic_stage'], as_index=False
#     ).agg({'Expression': 'mean'})

#     # Filter out "Unknown" values for the 'ajcc_pathologic_stage' column in the aggregated_data
#     filtered_data = aggregated_data[aggregated_data['ajcc_pathologic_stage'] != "Unknown"]

#     # Ensure 'Cancer Stage' is ordered correctly
#     sorted_stages = ['Stage I', 'Stage II', 'Stage III']
#     filtered_data['Cancer Stage'] = pd.Categorical(filtered_data['Cancer Stage'], categories=sorted_stages, ordered=True)

#     # Count cases by stage
#     stage_counts = filtered_data['Cancer Stage'].value_counts().sort_index()

#     # Create a DataFrame for Plotly
#     plot_data = stage_counts.reset_index()
#     plot_data.columns = ['Cancer Stage', 'Number of Cases']

#     # Create a bar plot using Plotly
#     fig_stage = px.bar(
#         plot_data,
#         x='Cancer Stage',
#         y='Number of Cases',
#         text='Number of Cases',
#         title='Distribution of Cases by AJCC Pathologic Stage',
#         labels={'Cancer Stage': 'AJCC Pathologic Stage', 'Number of Cases': 'Number of Cases'},
#     )

#     # Customize plot appearance
#     fig_stage.update_traces(textposition='outside', marker_color='lightblue', marker_line_color='black', marker_line_width=1)
#     fig_stage.update_layout(xaxis_title='AJCC Pathologic Stage', yaxis_title='Number of Cases', xaxis_tickangle=45)

#     return fig_stage

# # Initially display all cases
# fig_stage = get_bar_plot(df_drop_Clean)
# st.plotly_chart(fig_stage)

# # Debugging: Explicitly check if selectedData exists in session_state
# if 'selectedData' in st.session_state:
#     st.write("Selected Data exists in session state.")
#     selected_data = st.session_state.selectedData
#     st.write(selected_data)
# else:
#     st.write("No selected data in session state.")


# # Check for selected data from the heatmap
# if 'selectedData' in st.session_state:
#     selected_data = st.session_state.selectedData
    
#     # Extract selected cases and genes
#     selected_cases = [point['y'] for point in selected_data['points']]
#     selected_genes = [point['x'] for point in selected_data['points']]

#     # Filter the dataframe based on selected 'Case' and 'Gene' values
#     filtered_df = df_drop_Clean[df_drop_Clean['Case'].isin(selected_cases) & df_drop_Clean['Gene'].isin(selected_genes)]

#     # Update the bar plot to reflect the filtered data
#     fig_stage = get_bar_plot(filtered_df)
#     st.plotly_chart(fig_stage)

import pandas as pd
import plotly.express as px
import requests
from io import StringIO
import streamlit as st

# Load data
response = requests.get('https://raw.githubusercontent.com/aaditya0106/cancer-dashboard/data-processing/geneClinicalCleanStageGeneUpdate.csv')
df = pd.read_csv(StringIO(response.text), sep=',')
df = df.drop(columns = ['Unnamed: 0'])
df_drop = df.drop(columns = ['treatment_or_therapy', 'treatment_type'])
df_drop_Clean = df_drop.drop_duplicates()

# Prepare heatmap data
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

# Display the heatmap with interactive selection
selected_data = st.plotly_chart(fig, use_container_width=True)

# Capture selected data and store it in session_state
if selected_data:
    selected_cases = [point['y'] for point in selected_data['points']]
    selected_genes = [point['x'] for point in selected_data['points']]
    st.session_state.selectedData = selected_data  # Store in session state

# Debugging: Check if selected data is being stored in session state
if 'selectedData' in st.session_state:
    st.write("Selected Data:", st.session_state.selectedData)
else:
    st.write("No selected data in session state.")

