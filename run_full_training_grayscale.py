import os
import torch
import matplotlib.pyplot as plt
from torchvision.transforms.transforms import Normalize

from network.main_trainer import main_training_loop
from network.dataloader import LabelFolderDataset, obtain_channel_mean_std
from network.evaluation import eval_on_folder

from torchvision import transforms

DATA_DIR = "./yotsubanet_scraped_data/data"
DATA_LIMIT = 150
EPOCHS = 50
VALIDATION_FACTOR = 0.2
DEVICE = "cuda:0"

TEST_DATA_DIR = "/home/shaoren/Desktop/yotsubanet/extra_unlabelled_data/multiple_faces"
EVAL_IMAGES_LIMIT = 100

if __name__ == "__main__":
    if "cuda" in DEVICE:
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

    # val for sublist in list_of_lists for val in sublist
    mean, std = obtain_channel_mean_std(
        [val for sublist in [
            [
                os.path.join(DATA_DIR, label, f) for f in os.listdir(os.path.join(DATA_DIR, label))
            ]
            for label in classes
        ] for val in sublist ]
    )

    dataset = LabelFolderDataset(
        data_dir=DATA_DIR,
        data_limit=DATA_LIMIT,
        transform=[
            transforms.ToTensor(),
            transforms.Normalize(mean=mean/255, std=std/255),
            transforms.Grayscale(num_output_channels=3),
            transforms.RandomHorizontalFlip(p=0.5)
        ]
    )

    final_model = main_training_loop(
        classes,
        dataset,
        EPOCHS,
        validation_set_factor=VALIDATION_FACTOR,
        batch_size=8,
        device=DEVICE,
    )

    # Testing model on unseen data.
    eval_on_folder(dataset, final_model, TEST_DATA_DIR, EVAL_IMAGES_LIMIT, device=DEVICE)