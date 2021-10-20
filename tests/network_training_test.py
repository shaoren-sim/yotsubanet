import os
import torch
import matplotlib.pyplot as plt

from network.main_trainer import main_training_loop
from network.dataloader import LabelFolderDataset
from network.evaluation import eval_on_folder

DATA_DIR = "./yotsubanet_scraped_data/data"
DATA_LIMIT = 10
EPOCHS = 3
VALIDATION_FACTOR = 0.1

TEST_DATA_DIR = "/home/shaoren/Desktop/yotsubanet/extra_unlabelled_data/multiple_faces"
EVAL_IMAGES_LIMIT = 10

if __name__ == "__main__":
    print("Test 1: Training on CPU.")
    # Creating dataset from webscraper output folder
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
    )

    final_model = main_training_loop(
        classes,
        dataset,
        EPOCHS,
        validation_set_factor=VALIDATION_FACTOR,
        batch_size=16,
        device="cpu",
    )

    # Testing model on unseen data.
    eval_on_folder(dataset, final_model, TEST_DATA_DIR, EVAL_IMAGES_LIMIT, device="cpu")

    print("Test 2: Training on GPU.")
    if torch.cuda.is_available():
        print("CUDA-capable GPU is available, proceeding.")
    else:
        raise RuntimeError("No CUDA-capable GPU, terminating.")
    
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
    )

    final_model = main_training_loop(
        classes,
        dataset,
        EPOCHS,
        validation_set_factor=VALIDATION_FACTOR,
        batch_size=16,
        device="cuda:0",
    )

    # Testing model on unseen data.
    eval_on_folder(dataset, final_model, TEST_DATA_DIR, EVAL_IMAGES_LIMIT, device="cuda:0")