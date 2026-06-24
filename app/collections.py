COLLECTIONS_SPOTLIGHT_DRAMA = [
    {"key": "today_pick", "label": "Today's Pick",
     "rules": {
         "score": 7,
         "user_count": 5000,
         "order": "score"
     }},
    {
        "key": "new_releases", "label": "New For You",
        "rules": {
            "year": 2026,
            "score": 7,
            "user_count": 5000
        }},
    {
        "key": "top_rated", "label": "Top Rated All the Time",
        "rules": {
            "score": 8.5,
            "user_count": 1000,
            "year": 2015
        }},
    {
        "key": "popular", "label": "Most Popular",
        "rules": {
            "user_count": 30000,
            "year": 2015
        }}
]

COLLECTIONS_SPOTLIGHT_MOVIE = [
    {"key": "today_pick", "label": "Today's Pick",
     "rules": {
         "score": 7,
         "user_count": 6000,
         "order": "score"
     }},
    {
        "key": "new_releases", "label": "New For You",
        "rules": {
            "year": 2025,
            "score": 7,
            "user_count": 3000
        }},
    {
        "key": "top_rated", "label": "Top Rated All the Time",
        "rules": {
            "score": 8.5,
            "user_count": 500,
            "year": 2015
        }},
    {
        "key": "popular", "label": "Most Popular",
        "rules": {
            "user_count": 10000,
            "year": 2015
        }}
]

COLLECTIONS = [
    {
        "key": "politic_power", "label": "Politic & Power Struggle",
        "rules": {
            "genres": ["political"],
            "score": 6,
            "year": 2015,
            "user_count": 5000
        }},
    {
        "key": "webtoon", "label": "From Page to Screen",
        "rules": {
            "tag": ["webtoon", "novel"],
            "score": 6,
            "user_count": 5000
        }},
    {
        "key": "horror", "label": "Horror",
        "rules": {
            "genres": ["horror", "supernatural"],
            "score": 7,
            "user_count": 5000
        }
    },
    {
        "key": "pyschological", "label": "Pyschological & Mind Bending",
        "rules": {
            "genres": ["psychological", "law"],
            "score": 6,
            "user_count": 5000
        }
    },
    {
        "key": "thriler", "label": "Suspenseful Thriller & Action",
        "rules": {
            "genres": ["thriller", "action", "crime"],
            "score": 6,
            "user_count": 5000
        }
    },
    {
        "key": "youth_life", "label": "The Freshness of Youth & Life",
        "rules": {
            "genres": ["life", "youth"],
            "score": 6,
            "user_count": 3000
        }
    },
    {
        "key": "easy_comedy", "label": "Your Next Binge  List",
        "rules": {
            "genres": ["comedy", "fantasy"],
            "score": 6,
            "user_count": 5000
        }
    },
]

GENRES = [
    "Action",
    "Crime",
    "Comedy",
    "Drama",
    "Fantasy",
    "Historical",
    "Horror",
    "Life",
    "Law",
    "Medical",
    "Political",
    "Psychological",
    "Romance",
    "Sci-fi",
    "Supernatural",
    "Thriller"
]

STYLE = """
<style>
div[data-testid="stSidebarContent"] p{
    font-size: 14px !important;            
}
span[data-baseweb="tag"] {
    background-color: #E50914 !important;
    color: #FFFFFF !important;
}
ul[data-testid="stSelectboxVirtualDropdown"], 
ul[data-testid="stSelectboxVirtualDropdownEmpty"]
{
    background-color: #E50914 !important;
}
/* === DROPDOWN ARROW === */
svg{
    fill: #E50914 !important;
    color: #E50914 !important:
}
svg[title="Delete"] {
    fill: #FFFFFF !important;
}
input[data-testid="stNumberInputField"],
div[value]            
{
    color: #E50914 !important;      
}
div[data-testid="stTooltipContent"], div[data-testid="stSidebarContent"] button[data-testid="stBaseButton-primary"] p{
    color: #E50914 !important;
}

</style>
"""
