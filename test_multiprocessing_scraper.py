from webscraper.utils import initialize_data_folder
from config.reddit_praw_login_details import RedditLoginDetails
from webscraper.reddit_scraper import RedditPrawler
from webscraper.thread_image_downloader import download_fanart_from_subreddits, download_images_from_thread, run_job
from webscraper.session_reader import extract_labels_and_jobs_from_session
import os
from multiprocessing import Pool

DATA_FOLDER = "data"
SESSION_FILE = "webscraper_session/gotoubun_no_hanayome.py"
PROCESSES = 4

if __name__ == "__main__":
    labels, jobs = extract_labels_and_jobs_from_session(SESSION_FILE)

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

    zipped_jobs_iterable = [(reddit, job, labels, DATA_FOLDER) for job in jobs]

    with Pool(processes=PROCESSES) as pool:
        pool.starmap(run_job, zipped_jobs_iterable)

    # for job in jobs:
    #     print(job)
        # run_job(reddit, job, labels, DATA_FOLDER)