from utils import chooseRandomDate, getTinyURL
from gallica import getGallicaReferences, parseImage
from ocr import getOCR
from recap import getRecap
from twitter import postTweet
from cohere import cohereChat
import os
import datetime
import shutil

def main():
    #list all folders in result
    folders = os.listdir("result/")
    print(f"{len(folders)} dossier(s) trouvé(s)")

    #check if folder is not from the current day, if so, delete it
    for folder in folders:
        if folder != datetime.datetime.now().strftime("%Y-%m-%d"):
            shutil.rmtree(f"result/{folder}")
            print(f"Dossier supprimé: result/{folder}")
        else:
            pass

    # Get random date
    year, month, day = chooseRandomDate()
    print(f"Date choisie")

    # Get doc references
    title, link, highResCoverLink = getGallicaReferences(year, month, day)
    print(f"Références du document extraites --")

    # Get docId
    docId = link.removeprefix("https://gallica.bnf.fr/ark:/12148/")
    print(f"ID du document extrait ------------")

    # Check if document already downloaded
    if os.path.exists(f"""result/{datetime.datetime.now().strftime('%Y-%m-%d')}/{docId}"""):
        print("Document déjà téléchargé, nouvelle recherche...")
        return main()
    else:
        pass

    # Get tiny link
    tinyLink = getTinyURL(link)
    print(f"Lien vers le document raccourci ---")

    # Download and parse image of 2 resolutions
    nativeResCoverLink, nativeResCoverPath, highResCoverPath, medResCoverPath = parseImage(highResCoverLink, docId, datetime.datetime.now().strftime('%Y-%m-%d'))
    print("Images téléchargées ---------------")

    # Get OCR of native resolution image
    text = getOCR(docId)
    print(f"OCR exécuté -----------------------")

    # Get recap of all data about the document
    getRecap(title, link, nativeResCoverLink, text, tinyLink)

    #ask cohere 
    tweet_content = cohereChat(text, year)
    print(f"Texte du tweet généré -------------")


    # Post tweet
    if tweet_content is not None:
        postTweet(f"{year} - {tweet_content} {tinyLink}")
        print("Tweet posté -----------------------")
    else:
        print("No tweet content, retrying...")
        main()


if __name__ == "__main__":
    main()

"""
Écris un tweet en style 1890, intégrant des hashtags pertinents, sur ce texte ##""##. Le texte doit être concis et de la même longueur que les tweets que je t'ai fournis précédemment. Utilise un langage approprié à l'époque pour évoquer la situation décrite, en gardant une tonalité informative et respectueuse.
"""