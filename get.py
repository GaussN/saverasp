#function to get couple schedule

from requests import get  
from bs4 import BeautifulSoup as parser

mgke = 'http://mgke.minsk.edu.by/ru/main.aspx?guid=3831'

def getSchedule():
    try:
        response = get(mgke)
        soup = parser(response.text, "html.parser")
        return soup.table
    except Exception as e:
        print('exception: ', e)

if __name__ == '__main__': 
    print(getSchedule())
