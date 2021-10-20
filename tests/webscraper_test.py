import os
from webscraper.utils import preview_image
from webscraper.downloaders import download_image
import shutil

WEBSCRAPER_TEST_DIR = "./webscraper_test_data"

# creating target_data directory to store images for target
if not os.path.isdir(WEBSCRAPER_TEST_DIR):
    os.mkdir(WEBSCRAPER_TEST_DIR)

target_image_url_list = ['https://i.imgur.com/mA0x4tg.jpg', 'https://i.imgur.com/EqsTNj6.png']

if __name__ is "__main__":
    from webscraper.utils import preview_image
    from webscraper.downloaders import download_image
    from webscraper.face_extract import extract_face_coordinates, crop_faces, resize_image_to_square
    import matplotlib.pyplot as plt
    from matplotlib import patches
    import PIL
    import shutil
    
    # Testing image downloads
    print('-'*12)
    print("Test 1: Image downloading with preset links.")
    for target_image_url in target_image_url_list:
        print(f"Downloading {target_image_url}")
        img_filename = target_image_url.split("/")[-1]
        download_image(target_image_url, os.path.join(WEBSCRAPER_TEST_DIR, img_filename))
    
    # Plot images
    target_images = [os.path.join(WEBSCRAPER_TEST_DIR, el) for el in os.listdir(WEBSCRAPER_TEST_DIR) if el.endswith(('.png', '.jpg'))]
    print(target_images)
    preview_image(target_images)

    print("Test 1 Passed.")
    shutil.rmtree(WEBSCRAPER_TEST_DIR)
    print('-'*12)

    print("Test 2: Testing single face case.")
    # Create temp directory
    if not os.path.exists("temp"):
        os.mkdir("temp")

    _image_link = 'https://i.imgur.com/mA0x4tg.jpg'
    print(f"Downloading {_image_link}")
    img_filename = _image_link.split("/")[-1]
    img_path = os.path.join("temp", f"_temp{_image_link[-4:]}")
    download_image(_image_link, img_path)

    print("Test 2a: Running individual component functions.")
    print("Extracting face cooredinates...")
    coor_list = extract_face_coordinates(img_path)
    print(f"Face coordinates: {coor_list}")

    print("...and cropping.")
    fig, ax = plt.subplots(1+len(coor_list), 1, figsize=(5, 15))
    image = PIL.Image.open(img_path)

    ax[0].imshow(image)
    ax[0].set_title(f"{img_path.split('/')[-1]} - pre-crop")
    for coor in coor_list:
        rect = patches.Rectangle((coor[0], coor[1]), coor[2]-coor[0], coor[3]-coor[1], linewidth=1, edgecolor='r', facecolor='none')
        ax[0].add_patch(rect)
    ax[0].axis('off')

    for ind, coor in enumerate(coor_list):
        cropped = crop_faces(image, coor)
        cropped = resize_image_to_square(cropped)

        ax[ind+1].imshow(cropped)
        ax[ind+1].set_title(f"{img_path.split('/')[-1]} - face {ind}")
        ax[ind+1].axis('off')
    plt.tight_layout()
    plt.show()

    # Testing preprocessing wrapper
    print("Test 2b: Testing pre-processing wrapper.")
    from webscraper.face_extract import preprocess_image
    print('Pre-processing', img_path)
    preprocess_image(img_path)
    preview_image(img_path)
    print('-'*12)

    print("Completed test, wiping temp folder.")
    shutil.rmtree("./temp")

    print("Test 3: Testing multi face case.")
    # Create temp directory
    if not os.path.exists("temp"):
        os.mkdir("temp")

    _image_link = 'https://i.imgur.com/L6Z3TUH.png'
    print(f"Downloading {_image_link}")
    img_filename = _image_link.split("/")[-1]
    img_path = os.path.join("temp", f"_temp{_image_link[-4:]}")
    download_image(_image_link, img_path)

    print("Test 3a: Running individual component functions.")
    print("Extracting face cooredinates...")
    coor_list = extract_face_coordinates(img_path)
    print(f"Face coordinates: {coor_list}")

    print("...and cropping.")
    fig, ax = plt.subplots(1+len(coor_list), 1, figsize=(5, 15))
    image = PIL.Image.open(img_path)

    ax[0].imshow(image)
    ax[0].set_title(f"{img_path.split('/')[-1]} - pre-crop")
    for coor in coor_list:
        rect = patches.Rectangle((coor[0], coor[1]), coor[2]-coor[0], coor[3]-coor[1], linewidth=1, edgecolor='r', facecolor='none')
        ax[0].add_patch(rect)
    ax[0].axis('off')

    for ind, coor in enumerate(coor_list):
        cropped = crop_faces(image, coor)
        cropped = resize_image_to_square(cropped)

        ax[ind+1].imshow(cropped)
        ax[ind+1].set_title(f"{img_path.split('/')[-1]} - face {ind}")
        ax[ind+1].axis('off')
    plt.tight_layout()
    plt.show()

    # Testing preprocessing wrapper
    print("Test 3b: Testing pre-processing wrapper.")
    from webscraper.face_extract import preprocess_image
    print('Pre-processing', img_path)
    preprocess_image(img_path, folder_for_multiple_faces=os.path.join("temp", "multiple_faces"))
    preview_image([os.path.join("temp", "multiple_faces", f) for f in os.listdir(os.path.join("temp", "multiple_faces"))])
    print('-'*12)

    print("Completed test, wiping temp folder.")
    shutil.rmtree("./temp")