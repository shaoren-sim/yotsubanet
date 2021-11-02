# yotsuba-net

An all-in-one solution for training anime face classification models by leveraging Reddit webscraping.

# Introduction
Machine learning classifier require a large dataset of labelled data for satisfactory performance. This generally requires established, curated datasets such as [ImageNet](https://www.image-net.org/) or [CIFAR-10/CIFAR-100](https://www.cs.toronto.edu/~kriz/cifar.html).

For the problem of anime face classification, large datasets such as [Anime-Face-Dataset](https://github.com/bchao1/Anime-Face-Dataset) and [Danbooru2020](https://www.gwern.net/Danbooru2020#danbooru2018) exist, but they are primarily designed for generative or detection tasks.

In this project, we leverage Reddit fan communities as a source of labelled data for targeted classification. Assuming an anime property is popular enough, one can find many sources of labelled image data through webscraping. In our implementation, we use the following sources.

- Image posts on character-specific subreddits (i.e. images of Yotsuba from [/r/Yotsubros/](www.reddit.com/r/Yotsubros/))
- Image posts on a property-specific title with a character's name in title (i.e. posts titled 'Yotsuba' from [/r/5ToubunNoHanayome/](https://www.reddit.com/r/5ToubunNoHanayome/))
- Image links in comments of anime discussion posts with a character's name in link text (i.e. [comment links with text string 'Yotsuba'](https://www.reddit.com/r/anime/comments/m80o69/comment/greqvhm/?utm_source=share&utm_medium=web2x&context=3) from episode discussion threads on [/r/anime](www.reddit.com/r/anime))

We designed a job-based interface for constructing a webscraping routine through [Reddit's PRAW API](https://pypi.org/project/praw/), and include some common dataset cleanup routines that can automate improvement of the dataset quality.

A complete CNN backbone (Resnet18) is also provided, and has been validated to work sufficiently well on test tasks.

# Quickstart (default Gotoubun no Hanayome task)
1. Clone this repository.
2. Ensure Python 3.6+ is installed.
3. Navigate to main directory. 
    `$ cd /path/to/cloned/repository`
4. Install requirements. 
    `$ pip install -r requirements.txt`
5. Download [lbpcascade_animeface](https://github.com/nagadomi/lbpcascade_animeface) HAAR cascade file. 
    `$ wget https://raw.githubusercontent.com/nagadomi/lbpcascade_animeface/master/lbpcascade_animeface.xml`
6. Run webscraper with pre-defined job. **OR** Extract example dataset.
    `$ python run_webscraper.py` **OR** `$ gzip -d test_dataset.tar.gz`
7. Run CNN classifier training.
    `$ python run_classifier_training.py`
8. Test classifier model on movie key visual. 
    `$ python run_eval_single_image.py`

# Install and Run (custom webscraper task)
1. Clone this repository.
2. Ensure Python 3.6+ is installed.
3. Navigate to main directory. 
    `$ cd /path/to/cloned/repository`
4. Install requirements. 
    `$ pip install -r requirements.txt`
5. Download [lbpcascade_animeface](https://github.com/nagadomi/lbpcascade_animeface) HAAR cascade file. 
    `$ wget https://raw.githubusercontent.com/nagadomi/lbpcascade_animeface/master/lbpcascade_animeface.xml`
6. Set up Reddit credentials at `config/reddit_praw_login_details.py` by creating a script app at [https://old.reddit.com/prefs/apps/](https://old.reddit.com/prefs/apps/). A working scraper bot agent's credentials are provided by default, but not guaranteed to work.
6. Configure custom scraper session JSON with jobs.
7. Run webscraper. 
    `$ python run_webscraper.py --i /path/to/session/joblist.json --o /path/to/output/dir`
8. **(Recommended)** Do manual data cleanup for labelled training data.
9. Run CNN classifier training.  
    `$ python run_classifier_training.py`
10. Test classifier predictions on unlabelled faces. 
    `$ python run_model_evaluation.py --model /path/to/model.pth --data /path/to/unlabelled/data`

## Notes
Python scripts can be alternatively run without CLI arguments by editing global constants in scripts.

In `run_webscraper.py`:
```python
SESSION_FILE = "examples/gotoubun_no_hanayome/gotoubun_no_hanayome.json"
SESSION_DIR = "goutoubun_no_hanayome"
PROCESSES = 4
```

Sample webscraper session JSON for 五等分の花嫁  *(Gotoubun no Hanayome)* is available under `./examples/gotoubun_no_hanayome/gotoubun_no_hanayome.json`.

# Testing Model on Images
After model training, run the following file after modifying settings:
    `$ python run_eval_single_image.py`

```python
FILE_TO_EVAL = "path/to/image.png"
OUTPUT_FILE = "path/for/saved/image.png"
SESSION_DIR = "session_directory"
DEVICE = "cuda:0" OR "cpu"

USE_BEST = False

# Viola cascade parameters. Worth tuning for images to detect faces properly.
CASCADE_MIN_NEIGHBORS = 6
CASCADE_SCALE = 1.01
```
Modifying the cascade variables is recommended to fine-tune face detection.

![result](examples/gotoubun_no_hanayome/results/single_image_eval.png)

- Original image obtained from https://pbs.twimg.com/media/ExVxLqtUUAErTkv.jpg?name=large.
- Resnet18 weights used for image predictions available in `examples/gotoubun_no_hanayome/results/checkpoint.pth.tar`.
- Dataset used for model training available in `test_dataset.tar.gz`.

# Features
The primary component in this package is the Reddit webscraper, which includes the following features:
- Reddit image scraping with PRAW
    - Reddit comment link scraper
    - Reddit image post scraper
    - Image downloader (with Imgur and Reddit gallery support)
    - Multiprocessing support
    - #TODO ~~Job creator CLI utility~~
- Dataset preparation
    - Face detection
    - Image crop and rescaling
    - Labelled and unlabelled data sorting
- Dataset cleanup
    - Image similarity detection with perceptual hashing
        - `phash`, `dhash` and `ahash` algorithms
    - Grayscale/manga image removal
- Dataset visualization

For CNN classifier training, a Pytorch backbone is provided, with an end-to-end Resnet18 model included by default.
- Dataset per-class max size constraint
    - For datasets with unbalanced class sizes.
- Multiple normalization methods
    - Dataset-wide automatic channel normalization (default)
    - Per-image normalization layer (using `nn.Sequential` wrapper)
- One-liner model training with modularity
    - Tracks and save model with best validation loss.
- Visualize model predictions
- Extract and classify faces from images.

While Pytorch is used, the webscraper outputs are in can be used with any machine learning framework or techniques.

The name **'yostuba-net'** was inspired by the 2021 anime 五等分の花嫁∬  *(Gotoubun no Hanayome ∬)*, the initial toy problem which the project was designed on.

# Requirements
- [PRAW](https://pypi.org/project/praw/)
- [imgur_downloader](https://github.com/jtara1/imgur_downloader)
- [lbpcascade_animeface](https://github.com/nagadomi/lbpcascade_animeface)
- [Pytorch](https://pytorch.org/)
- [OpenCV](https://opencv.org/)
- [PIL](https://python-pillow.org/)
- [Numpy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/)

# To-do list:
## Webscraper
- Implement CLI session and job generator.
- ~~Modify session files to be in JSON format for easier parsing.~~
- Test on alternative labelled dataset.
- Sort out tests and provide clear example.
- Add detailed documentation.
- Add references.

## Machine Learning
- ~~Add early stopping constraint~~
- Add alternative model wrappers.