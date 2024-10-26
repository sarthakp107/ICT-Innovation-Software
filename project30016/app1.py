import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the datasets
df_techniques_and_tactics = pd.read_csv("data/Techniques_and_Tactics.csv")
df_techniques_and_groups = pd.read_csv("data/Techniques_and_Groups.csv")
df_techniques_and_software = pd.read_csv("data/Techniques_and_Software.csv")

# Sidebar for modular navigation
st.sidebar.title("Modular Threat Mapping Dashboard")
selected_module = st.sidebar.selectbox("Select Module", ["Techniques and Tactics", "Techniques and Groups", "Techniques and Software"])

# Module 1: Techniques and Tactics
if selected_module == "Techniques and Tactics":
    st.title("Techniques and Tactics")
    selected_tactic = st.sidebar.selectbox("Select Tactic", df_techniques_and_tactics['tactics'].unique())
    
    # Use Pandas to filter the data based on the selected tactic
    filtered_tactics_data = df_techniques_and_tactics[df_techniques_and_tactics['tactics'] == selected_tactic]
    
    # Aggregate data
    techniques_count = filtered_tactics_data.groupby('name').size().reset_index(name='count')
    
    # Use Plotly to create a bar chart to display the number of techniques under each tactic
    st.write(f"Techniques used under {selected_tactic}")
    fig_tactics = px.bar(techniques_count, x='name', y='count', title=f'Techniques under {selected_tactic}', 
                         labels={'name': 'Technique', 'count': 'Count'}, text='count')
    
    # Optimize chart for responsiveness
    fig_tactics.update_layout(autosize=True, margin=dict(l=50, r=50, t=50, b=50))
    st.plotly_chart(fig_tactics)

# Module 2: Techniques and Groups
elif selected_module == "Techniques and Groups":
    st.title("Techniques and Groups")
    selected_group = st.sidebar.selectbox("Select Group", df_techniques_and_groups['source name'].unique())
    
    # Use Pandas to filter data based on the selected group
    filtered_groups_data = df_techniques_and_groups[df_techniques_and_groups['source name'] == selected_group]
    
    # Aggregate data
    techniques_per_group = filtered_groups_data.groupby('target name').size().reset_index(name='count')
    
    # Use Plotly to create a bar chart to display techniques used by the selected group
    st.write(f"Techniques used by {selected_group}")
    fig_groups = px.bar(techniques_per_group, x='target name', y='count', title=f'Techniques used by {selected_group}', 
                        labels={'target name': 'Techniques', 'count': 'Count'}, text='count')
    
    # Optimize chart for responsiveness
    fig_groups.update_layout(autosize=True, margin=dict(l=50, r=50, t=50, b=50))
    st.plotly_chart(fig_groups)

# Module 3: Techniques and Software
elif selected_module == "Techniques and Software":
    st.title("Techniques and Software")
    selected_software = st.sidebar.selectbox("Select Software", df_techniques_and_software['name_software'].unique())
    
    # Use Pandas to filter the data based on the selected software
    filtered_software_data = df_techniques_and_software[df_techniques_and_software['name_software'] == selected_software]
    
    # Aggregate data
    techniques_per_software = filtered_software_data.groupby('name_technique').size().reset_index(name='count')
    
    # Use Plotly to create a bubble chart for techniques supported by the selected software
    st.write(f"Techniques supported by {selected_software}")
    fig_software = px.scatter(techniques_per_software, x='name_technique', y='count', size='count', title=f'Techniques supported by {selected_software}', 
                              labels={'name_technique': 'Technique', 'count': 'Count'}, text='count')
    
    # Optimize chart for responsiveness
    fig_software.update_layout(autosize=True, margin=dict(l=50, r=50, t=50, b=50))
    st.plotly_chart(fig_software)

# Sidebar footer
st.sidebar.markdown("### Explore specific aspects of the MITRE ATT&CK dataset by selecting a module.")