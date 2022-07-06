#

import re
from get import getSchedule

GROUP = '46'

def findFuckingGroup():
    result = {}
    table_rows = getSchedule().findAll('tr')
    i = 0
    while i < len(table_rows):
        result = {}
        date = re.search(r"\d{1,2}\.\d{1,2}\.\d{2,4}", table_rows[i].prettify())
        if date is not None:
            #после строки с датой идёт строка с номерами групп
            #i указывает на строку с номерами групп
            i += 1 
            groups = re.findall(r"<strong>\s*(\d+)\s*</strong>", table_rows[i].prettify());
            if GROUP in groups:
                column = groups.index(GROUP)
                #после строки с номерами групп идес строка с бесполезным шлаком
                i += 2
                while (re.search(r'\d{1,2}\.\d{1,2}\.\d{2,4}', table_rows[i].prettify()) is None) and (i < len(table_rows)):
                    table_data = table_rows[i].findAll('td')
                    nomera_par = table_data[0::3]
                    pary = table_data[2::3]
                    nomera_kab = table_data[1::3]
                    #result: словарь; ключ - номер пары, значение - словарь(ключ - пара с преподом, значение - номер кабинета)
                    result[str(nomera_par[0])] =  { pary[0] : nomera_kab[0] }

                    print({ nomera_par[0] : { pary[0] : nomera_kab[0] } })

                    i += 1
                break
        i += 1
    print("result:\n\n", result)
    
if __name__ == '__main__':
    findFuckingGroup()

    pass