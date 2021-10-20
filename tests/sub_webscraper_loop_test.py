from webscraper.utils import initialize_data_folder
from config.reddit_praw_login_details import RedditLoginDetails
from webscraper.reddit_scraper import RedditPrawler
from webscraper.thread_image_downloader import download_fanart_from_subreddits
import os

if __name__ == "__main__":
    # Initialize test data folder
    labels = ["ichika", "nino", "miku", "yotsuba", "itsuki"]
    subreddits = ['IchikaFanclub', 'NinoNakano', 'MikuNakano', 'Yotsubros', 'ItsukiClassroom']
    filter_thread_flairs = ['Fanart', 'Fanart', 'KAWAII', 'Fanart', 'Fanart']
    initialize_data_folder(labels, "test_data")

    client_id = RedditLoginDetails.client_id
    client_secret = RedditLoginDetails.client_secret
    user_agent = RedditLoginDetails.user_agent
    username = RedditLoginDetails.username
    password = RedditLoginDetails.password
    reddit = RedditPrawler(
        client_id=client_id,      # your client id
        client_secret=client_secret,  #your client secret
        user_agent=user_agent, #user agent name
        username=username,     # your reddit username
        password=password,
        check_for_async=False     # your reddit password
        )
    
    subreddits = [reddit.subreddit(sub) for sub in subreddits]

    for label, subreddit, filter_thread_flair in zip(labels, subreddits, filter_thread_flairs):
        download_fanart_from_subreddits(
            reddit,
            label,
            label,
            subreddit,
            filter_thread_flair,
            data_folder="test_data",
            images_required=10
        )

    print('-'*12)
    print(f'Unlabelled images: {len([name for name in os.listdir("extra_unlabelled_data/multiple_faces") if os.path.isfile(os.path.join("extra_unlabelled_data/multiple_faces", name))])}')
