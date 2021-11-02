import os
import torch
import argparse
import pickle
import matplotlib.pyplot as plt

from network.main_trainer import main_training_loop
from network.dataloader import LabelFolderDataset
from network.evaluation import eval_on_image
from network.network_architectures import resnet_18

FILE_TO_EVAL = "examples/gotoubun_no_hanayome/ExVxLqtUUAErTkv.jpg"
OUTPUT_FILE = "examples/gotoubun_no_hanayome/results/single_image_eval.png"
SESSION_DIR = "goutoubun_no_hanayome"
DEVICE = "cuda:0"

USE_BEST = False

# Viola cascade parameters. Worth tuning for images to detect faces properly.
CASCADE_MIN_NEIGHBORS = 6
CASCADE_SCALE = 1.01

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="session_folder", required=False, help="Input/Webscraper output folder.", default=SESSION_DIR)
    parser.add_argument("-d", "--device", dest="device", required=False, help=f"Model training device, can be 'cpu' or 'cuda:gpu_index'. Default is {DEVICE}.", default=DEVICE)
    parser.add_argument("-f", "--file", dest="file", required=False, help=f"File to load for evaluation.", default=FILE_TO_EVAL)
    parser.add_argument("-b", "--best", dest="use_best", required=False, help=f"Whether to use final checkpoint (False) or best validation loss model (True). Default is {USE_BEST}.", default=USE_BEST)
    args = parser.parse_args()

    session_folder = args.session_folder
    device = args.device
    file = args.file
    use_best = bool(args.use_best)

    dataset_transforms = torch.load(os.path.join(session_folder, "checkpointing", "dataset_transforms.pth"))
    classes = sorted(os.listdir(os.path.join(session_folder, "data")))

    if "cuda" in device:
        if torch.cuda.is_available():
            print("CUDA-capable GPU is available, proceeding.")
        else:
            raise RuntimeError("No CUDA-capable GPU, terminating.")

    model = resnet_18(num_classes=len(classes))
    if use_best:
        _path_to_checkpoint = os.path.join(session_folder, "checkpointing", "model_best.pth.tar")
    else:
        _path_to_checkpoint = os.path.join(session_folder, "checkpointing", "checkpoint.pth.tar")
    model.load_state_dict(torch.load(_path_to_checkpoint, map_location=device)['state_dict'])
    model.to(device)

    # Testing model on unseen data.
    eval_on_image(file, model, dataset_transforms, classes, device=device, save_prediction_image_name=OUTPUT_FILE, cascade_min_neighbors=CASCADE_MIN_NEIGHBORS, cascade_scale_factor=CASCADE_SCALE)