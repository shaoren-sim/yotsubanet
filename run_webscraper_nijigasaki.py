from webscraper.utils import initialize_data_folder
from config.reddit_praw_login_details import RedditLoginDetails
from webscraper.reddit_scraper import RedditPrawler
from webscraper.thread_image_downloader import download_fanart_from_subreddits, download_images_from_thread
import os

DATA_FOLDER = "niji_data"

if __name__ == "__main__":
    labels = ["ayumu", "kasumi", "shizuku", "emma", "karin", "ai", "kanata", "setsuna", "rina", "yuu"]
    sub = 'anime'
    search_strings = ["Nijigasaki Episode Discussion"]

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
        download_images_from_thread(thread, labels, DATA_FOLDER, delete_images_with_no_faces=True, folder_for_multiple_faces="./extraneous_data_nijigasaki")

    for label in labels:
        label_dir_path = os.path.join(DATA_FOLDER, label)
        image_counts = len([name for name in os.listdir(label_dir_path) if os.path.isfile(os.path.join(label_dir_path, name))])
        print(f'{label}: {image_counts} images')

    print('-'*12)
    print(f'Unlabelled images: {len([name for name in os.listdir("extra_unlabelled_data/extraneous_data_nijigasaki") if os.path.isfile(os.path.join("extra_unlabelled_data/extraneous_data_nijigasaki", name))])}')

    labels = ["ayumu", "kasumi", "shizuku", "emma", "karin", "ai", "kanata", "setsuna", "rina", "yuu"]
    sub = 'LoveLive'
    search_strings = ["Nijigasaki Discussion"]
    # Search discussion posts on r/anime
    subreddit = reddit.subreddit(sub)
    print(subreddit.display_name)
    print(subreddit.title)

    threads = [reddit.search_for_threads(subreddit, search_string) for search_string in search_strings]

    # Flatten threads: https://stackoverflow.com/questions/11264684/flatten-list-of-lists by Paul Seeb
    threads = [val for sublist in threads for val in sublist]

    for thread in threads:
        print(thread.title)
        download_images_from_thread(thread, labels, DATA_FOLDER, delete_images_with_no_faces=True, folder_for_multiple_faces="./extraneous_data_nijigasaki")

    for label in labels:
        label_dir_path = os.path.join(DATA_FOLDER, label)
        image_counts = len([name for name in os.listdir(label_dir_path) if os.path.isfile(os.path.join(label_dir_path, name))])
        print(f'{label}: {image_counts} images')

    print('-'*12)
    print(f'Unlabelled images: {len([name for name in os.listdir("extra_unlabelled_data/extraneous_data_nijigasaki") if os.path.isfile(os.path.join("extra_unlabelled_data/extraneous_data_nijigasaki", name))])}')
    
    subreddits = ['LoveLive', 'LoveLive', 'LoveLive', 'LoveLive', 'LoveLive', 'LoveLive', 'LoveLive', 'LoveLive', 'LoveLive', 'LoveLive', 'TheTheatreIdol', 'AyumusShoulder', 'LoveLive']
    corresponding_label = ["ayumu", "kasumi", "shizuku", "emma", "karin", "ai", "kanata", "setsuna", "rina", "yuu", "shizuku", "ayumu", None]
    filter_thread_flairs = ['Fan Art', 'Fan Art', 'Fan Art', 'Fan Art', 'Fan Art', 'Fan Art', 'Fan Art', 'Fan Art', 'Fan Art', 'Fan Art', None, None, 'Fan Art']

    subreddits = [reddit.subreddit(sub) for sub in subreddits]

    for label, subreddit, filter_thread_flair in zip(corresponding_label, subreddits, filter_thread_flairs):
        download_fanart_from_subreddits(
            reddit,
            label,
            label,
            subreddit,
            filter_thread_flair,
            folder_for_multiple_faces="./extraneous_data_nijigasaki",
            data_folder=DATA_FOLDER
        )
    print('-'*12)
    print(f'Unlabelled images: {len([name for name in os.listdir("extra_unlabelled_data/extraneous_data_nijigasaki") if os.path.isfile(os.path.join("extra_unlabelled_data/extraneous_data_nijigasaki", name))])}')

for label in labels:
    label_dir_path = os.path.join('data', label)
    image_counts = len([name for name in os.listdir(label_dir_path) if os.path.isfile(os.path.join(label_dir_path, name))])
    print(f'{label}: {image_counts} images')

print('-'*12)
unlabelled_images_dir = os.path.join("extra_unlabelled_data/multiple_faces")
print(f'Unlabelled images: {len([name for name in os.listdir(unlabelled_images_dir) if os.path.isfile(os.path.join(unlabelled_images_dir, name))])}')