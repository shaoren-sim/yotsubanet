import torch
import torchvision.models as models
from torch.utils.data import DataLoader

from network.dataloader import train_test_split
from network.training_utils import train_model, validate_model, Checkpointing

def main_training_loop(
    labels,
    dataset, 
    epochs,
    validation_set_factor: float = 0.1,
    batch_size: int = 16,
    checkpoint_dir: str = "checkpointing",
    model=models.resnet18, 
    optimizer=torch.optim.AdamW, 
    criterion=torch.nn.CrossEntropyLoss(),
    device="cuda:0"
    ):

    previous_best_validation_loss = 0.0
    
    # Split dataset into training and validation sets
    train_set, valid_set = train_test_split(dataset, validation_set_factor)

    train_loader = DataLoader(train_set, batch_size, shuffle=True)
    valid_loader = DataLoader(valid_set, batch_size, shuffle=True)

    # Initialize model and optimizer.
    model = model(num_classes=len(labels)).to(device)
    optimizer = optimizer(model.parameters(), lr=0.001, eps=0.1)
    print("Model and optimizer initialized")

    if checkpoint_dir is not None:
        checkpointing = Checkpointing(
            mode='min', 
            checkpoint_dir='checkpointing', 
            checkpoint_path='checkpoint.pth.tar'
        )
    
    for epoch in range(epochs):
        training_loss, training_acc = train_model(model, train_loader, optimizer, device=device)
        validaiton_loss, validation_acc = validate_model(model, valid_loader, device=device)

        is_best = checkpointing.check(validaiton_loss, epoch, model, optimizer)

        if validaiton_loss < previous_best_validation_loss:
            previous_best_validation_loss = validaiton_loss
            torch.save(model.state_dict(), 'best_model.pth.tar')

        print(f'Epoch {epoch+1} - Training Loss: {training_loss:.4f}; Training Acc: {training_acc:.3f}%; Test Loss: {validaiton_loss:.4f}{"*" if is_best else ""}; Test Acc: {validation_acc:.3f}%')
    
    return model
    
