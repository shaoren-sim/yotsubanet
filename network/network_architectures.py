from re import X
import torchvision.models as models
import torch

def resnet_18(num_classes):
    return models.resnet18(num_classes=num_classes)

def resnet_18_internal_normalizer(num_classes):
    return torch.nn.Sequential(NormalizeInput(), models.resnet18(num_classes=num_classes))

class NormalizeInput(torch.nn.Module):
    def __init__(self):
        super(NormalizeInput, self).__init__()

    def forward(self, x):
        _per_channel_pixels = x.reshape(-1, x.size(1), x.size(2)*x.size(3))

        # x = input / 255.0
        x = x - _per_channel_pixels.mean(2).reshape(x.size(0), x.size(1), 1, 1)
        x = x / _per_channel_pixels.std(2).reshape(x.size(0), x.size(1), 1, 1)
        return x