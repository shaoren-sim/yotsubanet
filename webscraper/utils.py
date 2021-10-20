from matplotlib import image
import PIL
import matplotlib.pyplot as plt
import os

def initialize_data_folder(list_of_labels: list, folder_name: str = "./data"):
    # Initializing dataset storage
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    for ind, label in enumerate(list_of_labels):
        # directory = os.path.join(folder_name, f"{ind}_{label}")
        directory = os.path.join(folder_name, f"{label}")
        if not os.path.isdir(directory):
            os.mkdir(directory)

def preview_image(image_path):
    """Preview the full image. Input argument can be a single image or multiple."""
    if type(image_path) is str:
        if not image_path.endswith((".png", ".jpg")):
            raise ValueError("Image must be .png or .jpg.")
        img = PIL.Image.open(image_path)
        plt.imshow(img)
        plt.title(image_path)
        plt.show()
    elif type(image_path) is list:
        _len_images = len(image_path)
        if _len_images < 4:
            fig, ax = plt.subplots(1, _len_images)
        else:
            print("More than 4 images detected, previewing first 4 images.")
            image_path = image_path[:4]
            fig, ax = plt.subplots(2, 2)
            
        for ind, image in enumerate(image_path):
            print(ind, image)
            if not image.endswith((".png", ".jpg")):
                raise ValueError("Image must be .png or .jpg.")
            img = PIL.Image.open(image)

            if _len_images < 4:
                ax[ind].imshow(img)
                ax[ind].set_title(image)
            else:
                _x = ind // 2
                _y = ind % 2
                ax[_x, _y].imshow(img)
                ax[_x, _y].set_title(image)
        plt.tight_layout()
        plt.show()

def count_data_in_folder(folder: str):
    image_counts = len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])
    return image_counts

def preview_data_folder(data_folder: str, title: str,):
    labeled_images = [name for name in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, name))]
    rows = len(labeled_images) // 10
    fig, axes = plt.subplots(rows, 10)
    fig.set_figheight(2*rows+2)
    fig.set_figwidth(20)
    # for ind, img in enumerate(labeled_images):
    for ind, ax in enumerate(axes.ravel()):
        img = labeled_images[ind]
        # print(ind, img)
        if ind == rows*10:
            break
        im = PIL.Image.open(os.path.join(data_folder, img), 'r')
        ax.imshow(im)
        ax.axis('off')
    fig.suptitle(f'{title}')
    plt.tight_layout()
    plt.show()
    print('-'*12)

