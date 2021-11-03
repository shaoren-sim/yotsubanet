# %%
from pathlib import Path
from webscraper.dataset_cleanup.image_hashing import hamming_distance, perceptual_hash, difference_hash, average_hash
import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

IMAGE_FORMATS = [".png", ".jpg", ".jpeg"]

class DatasetCleanup():
    def __init__(
        self,
        labelled_data_folder: str,
        unlabelled_data_folder: str,
        image_hash_method: str = "dhash",
        hamming_distance_threshold: int = 7,
        grayscale_threshold_value: float = 0.005,
    ):
        """Class for duplicate detection and deletion. Wraps around hashing algorithms and plotting function.

        Args:
            labelled_data_folder (str): Folder path for labelled data.
            unlabelled_data_folder (str): Folder path for unlabelled data.
            image_hash_method (str, optional): Chosen hashing method, must be in ["dhash", "phash", "ahash"]. Can pass custom hashing method. Default "dhash" setting is fastest, performing best on Gotoubun no Hanayome test set. Defaults to "dhash".
            hamming_distance_threshold (int, optional): Hamming distance threshold. For default d-hash setting, default value performs best on Gotoubun no Hanayome test set. Defaults to 7.
        """    
        labelled_data_folder = Path(labelled_data_folder)
        unlabelled_data_folder = Path(unlabelled_data_folder)

        if image_hash_method == "dhash":
            self.image_hash_method = difference_hash
        elif image_hash_method == "phash":
            self.image_hash_method = perceptual_hash
        elif image_hash_method == "ahash":
            self.image_hash_method = average_hash
        else:
            raise ValueError("image_hash_method must be in ['dhash', 'ahash', 'phash']")

        if hamming_distance_threshold < 0 or hamming_distance_threshold > 64:
            raise ValueError("hamming_distance_threshold must be withing bounds (0, 64) with hash_size of 4.")
        
        self.labelled_data_folder = labelled_data_folder
        self.unlabelled_data_folder = unlabelled_data_folder
        self.hamming_distance_threshold = hamming_distance_threshold
        self.grayscale_threshold_value = grayscale_threshold_value
    
    def count_images(self):
        """Count images in each folder, based on the class' labelled_data_folder and unlabelled_data_folder arguments.
        """
        print("Labelled Data")
        _labeled_data_folders = os.listdir(self.labelled_data_folder)
        for label in _labeled_data_folders:
            print(f"{label}: {len([f for f in os.listdir(os.path.join(self.labelled_data_folder, label)) if os.path.splitext(f)[-1] in IMAGE_FORMATS])} images")
        
        print(f"Unlabelled Data: {len(os.listdir(self.unlabelled_data_folder))} images")
    
    def inspect_duplicates(self):
        """
        Sequentially find and plot all duplicates. Does not delete duplicates, and can be used as an initial run to test if the chosen hashing method and distance threshold is properly set up.
        Notebook or Interactive Python environment is recommended for this.
        """
        for folder in [os.path.join(self.labelled_data_folder, f) for f in os.listdir(self.labelled_data_folder)] + [self.unlabelled_data_folder]:
            print(folder)
            file_list = get_images(os.path.join(folder))
            file_hash_dict = generate_hash_dict(file_list, self.image_hash_method)
            print(len(file_hash_dict), "total images.")
            duplicate_dict = get_duplicates_of_files(file_hash_dict)
            print(len(duplicate_dict), "duplicate images.")
            # delete_duplicates(duplicate_dict)
        
            key_list = list(duplicate_dict.keys())
            key_value_list = list(duplicate_dict.items())
            print(len(duplicate_dict.values()))
            _removed_keys = []
            for key, value in key_value_list:
                # Ugly loop required as duplicate_dicts are modified in the loop.
                if key in _removed_keys:
                    continue
                    
                # removes the current key from the values, as the image itself is a perfect match regardless of hashing.
                value.remove((key, 0))

                # pop the current values from keys, which will make plotting easier due to no recursiveness.
                for img, score in value:
                    duplicate_dict.pop(img, None)
                    try:
                        key_list.remove(img)
                    except ValueError:
                        continue
                    _removed_keys.append(img)
            
            # Plotting code.
            # Determine maximum number of duplicates, to use for subplot axis
            aspect = "equal"
            for ind, (img, dupes) in enumerate(duplicate_dict.items()):
                _max_dupes = len(dupes)
                fig, ax = plt.subplots(
                    # 1, 
                    _max_dupes+1, 
                    1,
                    # figsize=(7, _max_dupes*3),
                    # figsize=(_max_dupes*3, 4)
                )
            
                ax[0].imshow(Image.open(img), aspect=aspect)
                ax[0].set_title(os.path.split(img)[-1])
                _plotted_dupes = 0
                for dupe_ind, (dupe, distance) in enumerate(dupes):
                    ax[1+dupe_ind].imshow(Image.open(dupe), aspect=aspect)
                    # ax[ind, 1+dupe_ind].set_xticks([])
                    # ax[ind, 1+dupe_ind].set_yticks([])
                    ax[1+dupe_ind].set_title(f"{dupe.split(os.path.sep)[-1]} - {distance}")
                    _plotted_dupes += 1
                plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])
                plt.tight_layout()
                plt.show()

    def delete_duplicates(self):
        """Wrapper around hashing function, distance metric and duplicate deletion.
        """
        # Labelled data deduplication
        for folder in os.listdir(self.labelled_data_folder):
            print(folder)
            file_list = get_images(os.path.join(self.labelled_data_folder, folder))
            file_hash_dict = generate_hash_dict(file_list, self.image_hash_method)
            print(len(file_hash_dict), "total images.")
            duplicate_dict = get_duplicates_of_files(file_hash_dict)
            print(len(duplicate_dict), "duplicate images.")
            delete_duplicates(duplicate_dict)
        # Unlabelled data deduplication
        print(f"Unlabelled data: {self.unlabelled_data_folder}")
        file_list = get_images(self.unlabelled_data_folder)
        file_hash_dict = generate_hash_dict(file_list, self.image_hash_method)
        print(len(file_hash_dict), "total images.")
        duplicate_dict = get_duplicates_of_files(file_hash_dict)
        print(len(duplicate_dict), "duplicate images.")
        delete_duplicates(duplicate_dict)

    def preview_grayscale(self):
        """Preview grayscale images determined by pixel threshold test"""
        grayscale_list = []
        for folder in os.listdir(self.labelled_data_folder):
            print(folder)
            file_list = get_images(os.path.join(self.labelled_data_folder, folder))
            grayscale_list.append([img for img in file_list if is_grayscale(img, self.grayscale_threshold_value)])
        # Unlabelled data deduplication
        print(f"Unlabelled data: {self.unlabelled_data_folder}")
        file_list = get_images(self.unlabelled_data_folder)
        grayscale_list.append([img for img in file_list if is_grayscale(img, self.grayscale_threshold_value)])
        
        # Flatten list of grayscale images
        grayscale_list = [val for sublist in grayscale_list for val in sublist]
        print(len(grayscale_list), "grayscale images.")

        fig, ax = plt.subplots(len(grayscale_list) // 10, 10)
        fig.set_figheight((len(grayscale_list) // 10) * 3)
        fig.set_figwidth(25)

        for ind, a in enumerate(ax.flat):
            image_to_eval_fn = grayscale_list[ind]
            image_to_eval = Image.open(os.path.join(image_to_eval_fn)).convert('RGB')
            a.imshow(image_to_eval)
            a.axis('off')
        plt.tight_layout()
        plt.show()
    
    def remove_grayscale(self):
        """Find and remove grayscale images.
        """
        grayscale_list = []
        for folder in os.listdir(self.labelled_data_folder):
            print(folder)
            file_list = get_images(os.path.join(self.labelled_data_folder, folder))
            grayscale_list.append([img for img in file_list if is_grayscale(img, self.grayscale_threshold_value)])
        # Unlabelled data deduplication
        print(f"Unlabelled data: {self.unlabelled_data_folder}")
        file_list = get_images(self.unlabelled_data_folder)
        grayscale_list.append([img for img in file_list if is_grayscale(img, self.grayscale_threshold_value)])
        
        # Flatten list of grayscale images
        grayscale_list = [val for sublist in grayscale_list for val in sublist]
        print(len(grayscale_list), "grayscale images.")
        for grayscale_img in grayscale_list:
            os.remove(grayscale_img)

def get_images(data_dir):
    """Walks across full data folder and obtains filepath of all images."""

    results = [os.path.join(d, x) for d, dirs, files in os.walk(data_dir) for x in files if os.path.splitext(x)[-1] in IMAGE_FORMATS]

    return results

def generate_hash_dict(file_list, hash_method = perceptual_hash):
    """Using list of files, generate a dictionary of hashes based on input hash method."""

    hash_list = [hash_method(Image.open(f)) for f in file_list]

    # print(hash_list)

    return dict(zip(file_list, hash_list))

def _get_duplicates_of_file(file_path, hash_dict: dict, distance_tol: int = 10):
    return [
        (
            comp_file_path, 
            hamming_distance(hash_dict[file_path], hash_dict[comp_file_path])
        )
        for comp_file_path in hash_dict
        if hamming_distance(hash_dict[file_path], hash_dict[comp_file_path]) <= distance_tol
        # and comp_file_path != file_path
    ]

def get_duplicates_of_files(file_hash_dict: dict):
    duplicate_dict = dict()
    for f in file_hash_dict:
        duplicates = _get_duplicates_of_file(f, file_hash_dict, 7)

        # File will always match itself as a perfect duplicate.
        # We retain the path of the original image in the returned dictionary.
        # We delete using a simple 'keep one' strategy.
        if len(duplicates) > 1:
            duplicate_dict[f] = duplicates
        
    return duplicate_dict

def delete_duplicates(dictionary_of_duplicates: dict):
    for image, duplicates in dictionary_of_duplicates.items():
        # Checking if current image still exists, as it might have been deleted.
        if os.path.exists(image):
            for dupe_path, dupe_score in duplicates[1:]:
                print(dupe_path)
                try:
                    os.remove(dupe_path)
                except FileNotFoundError:
                    continue

def is_grayscale(img_path: str, threshold: float = 0.01):
    img = Image.open(img_path)

    ### splitting b,g,r channels
    channels = img.split()
    if len(channels) == 4:
        r, g, b, a = channels
        r = np.array(r)
        g = np.array(g)
        b = np.array(b)
    elif len(channels) == 3:
        r, g, b = channels
        r = np.array(r)
        g = np.array(g)
        b = np.array(b)
    elif len(channels) == 1:
        # Is grayscale
        return True

    ### getting differences between per-channel pixels
    r_g = np.sum(np.abs(r - g))
    r_b = np.sum(np.abs(r - b))
    g_b = np.sum(np.abs(g - b))

    ### summing differences in channels
    diff_sum = np.sum(r_g + r_b + g_b)

    ### finding ratio of diff_sum with respect to size of image
    ratio = diff_sum / get_num_pixels(img)
    if ratio > threshold:
        return False
    else:
        return True

def get_num_pixels(img: Image):
    width, height = img.size
    return width*height

if __name__ == "__main__":
    bw_img_path = '/home/shaoren/Desktop/yotsubanet/goutoubun_no_hanayome/data/miku/daily_miku_49.png'
    print(is_grayscale(bw_img_path))

    # dupe_detect.delete_duplicates()