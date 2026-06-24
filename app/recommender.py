import pandas as pd
import streamlit as st
import numpy as np
from annoy import AnnoyIndex
from typing import Optional

@st.cache_data
def load_data():
    df = pd.read_csv('src/data/processed_moviesdrama.csv',
                     dtype={'episodes': 'Int64'})
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["id"] = df["id"].astype(str)  # keep id as string for consistency
    df["primary_genre"] = (df['genre'].str.split(",").str[0].str.strip())

    ## new dataframe for searching purpose
    drama = df[df["type"] == "Drama"].copy()
    movie = df[df["type"] == "Movie"].copy()
    return df, drama, movie
    # return df


@st.cache_resource(show_spinner="Loading recommendation engine...")
def load_artifacts():
    tfidf_sim = np.load("src/artifact/tfidf_sim_v2.npy")
    annoy_index = AnnoyIndex(384, 'angular')
    annoy_index.load("src/artifact/index_movdrama.ann")
    return tfidf_sim, annoy_index

def recommender(
        df,
        drama_idx: int,
        top_n: int,
        w_tfidf: float = 0.3,
        w_minilm: float = 0.5,
        w_rating: float = 0.2,
        min_rating: Optional[int] = None,
        candidate_pool: int = 200
    ):
    drama_idx = int(drama_idx)
    tfidf_sim, annoy_index = load_artifacts()
        
    # TF-IDF
    tfidf_scores = tfidf_sim[drama_idx]

    # Annoy Index
    neighbor_ids, distances = annoy_index.get_nns_by_item(
        drama_idx, candidate_pool, include_distances=True)
    
    minilm_scores = np.zeros(len(df))
    for idx, distance in zip(neighbor_ids, distances):
        minilm_scores[idx] = 1 - (distance**2)/2

    # Final score for recommendation
    final_scores = (
        w_tfidf * tfidf_scores +
        w_minilm * minilm_scores +
        w_rating * df['rating_norm'].values
    )

    # Exclude query drama
    final_scores[drama_idx] = -1
    top_idx = final_scores.argsort()[::-1].tolist()
    if min_rating > 0:
        filtered_top = [
            idx for idx in top_idx
            if df.loc[idx, "score"] >= min_rating
        ]
        return filtered_top[:top_n]

    # Get Top-N
    return top_idx[:top_n]

