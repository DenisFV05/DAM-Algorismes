# Exercici 1

Cal entrenar una xarxa neuronal que permeti classificar textos d'opinió sobre una aerolinia en: 

- butterfly, cat, chicken, cow, dog, elephant, horse, sheep, spider, squirrel

Fes servir les ddades dels arxius './data/training.zip' i './data/testing.zip', que ja tenen les carpetes

Per la part de test acaba de completar la llista d'imatges disponibles:
```python
test_images = [
    # Llista d'imatges i etiquetes esperades
    [f"./data/testing/im832E2E543DD946A797309D12A95D8697.jpeg", "squirrel"],
    [f"./data/testing/im351744278DA544B6A1365A3EA33880E3.jpg", "sheep"]
    # Acabar la llista amb totes les imatges de test
]
```

## Tasques:

0) Fes els arxius **"model_config.json"** i **"ai_train.py"** per entrenar la xarxa anterior i generar els arxius **"model_metadata.json"** i **"model_network.pth"**

1) Fes un arxiu **"ai_classify.py"** que esculli 50 imatges a l'arzar de l'arxiu de test i mostri les estadistiques de classificar-los amb la xarxa de l'arpartat 0

2) Fes un arxiu **"ai_classify_single.py"** que demana per input: "Type an image path to classify?" i fa servir la xarxa anterior per dir: "This is a X" on X és el resultat de la classificació

3) Fes un document **"millores.pdf"** en el que expliquins quines configuracions es poden posar a la xarxa per millorar els resultats obtinguts.

<br/><br/>

**Nota**: La classificació de la tasca 1 ha de ser de l'estil:

```text
... resultats previs ...

Image: ./data/testing/im832E2E543DD946A797309D12A95D8697.jpeg, Prediction: squirrel, Label: squirrel
Image: ./data/testing/im351744278DA544B6A1365A3EA33880E3.jpg, Prediction: sheep, Label: sheep

Validation of 50 examples: success: X/Y, accuracy: 100.00%, Error rate: 0.00%
```