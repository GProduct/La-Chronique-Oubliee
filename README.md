# La Chronique Oubliée

> [!CAUTION]
> Il est possible que le bot dysfonctionne parfois. Les articles sont décryptés par une IA, qui peut avoir des difficultés à différencier les parodies (et/ou bandes dessinées) des véritables articles. Ainsi, certains résumés peuvent être totalement erronés ou sans rapport avec les articles d’origine

![Thumbnail](res/thumbnail.png)

## Description

La Chronique Oubliée est un bot qui sélectionne aléatoirement une Une de journal du même jour entre les années 1870 et 1955 à partir des archives de la [BnF](bnf.fr) via [l'API de Gallica](https://api.bnf.fr/fr/api-gallica-de-recherche). Il analyse la Une OCérisée par [Tesseract](https://github.com/tesseract-ocr/tesseract) publie un résumé d'un article via BlueSky.

## Retouvez-le sur BlueSky 🦋

👉 [LaChroniqueOubliee.bsky.social](https://lachroniqueoubliee.bsky.social)

## Fonctionnalités

- Sélection aléatoire de journaux via Gallica (1870-1955).
- Analyse OCR de la Une pour extraire du texte.
- Résumé automatique d'un article.
- Publication sur BlueSky.

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/GProduct/La-Chronique-Oubliee
cd La-Chronique-Oubliee
```

### 2. Installer les dépendances Python

Assurez-vous d'avoir Python 3.x installé, puis exécutez :

```bash
pip install -r requirements.txt
```

### 3. Installer Tesseract

#### Sous Linux

1. Installez Tesseract via le gestionnaire de paquets :

   ```bash
   sudo apt update
   sudo apt install tesseract-ocr
   ```

2. Pour le français, installez également :

   ```bash
   sudo apt install tesseract-ocr-fra
   ```

3. Vérifiez que `TESSERACT_OCR_PATH` dans `.env` pointe vers l'exécutable, par exemple:

   ```bash
   TESSERACT_OCR_PATH=/usr/bin/tesseract
   ```

#### Sous Windows

1. Téléchargez Tesseract [ici](https://github.com/tesseract-ocr/tesseract) et installez-le.
2. Vérifiez que `TESSERACT_OCR_PATH` dans `.env` pointe vers l'exécutable, par exemple:

   ```bash
   TESSERACT_OCR_PATH=C:/Program Files/Tesseract-OCR/tesseract.exe
   ```

## Utilisation

1. Configurez vos clés API pour BlueSky et Cohere ainsi que le chemin vers Tesseract dans un fichier `.env` sous les noms suivants :

   ```bash
   BSKY_USERNAME=example.bsky.social
   BSKY_PASSWORD=strongPassword
   TESSERACT_OCR_PATH=/path/to/tesseract
   COHERE_API_KEY=strongApiKey
   ```

2. Utilisez vos propres données pour entrainer le modèle de résumé de Cohere, puis enregistrez les échanges d'entrainement dans `./res/examples.json`. Les exemples doivent être sous la forme :

   ```json
   {
      "chat_history": [
         {
            "message": "réponse de Cohere",
            "role": "CHATBOT"
         },
         {
            "message": "OCR de l'article",
            "role": "USER"
         },
         ...
         ...
         ...
      ],
      "max_input_tokens": 100, //Nombre de tokens max de l'OCR
      "model": "model-1", // Nom du modèle
      "preamble": "Tu dois résumer un article" // Prompt de l'entrainement
   }
   ```

   > [!NOTE]
   > Les valeurs données sont des exemples. Vous devez les remplacer par vos propres données.

3. Lancez le bot :

   ```bash
   python main.py
   ```

## Contributions

[🐐](https://github.com/cherifad)

- Les contributions sont bienvenues. Ouvrez une issue pour discuter des changements ou des améliorations.

## Avertissement

Il est possible que le bot dysfonctionne parfois. Les articles sont décryptés par une IA, qui peut avoir des difficultés à différencier les parodies (et/ou bandes dessinées) des véritables articles. Ainsi, certains résumés peuvent être totalement erronés ou sans rapport avec les articles d’origine.