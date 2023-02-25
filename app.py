
import streamlit as st
import requests
import pandas as pd
import json
from pandas import json_normalize
from streamlit_extras.function_explorer import function_explorer

from streamlit_extras.app_logo import add_logo


def page_profile():

    st.title("_PROFILE SCOUT_ :soccer:")
    st.write('**Done by :** blue[Ahlem Belko], blue[Ahlem Belko], blue[Ahlem Belko] et blue[Ahlem Belko] ')

    df = pd.read_csv('Fifa23_data.csv')

    with st.sidebar :
        with st.form(key='params_for_api'):
            st.header('Player Choice')
            player_name = st.selectbox('Select a player :', df['Full Name'], key = 'player')
            number_of_similar_profiles = st.number_input('Number of similar player :', 5)

            st.header('Selection Criteria')

            value_euro = st.number_input('Select a budget :', min(df['Value(in Euro)']), max(df['Value(in Euro)']), max(df['Value(in Euro)']), key = 'budget')
            age = st.number_input('Select a maximum Age :', min(df['Age']), max(df['Age']), max(df['Age']), key = 'age')
            height = st.number_input('Select Height (cm) :', min(df['Height(in cm)']), key = 'height')
            year = st.number_input('Select end of current contract :', 2023, 2100, 2100, key = 'year')
            release_clause = st.number_input('Select Release Clause :', min(df['Release Clause']), max(df['Release Clause']), max(df['Release Clause']), key = 'rc')

            liste = list(df['Nationality'].unique())
            liste.insert(0, 'None')
            nationality = st.selectbox('Select a Nationality :', liste, key = 'nation')

            submit_button = st.form_submit_button(label ='Get Similar Players')

    if submit_button:
        params = dict(
        player_name=player_name,
        number_of_similar_profiles=number_of_similar_profiles)


        profile_scout_api_url = 'https://profilescout-snwo4rgu6a-ew.a.run.app/get_profiles'
        response = requests.get(profile_scout_api_url, params=params)
        results = response.json()

        df2 = pd.read_json(json.dumps(results), orient ='index')
        df = df2.T
        select = ['Similar Players','Value(in Euro)',"Positions Played", 'Best Position', 'Image Link','Age','Club Name','Contract Until','National Team Image Link' ]

        py_results = df[select]

        default_image = 'https://www.pngkit.com/png/detail/126-1262807_instagram-default-profile-picture-png.png'

        st.header(py_results.index[0])
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if py_results['Value(in Euro)'].loc[py_results.index[0]]//1000000 != 0 :
                st.write(f'{round(py_results["Value(in Euro)"].loc[py_results.index[0]]/1000000, 1)}M €')
            elif py_results['Value(in Euro)'].loc[py_results.index[0]]//1000 != 0 :
                st.write(f'{int(py_results["Value(in Euro)"].loc[py_results.index[0]]/1000)}K €')
            else :
                st.write(f'{py_results["Value(in Euro)"].loc[py_results.index[0]]} €')
            st.image(py_results['Image Link'].loc[py_results.index[0]], width=70)

        with col2:
            st.write(py_results["Positions Played"].loc[py_results.index[0]])
            st.write(py_results["Best Position"].loc[py_results.index[0]])
            if py_results['National Team Image Link'].loc[py_results.index[0]]!= '-':
                st.image(py_results['National Team Image Link'].loc[py_results.index[0]])
            else:
                st.write('No national team')

        with col3:
            st.write(py_results["Age"].loc[py_results.index[0]])
            st.write(py_results["Club Name"].loc[py_results.index[0]])
            st.write(py_results['Contract Until'].loc[py_results.index[0]])

        st.header(f'Here are {number_of_similar_profiles} Similar players of {player_name}')

        for i in range(1, number_of_similar_profiles+1):
            st.subheader(py_results.index[i])
            col1, col2, col3, col4 = st.columns([1, 1, 2,1])

            with col1:
                if py_results['Value(in Euro)'].loc[py_results.index[i]]//1000000 != 0 :
                    st.write(f'{round(py_results["Value(in Euro)"].loc[py_results.index[i]]/1000000, 1)}M €')
                elif py_results['Value(in Euro)'].loc[py_results.index[i]]//1000 != 0 :
                    st.write(f'{int(py_results["Value(in Euro)"].loc[py_results.index[i]]/1000)}K €')
                else :
                    st.write(f'{py_results["Value(in Euro)"].loc[py_results.index[i]]} €')
                st.image(py_results['Image Link'].loc[py_results.index[i]], width=70)

            with col2:
                st.write(py_results["Positions Played"].loc[py_results.index[i]])
                st.write(py_results["Best Position"].loc[py_results.index[i]])
                if py_results['National Team Image Link'].loc[py_results.index[i]]!= '-':
                    st.image(py_results['National Team Image Link'].loc[py_results.index[i]])
                else:
                    st.write('No national team')

            with col3:
                st.write(py_results["Age"].loc[py_results.index[i]])
                st.write(py_results["Club Name"].loc[py_results.index[i]])
                st.write(py_results['Contract Until'].loc[py_results.index[i]])

            with col4:
                pourcentage = py_results['Similar Players'].loc[py_results.index[i]]*100
                st.write(f'{round(pourcentage, 1)} %')

            st.markdown('-----------------')

if __name__ == "__main__":
    page_profile()
