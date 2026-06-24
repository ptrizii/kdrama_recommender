import streamlit as st
from app.recommender import recommender, load_data

df, _, _ = load_data()

def format_user_count(num):
    try:
        num = int(num)
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M".replace('.0M', 'M')
        elif num >= 1_000:
            return f"{num / 1_000:.1f}k".replace('.0k', 'k')
        return str(num)
    except (ValueError, TypeError):
        return "0"

def clean_state(reset_state=True):
    st.session_state["active_drama_id"] = []
    st.session_state["modal_history"] = []

def base_filter(df):
    cfg = st.session_state["filter_config"]
    subset = df.copy()
    # release year
    subset = subset[subset["release_year"].between(cfg["year"][0], cfg["year"][1])]
    # genre
    if cfg["include_genre"]:
        genre_mask = subset["genre"].dropna().apply(
            lambda row_text: any(g.lower() in row_text.lower() for g in cfg["include_genre"]))
        subset = subset[genre_mask]
    if cfg["exclude_genre"]:
        genre_mask = subset["genre"].dropna().apply(
            lambda row_text: any(g.lower() in row_text.lower() for g in cfg["exclude_genre"]))
        subset = subset[~genre_mask]
    
    return subset

def apply_collection_filter(df, collection, seen_ids):
    rules = collection["rules"]
    subset = df.copy()
        
    if "genres" in rules:
        genre_mask = subset["genre"].dropna().apply(
            lambda row_text: any(g.lower() in row_text.lower() for g in rules["genres"]))
        subset = subset[genre_mask]
    if "score" in rules:
        subset = subset[subset["score"] >= rules["score"]]
    if "user_count" in rules:
        subset = subset[subset["user_count"] >= rules["user_count"]]
    if "year" in rules:
        subset = subset[subset["release_year"] >= rules["year"]]

    subset = subset[~subset["id"].isin(seen_ids)]
    sample_ids = subset.sample(min(8, len(subset)))["id"].tolist()
    
    return sample_ids

def get_collection_ids(df, collection, seen_ids, type):
    cache = st.session_state[f"homepage_rows_{type}"]
    version = st.session_state["filter_version"]
    key = f"{collection["key"]}_v{version}"

    if key not in cache:
        user_filtered = base_filter(df)
        curated = apply_collection_filter(user_filtered, collection, seen_ids)
        cache[key] = curated
    seen_ids.update(cache[key])
    return cache[key]

def navigate_modal(drama_id, *, reset_history=False, push_current=None):
    ## Reset history when homepage poster being clicked
    if reset_history:
        st.session_state["modal_history"] = []
    ## Update modal history state for back button
    if push_current is not None:
        st.session_state["modal_history"].append(push_current)
    st.session_state["active_drama_id"] = drama_id
    st.rerun()

## Function to display drama poster at homepage
def clickable_poster(row):
    st.image(row["poster"], width='stretch')
    if st.button(
        row["title"][:20] +
            "..." if len(row["title"]) > 22 else row["title"],
        key=f"btn_{row['id']}",
        use_container_width=True,
        type="tertiary"
    ):
        navigate_modal(
            row["id"],
            reset_history=True
        )

# Render homepage display
def render_row(data, type, collection, seen_ids:set):
    ids = get_collection_ids(data, collection, seen_ids, type)
    if not ids:
        return
    
    st.subheader(collection["label"])  # title for each genre
    subset = data[data["id"].isin(ids)]
    cols = st.columns(8)

    for col, (_, row) in zip(cols, subset.iterrows()):
        with col:
            clickable_poster(row)


@st.dialog("Drama Information", width="large", on_dismiss=clean_state)
def drama_popup(row, rec_df, result_idx):
    if "modal_history" not in st.session_state:
        st.session_state["modal_history"] = []

    # Display drama information
    leftcol, rightcol = st.columns([0.18, 0.82])
    with leftcol:
        st.image(row["poster"])
    with rightcol:
        if row["type"] == "Movie":
            ep_line = ""
        else:
            ep_line = f"<strong>Episode:</strong> {row["episodes"]}</br>  "
        st.markdown(
            f"<h2 style='color: #E50914; font-weight: semi bold; padding-bottom:10px';>{row["title"]} ({row["release_year"]})</h2>", unsafe_allow_html=True)
        st.markdown(f"""
                 <span style = font-size:14px;>
                    <strong>Type:</strong> {row["type"]}</br>  
                    <strong>Genre:</strong> {row["genre"]}</br>  
                    {ep_line}
                    <strong>Rating:</strong> {row["score"]} ({format_user_count(row["user_count"])})</br>  
                    <strong>Cast:</strong> {row["actor"]}</br>
                    </br>
                 </span>
                    """, unsafe_allow_html=True)
        st.markdown(
            f"""
                <style> 
                details summary, details p{{ 
                    font-size: 14px !important
                 }}
                details summary:hover {{
                    color:#E50914;
                    cursor: pointer; 
                }};   
                </style>
                <details>
                <summary><b>Synopsis</b></summary>
                <p>{row["synopsis"]}</p>
                </details>
                """,
            unsafe_allow_html=True
        )

    # back button if user navigated from a recommendation
    if st.session_state["modal_history"]:
        if st.button("← Back", type='primary'):
            prev_id = st.session_state["modal_history"].pop()
            navigate_modal(prev_id)

    result_df = rec_df
    st.divider()
    st.markdown(
        "<p style='color:#15213d; font-size:20px; font-weight: bold;color: #E50914; '> You might also like </p>  ",
        unsafe_allow_html=True)

    poster_per_row = 8
    for i in range(0, len(result_idx), poster_per_row):
        chunk = result_df[i:i+poster_per_row]
        cols = st.columns(poster_per_row)

        for col, (_, rec_row) in zip(cols, chunk.iterrows()):
            with col:
                st.image(rec_row["poster"], width='stretch')
                if st.button(
                    rec_row["title"],
                    key=f"rec_btn_{rec_row["id"]}",
                    width='stretch',
                    type="tertiary"
                ):
                    navigate_modal(
                        rec_row["id"],
                        push_current=row["id"]
                    )

def process_display(drama_id):
    row = df[df["id"]==drama_id].iloc[0]
    idx = int(row.name)

    topn = st.session_state["filter_config"]["top_n"]
    minRating = st.session_state["filter_config"]["min_rating"]
    ## Call recommender
    result_idx = recommender(df, idx, top_n=topn, min_rating=minRating)
    result_df = df.iloc[result_idx]

    ## Call modal 
    drama_popup(row, result_df, result_idx)
    return



# Function for search function
def search_titles(query):
    if not query:
        return []

    matches = df[df['title'].str.contains(
        query, case=False, na=False)][["id","title"]]
    return [
        (f"{row["title"]}",
         row["id"])
        for _, row in matches.head(15).iterrows()
    ]

# Filter function
def click_button(inc, exc, year, rate, topn):
    st.session_state["filter_config"] = {
        "include_genre": inc,
        "exclude_genre": exc,
        "year": year,
        "min_rating": rate,
        "top_n": topn
    }
    st.session_state["filter_version"] += 1
