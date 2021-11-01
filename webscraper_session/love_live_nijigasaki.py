# %%
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Labels to intiailize folder structure.
LABELS = ["ayumu", "kasumi", "shizuku", "emma", "karin", "ai", "kanata", "setsuna", "rina", "yuu"]

SCRAPER_JOBS = [
    {
        "TYPE": "comment_links",
        "SUBREDDIT": [
            "anime",
        ],
        "SEARCH_QUERY": [
            "Nijigasaki Episode Discussion",
        ],
        "THREAD_FLAIR": [
            None,
        ],
    },
    {
        "TYPE": "comment_links",
        "SUBREDDIT": [
            "LoveLive",
        ],
        "SEARCH_QUERY": [
            "Nijigasaki Discussion",
        ],
        "THREAD_FLAIR": [
            None,
        ],
    },
    # Test single case
    {
        "TYPE": "subreddit_posts",
        "SUBREDDIT": [
            'TheTheatreIdol', 
        ],
        "SEARCH_QUERY": [
            "shizuku",
        ],
        "THREAD_FLAIR": [
            None,
        ]
    },
    # Test multi case
    {
        "TYPE": "subreddit_posts",
        "SUBREDDIT": [
            'LoveLive', 
            'LoveLive', 
            'LoveLive', 
            'LoveLive', 
            'LoveLive', 
            'LoveLive', 
            'LoveLive', 
            'LoveLive', 
            'LoveLive', 
            'LoveLive', 
            'AyumusShoulder', 
            'LoveLive'
        ],
        "SEARCH_QUERY": [
            "ayumu", 
            "kasumi", 
            "shizuku", 
            "emma", 
            "karin", 
            "ai", 
            "kanata", 
            "setsuna", 
            "rina", 
            "yuu", 
            "ayumu", 
            None
        ],
        "THREAD_FLAIR": [
            'Fan Art', 
            'Fan Art', 
            'Fan Art', 
            'Fan Art', 
            'Fan Art', 
            'Fan Art', 
            'Fan Art', 
            'Fan Art', 
            'Fan Art', 
            'Fan Art', 
            None, 
            'Fan Art'
        ],
    },
]