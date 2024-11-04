#!/usr/bin/env python3

import os
import json
import shutil
import zipfile
print("Loading AI libraries ...")
import torch
import torch.nn as nn
from torchvision import transforms
from ai_utils_image import ModelConfig, ModelClassifier, getDevice

CONFIG_FILE = "model_config.json"

test_images = [
    # Llista d'imatges i etiquetes esperades
    ["./data/testing/img14469279.jpg", "non_cat"],
    ["./data/testing/img15019810.jpg", "non_cat"],
    ["./data/testing/img16615685.jpg", "non_cat"],
    ["./data/testing/img16745259.jpg", "cat"],
    ["./data/testing/img17242442.jpg", "cat"],
    ["./data/testing/img21960791.jpg", "non_cat"],
    ["./data/testing/img22921893.jpg", "cat"],
    ["./data/testing/img23001964.jpg", "non_cat"],
    ["./data/testing/img27753996.jpg", "non_cat"],
    ["./data/testing/img30802655.jpg", "cat"],
    ["./data/testing/img32929134.jpg", "non_cat"],
    ["./data/testing/img34040492.jpg", "cat"],
    ["./data/testing/img37438645.jpg", "non_cat"],
    ["./data/testing/img38446080.jpg", "cat"],
    ["./data/testing/img43753560.jpg", "non_cat"],
    ["./data/testing/img44113566.jpg", "cat"],
    ["./data/testing/img46733274.jpg", "non_cat"],
    ["./data/testing/img47486374.jpg", "cat"],
    ["./data/testing/img48140375.jpg", "cat"],
    ["./data/testing/img49165968.jpg", "cat"],
    ["./data/testing/img50470376.jpg", "cat"],
    ["./data/testing/img53355576.jpg", "cat"],
    ["./data/testing/img55000620.jpg", "cat"],
    ["./data/testing/img57107487.jpg", "cat"],
    ["./data/testing/img58115239.jpg", "non_cat"],
    ["./data/testing/img62846124.jpg", "cat"],
    ["./data/testing/img63161136.jpg", "non_cat"],
    ["./data/testing/img69539582.jpg", "cat"],
    ["./data/testing/img69679487.jpg", "non_cat"],
    ["./data/testing/img69957115.jpg", "non_cat"],
    ["./data/testing/img69968821.jpg", "non_cat"],
    ["./data/testing/img70610683.jpg", "non_cat"],
    ["./data/testing/img72202194.jpg", "non_cat"],
    ["./data/testing/img75381857.jpg", "non_cat"],
    ["./data/testing/img75918332.jpg", "cat"],
    ["./data/testing/img76888003.jpg", "cat"],
    ["./data/testing/img77688616.jpg", "non_cat"],
    ["./data/testing/img79053052.jpg", "cat"],
    ["./data/testing/img83842359.jpg", "cat"],
    ["./data/testing/img83918667.jpg", "cat"],
    ["./data/testing/img84146180.jpg", "non_cat"],
    ["./data/testing/img90037107.jpg", "cat"],
    ["./data/testing/img93578086.jpg", "cat"],
    ["./data/testing/img95378073.jpg", "non_cat"],
    ["./data/testing/img95996327.jpg", "non_cat"],
    ["./data/testing/img96295260.jpg", "non_cat"],
    ["./data/testing/img96872108.jpg", "cat"],
    ["./data/testing/img99363609.jpg", "non_cat"]
]

def clearScreen():
    if os.name == 'nt':     
        os.system('cls')
    else:                   
        os.system('clear')

clearScreen()

def decompress_data_zip(config, type):
    # Remove the data directory if it exists and extract the specified zip file
    if os.path.exists(config.data_path):
        shutil.rmtree(config.data_path)
    zip_filename = f"./data/{type}.zip"
    extract_to = './data/'
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        for member in zipf.namelist():
            # Filter out hidden folders and extract only the specified folder
            if member.startswith(f"{type}/") and not member.startswith('__MACOSX/'):
                zipf.extract(member, extract_to)

def predict_image(model, image_path, transform, device, class_names):
    from PIL import Image
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)
    output = model(image).squeeze().item()
    class_idx = 1 if output > 0.5 else 0
    return class_names[class_idx]

def main():
    with open(CONFIG_FILE) as f:
        config_data = json.load(f)

    # Load configuration and model
    config = ModelConfig(config_data, config_data["testing_path"])

    with open(config.metadata, "r", encoding="utf-8") as f:
        class_names = json.load(f)

    # Extract the test data
    decompress_data_zip(config, "testing")

    device = getDevice()
    model = ModelClassifier(config).to(device)
    model.load_state_dict(torch.load(config.model_path, map_location=device, weights_only=True)["model_state_dict"])
    model.eval()  # Set the model to evaluation mode

    # Define transformations as per configuration
    transform = transforms.Compose([
        transforms.Resize(tuple(config.image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=config.normalize_mean, std=config.normalize_std)
    ])

    correct = 0  # Counter for correct predictions
    total = len(test_images)  # Total number of images to evaluate

    # Process each test image
    for image_path, label in test_images:
        prediction = predict_image(model, image_path, transform, device, class_names)  # Predict the class
        if prediction == label:  # Check if prediction is correct
            correct += 1
        print(f"Image: {image_path}, Prediction: {prediction}, Label: {label}")

    # Calculate accuracy and error rate
    accuracy = correct / total
    error_rate = (1 - accuracy) * 100
    print(f'\nValidation of {total} examples: success: {correct}/{total}, '
          f'accuracy: {accuracy*100:.2f}%, Error rate: {error_rate:.2f}%')

    # Delete the test data directory to clean up space
    if os.path.exists(config.data_path):
        shutil.rmtree(config.data_path)

if __name__ == "__main__":
    main()
