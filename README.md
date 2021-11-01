# yotsuba-net

An all-in-one solution for training anime face classification convolutional neural networks by leveraging Reddit webscraping.

# Description and Background
Machine learning classifier require a large dataset of labelled data for satisfactory performance. This generally requires established, curated datasets such as [ImageNet](https://www.image-net.org/), [CIFAR-10/CIFAR-100](https://www.cs.toronto.edu/~kriz/cifar.html) or [MNIST](http://yann.lecun.com/exdb/mnist/).

Alternatively, one could use services such as Amazon Mechanical Turk (https://www.mturk.com/), which allows crowdsourced labelling by humans, but this is expensive and beyond the bounds of most toy problems.

For the problem of anime face classification, large datasets such as [Anime-Face-Dataset](https://github.com/bchao1/Anime-Face-Dataset) and [Danbooru2020](https://www.gwern.net/Danbooru2020#danbooru2018) exist, but they are primarily designed for generative or detection tasks.

In this project, we leverage Reddit fan communities as a source of labelled data. Assuming an anime property is popular enough, one can find many sources of labelled image data through webscraping. In our implementation, we use the following sources.

- Image posts on character-specific subreddits (i.e. images of Yotsuba from [/r/Yotsubros/](www.reddit.com/r/Yotsubros/))
- Image posts on a property-specific title with a character's name in title (i.e. posts titled 'Yotsuba' from [/r/5ToubunNoHanayome/](https://www.reddit.com/r/5ToubunNoHanayome/))
- Image links in comments of anime discussion posts with a character's name in link text (i.e. [comment links with text string 'Yotsuba'](https://www.reddit.com/r/anime/comments/m80o69/comment/greqvhm/?utm_source=share&utm_medium=web2x&context=3) from episode discussion threads on [/r/anime](www.reddit.com/r/anime))

We designed a job-based interface for constructing a webscraping routine through Reddit's PRAW API, and include some common dataset cleanup routines that can improve the quality of the dataset

A basic CNN backbone is also provided, and has been validated to work reasonably well on test tasks.

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
    - Image duplicate/similarity detection with perceptual hashing
        - `phash`, `dhash` and `ahash` algorithms
    - #TODO ~~Grayscale/manga image removal~~
- Dataset visualization

For CNN classifier training, a Pytorch backbone is provided, with an end-to-end Resnet18 model included by default.
- Dataset per-class max size constraint
    - For datasets which have unbalanced class sizes.
- Multiple normalization methods
    - Per-image normalization layer (using `nn.Sequential` wrapper)
    - Dataset-wide automatic channel normalization
- One-liner model training with modularity
    - Track and save model with best validation loss.
- Visualize model predictions

While Pytorch is used, the webscraper outputs are in can be used with any machine learning framework or technique.

The name **'yostuba-net'** was inspired by the 2021 anime 五等分の花嫁∬  *(Gotoubun no Hanayome ∬)*, the initial toy problem which the webscraper/network combo was designed on.

# Requirements
- [PRAW](https://pypi.org/project/praw/)
- [imgur_downloader](https://github.com/jtara1/imgur_downloader)
- [lbpcascade_animeface](https://github.com/nagadomi/lbpcascade_animeface)
- [Pytorch](https://pytorch.org/)

# To-do list:
## Webscraper
- Implement CLI session and job generator.
- Modify session files to be in JSON format for easier parsing.
- Test on alternative labelled dataset.
- Code dependency resolving `setup.py` file.
- Sort out tests and provide clear example.
- Add detailed documentation instead of 'it just works' mentaility for easier modularity.
- Add detailed references.

## Machine Learning
- Add early stopping constraint