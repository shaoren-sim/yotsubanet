import torchvision.models as models

def resnet_18(num_classes):
    return models.resnet18(num_classes=num_classes)