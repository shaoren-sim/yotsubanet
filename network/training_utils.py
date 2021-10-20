import shutil
import numpy as np
import os
import torch

def train_model(model, dataloader, optimizer, loss_criterion=torch.nn.CrossEntropyLoss(), device="cuda:0"):
    training_loss = 0.0
    train_correct = 0
    train_total = 0
    for i, data in enumerate(dataloader, 0):
        model.train()
        # get the inputs; data is a list of [inputs, labels]
        images, labels = data
        images = images.to(device)
        labels = labels.to(device)

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = model(images)

        _, predicted = torch.max(outputs.data, 1)
        train_total += labels.size(0)
        train_correct += (predicted.cpu().detach() == labels.cpu().detach()).sum().item()

        loss = loss_criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        training_loss += loss.item()
    train_acc = 100*(train_correct/train_total)
    return training_loss, train_acc

def validate_model(model, dataloader, loss_criterion=torch.nn.CrossEntropyLoss(), device="cuda:0"):
    # Evaluating on Test data
    model.eval()
    test_loss = 0.0
    test_correct = 0
    test_total = 0
    with torch.no_grad():
        for i, data in enumerate(dataloader, 0):
            images, labels = data
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            
            _, predicted = torch.max(outputs.data, 1)
            test_total += labels.size(0)
            test_correct += (predicted.cpu().detach() == labels.cpu().detach()).sum().item()

            loss = loss_criterion(outputs, labels)
            test_loss += loss.item()
    test_acc = 100*(test_correct/test_total)
    return test_loss, test_acc

class Checkpointing():
    def __init__(self, mode='min', checkpoint_dir='checkpoints', checkpoint_path='checkpoint.pth.tar'):
        if mode not in ['min', 'max']:
            raise ValueError("Mode must be 'min' or 'max'.")
        
        self.checkpoint_dir = checkpoint_dir
        if os.path.exists(self.checkpoint_dir):
            pass
        else:
            os.mkdir(self.checkpoint_dir)
        
        self.checkpoint_path = os.path.join(self.checkpoint_dir, checkpoint_path)
        self.mode = mode
        self.best = np.Inf if mode == "min" else -np.Inf
    
    def check(self, metric, epoch, model, opt):
        is_best = False     # boolean indicating whether new best is achieved.
        if self.mode == 'min':
            if metric < self.best:
                self.best = metric
                is_best = True
        elif self.mode == 'max':
            if metric > self.best:
                self.best = metric
                is_best = True
        
        self.__save_checkpoint({
            'epoch': epoch + 1,
            'state_dict': model.state_dict(),
            'best_val_loss': self.best,
            'optimizer' : opt.state_dict(),
        }, is_best)

        return is_best
        
    # Checkpoint state_dict utility
    def __save_checkpoint(self, state, is_best):
        torch.save(state, self.checkpoint_path)
        if is_best:
            shutil.copyfile(self.checkpoint_path, os.path.join(self.checkpoint_dir, 'model_best.pth.tar'))
            # print('New best, saving model_best.pth.tar')