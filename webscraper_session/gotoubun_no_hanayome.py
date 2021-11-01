# %%
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Labels to intiailize folder structure.
LABELS = ["ichika", "nino", "miku", "yotsuba", "itsuki"]

SCRAPER_JOBS = [
    {
        "TYPE": "comment_links",
        "SUBREDDIT": [
            "anime",
        ],
        "SEARCH_QUERY": [
            "Go-toubun no Hanayome Episode Discussion",
        ],
        "THREAD_FLAIR": [
            None,
        ],
        "LABEL": ["ichika"]
    },
    {
        "TYPE": "comment_links",
        "SUBREDDIT": [
            "anime",
        ],
        "SEARCH_QUERY": [
            "Go-toubun no Hanayome Episode Discussion",
        ],
        "THREAD_FLAIR": [
            None,
        ],
        "LABEL": ["nino"]
    },
    {
        "TYPE": "comment_links",
        "SUBREDDIT": [
            "anime",
        ],
        "SEARCH_QUERY": [
            "Go-toubun no Hanayome Episode Discussion",
        ],
        "THREAD_FLAIR": [
            None,
        ],
        "LABEL": ["miku"]
    },
    {
        "TYPE": "comment_links",
        "SUBREDDIT": [
            "anime",
        ],
        "SEARCH_QUERY": [
            "Go-toubun no Hanayome Episode Discussion",
        ],
        "THREAD_FLAIR": [
            None,
        ],
        "LABEL": ["yotsuba"]
    },
    {
        "TYPE": "comment_links",
        "SUBREDDIT": [
            "anime",
        ],
        "SEARCH_QUERY": [
            "Go-toubun no Hanayome Episode Discussion",
        ],
        "THREAD_FLAIR": [
            None,
        ],
        "LABEL": ["itsuki"]
    },
    {
        "TYPE": "subreddit_posts",
        "SUBREDDIT": ['IchikaFanclub', 'NinoNakano', 'MikuNakano', 'Yotsubros', 'ItsukiClassroom'],
        "SEARCH_QUERY": ['ichika', 'nino', 'miku', 'yotsuba', 'itsuki'],
        "THREAD_FLAIR": ['Fanart', 'Fanart', 'KAWAII', 'Fanart', 'Fanart'],
        "LABEL": ['ichika', 'nino', 'miku', 'yotsuba', 'itsuki'],
    },
    {
        "TYPE": "subreddit_posts",
        "SUBREDDIT": ['IchikaFanclub', 'NinoNakano', 'MikuNakano', 'Yotsubros', 'ItsukiClassroom'],
        "SEARCH_QUERY": [None, None, None, None, None],
        "THREAD_FLAIR": ['Fanart', 'Fanart', 'KAWAII', 'Fanart', 'Fanart'],
        "LABEL": ['ichika', 'nino', 'miku', 'yotsuba', 'itsuki'],
    },
]