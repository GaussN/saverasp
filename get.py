import log
from requests import get
from bs4 import BeautifulSoup as parser
    
MGKE = 'http://mgke.minsk.edu.by/ru/main.aspx?guid=3831'


def getSchedule():
    try:
        response = get(MGKE)
        soup = parser(response.text, "html.parser")
        return soup.table
    except Exception as e:
        log.errorLog(f'Module get.py: {e}');
        raise