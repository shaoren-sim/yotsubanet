import requests
import shutil
from webscraper.reddit_scraper import strip_and_lowercase

def download_image(image_url: str, filename: str):
    """Function to download an image
    source: https://towardsdatascience.com/how-to-download-an-image-using-python-38a75cfa21c"""

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream = True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        try:
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
        except OSError as e:    # Catching error if filename is too long.
            print(e)
            print("truncating filename")
            filename = filename[:30]
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
            
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')