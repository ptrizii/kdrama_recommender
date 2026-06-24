# K-DRAMA RECOMMENDER 
A Netflix-inspired K-drama discovery app built with Streamlit, that helps users discover dramas through curated collections, genre-based rows, and interactive filtering. This system powered by scraped data and lightweight recommendation logic designed to run entirely on CPU — no GPU required.

This repository also serves as an archive of the full project lifecycle, including data scraping, preprocessing, modeling, and the final deployed application.

## 🧪 Data
Drama metadata is collected via custom scraping scripts of Mydramalist website.

## ⚙️ Recommendation Engine
The recommendation engine uses **content-based filtering** to match dramas based on metadata similarity. It combines **MiniLM embeddings** and **TF-IDF vectors** to capture both semantic meaning and keyword relevance, with **Annoy Index** enabling fast nearest-neighbor lookup at scale.

**Feature used for matching:**
1. Title
2. Genre
3. Director
4. Synopsis (*use exclusively for embedding*)
5. Cast

Recommendations are shown as **You might also like** in the drama detail modal. By default, the system return **20 recommendations**, which can be customized via the sidebar filter.

## ✨ Features
* 🎯 **Curated Collections**
    * Spotlight rows (e.g. Today’s Pick, New Releases, Most Popular)
    * Genre-based collections with custom rule sets
* 🧩 **Interactive Filters**
    * Include / exclude genres
    * Release year range
    * Rating threshold
    * Number of recommendation to display
* 🔎 **Search & Discovery**
    * Support Search dramas directly by title
* **Persistent session state**
    Homepage stays stable when opening and closing drama detail modals.
* 🖼️ **Visual Browsing Experience**
    * Poster-based layout
    * Clickable drama cards
    * Modal/detail view per drama

## 🚀 How to Run the App
Access the [streamlit app here](https://kdrama-matchmaker.streamlit.app/) or 

**1. Clone the repository**
```
git clone https://github.com/your-username/kdrama-recommender.git
cd kdrama-recommender
```
**2. Install Dependencies**
```
pip install -r requirements.txt
```
**3. Run Streamlit**
```
streamlit run streamlit.app.py
```

## Acknowledgements
Built as a learning-driven project exploring:
* Data scraping
* Recommendation systems
* Streamlit state management
* Real-world app architecture