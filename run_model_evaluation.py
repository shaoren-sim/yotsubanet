import os
import torch
import argparse
import pickle
import matplotlib.pyplot as plt

from network.main_trainer import main_training_loop
from network.dataloader import LabelFolderDataset
from network.evaluation import eval_on_folder
from network.network_architectures import resnet_18

SESSION_DIR = "goutoubun_no_hanayome"
DATA_DIR = "data"
DATA_LIMIT = 250
BATCH_SIZE = 16
EPOCHS = 100
VALIDATION_FACTOR = 0.2
DEVICE = "cuda:0"
EARLY_STOPPING_PATIENCE = 20

USE_BEST = False

EVAL_IMAGES_LIMIT = 200

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="session_folder", required=False, help="Input/Webscraper output folder.", default=SESSION_DIR)
    parser.add_argument("-d", "--device", dest="device", required=False, help=f"Model training device, can be 'cpu' or 'cuda:gpu_index'. Default is {DEVICE}.", default=DEVICE)
    parser.add_argument("-l", "--datalimit", dest="eval_limit", required=False, help=f"Maximum amount of images in unlabelled folder to evaluate, can be None to use all. Default is {EVAL_IMAGES_LIMIT}.", default=DATA_LIMIT)
    parser.add_argument("-b", "--best", dest="use_best", required=False, help=f"Whether to use final checkpoint (False) or best validation loss model (True). Default is {USE_BEST}.", default=USE_BEST)
    args = parser.parse_args()

    session_folder = args.session_folder
    device = args.device
    eval_limit = int(args.eval_limit)
    use_best = bool(args.use_best)

    dataset_transforms = torch.load(os.path.join(session_folder, "checkpointing", "dataset_transforms.pth"))
    classes = sorted(os.listdir(os.path.join(session_folder, "data")))

    if "cuda" in device:
        if torch.cuda.is_available():
            print("CUDA-capable GPU is available, proceeding.")
        else:
            raise RuntimeError("No CUDA-capable GPU, terminating.")

    test_data_dir = os.path.join(session_folder, "unlabelled_data", "multiple_faces")

    model = resnet_18(num_classes=len(classes))
    if use_best:
        _path_to_checkpoint = os.path.join(session_folder, "checkpointing", "model_best.pth.tar")
    else:
        _path_to_checkpoint = os.path.join(session_folder, "checkpointing", "checkpoint.pth.tar")
    model.load_state_dict(torch.load(_path_to_checkpoint, map_location=device)['state_dict'])
    model.to(device)

    # Testing model on unseen data.
    eval_on_folder(model, dataset_transforms, classes, test_data_dir, eval_limit, device=device, save_prediction_image_name="yotsubanet_predictions.png")