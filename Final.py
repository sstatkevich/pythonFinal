import pydeck as pdk
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import random as rd
import re
import numpy as np

st.image('VolcanoIcon2.png', width= 200)
st.markdown("<h1 style='text-align: center; color: maroon;'>Volcanoes</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: black;'>Welcome to my volcanoes analytics program. You can analyze using charts in the Charts Tab, or use maps in the Maps Tab </h2>", unsafe_allow_html=True)

tab1, tab2, = st.tabs(['Charts', 'Maps'])


# Load the data from the 'volcanoes.csv' file
df = pd.read_csv('volcanoes.csv')

# Create a streamlit app

def create_pie_chart_1(region, df):
    # Filter the dataframe by the selected region

    df_region = df[df['Region'] == region]

    # Create a pie chart showing the proportions of primary volcano type, with labels
    fig1, ax1 = plt.subplots()
    ax1.pie(df_region['Primary Volcano Type'].value_counts() / len(df_region),
                     labels=df_region['Primary Volcano Type'].unique(), autopct= '%.1f%%')

    return fig1

with tab1:

    selected_graphs = st.sidebar.multiselect('Please select which of the graphs you would like to use:', ['Proportions of Volcano Types by Region', 'Proportions of Activity Evidence by Region and Primary Volcano Type', 'Dominant Rock Type by Sub Region', 'Volcano Type by Elevation Range', 'Volcanoes in each Subregion by Dominant Rock Type and Region'])
    for i in selected_graphs:
        if i == 'Proportions of Volcano Types by Region':


            st.subheader('Proportions of Volcano Types by Region')
            # Create a select box for the user to choose a region
            region = st.selectbox('Region:', df['Region'].unique())

            fig = create_pie_chart_1(region, df)
            st.pyplot(fig)
            st.write(f"*****"*50)

        if i == 'Proportions of Activity Evidence by Region and Primary Volcano Type':

            st.subheader('Proportions of Activity Evidence by Region and Primary Volcano Type')
            region2 = st.selectbox('Region:', df['Region'].unique(), key = 'region')

            # Create a radio button for the user to choose a primary volcano type
            primary_volcano_type = st.radio('Primary Volcano Type:', df['Primary Volcano Type'].unique())

            # Filter the dataframe by the selected region and primary volcano type
            df_filtered = df[(df['Region'] == region2) & (df['Primary Volcano Type'] == primary_volcano_type)]

            # Create a pie chart showing the proportions of activity evidence, with labels
            if df_filtered.empty:
                # Display a message if the dataframe is empty
                st.markdown("**Sorry, there are no volcanoes which fall into this criteria. Try a different selection**")
                st.write(f"*****"*50)
            else:
                # Create a pie chart showing the proportions of activity evidence, with labels
                fig, ax = plt.subplots()
                ax.pie(df_filtered['Activity Evidence'].value_counts() / len(df_filtered),
                                 labels=df_filtered['Activity Evidence'].unique(), autopct= '%.1f%%')
                st.pyplot(fig)
                st.write(f"*****"*50)

        if i == 'Dominant Rock Type by Sub Region':

            st.subheader('Dominant Rock Type by Sub Region')
            selected_region = st.selectbox("Select a region for the bar chart:", df["Region"].unique())
            # Filter the DataFrame to only include data for the selected region
            filtered_df = df[df["Region"] == selected_region]
            filtered_df = filtered_df.sort_values(by='Primary Volcano Type', ascending=True)

            # Create a pivot table from the filtered data, with the total count of volcanoes for each dominant rock type
            chart_data = filtered_df.pivot_table(index = 'Dominant Rock Type', values = "Volcano Name", aggfunc="count")

            chart_data.sort_values(by = ['Volcano Name'], ascending= False, inplace= True)
            # Use the pivot table to create a bar chart
            st.bar_chart(data = chart_data)
            st.write(f"*****"*50)

        if i == 'Volcano Type by Elevation Range':

            st.subheader('Volcano Type by Elevation Range')
            # Get the minimum and maximum values in the "Elevation (m)" column
            min_altitude = df['Elevation (m)'].min()
            max_altitude = df['Elevation (m)'].max()

            st.write(f"The minimum elevation of volcanoes in the dataset is {min_altitude} and the maximum is {max_altitude}.\n Please select a range using the sliders below:")

            # Create sliders to select the minimum and maximum altitudes
            min_elevation = st.slider('Minimum Elevation:', min_value=-5700, max_value=6879)
            max_elevation = st.slider('Maximum Elevation:', min_value=-5700, max_value=6879)

            # Filter the DataFrame to only include data within the selected altitude range
            filtered_df_alt = df[(df['Elevation (m)'] >= min_elevation) & (df['Elevation (m)'] <= max_elevation)]

            # Create a pivot table from the filtered data, with the total count of volcanoes for each primary volcano type
            chart_data = filtered_df_alt.pivot_table(index = 'Primary Volcano Type', values = "Volcano Name", aggfunc="count")

            # Use the pivot table to create a bar chart
            st.bar_chart(data = chart_data)
            st.write(f"*****"*50)

        if i == 'Volcanoes in each Subregion by Dominant Rock Type and Region':

            st.subheader('Volcanoes in each Subregion by Dominant Rock Type and Region')
            selected_region = st.selectbox('Region:', df['Region'].unique(), key = 'region3')

            # Create a radio button for the user to choose a primary volcano type
            primary_volcano_type = st.radio('Dominant Rock Type:', df['Dominant Rock Type'].unique())
            # Filter the DataFrame to only include data for the selected region
            filtered_df = df[df["Region"] == selected_region]

            # Create a pivot table from the filtered data, with the total count of volcanoes for each dominant rock type
            chart_data = filtered_df.pivot_table(index = 'Subregion', values = "Volcano Name", aggfunc="count")
            chart_data.sort_values(by = ['Volcano Name'], ascending= False, inplace= True)
            # Use the pivot table to create a bar chart
            st.bar_chart(data = chart_data)
            st.write(f"*****"*50)




with tab2:

    selected_maps = st.sidebar.multiselect('Please select which of the maps you would like to view:', ['Map Based on Rock Type', 'Multi-Variable Map'])

    for m in selected_maps:
        if m == 'Map Based on Rock Type':

            st.subheader('Map (Dominant Rock Type)')


            selected_rocktype = st.selectbox("Select a Rock Type to Display:", df['Dominant Rock Type'].unique())
            # Filter the DataFrame to only include data for the selected region

            filtered_df_map1 = df[df["Dominant Rock Type"] == selected_rocktype]
            if filtered_df_map1.empty:
                st.markdown("**Sorry, there are no volcanoes which fall into this criteria. Try a different selection**")
            else:

                st.map(filtered_df_map1[['latitude', 'longitude']], zoom=1)

        if m == 'Multi-Variable Map':
            st.subheader('Map (Multiple Variables)')

            # Create a select box for the user to choose multiple variables
            variables = st.multiselect('Select the Variables to Filter Map By:', ['Region', 'Primary Volcano Type', 'Tectonic Setting'])

            # Filter the dataframe by the selected variables
            df_variables = df
            for variable in variables:
                df_variables = df_variables[df_variables[variable].isin(st.multiselect(variable, df[variable].unique()))]

            if df_variables.empty:
                # Display a message if the dataframe is empty
                st.markdown("**Sorry, there are no volcanoes which fall into this criteria. Try a different selection**")

            else:

                # Create a map showing the locations of volcanoes based on the selected variables

                st.map(df_variables[['latitude', 'longitude']], zoom=1)
