# %%
from PIL import Image
import numpy as np
from scipy.spatial.distance import hamming

def hamming_distance(arr_1, arr_2):
    """Simplified Hamming distance function designed to work with arrays as well as bit strings.

    String comparison based on https://stackoverflow.com/questions/54172831/hamming-distance-between-two-strings-in-python
    
    """
    if not type(arr_1) == type(arr_2):
        raise ValueError("Arguments for hamming_distance must be of the same type.")
    if type(arr_1) is np.ndarray:
        return np.sum(np.count_nonzero(arr_1 != arr_2))
    elif type(arr_1) is str:
        return sum(c1 != c2 for c1, c2 in zip(arr_1, arr_2))

def average_hash(image: Image, dim_x: int = 8, dim_y: int = 8, return_bitstring: bool = True):
    """Average hashing algorithm implemented from: http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
    
    Hashing implementation based on: https://web.archive.org/web/20171112054354/https://www.safaribooksonline.com/blog/2013/11/26/image-hashing-with-python/
    """
    # Shrink image
    image = image.resize((dim_x, dim_y), Image.ANTIALIAS)

    # Convert image to grayscale.
    image = image.convert("L")

    # Average colours.
    pixel_array = np.asarray(image)
    pixel_mean = np.mean(pixel_array)

    # Compute bits, based on whether the color value is above or below the mean.
    pixels_above_mean = np.reshape(pixel_array > pixel_mean, -1).astype(np.intc)

    if return_bitstring:
        bit_string = "".join(map(str, pixels_above_mean.tolist()))

        return bit_string
    else:
        return pixels_above_mean

def perceptual_hash(image: Image, dim_x: int = 32, dim_y: int = 32, return_bitstring: bool = True):
    """Perceptual hashing algorithm implemented from: http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

    Requires scipy for the dct algorithm
    """
    from scipy.fftpack import dct
    # Shrink image
    image = image.resize((dim_x, dim_y), Image.ANTIALIAS)
    # Convert image to grayscale.
    image = image.convert("L")

    # Compute discrete cosine transform, and take only top-left 8x8
    pixel_array = np.asarray(image)
    discrete_cosine_transform = dct(dct(pixel_array, axis=0), axis=1)
    
    # Compute average values, using mean DCT value, excluding first term since DC coefficient can be different and throw off the average.
    dct_mean = np.mean(discrete_cosine_transform)

    pixels_above_mean = np.reshape(discrete_cosine_transform > dct_mean, -1).astype(np.intc)

    if return_bitstring:
        bit_string = "".join(map(str, pixels_above_mean.tolist()))

        return bit_string
    else:
        return pixels_above_mean

def perceptual_hash_simple(image: Image, dim_x: int = 32, dim_y: int = 32, hash_size: int = 8, return_bitstring: bool = True):
    """Perceptual hashing algorithm implemented from: http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

    Requires scipy for the dct algorithm
    """
    from scipy.fftpack import dct
    # Shrink image
    image = image.resize((dim_x, dim_y), Image.ANTIALIAS)
    # Convert image to grayscale.
    image = image.convert("L")

    # Compute discrete cosine transform, and take only top-left 8x8
    pixel_array = np.asarray(image)
    discrete_cosine_transform = dct(pixel_array)[:hash_size, 1:hash_size+9]
    
    # Compute average values, using mean DCT value, excluding first term since DC coefficient can be different and throw off the average.
    dct_mean = np.mean(discrete_cosine_transform)

    pixels_above_mean = np.reshape(discrete_cosine_transform > dct_mean, -1).astype(np.intc)

    if return_bitstring:
        bit_string = "".join(map(str, pixels_above_mean.tolist()))

        return bit_string
    else:
        return pixels_above_mean

def difference_hash(image: Image, dim_x: int = 9, dim_y: int = 8, hash_size: int = 8, return_bitstring: bool = True):
    """Difference hashing algorithm implemented from: http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html

    Requires scipy for the dct algorithm
    """
    # Shrink image
    image = image.resize((dim_x, dim_y), Image.ANTIALIAS)

    # Convert image to grayscale.
    image = image.convert("L")

    # Average colours.
    pixel_array = np.asarray(image)

    # Comparing pixels with adjacent pixels
    difference = np.reshape(pixel_array[:, 1:] > pixel_array[:, :-1], -1).astype(np.intc)

    if return_bitstring:
        bit_string = "".join(map(str, difference.tolist()))

        return bit_string
    else:
        return difference