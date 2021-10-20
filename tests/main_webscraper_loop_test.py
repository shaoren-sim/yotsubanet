from webscraper.utils import initialize_data_folder
from config.reddit_praw_login_details import RedditLoginDetails
from webscraper.reddit_scraper import RedditPrawler
from webscraper.thread_image_downloader import download_images_from_thread
import os

if __name__ == "__main__":
    # Initialize test data folder
    labels = ["ichika", "nino", "miku", "yotsuba", "itsuki"]
    sub = 'anime'
    search_string = "Go-toubun no Hanayome ∬ - Episode 10 discussion"
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
    
    # Search discussion posts on r/anime
    subreddit = reddit.subreddit(sub)
    print(subreddit.display_name)
    print(subreddit.title)

    threads = reddit.search_for_threads(subreddit, search_string)
    for thread in threads[:3]:
        print(thread.title)
        download_images_from_thread(thread, labels, "test_data", delete_images_with_no_faces=True)

    for label in labels:
        label_dir_path = os.path.join("test_data", label)
        image_counts = len([name for name in os.listdir(label_dir_path) if os.path.isfile(os.path.join(label_dir_path, name))])
        print(f'{label}: {image_counts} images')

    print('-'*12)
    print(f'Unlabelled images: {len([name for name in os.listdir("extra_unlabelled_data/multiple_faces") if os.path.isfile(os.path.join("extra_unlabelled_data/multiple_faces", name))])}')
