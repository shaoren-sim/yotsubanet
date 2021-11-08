import os

import cv2 as cv
import numpy as np
import PIL
import shutil

TARGET_SIZE = 224   # scale image to a square shape of (TARGET_SIZE, TARGET_SIZE). 224 is Resnet's input size.
MIN_SIZE = 100       # Minimum face size to avoid tiny images and low-res false positives

def detect_faces(filename, save_image=False, show_image=False, cascade_file="lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv.CascadeClassifier(cascade_file)
    image = cv.imread(filename, cv.IMREAD_COLOR)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.equalizeHist(gray)
    
    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor = 1.1,
                                     minNeighbors = 5,
                                     minSize = (MIN_SIZE, MIN_SIZE))
    for (x, y, w, h) in faces:
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv.imshow("face", image)
    cv.waitKey(0)
    # cv.imwrite("out.png", image)

def extract_face_coordinates(filename, expand_factor=10, cascade_file="lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv.CascadeClassifier(cascade_file)
    image = cv.imread(filename, cv.IMREAD_COLOR)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.equalizeHist(gray)
    
    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor = 1.1,
                                     minNeighbors = 5,
                                     minSize = (MIN_SIZE, MIN_SIZE))
    if len(faces) == 0:
        return []
    else:
        faces = faces.reshape(-1)
    
    # note, faces array is returned in convention (x_upper_left, y_upper_left, width, height)
    # need to modify to fit with PIL convention of (left, upper, right, lower)

    # loop through each face, and add to a list
    face_coordinate_list = []

    for i in range(len(faces)//4):
        face_coordinate_list.append(
            (
                faces[i*4+0]+expand_factor, 
                faces[i*4+1]-expand_factor, 
                faces[i*4+0]+faces[i*4+2]-expand_factor, 
                faces[i*4+1]+faces[i*4+3]+expand_factor)
            )
    return face_coordinate_list

def crop_faces(image, face_coordinates):
    return image.crop(face_coordinates)

def resize_image_to_square(image, target_size=TARGET_SIZE):
    # crop a non-square image into a square.
    if image.size[0] != image.size[1]:
        size_to_crop_to = np.minimum(image.size[0], image.size[1])

        # cropping to centre
        left = (image.size[0] - size_to_crop_to)//2
        top = (image.size[1] - size_to_crop_to)//2
        right = (image.size[0] + size_to_crop_to)//2
        bottom = (image.size[1] + size_to_crop_to)//2

        # Crop the center of the image
        image = image.crop((left, top, right, bottom))

    # resize a larger or smaller image 
    if image.size != (target_size, target_size):
        image = image.resize((target_size, target_size))

    return image

def preprocess_image_hardcoded(image_path):
    """Wrapping cropping, transforms and saving into a single callable function. Includes auto delete for files that do not have detectable faces."""
    # Extract face coordinates
    coor_list = extract_face_coordinates(image_path)

    # if there is a single face, crop and replace the image with a face image.
    if len(coor_list) == 1:
        print('Single face detected.')
        image = PIL.Image.open(image_path)
        image = crop_faces(image, coor_list[0])
        image = resize_image_to_square(image)
        image.save(image_path)
        print(f'{image_path} replaced.')
    # if there is no face detected, skip and delete downloaded image.
    elif len(coor_list) == 0:
        print('No faces detected.')
        os.remove(image_path)
        print(f'{image_path} deleted.')
    # if there is more than one detected face, extract faces and save in an alternate folder.
    else:
        print(f'{len(coor_list)} faces detected.')
        image = PIL.Image.open(image_path)
        filename, ext = os.path.splitext(image_path.split('/')[-1])
        for ind, coor in enumerate(coor_list):
            image_cropped = crop_faces(image, coor)
            image_cropped = resize_image_to_square(image_cropped)

            image_cropped.save(os.path.join('./multiple_faces', f'{filename}_{ind}{ext}'))
            print(f"{os.path.join('./multiple_faces', f'{filename}_{ind}{ext}')} saved.")
        os.remove(image_path)
        print(f'{image_path} deleted.')

def preprocess_image(
    image_path: str, 
    preprocessing_function_list: list = [resize_image_to_square],
    save_multiple_faces: bool = True,
    folder_for_multiple_faces: str = "multiple_faces",
    delete_images_with_no_faces: bool = True,
    folder_for_no_detected_faces: str = "no_detected_faces"
    ):
    """Wrapping cropping, transforms and saving into a single callable function. Includes auto delete for files that do not have detectable faces."""
    # Extract face coordinates
    coor_list = extract_face_coordinates(image_path)

    # Create multiple face folder if it does not exist
    if not os.path.isdir(folder_for_multiple_faces):
        os.mkdir(folder_for_multiple_faces)

    if not delete_images_with_no_faces:
        if not os.path.isdir(folder_for_no_detected_faces):
            os.mkdir(folder_for_no_detected_faces)

    # if there is a single face, crop and replace the image with a face image.
    if len(coor_list) == 1:
        print('Single face detected.')
        image = PIL.Image.open(image_path)
        image = crop_faces(image, coor_list[0])
        for func in preprocessing_function_list:
            image = func(image)
        try:
            image.save(image_path)
            print(f'{image_path} replaced.')
        except Exception as e:
            print(e)
            os.remove(image_path)
            print(f"{image_path} removed.")

    # if there is no face detected, skip and delete downloaded image.
    elif len(coor_list) == 0:
        print('No faces detected.')
        if delete_images_with_no_faces:
            os.remove(image_path)
            print(f'{image_path} deleted.')
        else:
            shutil.move(image_path, os.path.join(folder_for_no_detected_faces, os.path.split(image_path)[-1]))

    # if there is more than one detected face, extract faces and save in an alternate folder.
    else:
        if save_multiple_faces:
            print(f'{len(coor_list)} faces detected.')
            image = PIL.Image.open(image_path)
            filename, ext = os.path.splitext(image_path.split(os.path.sep)[-1])
            for ind, coor in enumerate(coor_list):
                image_cropped = crop_faces(image, coor)
                for func in preprocessing_function_list:
                    image_cropped = func(image_cropped)

                image_cropped.save(os.path.join(folder_for_multiple_faces, f'{filename}_{ind}{ext}'))
                print(f"{os.path.join(folder_for_multiple_faces, f'{filename}_{ind}{ext}')} saved.")
        os.remove(image_path)
        print(f'{image_path} deleted.')

if __name__ == "__main__":
    from utils import download_image, preview_image
    import matplotlib.pyplot as plt
    from matplotlib import patches
    import PIL
    import shutil

    # Create temp directory
    if not os.path.exists("temp"):
        os.mkdir("temp")

    # _image_link = 'https://i.imgur.com/mA0x4tg.jpg'
    _image_link = 'https://i.imgur.com/L6Z3TUH.png'
    print(f"Downloading {_image_link}")
    img_filename = _image_link.split("/")[-1]
    img_path = os.path.join("temp", f"_temp{_image_link[-4:]}")
    download_image(_image_link, img_path)

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
    print("Testing pre-processing wrapper.")
    print('Pre-processing', img_path)
    preprocess_image(img_path, folder_for_multiple_faces=os.path.join("temp", "multiple_faces"))
    preview_image([os.path.join("temp", "multiple_faces", f) for f in os.listdir(os.path.join("temp", "multiple_faces"))])
    print('-'*12)

    print("Completed test, wiping temp folder.")
    shutil.rmtree("./temp")


