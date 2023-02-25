
import streamlit as st
import requests
import pandas as pd
import json
import numpy as np



def page_profile():

    st.markdown("<h1 style='text-align: center;'> <i>PROFILE SCOUT</i> &#x26BD</h1>", unsafe_allow_html=True)
    st.markdown('<p><strong>Done by :</strong> <span style="color:Blue;">Alhem Belko</span>, <span style="color:Blue;">Ali Jamal Eddine</span>, <span style="color:Blue;">Romain Lecocq</span> et <span style="color:Blue;">Alix Macgregor</span></p>', unsafe_allow_html=True)

    df = pd.read_csv('Fifa23_data.csv')

    with st.sidebar :
        with st.form(key='params_for_api'):
            st.header('Player Choice')
            player_name = st.selectbox('Select a player :', df['Full Name'], key = 'player')
            number_of_similar_profiles = st.number_input('Number of similar player :', 5)

            st.header('Selection Criteria')
            # Value in Euro
            liste_ve = [0, 1000, 10000, 50000] + list(np.linspace(100000, 900000, 9, dtype = int)) + list(np.linspace(1000000, 50000000, 50, dtype = int)) + list(np.linspace(50000000, 200000000, 40, dtype=int))
            liste_ve.sort()
            liste_ve.insert(0, None)
            value_euro = st.selectbox('Select a budget :', liste_ve, key = 'budget')

            # Age
            liste_a = list(np.linspace(min(df['Age']), max(df['Age']), max(df['Age'])-min(df['Age'])+1, dtype=int))
            liste_a.insert(0, None)
            age = st.selectbox('Select Age', liste_a, key = 'age')

            # Height
            liste_h = list(np.linspace(min(df['Height(in cm)']), max(df['Height(in cm)']), max(df['Height(in cm)'])-min(df['Height(in cm)'])+1, dtype=int))
            liste_h.sort()
            liste_h.insert(0, None)
            height = st.selectbox('Select Age', liste_h, key = 'height')

            # Contract Until
            liste_cu = list(np.linspace(2023, 2050, 28, dtype=int))
            liste_cu.insert(0, None)
            contract_until = st.selectbox('Select end of current contract', liste_cu, key = 'contract_until')

            # Release Clause
            liste_rc = [0, 1000, 10000, 50000] + list(np.linspace(100000, 900000, 9, dtype = int)) + list(np.linspace(1000000, 50000000, 50, dtype = int)) + list(np.linspace(50000000, 400000000, 80, dtype=int))
            liste_rc.insert(0, None)
            release_clause = st.selectbox('Select Release Clause', liste_rc, key = 'release_clause')

            # Nationality
            liste = list(df['Nationality'].unique())
            liste.sort()
            liste.insert(0, None)
            nationality = st.selectbox('Select a Nationality :', liste, key = 'nation')

            submit_button = st.form_submit_button(label ='Get Similar Players')

    if submit_button:

        params = dict(
        player_name = player_name,
        number_of_similar_profiles = number_of_similar_profiles,
        age = age,
        height = height,
        contract_until = contract_until,
        release_clause = release_clause,
        nationality = nationality,
        value_euro = value_euro)


        # profile_scout_api_url = 'https://profile-scout-snwo4rgu6a-ew.a.run.app/get_profiles?player_name=Lionel%20Messi&number_of_similar_profiles=10'
        profile_scout_api_url = 'https://profile-scout-snwo4rgu6a-ew.a.run.app/get_profiles'
        response = requests.get(profile_scout_api_url
                                , params=params)

        player, results = response.json()

        player = pd.read_json(json.dumps(player), orient ='index')
        df2 = pd.read_json(json.dumps(results), orient ='index')
        py_results = df2.T
        player = player.T
        select = ['Similar Players','Height(in cm)', 'Value(in Euro)',"Positions Played", 'Best Position', 'Image Link','Age','Club Name','Contract Until','National Team Image Link' ]

        player = player[select]

        default_image = 'https://www.pngkit.com/png/detail/126-1262807_instagram-default-profile-picture-png.png'
        # st.image(f'<img src={player["Image Link"]} onerror="this.onerror=null;this.src={default_image};" />', unsafe_allow_html= True)

        st.header(player_name)
        col1, col_sep1, col2, col_sep2, col3 = st.columns([2, 1, 3, 1, 3])
        with col1:
            if player['Value(in Euro)'].loc[player.index[0]]//1000000 != 0 :
                st.write(f'Value : {round(player["Value(in Euro)"].loc[player.index[0]]/1000000, 1)}M €')
            elif player['Value(in Euro)'].loc[player.index[0]]//1000 != 0 :
                st.write(f'Value : {int(player["Value(in Euro)"].loc[player.index[0]]/1000)}K €')
            else :
                st.write(f'Value : {player["Value(in Euro)"].loc[player.index[0]]} €')

            st.image(player['Image Link'].loc[player.index[0]], width=70)

        with col_sep1 :
            st.markdown('|')

        with col2:
            st.write(f'Best Position : {player["Best Position"].loc[player.index[0]]}')
            st.write(f'Club : {player["Club Name"].loc[player.index[0]]}')
            st.write(f'Contract Until : {player["Contract Until"].loc[player.index[0]]}')

        with col3:
            st.write(f'Age : {player["Age"].loc[player.index[0]]}')
            st.write('Height : ' + str(player['Height(in cm)'].loc[player.index[0]]) + ' cm')
            if player['National Team Image Link'].loc[player.index[0]]!= '-':
                st.image(player['National Team Image Link'].loc[player.index[0]])
            else:
                st.write('No national team')

        if py_results.shape[0] == 0 :
            st.subheader('There are no matches with these criterias')
        else :
            py_results = py_results[select]
            if py_results.shape[0]!= number_of_similar_profiles :
                st.subheader(f'There are only {py_results.shape[0]} similar players with these criterias')
            else :
                st.header(f'Here are {py_results.shape[0]} Similar players to {player_name}')

            for i in range(py_results.shape[0]):
                pourcentage = py_results['Similar Players'].loc[py_results.index[i]]*100

                st.subheader(py_results.index[i])
                st.text(f'Similarity : {round(pourcentage, 1)} %')
                col1, col2, col3 = st.columns([2, 4, 3])

                with col1:
                    if py_results['Value(in Euro)'].loc[py_results.index[i]]//1000000 != 0 :
                        st.write(f'Value : {round(py_results["Value(in Euro)"].loc[py_results.index[i]]/1000000, 1)}M €')
                    elif py_results['Value(in Euro)'].loc[py_results.index[i]]//1000 != 0 :
                        st.write(f'Value : {int(py_results["Value(in Euro)"].loc[py_results.index[i]]/1000)}K €')
                    else :
                        st.write(f'Value : {py_results["Value(in Euro)"].loc[py_results.index[i]]} €')
                    st.image(py_results['Image Link'].loc[py_results.index[i]], width=70)

                with col2:
                    st.write(f'Positions played : {py_results["Positions Played"].loc[py_results.index[i]]}')
                    st.write(f'Club : {py_results["Club Name"].loc[py_results.index[i]]}')
                    st.write(f'Contract Until : {py_results["Contract Until"].loc[py_results.index[i]]}')

                with col3:
                    st.write(f'Age : {py_results["Age"].loc[py_results.index[i]]}')
                    st.write('Height : ' + str(py_results['Height(in cm)'].loc[py_results.index[i]]) + ' cm')
                    if py_results['National Team Image Link'].loc[py_results.index[i]]!= '-':
                        st.image(py_results['National Team Image Link'].loc[py_results.index[i]])
                    else:
                        st.write('No national team')

                st.markdown('-----------------')

if __name__ == "__main__":
    page_profile()


### Chose qu'il reste à faire :
#       - séparer les colonnes
#       - mettre une image par défaut pour les players qui ont pas de photos
