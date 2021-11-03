# %%
from pathlib import Path
from webscraper.utils import initialize_data_folder, initialize_session_dir
from config.reddit_praw_login_details import RedditLoginDetails
from webscraper.reddit_scraper import RedditPrawler
from webscraper.thread_image_downloader import run_job
from webscraper.session.parser import extract_labels_and_jobs_from_session
import os
from webscraper.dataset_cleanup.image_duplicate_detection import DatasetCleanup
from multiprocessing import Pool
import argparse
import datetime

SESSION_FILE = "examples/gotoubun_no_hanayome/gotoubun_no_hanayome.json"
SESSION_DIR = "goutoubun_no_hanayome"
PROCESSES = 4

DATA_FOLDER = "data"
UNLABELLED_DATA_FOLDER = "unlabelled_data"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="session_file", required=False, help="Webscraper joblist JSON.", default=SESSION_FILE)
    parser.add_argument("-o", "--output", dest="session_dir", required=False, help="Webscraper output folder.", default=SESSION_DIR)
    args = parser.parse_args()

    session_file = Path(args.session_file)
    session_dir = Path(args.session_dir)

    # Initializing folder structure
    # labels, jobs = extract_labels_and_jobs_from_session(session_file)
    # session_dir, data_dir, unlabelled_data_dir = initialize_session_dir(session_dir, DATA_FOLDER, UNLABELLED_DATA_FOLDER)
    # initialize_data_folder(labels, data_dir)
    data_dir = os.path.join(session_dir, DATA_FOLDER)
    unlabelled_data_dir = os.path.join(session_dir, UNLABELLED_DATA_FOLDER)

    save_multiple_faces = True
    folder_for_multiple_faces = os.path.join(unlabelled_data_dir, "multiple_faces")
    delete_images_with_no_faces = True
    folder_for_no_detected_faces = os.path.join(unlabelled_data_dir, "no_detected_faces")
    extraneous_data_folder = unlabelled_data_dir

    # Data cleanup.
    dataset_cleaner = DatasetCleanup(
        data_dir,
        folder_for_multiple_faces,
    )
    print("Pre-cleanup.")
    dataset_cleaner.count_images()
    # dataset_cleaner.preview_grayscale()
    dataset_cleaner.remove_grayscale()
    # dataset_cleaner.inspect_duplicates()
    dataset_cleaner.delete_duplicates()
    print("Post-cleanup.")
    dataset_cleaner.count_images()

if __name__ == "__main__":
    main()