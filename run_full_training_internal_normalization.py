import os
import torch
import matplotlib.pyplot as plt

from network.main_trainer import main_training_loop
from network.dataloader import LabelFolderDataset
from network.evaluation import eval_on_folder

from torchvision import transforms

from network.network_architectures import resnet_18_internal_normalizer

DATA_DIR = "data"
DATA_LIMIT = 100
EPOCHS = 100
VALIDATION_FACTOR = 0.2
DEVICE = "cuda:0"

TEST_DATA_DIR = "extra_unlabelled_data/multiple_faces"
EVAL_IMAGES_LIMIT = 200

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

    dataset = LabelFolderDataset(
        data_dir=DATA_DIR,
        data_limit=DATA_LIMIT,
        transform=[
            transforms.ToTensor(),
            transforms.RandomHorizontalFlip(p=0.5)
        ]
    )

    final_model = main_training_loop(
        classes,
        dataset,
        EPOCHS,
        model=resnet_18_internal_normalizer(num_classes=len(classes)),
        validation_set_factor=VALIDATION_FACTOR,
        batch_size=16,
        device=DEVICE,
    )

    # Testing model on unseen data.
    eval_on_folder(dataset, final_model, TEST_DATA_DIR, EVAL_IMAGES_LIMIT, device=DEVICE, save_prediction_image_name="yotsubanet_predictions_internal_normalization_manga_removed.png")
    torch.save(final_model.state_dict(), os.path.join("final_model.pth"))