
import streamlit as st
import requests
import pandas as pd
import json
from pandas import json_normalize


def page_profile():

    st.title("_PROFILE SCOUT_ :soccer:")

    df = pd.read_csv('Fifa23_data.csv')

    with st.form(key='params_for_api'   ):
        st.header('Player Choice')
        player_name = st.selectbox('Select a player', df['Full Name'])
        number_of_similar_profiles = st.number_input('Number of similar player', 5)
        submit_button = st.form_submit_button(label ='Get Similar Players')
        st.header('Selection Criteria')
        criteria = [ "Value(in Euro)", "Nationality", "Age", "Height(in cm)", "Release Clause", "Contract Until"]

        if st.multiselect("Nationality", df["Nationality"].unique().tolist(), key="Nationality"):
            df = df[df["Nationality"].isin(df["Nationality"].unique())]
            df = df.query("Nationality ==@Nationality")

        if st.select_slider("Maximum Age", df["Age"].unique().tolist(), key="Age"):
            df = df.query("Age <=@Age")







        # filter_1 = st.selectbox('Select Criteria', criteria)
        # if filter_1 != None :

        # filter_2 = st.selectbox('Select Criteria', criteria)
        # filter_3 = st.selectbox('Select Criteria', criteria)


    if submit_button:
        params = dict(
        player_name=player_name,
        number_of_similar_profiles=number_of_similar_profiles)


        profile_scout_api_url = 'https://profilescout-snwo4rgu6a-ew.a.run.app/get_profiles'
        response = requests.get(profile_scout_api_url, params=params)
        results = response.json()

        df2 = pd.read_json(json.dumps(results), orient ='index')
        df = df2.T
        select = ['Similar Players','Value(in Euro)',"Positions Played", 'Best Position', 'Image Link','Age','Club Name','Contract Until','National Team Image Link', ]

        # # Filtre 1
        # if filter_1 != 'None' :
        #     df = None

        # # Filtre 2
        # if filter_2 != 'None' :
        #     df = None

        # # Filtre 3
        # if filter_3 != 'None' :
        #     df = None

        py_results = df[select]
        py_results["Value(in Euro)"]= py_results["Value(in Euro)"].map('{:,.0f}'.format)


        st.header(py_results.index[0])
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
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

        # button = st.button("Nouvelle recherche")
        # if button :
        #     page_profile()

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

if __name__ == "__main__":
    page_profile()
