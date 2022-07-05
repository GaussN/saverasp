#

import re
from get import getSchedule

def findFucking44Group():
    trs = getSchedule().findAll('tr')
    i = 0
    while i < len(trs):
        date = re.search(r"\d{1,2}\.\d{1,2}\.\d{2,4}", trs[i].prettify())
        if date is not None:
            #после строки с датой идёт строка с номерами групп
            i += 1 #указывает на строку с номерами групп
            groups = re.findall(r"<strong>(\d+)</strong>", trs[i].prettify());

            print(groups)
            pass
        i += 1
    
def createJSON():
    rasp = "{\n"
    
    return rasp + "}"


if __name__ == '__main__':
    #print(getSchedule().findAll('tr')[3])
    #print(findFucking44Group())
    findFucking44Group()

    pass