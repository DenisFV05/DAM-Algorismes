#!/usr/bin/env python3

import os
import json
import torch
import torch.nn as nn
from transformers import BertTokenizer
from ai_utils_text import ModelConfig, ModelClassifier, getDevice
from sklearn.preprocessing import LabelEncoder

CONFIG_FILE = "ClasificacioText\\Exercici 1\\model_config.json"

def clearScreen():
    if os.name == 'nt':     
        os.system('cls')
    else:                   
        os.system('clear')

clearScreen()

def predict_single_text(text: str, model: nn.Module, tokenizer, device: torch.device, config: ModelConfig, label_encoder):
    # Prepara el texto de entrada para el modelo
    encoding = tokenizer(
        text,
        add_special_tokens=True,
        max_length=config.max_len,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )

    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    # Realiza la predicción sin cálculo de gradientes
    model.eval()
    with torch.no_grad():
        outputs = model(input_ids, attention_mask)
        probabilities = nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

    predicted_label = label_encoder.inverse_transform([predicted.item()])[0]
    confidence = confidence.item()
    return predicted_label, confidence

def main():
    # Cargar la configuración del modelo
    with open(CONFIG_FILE) as f:
        config_file = json.load(f)

    # Cargar las metadatos del modelo (categorías)
    with open(config_file['paths']['metadata'], 'r') as f:
        metadata = json.load(f)
    labels = metadata["categories"]

    # Inicializar el configurador del modelo
    config = ModelConfig(config_file, labels)

    # Inicializar el tokenizador y cargar el modelo entrenado
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    device = getDevice()

    model = ModelClassifier(config).to(device)
    model.load_state_dict(torch.load(config_file['paths']['trained_network'], map_location=device))

    # Cargar el label encoder
    le = LabelEncoder()
    le.fit(metadata['label_encoder'])

    # Solicitar la opinión al usuario
    text = input("What's your opinion about the airline? ")

    # Realizar la predicción
    predicted_label, confidence = predict_single_text(text, model, tokenizer, device, config, le)

    # Mostrar el resultado de la predicción
    print(f"Your opinion about the airline is {predicted_label} with a confidence of {confidence:.2%}")

if __name__ == "__main__":
    main()
