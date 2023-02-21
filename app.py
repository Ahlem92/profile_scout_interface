
import streamlit as st
import requests
import pandas as pd
import json
from pandas import json_normalize
from streamlit_extras.function_explorer import function_explorer

from streamlit_extras.app_logo import add_logo


st.title("PROFILE SCOUT")


with st.sidebar:
    with st.form(key='params_for_api'):
        player_name = st.text_input('Enter the name of the reference player', "Ex: Lionel Messi")
        number_of_similar_profiles = st.number_input('Number of similar player', 5)

        submit_button = st.form_submit_button(label ='Get Similar Players')




if submit_button:
    params = dict(
    player_name=player_name,
    number_of_similar_profiles=number_of_similar_profiles)


    profile_scout_api_url = 'https://y-snwo4rgu6a-ew.a.run.app/get_profiles'
    response = requests.get(profile_scout_api_url, params=params)
    results = response.json()

    df2 = pd.read_json(json.dumps(results), orient ='index')
    df = df2.T
    select = ['Similar Players','Value(in Euro)',"Positions Played",'Image Link','Age','Club Name','Contract Until','National Team Image Link', ]

    py_results = df[select]

    st.header(f'Here are {number_of_similar_profiles} Similar players of {player_name}')
    st.write(py_results)


    col1, col2 = st.columns(2)
    with col1:
        st.header(py_results.index[0])
        st.write(py_results["Value(in Euro)"].loc[py_results.index[0]])
        st.image(py_results['Image Link'].loc[py_results.index[0]])


        #st.image()
        #st.write(f"{player_name}")
        #st.write(position)
        # st.image(e)

#for n in df["Club Name", "Image Link"]:
    #st.write(n)
    #st.image(n)

#player_name: str, value: float, position: str,
    #data_player = pd.json_normalize(results)
    #Add a logo (optional) in the sidebar
#logo = Image.open(r'C:\Users\13525\Desktop\Insights_Bees_logo.png')
#st.sidebar.image(logo,  width=120)

#Add the expander to provide some information about the app
#with st.sidebar.expander("About the App"):
    # st.write("""
      #  This data profiling App was built by My Data Talk using Streamlit and pandas_profiling package. You can use the app to quickly generate a comprehensive data profiling and EDA report without the need to write any python code. \n\nThe app has the minimum mode (recommended) and the complete code. The complete code includes more sophisticated analysis such as correlation analysis or interactions between variables which may requires expensive computations. )
    # """)

# [url=https://logovtor.com/le-wagon-logo-vector-svg/][img]https://logovtor.com/wp-content/uploads/2020/10/le-wagon-logo-vector.png[/img][/url]
