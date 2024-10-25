import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import random

# Load datasets
df_techniques_and_tactics = pd.read_csv("/Users/sarthakpradhan/Desktop/UNI/ICT-Innovation-Software/project30016/dada/Techniques_and_Tactics.csv")
df_techniques_and_groups = pd.read_csv("/Users/sarthakpradhan/Desktop/UNI/ICT-Innovation-Software/project30016/dada/Techniques_and_Groups.csv")
df_techniques_and_software = pd.read_csv("/Users/sarthakpradhan/Desktop/UNI/ICT-Innovation-Software/project30016/dada/Techniques_and_Software.csv")

# Sidebar for modular navigation
st.sidebar.title("Modular Threat Mapping Dashboard")
selected_module = st.sidebar.selectbox("Select Module", ["Top Techniques", "Software Usage", "Adversary Group Analysis", "Relationship Analysis", "Combined Techniques, Groups, and Tactics"])

# Initialize session state for selected techniques and groups
if 'selected_techniques' not in st.session_state:
    all_techniques = df_techniques_and_tactics['name'].unique()
    st.session_state.selected_techniques = random.sample(list(all_techniques), 5)
if 'default_groups' not in st.session_state:
    unique_groups = df_techniques_and_groups['name_group'].unique()
    st.session_state.default_groups = random.sample(list(unique_groups), 5)

# Helper function to convert Plotly figure to a PDF file for download
def get_pdf_download_link(fig, filename):
    img_bytes = pio.to_image(fig, format='pdf')
    return st.download_button(f"Download {filename} Visualization as PDF", img_bytes, f"{filename}.pdf", "application/pdf")

# Top Techniques Visualization Module
if selected_module == "Top Techniques":
    st.title("Top Techniques Across Groups")
    top_techniques = df_techniques_and_groups.groupby('target name').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    fig_top = px.bar(top_techniques, x='target name', y='count', title="Top 10 Techniques", labels={'target name': 'Technique', 'count': 'Occurrences'})
    st.plotly_chart(fig_top)
    get_pdf_download_link(fig_top, "Top_Techniques")

# Software Usage Visualization Module
elif selected_module == "Software Usage":
    st.title("Software Usage Across Techniques")
    software_usage = df_techniques_and_software.groupby('name_software').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    fig_software = px.bar(software_usage, x='name_software', y='count', title="Top 10 Software", labels={'name_software': 'Software', 'count': 'Occurrences'})
    st.plotly_chart(fig_software)
    get_pdf_download_link(fig_software, "Software_Usage")

# Adversary Group Analysis Module
elif selected_module == "Adversary Group Analysis":
    st.title("Adversary Group Usage Across Techniques")
    group_usage = df_techniques_and_groups.groupby('source name').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    fig_group = px.bar(group_usage, x='source name', y='count', title="Top 10 Adversary Groups", labels={'source name': 'Adversary Group', 'count': 'Occurrences'})
    st.plotly_chart(fig_group)
    get_pdf_download_link(fig_group, "Group_Usage")

# Relationship Analysis Module
elif selected_module == "Relationship Analysis":
    st.title("Relationship Between Techniques, Tactics, and Software")
    selected_techniques = st.multiselect("Select techniques to compare (default 5 random):", options=all_techniques, default=st.session_state.selected_techniques)
    st.session_state.selected_techniques = selected_techniques if selected_techniques else st.session_state.selected_techniques

    filtered_tactics_data = df_techniques_and_tactics[df_techniques_and_tactics['name'].isin(st.session_state.selected_techniques)]
    filtered_groups_data = df_techniques_and_groups[df_techniques_and_groups['target name'].isin(st.session_state.selected_techniques)]
    filtered_software_data = df_techniques_and_software[df_techniques_and_software['name_technique'].isin(st.session_state.selected_techniques)]

    fig_stacked = px.bar(filtered_tactics_data.groupby(['tactics', 'name']).size().reset_index(name='count'), x='tactics', y='count', color='name', title="Techniques Grouped by Tactics (Stacked Bar Chart)")
    st.plotly_chart(fig_stacked)
    get_pdf_download_link(fig_stacked, "Stacked_Data")

    bar_data = filtered_groups_data.groupby(['target name', 'source name']).size().reset_index(name='count')
    if not bar_data.empty:
        fig_bar = px.bar(bar_data, x='target name', y='count', text='source name', color='source name', title="Techniques vs Adversary Groups (Bar Chart)")
        st.plotly_chart(fig_bar)
        get_pdf_download_link(fig_bar, "Bar_Data")

    fig_treemap = px.treemap(filtered_software_data.groupby(['name_software', 'name_technique']).size().reset_index(name='count'), path=['name_software', 'name_technique'], values='count', color='count', color_continuous_scale=px.colors.sequential.Plasma, title="Techniques by Software (Treemap)")
    fig_treemap.update_traces(textinfo='label+value')
    st.plotly_chart(fig_treemap)
    get_pdf_download_link(fig_treemap, "Treemap_Data")

# Combined Techniques, Groups, and Tactics Module
elif selected_module == "Combined Techniques, Groups, and Tactics":
    st.title("Techniques Grouped by Groups and Tactics")
    selected_groups = st.multiselect("Select groups to display:", options=unique_groups, default=st.session_state.default_groups)
    
    if selected_groups:
        combined_df = pd.merge(df_techniques_and_groups, df_techniques_and_tactics, left_on='name_technique', right_on='name', how='inner')
        filtered_combined_data = combined_df[combined_df['name_group'].isin(selected_groups)]
        aggregated_data = filtered_combined_data.groupby(['name_group', 'tactics']).size().reset_index(name='technique_count')
        fig_combined = px.bar(aggregated_data, x='name_group', y='technique_count', color='tactics', title='Techniques by Group and Tactic', barmode='group', labels={'name_group': 'Group', 'technique_count': 'Number of Techniques', 'tactics': 'Tactic'})
        st.plotly_chart(fig_combined)
        get_pdf_download_link(fig_combined, "Combined_Data")
    else:
        st.warning("No groups selected. Please select a group to display the chart.")
