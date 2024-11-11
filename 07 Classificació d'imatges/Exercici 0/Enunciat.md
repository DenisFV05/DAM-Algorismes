# Exercici 0

Cal entrenar una xarxa neuronal que permeti classificar si una foto té una persona somrient o no, segons les categories: 

- non_smile, smile

Fes servir les ddades dels arxius './data/training.zip' i './data/testing.zip', que ja tenen les carpetes

Per la part de test acaba de completar la llista d'imatges disponibles:
```python
test_images = [
    # Llista d'imatges i etiquetes esperades
    ["./data/testing/img10042414.jpg", "smile"],
    ["./data/testing/img11599296.jpg", "non_smile"]
    # Acabar la llista amb totes les imatges de test
]
```

## Tasques:

0) Fes els arxius **"model_config.json"** i **"ai_train.py"** per entrenar la xarxa anterior i generar els arxius **"model_metadata.json"** i **"model_network.pth"**

1) Fes un arxiu **"ai_classify.py"** que esculli 50 textos a l'arzar de l'arxiu **"./data/sentiments.csv"** i mostri les estadistiques de classificar-los amb la xarxa de l'arpartat 0

2) Fes un arxiu **"ai_classify_single.py"** que demana per input: "Write something ..." i fa servir la xarxa anterior per dir si s'ha escrit en anglès o en un altre idioma. Segons el resultat:

    - Si és **smile** mostra. "Smiling"
    - Si és **non_smile** mostra. "Not smiling"

3) Fes un document **"millores.pdf"** en el que expliquins quines configuracions es poden posar a la xarxa per millorar els resultats obtinguts.

<br/><br/>

**Nota**: La classificació de la tasca 1 ha de ser de l'estil:

```text
... resultats previs ...

Image: ./data/testing/img10042414.jpg, Prediction: smile, Label: smile
Image: ./data/testing/img11599296.jpg, Prediction: smile, Label: non_smile

Validation of X examples: success: Y/Z, accuracy: 50.00%, Error rate: 50.00%
```