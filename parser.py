import re
import json
from unicodedata import numeric
from get import getSchedule


def findGroupSchedule(table, group: str) -> dict or None:
    result = {}

    table_rows = table.findAll('tr')
    i = 0

    while i < len(table_rows):
        date = re.search(r"\d{1,2}\.\d{1,2}\.\d{2,4}", table_rows[i].prettify())  # поиск даты

        if date is not None:
            result['date'] = date[0]

            # после строки с датой идёт строка с номерами групп
            # i указывает на строку с номерами групп
            i += 1
            groups = re.findall(r"<strong>\s*(\d+)", table_rows[i].prettify());

            if group in groups:
                # номер колнки с парами группы
                column = groups.index(group)
                # после строки с номерами групп идес строка с бесполезным шлаком
                i += 2

                while (i < len(table_rows)) and (re.search(r'\d{1,2}\.\d{1,2}\.\d{2,4}', table_rows[i].prettify()) is None):
                    table_data = table_rows[i].findAll('td')
                    
                    number = table_data[0::3][column].strong.text.strip()
                    couple = table_data[1::3][column].p.text.strip()
                    cabinet = table_data[2::3][column].p.text.strip()
                    # для очистки от двойных пробелов и новых строк 
                    number = number.replace('\n', '')
                    couple = ' '.join(couple.replace('\n', ' ').split())
                    cabinet = ' '.join(cabinet.replace('\n', ' ').split())
                    #b pfxtv z htuekzhrb bcgjkmpjdfk
                    # ⠟⠛⠉⠉⠉⠉⠉⠉⠙⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                    # ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
                    # ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠙⠻⣿⣿⣿⣿⣿⣿
                    # ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⢻⣿⣿⣿⣿
                    # ⠄⠄⠄⠄⠄⢀⣀⣀⣀⣀⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⢻⣿⣿⣿
                    # ⠄⠄⠄⠉⠉⠉⠄⣀⣀⣀⡈⠉⠛⠛⠛⠉⠉⠲⠄⠄⠄⣿⣿⣿
                    # ⠠⠤⠤⠔⠒⠋⠉⠄⠄⠄⠈⠉⠒⠒⠒⠒⠒⠂⠄⠄⠄⢻⣿⣿
                    # ⠄⠄⢀⠤⠐⠒⠒⠒⠒⠂⠄⠄⠄⠄⠄⠐⠒⠒⠒⢄⠄⠄⢿⣿
                    # ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⠆⠄⠄⠄⠄⢰⠄⠄⠄⠄⠄⠄⢸⣿
                    # ⠄⠄⠄⢠⡖⢲⣶⣶⣤⡀⠄⠄⠄⠄⠄⠈⢀⣤⣤⣤⡀⠄⢸⣿
                    # ⠄⠄⠄⠈⠙⠚⠛⠛⠓⠃⠄⠄⠄⠄⠄⠄⠧⠤⢿⣿⡇⠄⢸⣿
                    # ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢰⡆⠄⠄⠄⠄⠄⠄⠄⣿
                    # ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠳⡀⠄⠄⠄⠄⠄⠄⢸
                    # ⠄⠄⠄⠄⠄⠄⠄⠄⠄⡤⠤⠄⠄⠄⠄⠄⢘⡆⠄⠄⠄⠄⢠⣿
                    # ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠻⣤⠄⠴⠆⠠⣄⡞⠄⠄⠄⠄⢀⣾⣿
                    # ⣆⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢀⣾⣿⣿
                    # ⠈⠳⣄⠄⠄⠄⠄⠄⠖⠒⠶⠤⠤⠤⠤⠤⢤⠄⠄⢀⣿⣿⣿⣿
                    # ⠄⠄⠈⠑⢦⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣼⣿⣿⣿⣿
                    # ⠄⠄⠄⠄⠄⠙⢦⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⣠⣿⣿⣿⣿⣿⣿
                    # ⠄⠄⠄⠄⠄⠄⠄⠈⠓⠲⠤⠤⠤⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿
                    # ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠣⡀⠄⠄⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                    # ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠉⠉⠉⠉⠉⠉⠛⠛
                    # ⠄⠄⠈⠉⠑⢆⣀⡔⠈⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
                    
                    
                    # проверка будет, но не сейчас
                    print(f'{number}\n{couple}\n{cabinet}')
                    #result[number]={"couple":[1группа, 2группа], "teacher":[...]}
                
                    i += 1
                return result
        i += 1
    return None


from bs4 import BeautifulSoup as parser

if __name__ == '__main__':
    #на сайте расписания боольше нет
    #остается использовать сохраненное  
    print('.htm')
    with open('output\.htm', 'r', encoding='utf-8') as file:
        table = parser(file.read(), "html.parser").table
        couples = findGroupSchedule(table, '44')
        #print(couples)
    print('timetable.html')
    with open('output\\timetable.html', 'r', encoding='utf-8') as file:
        table = parser(file.read(), "html.parser").table
        couples = findGroupSchedule(table, '44')
        #print(couples)