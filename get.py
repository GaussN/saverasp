# function to get couple schedule

from requests import get
from bs4 import BeautifulSoup as parser

MGKE = 'http://mgke.minsk.edu.by/ru/main.aspx?guid=3831'


def getSchedule():
    try:
        response = get(MGKE)
        soup = parser(response.text, "html.parser")
        return soup.table
    except Exception as e:
        print('exception: ', e)


if __name__ == '__main__':
    table = getSchedule()
    print(table)
    with open('output/timetable.html', 'w+', encoding='utf-8') as file:
        file.write(table.prettify())
