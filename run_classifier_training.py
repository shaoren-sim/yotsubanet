import os

import torch
import argparse

from network.main_trainer import main_training_loop
from network.dataloader import LabelFolderDataset
from network.network_architectures import resnet_18

SESSION_DIR = "goutoubun_no_hanayome"
DATA_DIR = "data"
DATA_LIMIT = 250
BATCH_SIZE = 16
EPOCHS = 100
VALIDATION_FACTOR = 0.2
DEVICE = "cuda:0"
EARLY_STOPPING_PATIENCE = 30

EVAL_IMAGES_LIMIT = 300

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="session_folder", required=False, help="Input/Webscraper output folder.", default=SESSION_DIR)
    parser.add_argument("-b", "--batchsize", dest="batch_size", required=False, help=f"Number of images per training batch. Default is {BATCH_SIZE}.", default=BATCH_SIZE)
    parser.add_argument("-d", "--device", dest="device", required=False, help=f"Model training device, can be 'cpu' or 'cuda:gpu_index'. Default is {DEVICE}.", default=DEVICE)
    parser.add_argument("-e", "--epochs", dest="epochs", required=False, help=f"Number of epochs for training. Default is {EPOCHS}.", default=EPOCHS)
    parser.add_argument("-v", "--validationfactor", dest="validation_factor", required=False, help=f"Fraction of labelled dataset to use for validation. Default is {VALIDATION_FACTOR}.", default=VALIDATION_FACTOR)
    parser.add_argument("-l", "--datalimit", dest="data_limit", required=False, help=f"Maximum amount of images per class, to prevent class imbalance, can be None to use all. Default is {DATA_LIMIT}.", default=DATA_LIMIT)
    parser.add_argument("-p", "--patience", dest="patience", required=False, help=f"Maximum number of epochs before stopping training with no improvement. Default is {EARLY_STOPPING_PATIENCE}.", default=EARLY_STOPPING_PATIENCE)
    args = parser.parse_args()

    session_folder = args.session_folder
    batch_size = int(args.batch_size)
    device = args.device
    epochs = int(args.epochs)
    validation_factor = float(args.validation_factor)
    if args.data_limit is "None" or "0":
        data_limit = None  
    else:
        data_limit = int(args.data_limit)
    early_stopping_patience = int(args.patience)

    if "cuda" in device:
        if torch.cuda.is_available():
            print("CUDA-capable GPU is available, proceeding.")
        else:
            raise RuntimeError("No CUDA-capable GPU, terminating. To use CPU training, run 'python run_classifier_training.py -d cpu'")

    data_dir = os.path.join(session_folder, "data")
    
    classes = os.listdir(data_dir)
    classes.sort()
    print("Classes:", classes)

    print("Data count per label:")
    for class_name in classes:
        available_files = os.listdir(os.path.join(data_dir, class_name))
        print(class_name, ":", len(available_files))

    dataset = LabelFolderDataset(
        data_dir=data_dir,
        data_limit=data_limit,
    )

    model = main_training_loop(
        classes,
        dataset,
        epochs,
        model = resnet_18(len(classes)),
        validation_set_factor=validation_factor,
        batch_size=batch_size,
        device=device,
        checkpoint_dir=os.path.join(session_folder, "checkpointing"),
        early_stopping_patience=early_stopping_patience
    )

    # Saving dataset transforms and classes for evaluation purposes.
    dataset_transform_chain = dataset.transform
    torch.save(dataset_transform_chain, os.path.join(session_folder, "checkpointing", 'dataset_transforms.pth'))
