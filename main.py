import sys
import json
import threading
from time import sleep
from get import getSchedule
from datetime import date
from parser import findGroupSchedule

from log import *

#43200
SUCCESS_CHECK_UPDATE_TIME = 60 * 5  # время сна после удачного обновления расписания
FAILURE_CHECK_UPDATE_TIME = 1800  # время сна после неудачного обновления расписания
FIND_GROUP = 44
        
def main():  
    schedule_old = ''
    while True:
        delay_time = 0

        log('Сheck schedule update')

        schedule = getSchedule()

        if schedule is None:
            errorLog('No schedule. Restart the program') 
            break
        

        if schedule_old != schedule.text:
            schedule_old = schedule.text
            schedule_dict = findGroupSchedule(schedule, str(FIND_GROUP))
            if schedule_dict is not None:
                successLog('New schedule')

                schedule_json = json.dumps(schedule_dict, ensure_ascii=False)
                delay_time = SUCCESS_CHECK_UPDATE_TIME

                # запись в файл
                with open(f'output/{date.today()}.json', 'w+', encoding='utf-8') as file:
                    file.write(schedule_json)
                    successLog('Schedule successfully written to file')
            else:
                warningLog('No schedule found for the selected group')
                delay_time = FAILURE_CHECK_UPDATE_TIME


        else:
            log('Nothing new')
            delay_time = FAILURE_CHECK_UPDATE_TIME

        sleep(delay_time)


if __name__ == '__main__':
    parse_thread = threading.Thread(target=main)
    parse_thread.daemon = True
    parse_thread.start()

    while True:
        cmd = input()
        if cmd.strip() in ['e', 'exit']:
            sys.exit(0)
        elif cmd.split(' ')[0] == 'set':
            argv = cmd.split(' ')
            try:
                #sunccess update time
                if argv[1] == 'SUT':
                    SUCCESS_CHECK_UPDATE_TIME = int(argv[2])
                #failure update time
                elif argv[1] == 'FUT':
                    FAILURE_CHECK_UPDATE_TIME = int(argv[2])
            except Exception as ex:
                print(ex)
        elif cmd == 'help':
            print('''
Type: "e" or "exit" to stop the process
Type "help" to get help
Type "set SUT(FUT) VAL" to set value SUCCESS_CHECK_UPDATE_TIME(FAILURE_CHECK_UPDATE_TIME)
''')