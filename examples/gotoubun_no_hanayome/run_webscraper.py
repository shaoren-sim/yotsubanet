from webscraper.utils import initialize_data_folder
from config.reddit_praw_login_details import RedditLoginDetails
from webscraper.reddit_scraper import RedditPrawler
from webscraper.thread_image_downloader import download_fanart_from_subreddits, download_images_from_thread
import os

DATA_FOLDER = "data"

if __name__ == "__main__":
    labels = ["ichika", "nino", "miku", "yotsuba", "itsuki"]
    sub = 'anime'
    search_strings = ["Go-toubun no Hanayome Episode Discussion"]

    subreddits = ['IchikaFanclub', 'NinoNakano', 'MikuNakano', 'Yotsubros', 'ItsukiClassroom']
    filter_thread_flairs = ['Fanart', 'Fanart', 'KAWAII', 'Fanart', 'Fanart']

    initialize_data_folder(labels, DATA_FOLDER)

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

    threads = [reddit.search_for_threads(subreddit, search_string) for search_string in search_strings]

    # Flatten threads: https://stackoverflow.com/questions/11264684/flatten-list-of-lists by Paul Seeb
    threads = [val for sublist in threads for val in sublist]

    for thread in threads:
        print(thread.title)
        download_images_from_thread(thread, labels, DATA_FOLDER, delete_images_with_no_faces=True)

    for label in labels:
        label_dir_path = os.path.join(DATA_FOLDER, label)
        image_counts = len([name for name in os.listdir(label_dir_path) if os.path.isfile(os.path.join(label_dir_path, name))])
        print(f'{label}: {image_counts} images')

    print('-'*12)
    print(f'Unlabelled images: {len([name for name in os.listdir("extra_unlabelled_data/multiple_faces") if os.path.isfile(os.path.join("extra_unlabelled_data/multiple_faces", name))])}')
    
    subreddits = [reddit.subreddit(sub) for sub in subreddits]

    for label, subreddit, filter_thread_flair in zip(labels, subreddits, filter_thread_flairs):
        download_fanart_from_subreddits(
            reddit,
            label,
            label,
            subreddit,
            filter_thread_flair,
        )
    print('-'*12)
    print(f'Unlabelled images: {len([name for name in os.listdir("extra_unlabelled_data/multiple_faces") if os.path.isfile(os.path.join("extra_unlabelled_data/multiple_faces", name))])}')

for label in labels:
    label_dir_path = os.path.join('data', label)
    image_counts = len([name for name in os.listdir(label_dir_path) if os.path.isfile(os.path.join(label_dir_path, name))])
    print(f'{label}: {image_counts} images')

print('-'*12)
unlabelled_images_dir = os.path.join("extra_unlabelled_data/multiple_faces")
print(f'Unlabelled images: {len([name for name in os.listdir(unlabelled_images_dir) if os.path.isfile(os.path.join(unlabelled_images_dir, name))])}')