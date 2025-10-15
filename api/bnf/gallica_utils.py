import xml.etree.ElementTree as ET
from utils.utils import getRandomNumber, getCurrentDate
import requests
import os
import logging

logger = logging.getLogger(__name__)


def downloadImage(url, filename):
    logger.info("Downloading image from %s -> %s", url, filename)
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except Exception as e:
        logger.exception("Failed to download image from %s", url)
        raise

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        file.write(response.content)
    logger.info("Saved image to %s (size=%s bytes)", filename, os.path.getsize(filename))


def isDocumentAlreadyProcessed(uri):
    log_path = './temp/processed_documents.csv'
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if uri in line:
                    logger.debug("URI %s already processed", uri)
                    return True
    logger.debug("URI %s not found in processed log", uri)
    return False


def writeUriToLog(uri):
    log_path = './temp/processed_documents.csv'
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, 'a', encoding='utf-8') as file:
        file.write(f"{uri}, {getCurrentDate()}\n")
    logger.info("Appended URI %s to %s", uri, log_path)


def blankLog():
    log_path = './temp/processed_documents.csv'
    if os.path.exists(log_path):
        with open(log_path, 'r+', encoding='utf-8') as file:
            lines = file.readlines()
            if lines and lines[-1].strip().endswith(getCurrentDate()):
                logger.debug("Processed log already up to date")
                return
            file.seek(0)
            file.truncate()
            file.write("uri, date\n")
            logger.info("Reset processed_documents.csv header")
    else:
        # create the file
        os.makedirs('./temp', exist_ok=True)
        with open(log_path, 'w', encoding='utf-8') as file:
            file.write("uri, date\n")
        logger.info("Created processed_documents.csv")