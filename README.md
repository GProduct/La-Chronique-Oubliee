# Gallica Newspaper Bot

## Description

Ce bot sélectionne aléatoirement une Une de journal du même jour entre les années 1870 et 1955 à partir des archives de la BnF via l'API de Gallica. Il analyse la Une et publie un résumé d'un article via Twitter.

## Fonctionnalités

- Sélection aléatoire de journaux via Gallica (1870-1955).
- Analyse OCR de la Une pour extraire du texte.
- Résumé automatique d'un article.
- Publication sur Twitter.

## Installation

### 1. Cloner le dépôt :
```bash
git clone https://github.com/GProduct/La-Chronique-Oubliee
cd La-Chronique-Oubliee
```

### 2. Installer les dépendances Python :
Assurez-vous d'avoir Python 3.x installé, puis exécutez :
```bash
pip install -r requirements.txt
```

**Contenu de `requirements.txt` :**
```
pytesseract
Pillow
tweepy
requests
```

### 3. Installer Tesseract :
Téléchargez et installez **Tesseract**. Installez-le dans le répertoire suivant :

- Chemin : `/utils/tesseract/tesseract.exe`

Téléchargez Tesseract [ici](https://github.com/tesseract-ocr/tesseract).

Vérifiez que le chemin dans le script Python pointe vers la bonne adresse :
```python
pytesseract.pytesseract.tesseract_cmd = r'/utils/tesseract/tesseract.exe'
```

## Utilisation

1. Configurez vos clés API pour Twitter et Gallica votre environnement sous les noms de: 
```bash
X_ACCESS_TOKEN
X_ACCESS_TOKEN_SECRET
X_CONSUMER_KEY
X_CONSUMER_SECRET
COHERE_API_KEY
```
2. Lancez le bot :
```bash
python bot.py
```

## Contributions

Les contributions sont bienvenues. Ouvrez une issue pour discuter des changements ou des améliorations.

## Licence

Ce projet est sous licence MIT.
