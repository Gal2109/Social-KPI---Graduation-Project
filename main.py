import streamlit as st
import time
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from background_img.background_img import set_png_as_page_bg
from login_page import login
from PIL import Image
import pydeck
import math
from functioned import *

st.set_page_config(page_title="SoCity", page_icon="building" ,layout="wide")
# set_png_as_page_bg('background_img/3_background_img_1920_1080.png')
set_png_as_page_bg('background_img/Simple Cute Desktop Wallpapers - WallpaperSafari.png')
# st.set_page_config(page_title='SoCity', layout = 'wide', page_icon = building, initial_sidebar_state = 'auto')
# st.set_page_config(
#         page_title="Hello world",
#         page_icon="chart_with_upwards_trend",
#         layout="wide",
#     )


# name, authentication_status, user_id, authenticator = login()

# if authentication_status:
#     authenticator.logout('Logout', 'main')
#     st.sidebar.write('Welcome *%s*' % (name))
# elif authentication_status == False:
#     st.error('Username/Password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

about_header = st.container()
pic_about_header = st.container()
Yuvi_pic = Image.open(r'Team_members_pictures/Yuval.jpeg')
Tal_pic = Image.open(r'Team_members_pictures/Tal.jpeg')
Dana_pic = Image.open(r'Team_members_pictures/Dana.jpeg')
Gal_pic = Image.open(r'Team_members_pictures/Gal.jpeg')
Niv_pic = Image.open(r'Team_members_pictures/Niv.jpeg')

kpi_header = st.container()
kpi_selection = st.container()
kpi_weights = st.container()

# global map_df
# global loneliness_dict
# global health_dict
# global economic_strength_dict

Loneliness_default_values = [0.15, 0.15, 0.15, 0.04, 0.1, 0.3, 0.06, 0.05]
# if flag == False:
# else:
#     flag = False

def header(name):
    st.markdown(f'<p style="color: #8F2A2A; font-size: 20px; font-family: Cooper Black;"> {name} </p>',
                unsafe_allow_html=True)

def update_session_state(key, value):
    del st.session_state[key]
    st.session_state[key] = value

# def file_update(df):
# #     global loneliness_dict
# #     global health_dict
# #     global economic_strength_dict
#     loneliness_dict, health_dict, economic_strength_dict = {}, {}, {}
#     loneliness_dict, health_dict, economic_strength_dict = default_weights(df, loneliness_dict, health_dict, economic_strength_dict)
#     st.session_state['loneliness_dict'] = loneliness_dict
#     st.session_state['health_dict'] = health_dict
#     st.session_state['economic_strength_dict'] = economic_strength_dict
    
#     df_scored = MetricsCalc(df, loneliness_dict, health_dict, economic_strength_dict)
#     st.session_state['df_scored'] = df_scored
    
# #     global map_df
#     map_df = df_scored[["lat", "lon", "Loneliness", "Health", "Economic_Strength"]]
#     st.session_state['map_df'] = map_df
    
#     return df_scored, map_df

with st.sidebar:
    # st.sidebar
    # options_names = ["Prediction", "KPI"]
    # choose_page = st.radio("Choose", options_names)
#     selectbox('Select page',['Country data','Continent data']) 
    choose = option_menu("SoCity", ["File Upload", "Social KPI", "Prediction", "About"],
                         icons=['upload', 'sliders', 'kanban', 'person lines fill'],
                         
                         menu_icon="building", default_index=0,
#                          bi bi-building
#                          app-indicator
                         styles={
                             "container": {"padding": "5!important", "background-color": "white"},
                             "icon": {"color": "black", "font-size": "25px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#eee"},
                             "nav-link-selected": {"background-color": "#FF4B4B"},
                         }
                         )
if 'flag' not in st.session_state:
    st.session_state['flag'] = False

if choose == "File Upload":
#     uploaded_file = None
    with about_header:
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">The File Upload section</p>', unsafe_allow_html=True)
        st.text("Team GABOT")
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'], key="uploaded_file")
        if uploaded_file is not None:
            st.session_state['flag'] = True
            with st.spinner('Working on your file, just a sec..'):
#                 time.sleep(20)
#             df = pd.read_csv(uploaded_file)
                df = rawToValCatagorized(uploaded_file)
                df.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)
                loneliness_dict, health_dict, economic_strength_dict = {}, {}, {}
                loneliness_dict, health_dict, economic_strength_dict = default_weights(df, loneliness_dict, health_dict, economic_strength_dict)
                st.session_state['loneliness_dict'] = loneliness_dict
                st.session_state['health_dict'] = health_dict
                st.session_state['economic_strength_dict'] = economic_strength_dict

                df_scored = MetricsCalc(df, loneliness_dict, health_dict, economic_strength_dict, False)
                st.session_state['df_scored'] = df_scored

            #     global map_df
                map_df = df_scored[["lat", "lon", "Loneliness_score", "Health_score", "Economic_Strength_score"]]

#                 R_color, G_color = [], []
#                 num_of_rows = df_scored.shape[0]
#                 num_of_rows_range = [i for i in range(num_of_rows)]
#                 for v in list(map_df["Loneliness_score"]):
#     #                     st.write(v)
#                     if v == 1:
#                         R_color.append(44)
#                         G_color.append(186)
#                     elif v == 2:
#                         R_color.append(163)
#                         G_color.append(255)
#                     elif v == 3:
#                         R_color.append(255)
#                         G_color.append(244)
#                     elif v == 4:
#                         R_color.append(255)
#                         G_color.append(167)
#                     elif v == 5:
#                         R_color.append(255)
#                         G_color.append(0)

#     #             map_df["R_color"] = R_color
#     #             map_df["G_color"] = G_color
#                 st.session_state["R_color"] = R_color
#                 st.session_state["G_color"] = G_color
                st.session_state['map_df'] = map_df
            
            st.success("File was uploaded!")
#             df_scored, map_df = file_update(df)
#             global loneliness_dict
#             global health_dict
#             global economic_strength_dict
#             loneliness_dict, health_dict, economic_strength_dict = {}, {}, {}
#             loneliness_dict, health_dict, economic_strength_dict = default_weights(df, loneliness_dict, health_dict, economic_strength_dict)
#             df_scored = MetricsCalc(df, loneliness_dict, health_dict, economic_strength_dict)
#             global map_df
#             map_df = df_scored[["lat", "lon", "Loneliness", "Health", "Economic_Strength"]]
#             st.write(df)
#             st.write(df_scored)
        else:
            st.session_state['flag'] = False

elif choose == "Social KPI" and st.session_state['flag'] is False:
    with kpi_header:
#         st.title("The visualization of our KPI's")
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">The visualization of our KPIs</p>', unsafe_allow_html=True)
    
    st.error("You didn't upload a CSV file. please go back to 'File Upload' section!")
    
elif choose == "Social KPI" and st.session_state['flag'] is True:
    with kpi_header:
#         st.title("The visualization of our KPI's")
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">The visualization of our KPIs</p>', unsafe_allow_html=True)
        st.write("An unfortunate phenomenon that has been occurring is reports by neighbors of bad smells coming from apartments, resulting in the discovery of lonely elderlies who have died in their homes.")
        st.write("In this project we wish to reduce the number of these sad cases by using data to indicate households in risk. \nDuring the project we came to an understanding that this situation is a combination of three social KPI’s which are Loneliness, health and economic strength.")
        st.write("By the data provided for us from the “HAMAL”, we were able to establish metrics to calculate these KPI’s. \nOn this view we give you the opportunity to control the weight of each metric’s parameters, so you can observe how much it has affected the social KPI's.")
#         uploaded_file = st.file_uploader("Choose a CSV file", type=['csv','xls','xlsx'], key="uploaded_file")
#         if uploaded_file is not None:
#             df = pd.read_csv(uploaded_file)
# #             df = rawToValCatagorized(uploaded_file)
#             df.rename(columns = {'east' : 'lon', 'north' : 'lat'}, inplace = True)
#             map_df = df[["lat", "lon", "Loneliness_min_score", "Health_min_score", "Economic_Strength_min_score", "Risk"]]
#             st.write(df)
            
#             st.write(dataframe)
#         for uploaded_file in uploaded_files:
#              bytes_data = uploaded_file.read()
#              st.write("filename:", uploaded_file.name)
#              st.write(bytes_data)
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Loneliness KPI:", "2", "-1")
#         col2.metric("Health KPI:", "4", "+1")
#         col3.metric("Economic Strength KPI:", "3", "-1")
#         col1.text("The average loneliness \nlevel of households in \nHadar neighborhood")
#         col2.text("The average health level \nof households in Hadar \nneighborhood")
#         col3.text("The average economic \nstrength level of \nhouseholds in Hadar \nneighborhood")

        with kpi_selection:
            header("KPI Selection")
            KPI_names = ["Loneliness", "Health", "Economic Strength"]
            KPI_page = st.radio("Choose", KPI_names)
            

        with kpi_weights:
            header("KPI weights")

            if KPI_page == "Loneliness":
                even_col, odd_col = st.columns(2)
                index = 0
                temp_col = even_col
                loneliness_dict = st.session_state['loneliness_dict']
                min_val = min(filter(lambda x: x > 0, list(loneliness_dict.values())))
#                 st.write(min_val)
                
                for key, val in loneliness_dict.items():
                    loneliness_dict[f"{key}"] = round(round(val/min_val, 3))
#                     loneliness_dict[f"{key}"] = round(val*10, 3)
                loneliness_hebrew_dict={'arnona_cat_score':('סוג הנחת ארנונה עבור משק בית', 'הסבר על המדד'),
                                        'members_Water_score':('מספר נפשות במשק בית', 'הסבר על המדד'),
                                        'martial_score':('סטטוס משפחתי של ראש משק הבית', 'הסבר על המדד'),
                                        'widow_grown_score':('מספר אלמנים מבוגרים באזור סטטיסטי', 'הסבר על המדד'),
                                        'widow_elderlies_score':('מספר אלמנים זקנים באזור סטטיסטי', 'הסבר על המדד'),
                                        'lonely_elderlies_score':('מספר מבוגרים בודדים באזור סטטיסטי', 'הסבר על המדד'),
                                        'p85_plus_score':('מספר בני 85 ומעלה באזור סטטיסטי', 'הסבר על המדד'),
                                        'accumulated_cases_score':('סה"כ מקרי הדבקות בקורונה באזור סטטיסטי', 'הסבר על המדד'),
                                        'age_score':('גיל ראש משק הבית', 'הסבר על המדד'),
                                        'area_per_person_score':('שטח לאדם במשק בית', 'הסבר על המדד'),
                                        'Ownership_score':('סוג בעלות על הדירה (שכירות/בעלות)', 'הסבר על המדד')
                                       }
                curr_loneliness_dict = loneliness_dict.copy()
                for key, val in curr_loneliness_dict.items():
                    if index % 2 == 0:
                        temp_col = even_col
                    if index % 2 == 1:
                        temp_col = odd_col
                    if val != 0:
                        curr_loneliness_dict[f'{key}'] = temp_col.select_slider(f'{loneliness_hebrew_dict[key][0]}', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                                    value=val, key=f'Loneliness_slider_{key}', help=f'{loneliness_hebrew_dict[key][1]}')
#                         curr_loneliness_dict[f'{key}'] = temp_col.slider(f'loneliness_slider: {key}', min_value=0.0, max_value=10.0,
#                                                                     value=val, key=f'loneliness_slider_{key}')
                        index += 1

                sum_of_weights = round(sum(list(curr_loneliness_dict.values())), 3)
#                 st.write(sum_of_weights)
                loneliness_dict = {key: round(weight/sum_of_weights, 5) for key, weight in curr_loneliness_dict.items()}
#                 update_session_state("loneliness_dict", loneliness_dict)
                st.session_state['loneliness_dict'] = loneliness_dict
#                 map_df = get_map_df()
#                 GUI_tuple = ("L", loneliness_dict)            
#                 loneliness_dict = weights_update(GUI_tuple)
#                 st.write(st.session_state['df_scored'])
                curr_df = MetricsCalc(st.session_state['df_scored'], loneliness_dict, st.session_state['health_dict'], st.session_state['economic_strength_dict'], True)
#                 update_session_state("df_scores", curr_df)
                R_color, G_color = [], []
                num_of_rows = curr_df.shape[0]
                num_of_rows_range = [i for i in range(num_of_rows)]
                for v in list(curr_df["Loneliness_score"]):
    #                     st.write(v)
                    if v == 1:
                        R_color.append(44)
                        G_color.append(186)
                    elif v == 2:
                        R_color.append(163)
                        G_color.append(255)
                    elif v == 3:
                        R_color.append(255)
                        G_color.append(244)
                    elif v == 4:
                        R_color.append(255)
                        G_color.append(167)
                    elif v == 5:
                        R_color.append(255)
                        G_color.append(0)

#                 map_df["R_color"] = R_color
#                 map_df["G_color"] = G_color
#                 st.session_state["R_color"] = R_color
#                 st.session_state["G_color"] = G_color
                st.session_state['df_scores'] = curr_df
                map_df = curr_df[["lat", "lon", "Loneliness_score", "Health_score", "Economic_Strength_score"]]
                map_df["R_color"] = R_color # st.session_state["R_color"]
                map_df["G_color"] = G_color # st.session_state["G_color"]        
#                 update_session_state("map_df", map_df)
                st.session_state['map_df'] = map_df
#                 layer = pydeck.Layer(
#                                 'HexagonLayer',
#                                 map_df,
#                                 get_position=['lon', 'lat','Risk'],
#                                 auto_highlight=True,
#                                 get_radius=100,
#                                 # 'Risk = 5 ? 255 : Risk = 4 ? 230 : Risk = 3 ? 200 : Risk = 2 ? 170 : 140',
#                                 get_fill_color=[255, 230, 200, 170, 140],
#                                 elevation_range=[0, 1000],
#                                 elevation_scale=2,
#                                 pickable=True,
#                                 extruded=True,
#                                 coverage=0.1)
                layer2 = pydeck.Layer(
                    'ScatterplotLayer', #'ColumnLayer',     # Change the `type` positional argument here
                    map_df,
                    get_position=['lon', 'lat'],
                    get_elevation="Loneliness_score",
                    elevation_scale=20,
#                     radius=40,
                    get_radius = 10,
                    auto_highlight=True,
#                     get_radius=10000,          # Radius is given in meters
                    # ["255 - (Loneliness * 10)", "Loneliness * 6 + 30", "Loneliness * 6", "140"]
                    # Green: ["Loneliness_score * 16", "38 + 40 * (Loneliness_score - 1)", "Loneliness_score % 2", "120"]
                    # Red-Black: ["63 * (Loneliness_score - 1)", "0", "0", "120"],
                    # new: ["R_color", "G_color", "0", "120"],
                    get_fill_color=["R_color", "G_color", "0", "120"],  # Set an RGBA value for fill
#                     elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                    coverage=5 #0.1
                    )
                tooltip = {
                    "html": "<b>Loneliness KPI = {Loneliness_score}</b>",
                    "style": {"background": "grey", "color": "black", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
                }

                view = pydeck.data_utils.compute_view(map_df[['lon', 'lat']])
                view.pitch = 75
                view.bearing = 60
                view.zoom = 14
                
                r = pydeck.Deck(
                    layer2,
                    initial_view_state=view,
                    tooltip=tooltip,
                    map_provider="mapbox",
                    map_style=pydeck.map_styles.SATELLITE,
                )
                st.pydeck_chart(r)

            elif KPI_page == "Health":
                even_col, odd_col = st.columns(2)
                index = 0
                temp_col = even_col
                health_dict = st.session_state['health_dict']
                min_val = min(filter(lambda x: x > 0, list(health_dict.values())))
#                 st.write(min_val)
                for key, val in health_dict.items():
                    health_dict[f"{key}"] = round(round(val/min_val, 3))
#                     loneliness_dict[f"{key}"] = round(val*10, 3)
                health_hebrew_dict={'arnona_cat_score':('סוג הנחת ארנונה עבור משק בית', 'הסבר על המדד'),
                                    'age_score':('גיל ראש משק הבית', 'הסבר על המדד'),
                                    'hashlama_kizvat_nechut_elderlies_score':('מספר מקבלי השלמה לקצבת נכות לאזרח ותיק באזור סטטיסטי', 'הסבר על המדד'),
                                    'Mekabley_kizbaot_nechut_score':('מספר מקבלי קיצבת נכות באזור סטטיסטי', 'הסבר על המדד'),
                                    'zachaim_kizbat_nechut_children_score':('מספר ילדים הזכאים לקצבת נכות באזור סטטיסטי', 'הסבר על המדד'),
                                    'mekabley_kizbaot_from_injured_Work_score':('מספר מקבלי קיצבת תאונות עבודה באזור סטטיסטי', 'הסבר על המדד'),
                                    'mekabley_kizba_siud_score':('מספר מקבלי קצבת סיעוד באזור סטטיסטי', 'הסבר על המדד'),
                                    'accumulated_cases_score':('סה"כ מקרי הדבקות בקורונה באזור סטטיסטי', 'הסבר על המדד'),
                                    'accumulated_recoveries_score':('סה"כ מקרי הבראה מקורונה באזור סטטיסטי', 'הסבר על המדד'),
                                    'accumulated_hospitalized_score':('סה"כ מקרי התאשפזות בעקבות קורונה באזור סטטיסטי', 'הסבר על המדד'),
                                    'accumulated_vaccination_first_dose_score':('סה"כ כמות מתחסנים בחיסון ראשון באזור סטטיסטי', 'הסבר על המדד'),
                                    'accumulated_vaccination_second_dose_score':('סה"כ כמות מתחסנים בחיסון שני באזור סטטיסטי', 'הסבר על המדד'),
                                    'accumulated_vaccination_third_dose_score':('סה"כ כמות מתחסנים בחיסון שלישי באזור סטטיסטי', 'הסבר על המדד')
                                   }
                curr_health_dict = health_dict.copy()
                for key, val in curr_health_dict.items():
                    if index % 2 == 0:
                        temp_col = even_col
                    if index % 2 == 1:
                        temp_col = odd_col
                    if val != 0:
                        curr_health_dict[f'{key}'] = temp_col.select_slider(f'{health_hebrew_dict[key][0]}', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                                    value=val, key=f'Health_slider_{key}', help=f'{health_hebrew_dict[key][1]}')
#                         curr_loneliness_dict[f'{key}'] = temp_col.slider(f'loneliness_slider: {key}', min_value=0.0, max_value=10.0,
#                                                                     value=val, key=f'loneliness_slider_{key}')
                        index += 1

                sum_of_weights = round(sum(list(curr_health_dict.values())), 3)
#                 st.write(sum_of_weights)
                health_dict = {key: round(weight/sum_of_weights, 5) for key, weight in curr_health_dict.items()}
#                 update_session_state("loneliness_dict", loneliness_dict)
                st.session_state['health_dict'] = health_dict
#                 map_df = get_map_df()
#                 GUI_tuple = ("L", loneliness_dict)            
#                 loneliness_dict = weights_update(GUI_tuple)
#                 st.write(st.session_state['df_scored'])
                curr_df = MetricsCalc(st.session_state['df_scored'], st.session_state['loneliness_dict'], health_dict, st.session_state['economic_strength_dict'], True)
#                 update_session_state("df_scores", curr_df)
                R_color, G_color = [], []
                num_of_rows = curr_df.shape[0]
                num_of_rows_range = [i for i in range(num_of_rows)]
                for v in list(curr_df["Health_score"]):
    #                     st.write(v)
                    if v == 1:
                        R_color.append(44)
                        G_color.append(186)
                    elif v == 2:
                        R_color.append(163)
                        G_color.append(255)
                    elif v == 3:
                        R_color.append(255)
                        G_color.append(244)
                    elif v == 4:
                        R_color.append(255)
                        G_color.append(167)
                    elif v == 5:
                        R_color.append(255)
                        G_color.append(0)

#                 map_df["R_color"] = R_color
#                 map_df["G_color"] = G_color
#                 st.session_state["R_color"] = R_color
#                 st.session_state["G_color"] = G_color
                st.session_state['df_scores'] = curr_df
                map_df = curr_df[["lat", "lon", "Loneliness_score", "Health_score", "Economic_Strength_score"]]
                map_df["R_color"] = R_color # st.session_state["R_color"]
                map_df["G_color"] = G_color # st.session_state["G_color"]  
#                 update_session_state("map_df", map_df)
                st.session_state['map_df'] = map_df
                layer2 = pydeck.Layer(
                    'ScatterplotLayer', #'ColumnLayer',     # Change the `type` positional argument here
                    map_df,
                    get_position=['lon', 'lat'],
                    get_elevation="Health_score",
                    elevation_scale=20,
#                     radius=40,
                    get_radius = 10,
                    auto_highlight=True,
#                     get_radius=10000,          # Radius is given in meters
                    # ["255 - (Loneliness * 10)", "Loneliness * 6 + 30", "Loneliness * 6", "140"]
                    # Green: ["Loneliness_score * 16", "38 + 40 * (Loneliness_score - 1)", "Loneliness_score % 2", "120"]
                    # Red-Black: ["63 * (Loneliness_score - 1)", "0", "0", "120"],
                    # new: ["R_color", "G_color", "0", "120"],
                    get_fill_color=["R_color", "G_color", "0", "120"],  # Set an RGBA value for fill
#                     elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                    coverage=5 #0.1
                    )
                tooltip = {
                    "html": "<b>Health KPI = {Health_score}</b>",
                    "style": {"background": "grey", "color": "black", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
                }

                view = pydeck.data_utils.compute_view(map_df[['lon', 'lat']])
                view.pitch = 75
                view.bearing = 60
                view.zoom = 14
                
                r = pydeck.Deck(
                    layer2,
                    initial_view_state=view,
                    tooltip=tooltip,
                    map_provider="mapbox",
                    map_style=pydeck.map_styles.SATELLITE,
                )
                st.pydeck_chart(r)
                
            elif KPI_page == "Economic Strength":
                even_col, odd_col = st.columns(2)
                index = 0
                temp_col = even_col
                economic_strength_dict = st.session_state['economic_strength_dict']
                min_val = min(filter(lambda x: x > 0, list(economic_strength_dict.values())))
#                 st.write(min_val)
                for key, val in economic_strength_dict.items():
                    economic_strength_dict[f"{key}"] = round(round(val/min_val, 3))
#                     loneliness_dict[f"{key}"] = round(val*10, 3)
                economic_strength_hebrew_dict={'area_per_person_score':('שטח לאדם במשק בית', 'הסבר על המדד'),
                                                'socio_economic_score':('ציון סוציו אקונומי', 'הסבר על המדד'),
                                                'mekabley_kizba_siud_score':('מספר מקבלי קצבת סיעוד באזור סטטיסטי', 'הסבר על המדד'),
                                                'mekabley_kizbaot_from_injured_Work_score':('מספר מקבלי קיצבת תאונות עבודה באזור סטטיסטי', 'הסבר על המדד'),
                                                'zachaim_kizbat_nechut_children_score':('מספר ילדים הזכאים לקצבת נכות באזור סטטיסטי', 'הסבר על המדד'),
                                                'Mekabley_kizbaot_nechut_score':('מספר מקבלי קיצבת נכות באזור סטטיסטי', 'הסבר על המדד'),
                                                'Mekabley_mezonot_score':('מספר מקבלי מזונות באזור סטטיסטי', 'הסבר על המדד'),
                                                'Hashlamat_hachnasa_sheerim_family_score':('מספר מקבלי השלמת הכנסה שארים באזור סטטיסטי', 'הסבר על המדד'),
                                                'hashlama_kizvat_nechut_elderlies_score':('מספר מקבלי השלמה לקצבת נכות לאזרח ותיק באזור סטטיסטי', 'הסבר על המדד'),
                                                'hashlamta_hachnasa_family_eldelies_score':('מספר מקבלי השלמת הכנסה מבוגרים במשפחה באזור סטטיסטי', 'הסבר על המדד'),
                                                'mekabley_kizva_elderlies_score':('מספר מקבלי קצבת זקנה באזור סטטיסטי', 'הסבר על המדד'),
                                                'avtachat_hachansa_family_score':('מספר מקבלי הבטחת הכנסה משפחות באזור סטטיסטי', 'הסבר על המדד'),
                                                'income_per_person_score':('סך הכל הכנסה פר נפש במשק בית', 'הסבר על המדד'),
                                                'arnona_cat_score':('סוג הנחת ארנונה עבור משק בית', 'הסבר על המדד'),
                                                'Ownership_score':('סוג בעלות על הדירה (שכירות/בעלות)', 'הסבר על המדד'),
                                                'age_score':('גיל ראש משק הבית', 'הסבר על המדד'),
                                                'martial_score':('סטטוס משפחתי של ראש משק הבית', 'הסבר על המדד'),
                                                'members_Water_score':('מספר נפשות במשק בית', 'הסבר על המדד'),
                                                'near_106_pizul_and_dangerous_buildings_score':('בניין שנמצא במרחק של עד 25 מטר מבניין מסוכן או בניין שעבר פיצול', 'הסבר על המדד')
                                              }
                curr_economic_strength_dict = economic_strength_dict.copy()
                for key, val in curr_economic_strength_dict.items():
                    if index % 2 == 0:
                        temp_col = even_col
                    if index % 2 == 1:
                        temp_col = odd_col
                    if val != 0:
                        curr_economic_strength_dict[f'{key}'] = temp_col.select_slider(f'{economic_strength_hebrew_dict[key][0]}', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                                    value=val, key=f'Economic_Strength_slider_{key}', help=f'{economic_strength_hebrew_dict[key][1]}')
#                         curr_loneliness_dict[f'{key}'] = temp_col.slider(f'loneliness_slider: {key}', min_value=0.0, max_value=10.0,
#                                                                     value=val, key=f'loneliness_slider_{key}')
                        index += 1

                sum_of_weights = round(sum(list(curr_economic_strength_dict.values())), 3)
#                 st.write(sum_of_weights)
                economic_strength_dict = {key: round(weight/sum_of_weights, 5) for key, weight in curr_economic_strength_dict.items()}
#                 update_session_state("loneliness_dict", loneliness_dict)
                st.session_state['economic_strength_dict'] = economic_strength_dict
#                 map_df = get_map_df()
#                 GUI_tuple = ("L", loneliness_dict)            
#                 loneliness_dict = weights_update(GUI_tuple)
#                 st.write(st.session_state['df_scored'])
                curr_df = MetricsCalc(st.session_state['df_scored'], st.session_state['loneliness_dict'], st.session_state['health_dict'], economic_strength_dict, True)
#                 update_session_state("df_scores", curr_df)
                R_color, G_color = [], []
                num_of_rows = curr_df.shape[0]
                num_of_rows_range = [i for i in range(num_of_rows)]
                for v in list(curr_df["Economic_Strength_score"]):
    #                     st.write(v)
                    if v == 1:
                        R_color.append(44)
                        G_color.append(186)
                    elif v == 2:
                        R_color.append(163)
                        G_color.append(255)
                    elif v == 3:
                        R_color.append(255)
                        G_color.append(244)
                    elif v == 4:
                        R_color.append(255)
                        G_color.append(167)
                    elif v == 5:
                        R_color.append(255)
                        G_color.append(0)

#                 map_df["R_color"] = R_color
#                 map_df["G_color"] = G_color
#                 st.session_state["R_color"] = R_color
#                 st.session_state["G_color"] = G_color
                st.session_state['df_scores'] = curr_df
                map_df = curr_df[["lat", "lon", "Loneliness_score", "Health_score", "Economic_Strength_score"]]
                map_df["R_color"] = R_color # st.session_state["R_color"]
                map_df["G_color"] = G_color # st.session_state["G_color"]  
#                 update_session_state("map_df", map_df)
                st.session_state['map_df'] = map_df
                layer2 = pydeck.Layer(
                    'ScatterplotLayer', #'ColumnLayer',     # Change the `type` positional argument here
                    map_df,
                    get_position=['lon', 'lat'],
                    get_elevation="Economic_Strength_score",
                    elevation_scale=20,
#                     radius=40,
                    get_radius = 10,
                    auto_highlight=True,
#                     get_radius=10000,          # Radius is given in meters
                    # ["255 - (Loneliness * 10)", "Loneliness * 6 + 30", "Loneliness * 6", "140"]
                    # Green: ["Loneliness_score * 16", "38 + 40 * (Loneliness_score - 1)", "Loneliness_score % 2", "120"]
                    # Red-Black: ["63 * (Loneliness_score - 1)", "0", "0", "120"],
                    # new: ["R_color", "G_color", "0", "120"],
                    get_fill_color=["R_color", "G_color", "0", "120"],  # Set an RGBA value for fill
#                     elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                    coverage=5 #0.1
                    )
                tooltip = {
                    "html": "<b>Health KPI = {Health_score}</b>",
                    "style": {"background": "grey", "color": "black", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
                }

                view = pydeck.data_utils.compute_view(map_df[['lon', 'lat']])
                view.pitch = 75
                view.bearing = 60
                view.zoom = 14
                
                r = pydeck.Deck(
                    layer2,
                    initial_view_state=view,
                    tooltip=tooltip,
                    map_provider="mapbox",
                    map_style=pydeck.map_styles.SATELLITE,
                )
                st.pydeck_chart(r)

elif choose == "Prediction":
#     st.balloons()
#     st.title("The Prediction section")
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">The Prediction section</p>', unsafe_allow_html=True)
    knn_file = st.file_uploader("Choose a CSV file for KNN", type=['csv'], key="knn_file")
    new_file = st.file_uploader("Choose a new CSV file for prediction", type=['csv'], key="new_file")

            
elif choose == "About":
    #         st.title("The About section")
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">The About section</p>', unsafe_allow_html=True)
    st.text("Team GABOT")
    Yuvi, Tal, Dana, Gal, Niv = st.columns(5)
    with Yuvi:
        st.image(Yuvi_pic, width=130)
    with Tal:
        st.image(Tal_pic, width=130)
    with Dana:
        st.image(Dana_pic, width=130)
    with Gal:
        st.image(Gal_pic, width=130)
    with Niv:
        st.image(Niv_pic, width=130)
#     st.markdown(""" <style> .font {
#     font-size:35px ; font-family: 'Cooper Black'; color: #FF4B4B;} 
#     </style> """, unsafe_allow_html=True)
#     st.markdown('<p class="font">Contact Form</p>', unsafe_allow_html=True)
#     with st.form(key='columns_in_form2', clear_on_submit=True):  # clear_on_submit=True > form will be reset/cleared once it's submitted
#         Name = st.text_input(label='Please Enter Your Name')  # Collect user feedback
#         Email = st.text_input(label='Please Enter Email')  # Collect user feedback
#         Message = st.text_input(label='Please Enter Your Message')  # Collect user feedback
#         submitted = st.form_submit_button('Submit')
#         if submitted:
#             st.write('Thanks for your contacting us. \nWe will respond to your questions or inquiries as soon as possible! \n   Team GABOT')
