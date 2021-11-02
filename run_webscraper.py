from webscraper.utils import initialize_data_folder, initialize_session_dir
from config.reddit_praw_login_details import RedditLoginDetails
from webscraper.reddit_scraper import RedditPrawler
from webscraper.thread_image_downloader import run_job
from webscraper.session.parser import extract_labels_and_jobs_from_session
import os
from webscraper.dataset_cleanup.image_duplicate_detection import DuplicateDetection
from multiprocessing import Pool
import argparse

SESSION_DIR = "goutoubun_no_hanayome"
DATA_FOLDER = "data"
UNLABELLED_DATA_FOLDER = "unlabelled_data"
SESSION_FILE = "webscraper_session/gotoubun_no_hanayome.json"
PROCESSES = 4

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="session_file", required=False, help="Webscraper joblist JSON.", default=SESSION_FILE)
    parser.add_argument("-o", "--output", dest="session_dir", required=False, help="Webscraper output folder.", default=SESSION_DIR)
    args = parser.parse_args()

    session_file = args.session_file
    session_dir = args.session_dir

    # Initializing folder structure
    labels, jobs = extract_labels_and_jobs_from_session(session_file)
    session_dir, data_dir, unlabelled_data_dir = initialize_session_dir(session_dir, DATA_FOLDER, UNLABELLED_DATA_FOLDER)
    initialize_data_folder(labels, data_dir)

    save_multiple_faces = True
    folder_for_multiple_faces = os.path.join(unlabelled_data_dir, "multiple_faces")
    delete_images_with_no_faces = True
    folder_for_no_detected_faces = os.path.join(unlabelled_data_dir, "no_detected_faces")
    extraneous_data_folder = unlabelled_data_dir

    # Webscraper process.
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

    zipped_jobs_iterable = [
            (
                reddit, 
                job, 
                data_dir, 
                unlabelled_data_dir, 
                save_multiple_faces, 
                folder_for_multiple_faces, 
                delete_images_with_no_faces, 
                folder_for_no_detected_faces, 
            ) for job in jobs
        ]

    with Pool(processes=PROCESSES) as pool:
        pool.starmap(run_job, zipped_jobs_iterable)

    # Data cleanup.
    dupe_detect = DuplicateDetection(
        data_dir,
        unlabelled_data_dir,
    )

    dupe_detect.count_images()
    # dupe_detect.inspect_duplicates()
    dupe_detect.delete_duplicates()

if __name__ == "__main__":
    main()