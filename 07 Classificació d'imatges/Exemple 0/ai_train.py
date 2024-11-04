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
    # Neteja la pantalla segons el sistema operatiu
    os.system('cls' if os.name == 'nt' else 'clear')

clearScreen()

def decompress_data_zip(config, type):
    # Elimina la carpeta de dades si existeix i descomprimeix el fitxer zip especificat
    if os.path.exists(config.data_path):
        shutil.rmtree(config.data_path)
    zip_filename = f"./data/{type}.zip"
    extract_to = './data/'
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        for member in zipf.namelist():
            # Filtra les carpetes ocultes i descomprimeix només la carpeta especificada
            if member.startswith(f"{type}/") and not member.startswith('__MACOSX/'):
                zipf.extract(member, extract_to)

def train_epoch(model, train_loader, criterion, optimizer, device, epoch, total_epochs):
    model.train()
    total_loss, correct, total = 0, 0, 0
    
    # Simplificat - només deixem leave=True i eliminem position
    pbar = tqdm(train_loader, 
                desc=f"Epoch {epoch}/{total_epochs} [Training]", 
                leave=True,
                bar_format="{desc}:   {percentage:3.2f}% |{bar:20}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]")
    
    for inputs, labels in pbar:
        inputs, labels = inputs.to(device), labels.float().to(device)
        optimizer.zero_grad()
        outputs = model(inputs).squeeze()
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        predicted = (outputs > 0.5).float()
        correct += (predicted == labels).sum().item()
        total += labels.size(0)
        pbar.set_postfix({'loss': f'{total_loss/len(train_loader):.4f}', 'acc': f'{100.*correct/total:.2f}%'})
    return total_loss / len(train_loader), 100. * correct / total

def evaluate_epoch(model, val_loader, criterion, device, epoch, total_epochs):
    model.eval()
    total_loss, correct, total = 0, 0, 0
    with torch.no_grad():
        pbar = tqdm(val_loader, 
                    desc=f"Epoch {epoch}/{total_epochs} [Validate]", 
                    leave=True,
                    bar_format="{desc}: {percentage:3.2f}% |{bar:20}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]")
        
        for inputs, labels in pbar:
            inputs, labels = inputs.to(device), labels.float().to(device)
            outputs = model(inputs).squeeze()
            loss = criterion(outputs, labels)
            total_loss += loss.item()
            predicted = (outputs > 0.5).float()
            correct += (predicted == labels).sum().item()
            total += labels.size(0)
            pbar.set_postfix({'loss': f'{total_loss/len(val_loader):.4f}', 'acc': f'{100.*correct/total:.2f}%'})
    return total_loss / len(val_loader), 100. * correct / total

def main():

    with open(CONFIG_FILE) as f:
        config_data = json.load(f)

    # Carrega la configuració des del fitxer JSON
    config = ModelConfig(config_data, config_data["training_path"])
    # Descomprimeix les dades d'entrenament
    decompress_data_zip(config, "training")
    # Configura el dispositiu (GPU si està disponible, sinó CPU)
    device = getDevice()

    # Crea el dataset i els DataLoaders per a entrenament i validació
    dataset = ModelDataset(config)
    train_loader, val_loader, classes = dataset.get_data_loaders(config.training['batch_size'])
    print(f"Classes: {classes}")

    # Guarda les classes en un fitxer per a futures referències
    with open(config.metadata, "w", encoding="utf-8") as f:
        json.dump(classes, f, ensure_ascii=False, indent=4)

    # Crea el model i el mou al dispositiu (CPU o GPU)
    model = ModelClassifier(config).to(device)
    print(f"Model created with {sum(p.numel() for p in model.parameters() if p.requires_grad)} weights and biases")

    # Defineix la funció de pèrdua per a classificació binària
    criterion = torch.nn.BCELoss()
    # Configura l'optimitzador AdamW
    optimizer = optim.AdamW(model.parameters(), lr=config.training['learning_rate'], weight_decay=0.01)
    # Configura el Scheduler per ajustar la taxa d'aprenentatge basant-se en la pèrdua de validació
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, 
        mode=config.reduce_lr_on_plateau['mode'], 
        factor=config.reduce_lr_on_plateau['factor'], 
        patience=config.reduce_lr_on_plateau['patience']
    )
    # Inicialitza l'early stopping amb els paràmetres de configuració
    early_stopping = EarlyStopping(config.early_stopping['patience'], config.early_stopping['min_delta'])
    best_val_acc = 0.0  # Variable per emmagatzemar la millor exactitud de validació aconseguida

    # Bucle principal d'entrenament/validació per a cada època
    for epoch in range(config.training['epochs']):
        print("")  # Afegim un salt de línia entre èpoques
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device, epoch, config.training['epochs'])
        val_loss, val_acc = evaluate_epoch(model, val_loader, criterion, device, epoch, config.training['epochs'])
        
        print(f"""Epoch {epoch}/{config.training['epochs']} - Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}% - Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}% - LR: {optimizer.param_groups[0]['lr']:.6f} """)

        # Actualitza el scheduler per ajustar la taxa d'aprenentatge segons la pèrdua de validació
        scheduler.step(val_loss)
        # Guarda el model si s'obté una millor exactitud de validació
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

        # Comprova si cal activar l'early stopping per acabar l'entrenament abans d'hora
        if early_stopping.check(val_loss):
            print("Early stopping activated")
            break

    # Esborra la carpeta de dades d'entrenament per netejar l'espai
    if os.path.exists(config.data_path):
        shutil.rmtree(config.data_path)

if __name__ == "__main__":
    main()
