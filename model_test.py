# %%
import os
import torch
import torchvision
import matplotlib.pyplot as plt

from network.main_trainer import main_training_loop
from network.dataloader import LabelFolderDataset
from network.evaluation import eval_on_folder

model = torchvision.models.resnet18(num_classes=5)
print(torch.load("/home/shaoren/Desktop/yotsubanet/checkpointing/model_best.pth.tar")["state_dict"])
model.load_state_dict(torch.load("/home/shaoren/Desktop/yotsubanet/checkpointing/model_best.pth.tar"))

model.to("cuda:0")
