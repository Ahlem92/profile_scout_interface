import requests
import pandas as pd
import streamlit as st

st.header("Profile Scout Generator")
with st.form(key='params_for_api'):

    player_name = st.text_input('Player full name')
    number_of_similar_profiles = st.number_input('Number of similar profiles',1,step=1)

    st.form_submit_button(f"Get similar profiles")

params = dict(
    player_name=player_name,
    number_of_similar_profiles=number_of_similar_profiles)

profile_scout_api_url = 'https://y-snwo4rgu6a-ew.a.run.app/get_profiles'
response = requests.get(profile_scout_api_url, params=params)

prediction = response.json()
profiles=st.dataframe(pd.DataFrame(prediction))

st.header(profiles)
