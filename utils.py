import datetime
import random
import requests

def bissex(year):
    if year % 4 == 0 and not year % 100 == 0:
        return True
    else:
        return False

def chooseRandomDate():
    day = datetime.datetime.now().day
    day = str(day).zfill(2)
    month = datetime.datetime.now().month
    month = str(month).zfill(2)
    year = random.randint(1880, 1955)
    if month == 2 and day > 28:
        while not bissex(year):
            year = random.randint(1870, 1955)
    else:
        pass
    return year, month, day

def getTinyURL(longUrl):
    tinyUrl = "http://tinyurl.com/api-create.php?url="
    tinyUrlResponse = requests.get(tinyUrl + longUrl)
    short_url = tinyUrlResponse.text
    return short_url