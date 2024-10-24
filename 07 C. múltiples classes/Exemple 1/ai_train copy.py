#!/usr/bin/env python3

import os
import json
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

# Configuration
config = {
    "config_path": "news_config.json",
    "model_path": "news_model.pth",
    "vocab_path": "news_vocab.json",
    "csv_path": "./data/news.csv",
    "training": {
        "batch_size": 32,
        "epochs": 25,
        "learning_rate": 0.001,
        "validation_split": 0.2
    },
    "model_params": {
        "hidden_size": 256,
        "dropout_rate": 0.5
    },
    "early_stopping": {
        "patience": 5,
        "min_delta": 0
    },
    "reduce_lr_on_plateau": {
        "mode": "min",
        "factor": 0.1,
        "patience": 3
    },
    "classes": []
}

# Custom Dataset for news articles
class NewsDataset(Dataset):
    def __init__(self, texts, labels, vectorizer, label_encoder):
        self.texts = texts
        self.labels = labels
        self.vectorizer = vectorizer
        self.label_encoder = label_encoder
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        # Transform text to vector
        vector = torch.FloatTensor(
            self.vectorizer.transform([text]).toarray()
        ).squeeze()
        # Convert label to one-hot encoding
        label = torch.tensor(self.label_encoder[self.labels[idx]], dtype=torch.long)
        return vector, label

# Neural Network for multi-class text classification
class NewsClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes, dropout_rate):
        super(NewsClassifier, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_size // 2, num_classes)
        )
    
    def forward(self, x):
        return self.model(x)

def create_data_loaders(csv_path):
    print("Loading dataset...")
    
    # Read CSV file
    df = pd.read_csv(csv_path)
    
    # Identify unique categories and create label encoder
    unique_categories = sorted(df['category'].unique())
    label_encoder = {cat: idx for idx, cat in enumerate(unique_categories)}
    config['classes'] = unique_categories
    
    # Convert labels using the encoder
    labels = df['category'].map(label_encoder)
    texts = df['body'].values
    
    # Create and fit the vectorizer
    vectorizer = CountVectorizer(max_features=5000)
    vectorizer.fit(texts)
    
    # Aconseguir les categories originals en lloc dels números
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, df['category'].values,  # Passar valors de text en lloc de map(label_encoder)
        test_size=config['training']['validation_split'],
        random_state=42
    )

    # Crear datasets amb les categories de text originals
    train_dataset = NewsDataset(train_texts, train_labels, vectorizer, label_encoder)
    val_dataset = NewsDataset(val_texts, val_labels, vectorizer, label_encoder)
        
    # Create datasets
    train_dataset = NewsDataset(train_texts, train_labels, vectorizer, label_encoder)
    val_dataset = NewsDataset(val_texts, val_labels, vectorizer, label_encoder)
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=config['training']['batch_size'],
        shuffle=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=config['training']['batch_size'],
        shuffle=False
    )
    
    print(f"Dataset loaded: {len(train_texts)} training articles, {len(val_texts)} validation articles")
    print(f"Categories: {', '.join(unique_categories)}")
    
    return train_loader, val_loader, vectorizer, label_encoder

def initialize_early_stopping():
    return {
        "patience": config['early_stopping']['patience'],
        "min_delta": config['early_stopping']['min_delta'],
        "counter": 0,
        "best_loss": None,
        "early_stop": False
    }

def check_early_stopping(state, val_loss):
    if state["best_loss"] is None or val_loss < state["best_loss"] - state["min_delta"]:
        state["best_loss"] = val_loss
        state["counter"] = 0
    else:
        state["counter"] += 1
        if state["counter"] >= state["patience"]:
            state["early_stop"] = True
    return state["early_stop"]

def train_one_epoch(model, train_loader, criterion, optimizer, device, epoch):
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    pbar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{config['training']['epochs']} [Training]")
    for inputs, labels in pbar:
        inputs = inputs.to(device)
        labels = labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        correct += (predicted == labels).sum().item()
        total += labels.size(0)
        
        pbar.set_postfix({
            'loss': f'{total_loss/len(train_loader):.4f}',
            'acc': f'{100.*correct/total:.2f}%'
        })
    
    return total_loss/len(train_loader), 100.*correct/total

def validate(model, val_loader, criterion, device, epoch):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():
        pbar = tqdm(val_loader, desc=f"Epoch {epoch+1}/{config['training']['epochs']} [Validate]")
        for inputs, labels in pbar:
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)
            
            pbar.set_postfix({
                'loss': f'{total_loss/len(val_loader):.4f}',
                'acc': f'{100.*correct/total:.2f}%'
            })
    
    return total_loss/len(val_loader), 100.*correct/total

def main():
    # Configurar el dispositiu (GPU si està disponible, sinó CPU)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
    if device.type == "cuda" or device.type == "mps":
        print(f"Using device: {device} (GPU accelerated)")
    else:
        print(f"Using device: {device} (CPU based)")
    
    # Create data loaders
    train_loader, val_loader, vectorizer, label_encoder = create_data_loaders(config['csv_path'])
    
    # Save config (with classes)
    with open(config['config_path'], 'w') as f:
        json.dump(config, f, indent=4)

    # Create model
    model = NewsClassifier(
        input_size=len(vectorizer.vocabulary_),
        hidden_size=config['model_params']['hidden_size'],
        num_classes=len(config['classes']),
        dropout_rate=config['model_params']['dropout_rate']
    )
    model = model.to(device)
    
    print(f"Model created with {sum(p.numel() for p in model.parameters() if p.requires_grad)} trainable parameters")
    
    # Save vectorizer vocabulary
    with open(config['vocab_path'], 'w') as f:
        json.dump({
            'vocabulary': {k: int(v) for k, v in vectorizer.vocabulary_.items()},
            'label_encoder': label_encoder
        }, f)
    
    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config['training']['learning_rate'])
    
    # Learning rate scheduler
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode=config['reduce_lr_on_plateau']['mode'],
        factor=config['reduce_lr_on_plateau']['factor'],
        patience=config['reduce_lr_on_plateau']['patience']
    )
    
    # Initialize early stopping
    early_stopping_state = initialize_early_stopping()
    best_val_acc = 0.0
    
    # Training loop
    for epoch in range(config['training']['epochs']):
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device, epoch)
        val_loss, val_acc = validate(model, val_loader, criterion, device, epoch)
        
        print(f"Epoch {epoch+1}/{config['training']['epochs']} - "
              f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}% - "
              f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}% - "
              f"LR: {optimizer.param_groups[0]['lr']:.6f}")
        
        scheduler.step(val_loss)
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            print(f"Saving better model with accuracy {val_acc:.2f}%")
            torch.save({
                'model_state_dict': model.state_dict(),
                'label_encoder': label_encoder
            }, config['model_path'])
        
        if check_early_stopping(early_stopping_state, val_loss):
            print("Early stopping activated")
            break

if __name__ == "__main__":
    main()