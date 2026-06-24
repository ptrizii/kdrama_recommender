import streamlit as st
import random
from streamlit_searchbox import st_searchbox
from components import render_row, search_titles, click_button, process_display
from recommender import load_data
from collections import COLLECTIONS_GENRE, COLLECTIONS_SPOTLIGHT_DRAMA, COLLECTIONS_SPOTLIGHT_MOVIE, GENRES, STYLE

st.markdown(STYLE, unsafe_allow_html=True)

st.set_page_config(
    page_icon="🍿",
    page_title= "K-Drama Matchmaker",
    layout="wide")
st.title("🍿 K-Drama Matchmaker")
st.write(
    "*Finding your next binge-watch using an interactive recommendation engine featuring automated content filtering and interactive web deployment*.")

# LOAD ESSENTIAL DATA AND INITIALIZE SESSION STATE
df, drama, movie = load_data()

## Homepage display
if "homepage_rows_drama" not in st.session_state:
    st.session_state["homepage_rows_drama"] = {}
    st.session_state["homepage_rows_movie"] = {}

## Search function
if "last_search" not in st.session_state:
    st.session_state["last_search"] = None

## Filter button
if "filter_version" not in st.session_state:
    st.session_state["filter_version"] = 0

if 'filter_config' not in st.session_state:
    st.session_state["filter_config"] = {
        'include_genre': None,
        'exclude_genre': None,
        'year': (2009, 2026),
        'min_rating':0,
        'top_n': 20
    }
if "rotation" not in st.session_state:
    st.session_state["rotation"] = random.sample(COLLECTIONS_GENRE, k=min(2, len(COLLECTIONS_GENRE)))

# SIDEBAR
with st.sidebar:
    left, center, right = st.columns(3)
    with center:    
        st.image("src/picture./movie_border.png", width=80)
    st.title("Customize")
    with st.expander("Homepage Display", expanded=True):
        f_igenre = st.multiselect("Include Genre", GENRES, max_selections=3, help="Genre to display. Up to 3")
        f_egenre = st.multiselect(
            "Exclude Genre", GENRES, max_selections=2, help="Genre not to display. Up to 3")
        f_year= st.slider("Release Year Range",2009, 2026, (2009, 2026))
        
    with st.expander("Recommendation Rules"):
        fr_rating = st.slider("Minimum Rating", 0, 10,value=0, help="Minimum rating of drama to be displayed. By default 0")
        fr_topn = st.number_input("Number of Recommendation", 10, 80, value=20, help="Number of recommendations will be displayed")
    left, center, right = st.columns([0.3,0.6,0.1])
    with center:
        st.button("Apply Filter", key="applyFilter", type="primary", on_click=click_button, 
                  kwargs={
                      "inc":f_igenre, 
                      "exc":f_egenre,
                      "year":f_year,
                      "rate":fr_rating,
                      "topn":fr_topn})
        
########################################### MAIN BODY ##########################################
header_container = st.container()
body_container = st.container()

with header_container:
    selected = st_searchbox(
        search_titles,
        placeholder="Search for a drama or movies...",
        clear_on_submit=True
    )

if selected and st.session_state["last_search"] != selected:
    st.session_state["active_drama_id"] = selected
    st.session_state["last_search"] = selected


with body_container:
    tab1, tab2 = st.tabs(["Drama", "Movies"])

    with tab1:
        seen_ids_d = set()
        for col in COLLECTIONS_SPOTLIGHT_DRAMA:
            render_row(drama, "drama", col, seen_ids_d)
        for rot in st.session_state["rotation"]:
            render_row(drama, "drama", rot, seen_ids_d)

    with tab2:
        seen_ids_m = set()
        for col in COLLECTIONS_SPOTLIGHT_MOVIE:
            render_row(movie, "movie", col, seen_ids_m)
        for rot in st.session_state["rotation"]:
            render_row(movie, "movie", rot, seen_ids_m)

if "active_drama_id" in st.session_state and st.session_state["active_drama_id"]:
    process_display(st.session_state["active_drama_id"])
    
