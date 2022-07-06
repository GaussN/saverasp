#

import re
from get import getSchedule

GROUP = '46'
#по этой ***** рефакторинг плачет :(
def findFuckingGroup(table):
    result = {}
    table_rows = table.findAll('tr')
    i = 0
    while i < len(table_rows):
        result = {}
        date = re.search(r"\d{1,2}\.\d{1,2}\.\d{2,4}", table_rows[i].prettify())
        if date is not None:
            #после строки с датой идёт строка с номерами групп
            #i указывает на строку с номерами групп
            result['date'] = date.group(0)
            i += 1 
            groups = re.findall(r"<strong>\s*(\d+)", table_rows[i].prettify());
            if GROUP in groups:
                #номер колнки с парами группы
                column = groups.index(GROUP)
                #после строки с номерами групп идес строка с бесполезным шлаком
                i += 2
                while (re.search(r'\d{1,2}\.\d{1,2}\.\d{2,4}', table_rows[i].prettify()) is None) and (i < len(table_rows)):
                    table_data = table_rows[i].findAll('td')
                    #
                    nomera_par = table_data[0::3]
                    pary = table_data[1::3]
                    nomera_kab = table_data[2::3]
                    #result: словарь; ключ - номер пары, значение - словарь(ключ - пара с преподом, значение - номер кабинета)
                    #result[nomera_par[column]] =  { pary[column] : nomera_kab[column] }
                    
                    num = re.search(r'<strong>(\d+)', str(nomera_par[column]))[1]
                    para = re.search(r'<p>(.+)</p>', str(pary[column]))[1].replace('<br/>', ',')
                    kabinet = re.search(r'<p>(.+)</p>', str(nomera_kab[column]))[1].replace('<br/>', ',')

                    #num = str(num.group(1))
                    #para = str(para.group(1)).replace('<br/>', ',')
                    #kabinet = str(kabinet.group(1)).replace('<br/>', ',')

                    result[num] = { 'para' : para, 'kabinet' : kabinet }

                    i += 1
                break
        i += 1
    print("result:\n\n", result)
    
if __name__ == '__main__':
    findFuckingGroup(getSchedule())

