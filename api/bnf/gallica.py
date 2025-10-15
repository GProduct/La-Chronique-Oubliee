import requests
import xml.etree.ElementTree as ET
import logging
from utils.utils import getRandomNumber, getFormattedRandomDate, containsForbiddenWord
from api.bnf.gallica_utils import downloadImage, isDocumentAlreadyProcessed, writeUriToLog, blankLog
from api.tesseract.tesseract import executeOCR
from time import sleep

logger = logging.getLogger(__name__)

def mainGallica():
    # We first check if the document has already been processed
    logger.info("Initializing Gallica fetch and resetting processed log")
    blankLog()
    
    # We first fetch the records
    fetchGallicaRecords()
    result = extractResults()
    
    # If the number of results is greater than the maximum number of records we can fetch at once, we will retry the request
    # If the title contains a forbidden word, we will retry the request
    while result['retry'] is not None or result['forbidden'] == True:
        if result['forbidden'] == True:
            logger.info("Document does not meet the requirements (forbidden word), retrying")
            fetchGallicaRecords() # year is not needed here, we want a random year
            result = extractResults()
        else:
            logger.info("Document out of range, retrying with startRecord=%s", result['retry'])
            sleep(10)
            fetchGallicaRecords(random_year=result['year'], startRecord=result['retry']) # we retry the request with the new startRecord value
            result = extractResults(fromIndex=1)
    
    # The document is now OK to be processed
    # We download the native resolution image to execute the OCR
    logger.info("Selected document: %s (%s)", result['data'].get('title'), result['data'].get('uri'))
    download_path = f"./temp/{result['data']['uri']}-native.jpg"
    logger.info("Downloading native resolution image to %s", download_path)
    downloadImage(result['data']['nativeres'], download_path)
    
    # We can now process the OCR
    # executeOCR already writes the result in a txt file
    ocr_txt = f"./temp/{result['data']['uri']}-ocr.txt"
    logger.info("Running OCR -> %s", ocr_txt)
    executeOCR(ocr_txt, download_path)

    # We must save the document uri in a file to keep track of the documents we have already processed
    # we write the uri to the log
    logger.info("Recording processed URI: %s", result['data']['uri'])
    writeUriToLog(result['data']['uri'])
    
    logger.info("Gallica processing complete for URI: %s", result['data']['uri'])
    return result
    
def fetchGallicaRecords(random_year=None, month=None, day=None, startRecord=1, maximumRecords=20):
    if random_year == None:
        random_year, month, day = getFormattedRandomDate()
    else:
        unused_year, month, day = getFormattedRandomDate()
    
    url = "https://gallica.bnf.fr/SRU"
    params = {
        'version': '1.2',
        'operation': 'searchRetrieve',
        'query': f"""dc.type any fascicule and dc.date all {random_year}{month}{day} and dc.language any fre or dc.language any frm or dc.language any fro""",
        'recordSchema': 'dc',
        'startRecord': startRecord,
        'maximumRecords': maximumRecords
    }
    
    response = requests.get(url, params=params)
    
    try:
        response.raise_for_status()
    except Exception as e:
        logger.exception("Failed to fetch Gallica SRU records: %s", e)
        # still write the response (if any) for debugging
    with open('./temp/temp.xml', 'w', encoding='utf-8') as file:
        file.write(response.text)
        file.close()
    logger.debug("Wrote Gallica SRU response to ./temp/temp.xml (startRecord=%s, maximumRecords=%s)", startRecord, maximumRecords)

# Search and retrieve the records from the Gallica API
# Select a document randomly and return its metadata
def extractResults(fromIndex=None):
    # Define namespaces
    namespaces = {
        'srw': 'http://www.loc.gov/zing/srw/',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
    }
    
    tree = ET.parse('./temp/temp.xml')
    root = tree.getroot() 
    
    # we parse the query to get the date
    query = root.find('.//srw:query', namespaces).text
    date = query.split() # query has always the same word count, so we can split it
    year = date[6][:4]
    month = date[6][4:6] # unused
    day = date[6][6:] # unused
    
    # We are looking for total number of results
    number_of_results = root.find('.//srw:numberOfRecords', namespaces).text
    
    # We now have to choose a random number between 1 and the number of results
    if fromIndex is not None:
        n = 1
        logger.debug("Selecting specific record (fromIndex provided)")
    else:
        n = getRandomNumber(1, int(number_of_results))
        logger.debug("Random number chosen: %s on %s total results", n, number_of_results)
    
    next_record_position = int(root.find('.//srw:nextRecordPosition', namespaces).text) # unused
    
    records = root.findall('.//srw:record', namespaces)

    if not records or n > len(records):
        return {
            'forbidden': False,
            'retry': n,
            'year': year
        }
    else:
        # With the 'findall' method, we can find all the 'record' tags, which contain the metadata of each documents
        record = root.findall('.//srw:record', namespaces)[n-1]

        # useful for displaying the results
        record_metadata = record.find('.//oai_dc:dc', namespaces)
        title = record_metadata.find('.//dc:title', namespaces).text
        date = record_metadata.find('.//dc:date', namespaces).text
        description = record_metadata.findall('.//dc:description', namespaces)
        identifier = record_metadata.findall('.//dc:identifier', namespaces)
        language = record_metadata.find('.//dc:language', namespaces).text
        publisher = record_metadata.find('.//dc:publisher', namespaces).text
        relation = record_metadata.findall('.//dc:relation', namespaces)
        source = record_metadata.find('.//dc:source', namespaces).text

        # useful for the download of the document
        extra_record_metadata = record.find('.//srw:extraRecordData', namespaces)
        highres = extra_record_metadata.find('.//highres', namespaces).text
        # not used
        # link = extra_record_metadata.find('.//link', namespaces).text.removesuffix('/date')
        lowres = extra_record_metadata.find('.//lowres', namespaces).text
        medres = extra_record_metadata.find('.//medres', namespaces).text
        nqamoyen = extra_record_metadata.find('.//nqamoyen', namespaces).text
        provenance = extra_record_metadata.find('.//provenance', namespaces).text
        thumbnail = extra_record_metadata.find('.//thumbnail', namespaces).text
        typedoc = extra_record_metadata.find('.//typedoc', namespaces).text
        uri = extra_record_metadata.find('.//uri', namespaces).text
        link = f"https://gallica.bnf.fr/ark:/12148/{uri}"

        logger.debug("Record metadata title=%s, date=%s, uri=%s", title, date, uri)
        logger.debug("Image links (highres/medres/lowres): %s / %s / %s", highres, medres, lowres)

        # native resolution is not directly in the metadata, so we have to build the url
        # Caution: the native resolution is very heavy, pay attention to the download
        nativeres = f"https://gallica.bnf.fr/iiif/ark:/12148/{uri}/f1/full/full/0/native.jpg"
        
        if containsForbiddenWord(title):
            return {
                'forbidden': True,
                'retry': None,
                'year': None,
            }
            
        return {
            'forbidden': False,
            'retry': None,
            'year': None,
            'data': {
                'search_year': year,
                'title': title,
                'date': date,
                'description': description,
                'identifier': identifier,
                'language': language,
                'publisher': publisher,
                'relation': relation,
                'source': source,
                'link': link,
                'nativeres': nativeres,
                'highres': highres,
                'lowres': lowres,
                'medres': medres,
                'nqamoyen': nqamoyen,
                'provenance': provenance,
                'thumbnail': thumbnail,
                'typedoc': typedoc,
                'uri': uri
            }    
        }