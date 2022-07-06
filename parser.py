from get import getSchedule
import json
import re

def findFuckingGroup(table, group : str) -> dict or None:
    result = {}
    
    findGroup = False

    table_rows = table.findAll('tr')
    i = 0
    
    while i < len(table_rows):
        date = re.search(r"\d{1,2}\.\d{1,2}\.\d{2,4}", table_rows[i].prettify())#нахождение даты 
        
        if date is not None:
            result['date'] = date[0]
            
            #после строки с датой идёт строка с номерами групп
            #i указывает на строку с номерами групп
            i += 1 
            groups = re.findall(r"<strong>\s*(\d+)", table_rows[i].prettify());
            
            if group in groups:
                findGroup = True

                #номер колнки с парами группы
                column = groups.index(group)    
                #после строки с номерами групп идес строка с бесполезным шлаком
                i += 2
                
                while (re.search(r'\d{1,2}\.\d{1,2}\.\d{2,4}', table_rows[i].prettify()) is None) and (i < len(table_rows)):
                    table_data = table_rows[i].findAll('td')
                    #
                    number_raw = table_data[0::3]
                    couple_raw = table_data[1::3]
                    cabinet_raw = table_data[2::3]

                    #result: словарь; ключ - номер пары, значение - словарь(ключ - пара с преподом, значение - номер кабинета)
                    number = re.search(r'<strong>(\d+)', str(number_raw[column]))[1]
                    couple = re.search(r'<p>(.+)</p>', str(couple_raw[column]))[1].replace('<br/>', ',')
                    cabinet = re.search(r'<p>(.+)</p>', str(cabinet_raw[column]))[1].replace('<br/>', ',')

                    #в couple хранится название пары(или пар) и ФИО препода в виде строки 
                    # couple_m - match содержащий название пары(или пар) и ФИО препода  
                    couple_m = re.search(r'(.+\))(.+)', couple);
                    couple_name = couple_m[1]#название пары
                    couple_teacher = couple_m[2]#ФИО препода

                    result[number] = { 'para' : couple_name, 'teacher': couple_teacher, 'kabinet' : cabinet }

                    i += 1
                break
        i += 1
    return (result if findGroup else None)
    
if __name__ == '__main__':
    couples = findFuckingGroup(getSchedule(), '44')
    couplesJson = json.dumps(couples, ensure_ascii=False)
    print(couples)
    print(couplesJson)