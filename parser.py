#

import re
from get import getSchedule

GROUP = '46'

def findFuckingGroup():
    table_rows = getSchedule().findAll('tr')
    i = 0
    while i < len(table_rows):
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
                while (re.search(r'\d{1,2}\.\d{1,2}\.\d{2,4}', table_rows[i].prettify()) is not None) and (i < len(table_rows)):
                    print('para\n', table_rows[i].findAll('td')[1].prettify())
                    i += 1
                break
        i += 1
    
def createJSON():
    rasp = "{\n"
    
    return rasp + "}"


if __name__ == '__main__':
    findFuckingGroup()

    pass