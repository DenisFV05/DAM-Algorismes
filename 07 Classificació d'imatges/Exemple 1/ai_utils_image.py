import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import datasets, transforms
from torchvision.models import resnet18, ResNet18_Weights

class ModelConfig:
    def __init__(self, config_data, data_path):
        self.config = config_data
        self.data_path = data_path
        self.image_size = tuple(self.config['image_size'])
        self.normalize_mean = self.config['normalize_mean']
        self.normalize_std = self.config['normalize_std']
        self.model_params = self.config['model_params']
        self.training = self.config['training']
        self.early_stopping = self.config['early_stopping']
        self.reduce_lr_on_plateau = self.config['reduce_lr_on_plateau']
        self.metadata = self.config['metadata']
        self.model_path = self.config['model_path']

class ModelDataset(Dataset):
    def __init__(self, config):
        transform = transforms.Compose([
            transforms.Resize(config.image_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=config.normalize_mean, std=config.normalize_std)
        ])
        self.dataset = datasets.ImageFolder(config.data_path, transform=transform)
        
        val_size = int(config.training['validation_split'] * len(self.dataset))
        train_size = len(self.dataset) - val_size
        self.train_dataset, self.val_dataset = random_split(self.dataset, [train_size, val_size], generator=torch.Generator().manual_seed(42))
    
    def get_data_loaders(self, batch_size):
        train_loader = DataLoader(self.train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
        val_loader = DataLoader(self.val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
        return train_loader, val_loader, self.dataset.classes

class ModelClassifier(nn.Module):
    def __init__(self, config, num_classes):
        super(ModelClassifier, self).__init__()
        self.model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
        # Freeze earlier layers if desired
        for param in list(self.model.parameters())[:-4]:
            param.requires_grad = False
        num_ftrs = self.model.fc.in_features
        # Replace the final fully connected layer
        self.model.fc = nn.Sequential(
            nn.Dropout(config.model_params['dropout_rate']),
            nn.Linear(num_ftrs, num_classes)
            # No activation here; CrossEntropyLoss expects raw logits
        )
    
    def forward(self, x):
        return self.model(x)

class EarlyStopping:
    def __init__(self, patience, min_delta):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.early_stop = False

    def check(self, val_loss):
        if self.best_loss is None or val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        return self.early_stop

def getDevice():
    device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
    if device.type == "cuda" or device.type == "mps":
        print(f"Using device: {device} (GPU accelerated)")
    else:
        print(f"Using device: {device} (CPU based)")
    
    return device
