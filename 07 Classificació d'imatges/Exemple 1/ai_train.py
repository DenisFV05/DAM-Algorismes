#!/usr/bin/env python3

import os
import json
import shutil
import zipfile
print("Loading AI libraries ..."); 
import torch
import torch.optim as optim
from tqdm import tqdm
from ai_utils_image import ModelConfig, ModelDataset, ModelClassifier, EarlyStopping, getDevice

CONFIG_FILE = "model_config.json"

def clearScreen():
    # Clear the screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

clearScreen()

def decompress_data_zip(config, type):
    # Remove the data folder if it exists and unzip the specified zip file
    if os.path.exists(config.data_path):
        shutil.rmtree(config.data_path)
    zip_filename = f"./data/{type}.zip"
    extract_to = './data/'
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        for member in zipf.namelist():
            # Filter out hidden folders and extract only the specified folder
            if member.startswith(f"{type}/") and not member.startswith('__MACOSX/'):
                zipf.extract(member, extract_to)

def train_epoch(model, train_loader, criterion, optimizer, device, epoch, total_epochs):
    model.train()
    total_loss, correct, total = 0, 0, 0
    
    pbar = tqdm(train_loader, 
                desc=f"Epoch {epoch+1}/{total_epochs} [Training]", 
                leave=True,
                bar_format="{desc}:   {percentage:3.2f}% |{bar:20}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]")
    
    for inputs, labels in pbar:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        correct += (predicted == labels).sum().item()
        total += labels.size(0)
        pbar.set_postfix({'loss': f'{total_loss/len(train_loader):.4f}', 'acc': f'{100.*correct/total:.2f}%'})
    return total_loss / len(train_loader), 100. * correct / total

def evaluate_epoch(model, val_loader, criterion, device, epoch, total_epochs):
    model.eval()
    total_loss, correct, total = 0, 0, 0
    with torch.no_grad():
        pbar = tqdm(val_loader, 
                    desc=f"Epoch {epoch+1}/{total_epochs} [Validate]", 
                    leave=True,
                    bar_format="{desc}: {percentage:3.2f}% |{bar:20}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]")
        
        for inputs, labels in pbar:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)
            pbar.set_postfix({'loss': f'{total_loss/len(val_loader):.4f}', 'acc': f'{100.*correct/total:.2f}%'})
    return total_loss / len(val_loader), 100. * correct / total

def main():

    with open(CONFIG_FILE) as f:
        config_data = json.load(f)

    # Load configuration from JSON file
    config = ModelConfig(config_data, config_data["training_path"])
    # Decompress training data
    decompress_data_zip(config, "training")
    # Set up device (GPU if available, else CPU)
    device = getDevice()

    # Create dataset and DataLoaders for training and validation
    dataset = ModelDataset(config)
    train_loader, val_loader, classes = dataset.get_data_loaders(config.training['batch_size'])
    print(f"Classes: {classes}")

    # Save classes to a file for future reference
    with open(config.metadata, "w", encoding="utf-8") as f:
        json.dump(classes, f, ensure_ascii=False, indent=4)

    # Create the model and move it to the device (CPU or GPU)
    model = ModelClassifier(config, num_classes=len(classes)).to(device)
    print(f"Model created with {sum(p.numel() for p in model.parameters() if p.requires_grad)} trainable parameters")

    # Define the loss function for multi-class classification
    criterion = torch.nn.CrossEntropyLoss()
    # Set up the AdamW optimizer
    optimizer = optim.AdamW(model.parameters(), lr=config.training['learning_rate'], weight_decay=0.01)
    # Set up the Scheduler to adjust the learning rate based on validation loss
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, 
        mode=config.reduce_lr_on_plateau['mode'], 
        factor=config.reduce_lr_on_plateau['factor'], 
        patience=config.reduce_lr_on_plateau['patience']
    )
    # Initialize early stopping with configuration parameters
    early_stopping = EarlyStopping(config.early_stopping['patience'], config.early_stopping['min_delta'])
    best_val_acc = 0.0  # Variable to store the best validation accuracy achieved

    # Main training/validation loop for each epoch
    for epoch in range(config.training['epochs']):
        print("")  # Add a newline between epochs
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device, epoch, config.training['epochs'])
        val_loss, val_acc = evaluate_epoch(model, val_loader, criterion, device, epoch, config.training['epochs'])
        
        print(f"""Epoch {epoch+1}/{config.training['epochs']} - Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}% - Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}% - LR: {optimizer.param_groups[0]['lr']:.6f} """)

        # Update the scheduler to adjust the learning rate based on validation loss
        scheduler.step(val_loss)
        # Save the model if a better validation accuracy is achieved
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            print(f"Saving a better model with accuracy {val_acc:.2f}%")
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
                'val_loss': val_loss,
            }, config.model_path)

        # Check if early stopping should be activated to end training early
        if early_stopping.check(val_loss):
            print("Early stopping activated")
            break

    # Remove the training data folder to clean up space
    if os.path.exists(config.data_path):
        shutil.rmtree(config.data_path)

if __name__ == "__main__":
    main()
