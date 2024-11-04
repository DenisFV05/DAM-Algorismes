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
    [f"./data/testing/0abad4440c4415b9707f11151762526c.jpg", "racing"],
    [f"./data/testing/0ea9451a8de9cf7581835ccb20940174.jpg", "family"],
    [f"./data/testing/1a3f888928097b855e49c1926b94a5dc.jpg", "truck"],
    [f"./data/testing/1b97666eaae94e70cba5e238017cab7a.jpg", "truck"],
    [f"./data/testing/1ded9b835b61b963f13d6b4374ef2492.jpg", "jeep"],
    [f"./data/testing/2b6da117b6b37e8fa1d48cddec05b5b2.jpg", "racing"],
    [f"./data/testing/2b96ccd24db32c2c47581afde8d42722.jpg", "bus"],
    [f"./data/testing/2f313143d05ede99c2458ba697161c1c.jpg", "truck"],
    [f"./data/testing/3acbdbd78d3270f626fa9eac8c182bb3.jpg", "family"],
    [f"./data/testing/3db10fa5700a75911c64410f35d7b94d.jpg", "racing"],
    [f"./data/testing/3dbb4fcf817656a9a865f3ea33f07a6a.jpg", "racing"],
    [f"./data/testing/3f7a8b1ae0bc3d5d82e1240f810ce47d.jpg", "truck"],
    [f"./data/testing/4aa43e160ee667c2deb922cd371204bc.jpg", "jeep"],
    [f"./data/testing/4b71b5a2fa94a71b0581c6650a0f8d0a.jpg", "truck"],
    [f"./data/testing/4baa8146de477ebafae4b3f46d5614c2.jpg", "truck"],
    [f"./data/testing/05a006ebd8667a39988a253b10956bb7.jpg", "racing"],
    [f"./data/testing/5d7514af404266c3f92efcee8662f640.jpg", "bus"],
    [f"./data/testing/5edeade7ca9e85efa46e1be268be129c.jpg", "truck"],
    [f"./data/testing/6a4e8af47c5b5b1412ce9a28a247d50e.jpg", "family"],
    [f"./data/testing/6f13f51f98bd1e2332bfa6f1c1c5ff14.jpg", "jeep"],
    [f"./data/testing/7a9027a09a9149fd901f97630a052b29.jpg", "taxi"],
    [f"./data/testing/7fe25c5c90c4f447fe3fa10adf4232cd.jpg", "bus"],
    [f"./data/testing/09bbbd3f758e129a2692844e3b62d5a8.jpg", "family"],
    [f"./data/testing/9cecedb8bfe67dbbc76d7723c3b4de43.jpg", "truck"],
    [f"./data/testing/9e37ae8bf11600a30afcd592d73a4be1.jpg", "bus"],
    [f"./data/testing/34d68f0a8eda8aadc568c1fd14b222b9.jpg", "family"],
    [f"./data/testing/37d329f08d105885c3e5d658921356c6.jpg", "family"],
    [f"./data/testing/48dc3c3c0038b87e330d7692cae4b0ff.jpg", "family"],
    [f"./data/testing/51a610fa467c9b6d0a0c9ebc87ebd6cd.jpg", "truck"],
    [f"./data/testing/61b29def40ee024890ebc2af8851a120.jpg", "truck"],
    [f"./data/testing/63f9f7dc8298317284bf7dbf2074b3ba.jpg", "bus"],
    [f"./data/testing/75f2660d690d5bc035c1f9d9424e253a.jpg", "truck"],
    [f"./data/testing/81eba54e555030c678afe71bb81c3480.jpg", "jeep"],
    [f"./data/testing/84c8aadbabbeb753042593faffa4e376.jpg", "truck"],
    [f"./data/testing/95ac3b0debba83ee706b4edef03ee2c2.jpg", "truck"],
    [f"./data/testing/98b83106dcaeeb585913fb59c8525757.jpg", "family"],
    [f"./data/testing/210d3833b9c3b0613e6c03a33b01d13a.jpg", "truck"],
    [f"./data/testing/383f5f3edc4dd305ba0d1eb57ac55892.jpg", "family"],
    [f"./data/testing/395e11b1214a0308f6a6e7834cebc379.jpg", "taxi"],
    [f"./data/testing/0419f656d61b42a6b2d567ed9ab6673f.jpg", "truck"],
    [f"./data/testing/433a57b6d7767b974279ef8fcd49cc16.jpg", "truck"],
    [f"./data/testing/508bc40d51bc31a77507595e528155e9.jpg", "taxi"],
    [f"./data/testing/766f0049a40eea217328d2975312d3e0.jpg", "truck"],
    [f"./data/testing/897c7be0d09ce1e992ab8e68fc3194f6.jpg", "racing"],
    [f"./data/testing/1570cbe2a81dd646e94bf5e4e3b1f2b1.jpg", "tuck"],
    [f"./data/testing/3037a9c243c43addf623e9609a09515c.jpg", "family"],
    [f"./data/testing/5789a84b08a72667f6ed1dc0e1400778.jpg", "jeep"],
    [f"./data/testing/6739b35e5a470fdb37862fb2bc5251ef.jpg", "bus"],
    [f"./data/testing/7141dc0b260cb428c6c0bcb5e51426fc.jpg", "truck"],
    [f"./data/testing/7855d33398a070b855381b5c0022a12a.jpg", "truck"],
    [f"./data/testing/7911da38a55c13ad65ee761999873d82.jpg", "truck"],
    [f"./data/testing/8189cbaa92299ea536be3ad23ddf1d00.jpg", "truck"],    
    [f"./data/testing/9129e0d08ecc8343ba0d45b297cb19d2.jpg", "jeep"],
    [f"./data/testing/9803fa77a01d28b1be669c4f2dc1a9d2.jpg", "family"],
    [f"./data/testing/45242c276cd516adb93561503a2f6ed7.jpg", "bus"],
    [f"./data/testing/62795dabbbbe425b28275c4a0a601a63.jpg", "truck"],
    [f"./data/testing/91409b182fe012ec4a4ffde63bf4f3e1.jpg", "jeep"],
    [f"./data/testing/99043f3239c13157c6f90db35fb7d412.jpg", "racing"],
    [f"./data/testing/6250695ca39f3d4e37303996a08a75e0.jpg", "truck"],
    [f"./data/testing/7678977975a2ab3fc51efbafd0baca37.jpg", "jeep"],
    [f"./data/testing/a2fec0c55e7c73d27fac134b9074846e.jpg", "taxi"],
    [f"./data/testing/a3c4f639c87e59383cfec1062b0ebd1b.jpg", "family"],
    [f"./data/testing/a3c9175c79d68d3a8aaf8719e59519d0.jpg", "jeep"],
    [f"./data/testing/a67cad73fd03d2d5cef3a81bf78ed0a3.jpg", "bus"],    
    [f"./data/testing/a72e4b986609cd50953f4c070f9df9a0.jpg", "jeep"],
    [f"./data/testing/aba61896c1391587795060868f00f6e9.jpg", "racing"],
    [f"./data/testing/adaf348564dd71ae2c318378d5f60051.jpg", "racing"],
    [f"./data/testing/ae648d1b856a00e9150e84a0af1c1e71.jpg", "truck"],
    [f"./data/testing/b0d111a7c355e47d040ba1f2282c04cb.jpg", "family"],
    [f"./data/testing/b52fbc88bc83acea1b0d374ccb460178.jpg", "taxi"],
    [f"./data/testing/b62c7d59cd74dc1bc2eaa1b951cfd0a7.jpg", "bus"],
    [f"./data/testing/b64c45c9bdffb475ad76641a8f111c49.jpg", "jeep"],
    [f"./data/testing/b0322b716be09e89ac21c22874194836.jpg", "truck"],
    [f"./data/testing/b00473a9f517bbfc5923c95288b40ff2.jpg", "taxi"],
    [f"./data/testing/be8a535960c82e4332eed118196f7d56.jpg", "jeep"],
    [f"./data/testing/c1adb1337eba00e584e3704af99d291c.jpg", "bus"],
    [f"./data/testing/c9ef804987778a3e0590e5e501f38b56.jpg", "family"],
    [f"./data/testing/ca68371ad50fa0575b1fac8c5796fbfb.jpg", "jeep"],
    [f"./data/testing/cd0e83983e36613ec5b154d2d6ddb0d1.jpg", "taxi"],
    [f"./data/testing/d0bc0f8b0754ea0f5c8736c769aaebaa.jpg", "truck"],
    [f"./data/testing/d4bb40dee633de3a610857f75d8fb037.jpg", "jeep"],
    [f"./data/testing/d6c4bc7127a99edbd4bcc615b771604d.jpg", "family"],
    [f"./data/testing/db1ada5a60a1562ac68263444a2595be.jpg", "jeep"],
    [f"./data/testing/ddfe9b3fd10abc7e11d7479ea32ec569.jpg", "jeep"],
    [f"./data/testing/def5ed8eda194f16fe75b17278d7dffd.jpg", "truck"],
    [f"./data/testing/e4d643544391d8c00db061075616e1b9.jpg", "racing"],
    [f"./data/testing/e8d28df25bb2b713af60360bd29e1ab4.jpg", "racing"],
    [f"./data/testing/e7299b9187f09e190127873fb0725e1c.jpg", "taxi"],
    [f"./data/testing/eafaa5fd38df370046f8b185488e7fa5.jpg", "bus"],
    [f"./data/testing/eb3e8701367c730dbdd6dc9298ebea61.jpg", "family"],
    [f"./data/testing/ebd1939d557a824d89e1017780d5a69c.jpg", "truck"],
    [f"./data/testing/f0a70d450423aa8c88d87a0a0c9c1acf.jpg", "family"],
    [f"./data/testing/f2cd6c805f084ce28812a62a0a582e7a.jpg", "family"],
    [f"./data/testing/f9d5513079dfa5dd43c3c996aeebd88b.jpg", "truck"],
    [f"./data/testing/f55500934c8cc648bc9ae7b39cecf6bc.jpg", "truck"],
    [f"./data/testing/f400677842675240319e69bc2e5998eb.jpg", "truck"],
    [f"./data/testing/fa218c0050ba94160ec0873ec80c4807.jpg", "family"],
    [f"./data/testing/fb1e25b446c8174cc443c366a1d0e38b.jpg", "bus"],
    [f"./data/testing/fe6ba3df4ec47d2107d4aed4844d0ca9.jpg", "racing"],
    [f"./data/testing/ff9974e9177a989100fae4b8c505cad5.jpg", "bus"]
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
    output = model(image)  # Output is logits of shape [1, num_classes]
    _, predicted_idx = torch.max(output, 1)
    class_idx = predicted_idx.item()
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
    model = ModelClassifier(config, num_classes=len(class_names)).to(device)

    # Load the saved model
    checkpoint = torch.load(config.model_path, map_location=device, weights_only=True)
    model.load_state_dict(checkpoint['model_state_dict'])
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
