# ICT-Innovation-Software
1. Introduction:
  - Overview of the Application:
  The Modular Threat Mapping Dashboard provides users with an interactive platform to explore, analyze, and visualize the MITRE ATT&CK dataset.
  The dashboard features five key modules: Top Techniques, Software Usage, Adversary Group Analysis, Relationship Analysis, and Combined Techniques, Groups, and Tactics.
  - Purpose:
  This manual explains how to navigate the application, interact with the different modules, and export visualizations for further analysis or reporting.
  - System Requirements:
  Python version 3.7+
  Required libraries: pandas, plotly, streamlit
  Modern web browser (Chrome, Firefox, or Edge)
2. Getting Started
  - How to Launch the Application:
    + Clone the Github Respository :
       - git clone https://github.com/team/project
    + Navigate to the project directory:
       - cd project-directory
    + Install requirement library :
       - pip install plotly
       - pip install streamlit
       - pip install pandas
       - pip install -U kaleido
    + Run the application using Streamlit:
       -streamlit run app.py
    + It will antomatically open your browser and navigate to http://localhost:8501 to view the dashboard.
3. Navigating the Dashboard
      1. Main Interface Overview:
          The dashboard is divided into the following sections:
          Sidebar: Used for navigation and filtering options.
          Main Display Area: Displays visualizations and charts based on the selected module.
      2. Modules:
          1. Top Techniques:
              - Displays the top 10 techniques used across adversary groups.
              - How to interact: Use the sidebar to select the module, and the visualization will automatically display. You can hover over the bars for more information or zoom into specific sections.
              - Export option: Click the "Download as PDF" button to export the visualization.
          2. Software Usage:
              - Shows the top 10 software used across techniques.
              - How to interact: After selecting the module, a bar chart will appear. You can hover and zoom in/out.
              - Export option: Click "Download as PDF" to save the chart.
          3. Adversary Group Analysis:
              - Displays the top 10 most active adversary groups using different techniques.
              - How to interact: Use the sidebar to choose this module, and the bar chart will update.
              - Export option: Use the "Download as PDF" option for export.
          4. Relationship Analysis:
              - Allows users to select techniques and visualize relationships between techniques, tactics, and software.
              - How to interact: Use the multiselect dropdown to choose techniques from the sidebar.
              - A stacked bar chart, a regular bar chart, and a treemap visualization will be displayed.
              - Export options: You can export each visualization by clicking the respective download buttons.
          5. Combined Techniques, Groups, and Tactics:
              - Combines data from techniques, adversary groups, and tactics for analysis.
              - How to interact: Use the multiselect dropdown to filter specific adversary groups. A bar chart will display techniques used by selected groups.
              - Export option: Click "Download as PDF" to save the chart.
4. Exporting Visualizations
  - How to Export Data:
    + Each visualization in the dashboard can be exported as a PDF.
  - Steps:
    + Once you generate a chart, click on the "Download as PDF" button below the visualization.
    + The file will download directly to your device.
  - Use Cases:
    + Exported charts can be used in reports or presentations to share insights on cyber adversary behavior.
5. Troubleshooting
  - Common Issues:
    + Application not running: Ensure you have installed all the required dependencies.
    + Visualization not updating: Try refreshing the page or re-selecting the filter options.
    + PDF not downloading: Make sure your browser allows downloads from the application and try re-clicking the button.
  - Contact Support:
    + If you encounter issues that are not resolved by this manual, please reach out to the development team via the GitHub Issues page.
