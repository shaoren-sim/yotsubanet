import torch
import torchvision
import torchvision.transforms as transforms

from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, datasets

import numpy as np
import matplotlib.pyplot as plt
from random import shuffle
import os
import PIL

class LabelFolderDataset(Dataset):
    def __init__(
        self, 
        data_dir, 
        data_limit=100, 
        transform=None
    ):
        self.data_dir = data_dir

        self.classes = os.listdir(data_dir)
        self.classes.sort()
        
        self.data_X = []
        self.data_y = []

        for ind, label_dir in enumerate(self.classes):
            available_images = os.listdir(os.path.join(data_dir, label_dir))
            if (data_limit is not None) and (len(available_images) > data_limit):
                shuffle(available_images)
                available_images = available_images[:data_limit]
            self.data_X.append(available_images)
            self.data_y.append([ind]*len(available_images))
        
        self.data_X = [item for sublist in self.data_X for item in sublist]
        self.data_y = [item for sublist in self.data_y for item in sublist]

        if transform is None:
            # print("default transform")
            # Calculating mean and standard deviations for all images for normalization
            """_images = [
                            np.array(PIL.Image.open(
                                os.path.join(
                                    self.data_dir, 
                                    self.classes[label_ind],
                                    img
                                    )
                                ).convert('RGB')).transpose(2, 0, 1).reshape(3, -1)
                            for label_ind, img in zip(self.data_y, self.data_X)
                        ]
            _images = np.array(_images)
            mean = _images.mean(axis=2).mean(axis=0) / 255
            std = _images.std(axis=2).mean(axis=0) / 255"""

            _images = [
                            os.path.join(
                                self.data_dir, 
                                self.classes[label_ind],
                                img
                            )
                        for label_ind, img in zip(self.data_y, self.data_X)]
            mean, std = obtain_channel_mean_std(_images)
            # print("mean:", mean)
            # print("std:", std)

            transform = [
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=mean/255,
                    std=std/255,
                    ),
                transforms.RandomHorizontalFlip(p=0.5)
            ]

        if type(transform) == list:
            self.transform = transforms.Compose(transform)
        else:
            self.transform = transform

    def __len__(self):
        return len(self.data_X)

    def __getitem__(self, idx):
        image = PIL.Image.open(
            os.path.join(
                self.data_dir, 
                self.classes[self.data_y[idx]],
                self.data_X[idx]
                )
            ).convert('RGB')

        if self.transform:
            image = self.transform(image)
            
        return (image, self.data_y[idx])
    
    def get_PIL_item(self, idx):
        image = PIL.Image.open(
            os.path.join(
                self.data_dir, 
                self.classes[self.data_y[idx]],
                self.data_X[idx]
                )
            ).convert('RGB')
            
        return (image, self.data_y[idx])

def obtain_channel_mean_std(images):
    if type(images) is list:    # input variable is a list of paths
        images = [
                        np.array(
                            PIL.Image.open(img_path).convert('RGB')
                        ).transpose(2, 0, 1).reshape(3, -1)
                        for img_path in images
                    ]
        images = np.array(images)
    elif type(images) is np.ndarray:
        if len(images.shape) != 4:
            raise ValueError("Input variable must either be a list of paths, or an array of images in the form (BATCH, CHANNELS, WIDTH, HEIGHT)")
        images = images
    else:
        raise ValueError("Input variable must either be a list of paths, or an array of images in the form (BATCH, CHANNELS, WIDTH, HEIGHT)")
    mean = images.mean(axis=2).mean(axis=0)
    std = images.std(axis=2).mean(axis=0)

    return mean, std

def train_test_split(dataset, split_factor: float = 0.05):
    train_set, validation_set = torch.utils.data.random_split(
        dataset,
        [
            int(np.round(len(dataset)*(1-split_factor))), 
            int(np.round(len(dataset)*split_factor))]
    )
    print(f'Training data: {len(train_set)}')
    print(f'Validation data: {len(validation_set)}')
    return train_set, validation_set

def preview_dataset(dataset: LabelFolderDataset, size: int = 10):
    dataset_classes = dataset.classes
    fig, ax = plt.subplots(2, 10)
    fig.set_figwidth(12)
    fig.set_figheight(7)
    for ind, i in enumerate(np.random.randint(len(dataset), size=size)):

        img, label_ind = dataset[i]
        img_pre_transform, _ = dataset.get_PIL_item(i)
        
        ax[0, ind].imshow(img.transpose(0, 2).transpose(0, 1))
        ax[0, ind].set_title(dataset_classes[label_ind])
        ax[0, ind].axis('off')
        ax[1, ind].imshow(img_pre_transform)
        ax[1, ind].axis('off')
    plt.tight_layout()
    plt.show()

def preview_subset(
    dataset: LabelFolderDataset, 
    subset: torch.utils.data.dataset.Subset, 
    size: int = 4,
    title: str = None
    ):
    dataset_classes = dataset.classes
    fig, ax = plt.subplots(1, size)
    # fig.set_figwidth(12)
    # fig.set_figheight(7)
    for ind, img in enumerate(list(subset)[:size]):
        # print(ind, i)
        img, label_ind = subset[ind]
        
        ax[ind].imshow(img.transpose(0, 2).transpose(0, 1))
        ax[ind].set_title(dataset_classes[label_ind])
        ax[ind].axis('off')
    plt.tight_layout()
    plt.suptitle(title)
    plt.show()