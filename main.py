import streamlit as st
import time
# from streamlit_option_menu import option_menu
# import streamlit.components.v1 as html
# from PIL import Image
# import cv2
# from st_aggrid import AgGrid
# import plotly.express as px
# import io

header = st.container()
kpi_selection = st.container()
kpi_weights = st.container()
Loneliness_default_values = [0.15, 0.15, 0.15, 0.04, 0.1, 0.3, 0.06, 0.05]


def update_slider(kpi_name, value):
    del st.session_state[kpi_name]
    st.session_state[kpi_name] = value


def count_by_sign(sign):
    # count_non_zeros = count_zeros + count_negatives
    count_zeros = 0
    count_negatives = 0
    for val in st.session_state.values():
        if val < 0:
            count_negatives += 1
        if val == 0:
            count_zeros += 1
    if sign == 0:
        return count_zeros
    elif sign == -1:
        return count_negatives
    else:
        return count_zeros + count_negatives


# def increase_one_kpi(kpi_name, decrease_val, kpis_dict):
#     diff_dict = {key: 0 for key in kpis_dict.keys()}
#     for key, val in kpis_dict.items():
#         diff_dict[key] = val - decrease_val
#     while diff_dict.values() < 0:
#         # max_negative_val = -1
#         # for val in diff_dict.values():
#         #     if val < 0 & val > max_negative_val:
#         #         max_negative_val = val
#         num_of_negatives = count_by_sign(-1)
#         min_negative_val = min(diff_dict.values())
#         diff_avg =
#         for key, val in kpis_dict.items():


# st.sidebar.slider("My slider", key="test_slider", min_value=-100, max_value=100)

# st.button("Update slider values", on_click=_update_slider, kwargs={"value": random.randint(-100, 100)})

# with st.sidebar:
#     # st.sidebar
#     # options_names = ["Prediction", "KPI"]
#     # choose_page = st.radio("Choose", options_names)
#
#     choose = option_menu("App Gallery", ["About", "Prediction", "Social KPI", "Contact"],
#                          icons=['person lines fill', 'pc display horizontal', 'people', 'pencil square'],
#                          menu_icon="app-indicator", default_index=0,
#                          styles={
#                              "container": {"padding": "5!important", "background-color": "orange"},
#                              "icon": {"color": "black", "font-size": "25px"},
#                              "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
#                                           "--hover-color": "#eee"},
#                              "nav-link-selected": {"background-color": "#02ab21"},
#                          }
#                          )

with header:
    st.title("The visualization of our KPI's")
    st.text("1: Loneliness KPI")
    st.text("2: Health KPI")
    st.text("3: Economic Strength KPI")

with kpi_selection:
    st.header("KPI Selection")
    KPI_names = ["Loneliness", "Health", "Economic Strength"]
    KPI_page = st.radio("Choose", KPI_names)
    # firstKPI, secondKPI, thirdKPI, clear = st.columns([0.5, 0.4, 1, 1])
    # with firstKPI:
    #     loneliness_kpi_button = st.button("Loneliness")
    # with secondKPI:
    #     health_kpi_button = st.button("Health")
    # with thirdKPI:
    #     economic_strength_kpi_button = st.button("Economic Strength")
    # with clear:
    #     clear_button = st.button("Clear")

with kpi_weights:
    st.header("KPI weights")
    current_values = [0.15, 0.15, 0.15, 0.04, 0.1, 0.3, 0.06, 0.05]
    Loneliness_kpi_dict = {"arnona_cat": 0, "members_Water": 0, "martial": 0, "widow_grown": 0, "widow_elderlies": 0,
                           "lonely_elderlies": 0, "p85_plus": 0, "accumulated_cases": 0}

    basic_ratio = [3, 3, 3, 1, 2, 6, 1, 1]
    current_ratio = [3, 3, 3, 1, 2, 6, 1, 1]

    if KPI_page == "Loneliness":
        st.balloons()
        Loneliness_kpi_dict_keys = list(Loneliness_kpi_dict.keys())
        index = 0
        for key in Loneliness_kpi_dict.keys():
            Loneliness_kpi_dict[key] = st.select_slider('Explanation', options=[1, 2, 3, 4, 5, 6, 7],
                                                        value=current_ratio[index], key=Loneliness_kpi_dict_keys[index])
            index += 1

        sum_of_weights = round(sum(list(Loneliness_kpi_dict.values())), 5)
        st.write(sum_of_weights)
        Loneliness_weights_dict = {key: round(weight/sum_of_weights, 5) for key, weight in Loneliness_kpi_dict.items()}
        st.write(Loneliness_weights_dict)

    elif KPI_page == "Health":
        st.snow()
    elif KPI_page == "Economic Strength":
        with st.spinner('Wait for it...'):
            time.sleep(5)
        st.success('Done!')

    # health_weights = [["arnona_cat", 0.2], ["age", 0.08], ["hashlama_kizvat_nechut_elderlies", (-2) * 0.08],
    #                   ["Mekabley_kizbaot_nechut", (-2) * 0.1], ["zachaim_kizbat_nechut_children", (-2) * 0.09],
    #                   ["mekabley_kizbaot_from_injured_Work", (-2) * 0.11], ["mekabley_kizba_siud", (-2) * 0.15],
    #                   ["accumulated_cases", 0.05], ["accumulated_recoveries", (-2) * 0.01],
    #                   ["accumulated_hospitalized", (-2) * 0.07], ["accumulated_vaccination_first_dose", (-2) * 0.02],
    #                   ["accumulated_vaccination_second_dose", (-2) * 0.02],
    #                   ["accumulated_vaccination_third_dose", (-2) * 0.02]]
    # economic_strength_weights = [["Ownership", 0.35], ["arnona_cat", 0.1], ["income_per_person", 0.2],
    #                              ["avtachat_hachansa_family", 0.022], ["mekabley_kizva_elderlies", 0.022],
    #                              ["hashlamta_hachnasa_family_eldelies", 0.022],
    #                              ["hashlama_kizvat_nechut_elderlies", 0.022],
    #                              ["Hashlamat_hachnasa_sheerim_family", 0.022], ["Mekabley_mezonot", 0.022],
    #                              ["Mekabley_kizbaot_nechut", 0.022], ["zachaim_kizbat_nechut_children", 0.022],
    #                              ["mekabley_kizbaot_from_injured_Work", 0.022], ["mekabley_kizba_siud", 0.022],
    #                              ["socio_economic", 0.1], ["area_per_person", 0.03]]

    #     st.text("In this section you will see all the weights that create the KPI you selected")
