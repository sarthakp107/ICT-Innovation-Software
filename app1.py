import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import random
import io

pio.templates.default = "plotly"

# Load datasets
df_techniques_and_tactics = pd.read_csv("project30016/data/Techniques_and_Tactics.csv")
df_techniques_and_groups = pd.read_csv("project30016/data/Techniques_and_Groups.csv")
df_techniques_and_software = pd.read_csv("project30016/data/Techniques_and_Software.csv")

# Sidebar for modular navigation
st.sidebar.title("Modular Threat Mapping Dashboard")
selected_module = st.sidebar.selectbox("Select Module", ["Top Techniques", "Software Usage", "Adversary Group Analysis", "Relationship Analysis", "Combined Techniques, Groups, and Tactics"])

# Initialize session state for selected techniques to prevent random reselection
if 'selected_techniques' not in st.session_state:
    all_techniques = df_techniques_and_tactics['name'].unique()
    st.session_state.selected_techniques = random.sample(list(all_techniques), 5)

# Function to convert Plotly figure to a PDF file
def get_pdf_download_link(fig):
    img_bytes = pio.to_image(fig, format='pdf')  # Convert the figure to PDF
    return img_bytes

# Module 1: Top Techniques Visualization
if selected_module == "Top Techniques":
    st.title("Top Techniques Across Groups")
    
    top_techniques = df_techniques_and_groups.groupby('target name').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    
    st.write("Displaying top 10 most used techniques across groups")
    fig_top = px.bar(top_techniques, x='target name', y='count', title="Top 10 Techniques", labels={'target name': 'Technique', 'count': 'Occurrences'})
    st.plotly_chart(fig_top)
    
    # Download button for PDF
    pdf_top_techniques = get_pdf_download_link(fig_top)
    st.download_button("Download Top Techniques Visualization as PDF", pdf_top_techniques, "top_techniques.pdf", "application/pdf")

# Module 2: Software Usage Visualization
elif selected_module == "Software Usage":
    st.title("Software Usage Across Techniques")
    
    software_usage = df_techniques_and_software.groupby('name_software').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    
    st.write("Displaying top 10 most frequently used software across techniques")
    fig_software = px.bar(software_usage, x='name_software', y='count', title="Top 10 Software", labels={'name_software': 'Software', 'count': 'Occurrences'})
    st.plotly_chart(fig_software)
    
    # Download button for PDF
    pdf_software_usage = get_pdf_download_link(fig_software)
    st.download_button("Download Software Usage Visualization as PDF", pdf_software_usage, "software_usage.pdf", "application/pdf")

# Module 3: Adversary Group Analysis
elif selected_module == "Adversary Group Analysis":
    st.title("Adversary Group Usage Across Techniques")
    
    group_usage = df_techniques_and_groups.groupby('source name').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    
    st.write("Displaying top 10 most active adversary groups across techniques")
    fig_group = px.bar(group_usage, x='source name', y='count', title="Top 10 Adversary Groups", labels={'source name': 'Adversary Group', 'count': 'Occurrences'})
    st.plotly_chart(fig_group)
    
    # Download button for PDF
    pdf_group_usage = get_pdf_download_link(fig_group)
    st.download_button("Download Adversary Group Analysis Visualization as PDF", pdf_group_usage, "group_usage.pdf", "application/pdf")

# Module 4: Relationship Analysis
elif selected_module == "Relationship Analysis":
    st.title("Relationship Between Techniques, Tactics, and Software")

    if 'selected_techniques' not in st.session_state:
        st.session_state.selected_techniques = df_techniques_and_tactics['name'].sample(n=5, random_state=1).tolist()

    selected_techniques = st.multiselect(
        "Select techniques to compare (default 5 random):", 
        options=df_techniques_and_tactics['name'].unique(), 
        default=st.session_state.selected_techniques  
    )

    if selected_techniques != st.session_state.selected_techniques:
        st.session_state.selected_techniques = selected_techniques

    filtered_tactics_data = df_techniques_and_tactics[df_techniques_and_tactics['name'].isin(st.session_state.selected_techniques)]
    filtered_groups_data = df_techniques_and_groups[df_techniques_and_groups['target name'].isin(st.session_state.selected_techniques)]
    filtered_software_data = df_techniques_and_software[df_techniques_and_software['name_technique'].isin(st.session_state.selected_techniques)]

    # Stacked Bar Chart
    st.subheader("Stacked Bar Chart: Techniques Grouped by Tactics")
    stacked_data = filtered_tactics_data.groupby(['tactics', 'name']).size().reset_index(name='count')
    fig_stacked = px.bar(stacked_data, x='tactics', y='count', color='name', title="Techniques Grouped by Tactics (Stacked Bar Chart)")
    st.plotly_chart(fig_stacked)
    
    # Download button for PDF
    pdf_stacked_data = get_pdf_download_link(fig_stacked)
    st.download_button("Download Stacked Data Visualization as PDF", pdf_stacked_data, "stacked_data.pdf", "application/pdf")

    # Bar Chart
    st.subheader("Bar Chart: Techniques vs Adversary Groups")
    
    bar_data = filtered_groups_data.groupby(['target name', 'source name']).size().reset_index(name='count')
    
    if bar_data.empty:
        st.warning("No adversary groups are using the selected techniques.")
    else:
        bar_data['label'] = bar_data['source name']  
        fig_bar = px.bar(
            bar_data,
            x='target name',  
            y='count',  
            title="Techniques vs Adversary Groups (Bar Chart)",
            text='label',  
            color='source name'  
        )
        st.plotly_chart(fig_bar)
        
        # Download button for PDF
        pdf_bar_data = get_pdf_download_link(fig_bar)
        st.download_button("Download Bar Data Visualization as PDF", pdf_bar_data, "bar_data.pdf", "application/pdf")

    # Treemap
    st.subheader("Treemap: Techniques by Software")
    treemap_data = filtered_software_data.groupby(['name_software', 'name_technique']).size().reset_index(name='count')

    fig_treemap = px.treemap(
        treemap_data, 
        path=['name_software', 'name_technique'], 
        values='count', 
        title="Techniques by Software (Treemap)",
        color='count',  
        color_continuous_scale=px.colors.sequential.Plasma,  
        hover_data={
            'name_technique': True,  
            'count': True,            
        },
        labels={'name_technique': 'Technique', 'name_software': 'Software'}  
    )
    fig_treemap.update_traces(
        textinfo='label+value',  
        textfont=dict(size=12)   
    )
    fig_treemap.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),  
        title_font=dict(size=18),               
    )
    st.plotly_chart(fig_treemap)

    # Download button for PDF
    pdf_treemap_data = get_pdf_download_link(fig_treemap)
    st.download_button("Download Treemap Visualization as PDF", pdf_treemap_data, "treemap_data.pdf", "application/pdf")

# Module 5: Combined Techniques, Groups, and Tactics
elif selected_module == "Combined Techniques, Groups, and Tactics":
    st.title("Techniques Grouped by Groups and Tactics")
    
    combined_df = pd.merge(df_techniques_and_groups, df_techniques_and_tactics, 
                       left_on='name_technique', right_on='name', how='inner')

    unique_groups = combined_df['name_group'].unique()
    
    if 'default_groups' not in st.session_state:
        st.session_state.default_groups = random.sample(list(unique_groups), 5)

    selected_groups = st.multiselect(
        "Select groups to display:", 
        options=unique_groups, 
        default=st.session_state.default_groups
    )
    
    if selected_groups:
        filtered_combined_data = combined_df[combined_df['name_group'].isin(selected_groups)]
        aggregated_data = filtered_combined_data.groupby(['name_group', 'tactics']).size().reset_index(name='technique_count')

        st.write("Techniques Distribution by Group and Tactic")
        fig_bar = px.bar(aggregated_data, x='name_group', y='technique_count', color='tactics', 
                         title='Techniques by Group and Tactic', barmode='group',
                         labels={'name_group': 'Group', 'technique_count': 'Number of Techniques', 'tactics': 'Tactic'})

        st.plotly_chart(fig_bar)
        
        # Download button for PDF
        pdf_combined_data = get_pdf_download_link(fig_bar)
        st.download_button("Download Combined Data Visualization as PDF", pdf_combined_data, "combined_data.pdf", "application/pdf")
    else:
        st.write("No groups selected. Please select a group to display the chart.")
