import datetime
import random

YEAR_MIN = 1870
YEAR_MAX = 1960

def containsForbiddenWord(string):
    with open('./res/forbidden_words.txt', 'r', encoding='utf-8') as file:
        forbidden_words = file.read()
        words = string.strip().split()
        for word in words:
            if word.lower() in forbidden_words:
                return True
        return False
    
def getCurrentDate():
    return datetime.datetime.now().strftime("%Y-%m-%d")    
    
def getRandomDate():
    today = getCurrentDate()
    today_day = datetime.datetime.strftime(today, "%d")
    today_month = datetime.datetime.strftime(today, "%m")
    
    if today_month == '02' and today_day == '29':
        year = random.randint(YEAR_MIN, YEAR_MAX)
        while not (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
            year = random.randint(YEAR_MIN, YEAR_MAX)
        return f"{year}-02-29"
    else:
        year = random.randint(YEAR_MIN, YEAR_MAX)
        return f"{year}-{today_month}-{today_day}"

def getFormattedRandomDate():
    today = datetime.datetime.strptime(getCurrentDate(), "%Y-%m-%d")
    today_day = today.strftime("%d")
    today_month = today.strftime("%m")
    
    if today_month == '02' and today_day == '29':
        year = random.randint(YEAR_MIN, YEAR_MAX)
        while not (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
            year = random.randint(YEAR_MIN, YEAR_MAX)
        return f"{year}-02-29"
    else:
        year = random.randint(YEAR_MIN, YEAR_MAX)
        return year, today_month, today_day

def getRandomNumber(a, b):
    return random.randint(a, b)

def formatTextToPost(text):
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')
    return text