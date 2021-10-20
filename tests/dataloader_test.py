import os
from network.dataloader import LabelFolderDataset, preview_dataset, train_test_split, preview_subset
from random import shuffle
from torchvision import transforms
from webscraper.utils import preview_image

if __name__ == "__main__":
    DATA_DIR = "./yotsubanet_scraped_data/data"
    DATA_LIMIT = 100

    print("Test 1: Default transforms")
    classes = os.listdir(DATA_DIR)
    classes.sort()
    print("Classes:", classes)

    print("Data count per label:")
    for class_name in classes:
        available_files = os.listdir(os.path.join(DATA_DIR, class_name))
        print(class_name, ":", len(available_files))

    dataset = LabelFolderDataset(
        data_dir=DATA_DIR,
        data_limit=DATA_LIMIT,
        # transform=[
        #     transforms.ToTensor(),
        #     transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225]),
        # ]
    )

    print("Check plotted dataset preview. If labels are off, check folder names. If images are not right, replace data.")
    preview_dataset(dataset)

    print("Test 2: Custom transform to grayscale.")
    dataset = LabelFolderDataset(
        data_dir=DATA_DIR,
        data_limit=DATA_LIMIT,
        transform=[
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225]),
            transforms.Grayscale()
        ]
    )

    print("Check plotted dataset preview. If labels are off, check folder names. If images are not right, replace data.")
    preview_dataset(dataset)

    print("Test 3: Testing train/test splitting")
    train_set, valid_set = train_test_split(dataset)
    
    preview_subset(dataset, train_set, title="training_set")
    preview_subset(dataset, valid_set, title="validation_set")