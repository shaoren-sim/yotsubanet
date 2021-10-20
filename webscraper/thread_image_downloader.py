import praw
from imgur_downloader import ImgurDownloader
from praw.models import MoreComments
import os
import requests
import datetime
from webscraper.downloaders import download_image
from webscraper.face_extract import preprocess_image
from webscraper.reddit_scraper import extract_links_from_comments, strip_and_lowercase
from webscraper.face_extract import resize_image_to_square
import re

def download_images_from_thread(
    discussion_thread: praw.models.reddit.submission.Submission,
    labels: list,
    data_folder: str = "data",
    preprocessing_function_list: list = [resize_image_to_square], 
    save_multiple_faces: bool = True, 
    folder_for_multiple_faces: str = "multiple_faces", 
    delete_images_with_no_faces: bool = True,
    folder_for_no_detected_faces: str = "no_detected_faces",
    extraneous_data_folder: str = "extra_unlabelled_data",
):
    if save_multiple_faces:
        if not os.path.isdir(extraneous_data_folder):
            os.mkdir(extraneous_data_folder)
        folder_for_multiple_faces = os.path.join(extraneous_data_folder, folder_for_multiple_faces)
        if not os.path.isdir(folder_for_multiple_faces):
            os.mkdir(folder_for_multiple_faces)
    if not delete_images_with_no_faces:
        if not os.path.isdir(extraneous_data_folder):
            os.mkdir(extraneous_data_folder)
        folder_for_no_detected_faces = os.path.join(extraneous_data_folder, folder_for_no_detected_faces)
        if not os.path.isdir(folder_for_no_detected_faces):
            os.mkdir(folder_for_no_detected_faces)
    
    for thread_comment in discussion_thread.comments:
        if isinstance(thread_comment, MoreComments):
            continue
        comment = thread_comment.body

        # Extract links from comment.
        links_in_comment, link_texts, urls = extract_links_from_comments(comment)
        # Adding logic to filter out names.
        for reddit_link, link_text, url in zip(links_in_comment, link_texts, urls):
            if url is None or 'http' not in url:
                continue
            # Check if quint names are included in link_text
            # print(reddit_link)

            # Assumption 1: If name is in link_text, 
            # can download image and label as character
            names_in_link_text = re.findall(r"(?=("+'|'.join(labels)+r"))", link_text.lower())
            
            if len(names_in_link_text) == 1:    # ignore if 2 names are included
                # print(link_text)
                label = names_in_link_text[0]

                # check if url contains '.jpg' or '.png' extension
                # print(url)

                # check returned mime-type just in case it is malicious
                if requests.get(url, allow_redirects=False).status_code == 200:
                    if requests.get(url, allow_redirects=False).headers['Content-Type'] == "text/html":
                        if 'imgur.com/a/' in url:
                            downloader = ImgurDownloader(url)
                            print(f'Album at {url} has {downloader.num_images()} images')
                            downloaded_album_images = downloader.save_images(os.path.join(data_folder, label))

                            for img_in_album in downloaded_album_images[0]:
                                file_path = os.path.join(data_folder, label, img_in_album)
                                try:
                                    preprocess_image(file_path, preprocessing_function_list, save_multiple_faces, folder_for_multiple_faces, delete_images_with_no_faces, folder_for_no_detected_faces)
                                except Exception as e:
                                    print(e)
                                    os.remove(file_path)
                                    print(f"{file_path} removed.")
                        elif 'imgur.com' in url:
                            force_image_link = f"{url}.png"
                            file_extension = "png"
                            file_name = strip_and_lowercase(link_text) + '.' + file_extension
                            file_path = os.path.join(data_folder, label, file_name)
                            if os.path.isfile(file_path):
                                file_path = os.path.join(data_folder, label, strip_and_lowercase(link_text) + '_' + datetime.datetime.today().strftime('%Y%m%d-%H%M%S') + '.' + file_extension)

                            # Try to download and preprocess image.
                            try:
                                download_image(force_image_link, file_path)
                                preprocess_image(file_path, preprocessing_function_list, save_multiple_faces, folder_for_multiple_faces, delete_images_with_no_faces, folder_for_no_detected_faces)
                            except Exception as e:
                                print(e)
                                if os.path.isfile(file_path):
                                    os.remove(file_path)
                                    print(f"{file_path} removed.")
                    else:
                        # If link does not link to an image, skip to next.
                        file_extension = url.split(".")[-1]
                        if file_extension not in ["jpg", "png"]:
                            continue

                        file_name = strip_and_lowercase(link_text) + '.' + file_extension
                        file_path = os.path.join(data_folder, label, file_name)
                        if os.path.isfile(file_path):
                            file_path = os.path.join(data_folder, label, strip_and_lowercase(link_text) + '_' + datetime.datetime.today().strftime('%Y%m%d-%H%M%S') + '.' + file_extension)
                        
                        # download image
                        download_image(url, file_path)
                        # preprocess image
                        try:
                            preprocess_image(file_path, preprocessing_function_list, save_multiple_faces, folder_for_multiple_faces, delete_images_with_no_faces, folder_for_no_detected_faces)
                        except Exception as e:
                            print(e)
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                                print(f"{file_path} removed.")
                print('-'*12)

def download_fanart_from_subreddits(
    prawler,
    label: str,
    subreddit: praw.models.subreddits.Subreddits,
    thread_flair: str,
    data_folder: str = "data",
    preprocessing_function_list: list = [resize_image_to_square], 
    save_multiple_faces: bool = True, 
    folder_for_multiple_faces: str = "multiple_faces", 
    delete_images_with_no_faces: bool = True,
    folder_for_no_detected_faces: str = "no_detected_faces",
    extraneous_data_folder: str = "extra_unlabelled_data",
    images_required: int = None,
):
    # If no specified number of images is provided, set no limit.
    if images_required is None:
        images_required = float("inf")

    if save_multiple_faces:
        if not os.path.isdir(extraneous_data_folder):
            os.mkdir(extraneous_data_folder)
        folder_for_multiple_faces = os.path.join(extraneous_data_folder, folder_for_multiple_faces)
        if not os.path.isdir(folder_for_multiple_faces):
            os.mkdir(folder_for_multiple_faces)
    if not delete_images_with_no_faces:
        if not os.path.isdir(extraneous_data_folder):
            os.mkdir(extraneous_data_folder)
        folder_for_no_detected_faces = os.path.join(extraneous_data_folder, folder_for_no_detected_faces)
        if not os.path.isdir(folder_for_no_detected_faces):
            os.mkdir(folder_for_no_detected_faces)
    
    print("label:", label)
    current_img_count = len([name for name in os.listdir(os.path.join(data_folder, label)) if os.path.isfile(os.path.join(os.path.join(data_folder, label), name))])
    print(f'{label} images: {current_img_count}/{images_required}')

    posts = [post for post in list(subreddit.search(f"{label}", sort='top', limit=None)) if post.link_flair_text == thread_flair]

    image_posts = [post for post in posts if post.url.split('.')[-1] in ['jpg', 'png', 'jpeg']]
    print(len(image_posts), "image posts.")
    for thread in image_posts:
        print(thread.title, thread.link_flair_text)
        print(thread.url)

        download_image(thread.url, os.path.join(
            data_folder, 
            label, 
            f'{strip_and_lowercase(thread.title)}{thread.url[-4:]}'))
        preprocess_image(os.path.join(
                data_folder, 
                label, 
                f'{strip_and_lowercase(thread.title)}{thread.url[-4:]}'
            ),
            preprocessing_function_list, 
            save_multiple_faces, 
            folder_for_multiple_faces, 
            delete_images_with_no_faces, 
            folder_for_no_detected_faces)
        if len([name for name in os.listdir(os.path.join(data_folder, label)) if os.path.isfile(os.path.join(os.path.join(data_folder, label), name))]) >= images_required:
            break
    print('='*12)

    if len([name for name in os.listdir(os.path.join(data_folder, label)) if os.path.isfile(os.path.join(os.path.join(data_folder, label), name))]) >= images_required:
        pass

    gallery_posts = [post for post in posts if "www.reddit.com/gallery" in post.url]
    print(len(gallery_posts), "gallery posts.")
    for thread in gallery_posts:
        print(thread.title, thread.link_flair_text)
        print(thread.url)
        image_dict = prawler.reddit.submission(url=thread.url).media_metadata
        for ind, image_item in enumerate(image_dict.values()):
            largest_image = image_item['s']
            image_url = largest_image['u']
            print(image_url)

            download_image(image_url, os.path.join(
                data_folder, 
                label, 
                f"{strip_and_lowercase(thread.title)}_{ind}.{image_url.split('?')[0].split('.')[-1]}"))
            preprocess_image(os.path.join(
                    data_folder, 
                    label, 
                    f"{strip_and_lowercase(thread.title)}_{ind}.{image_url.split('?')[0].split('.')[-1]}"
                ),
                preprocessing_function_list, 
                save_multiple_faces, 
                folder_for_multiple_faces, 
                delete_images_with_no_faces, 
                folder_for_no_detected_faces)
        if len([name for name in os.listdir(os.path.join(data_folder, label)) if os.path.isfile(os.path.join(os.path.join(data_folder, label), name))]) >= images_required:
            break
    print('='*12)