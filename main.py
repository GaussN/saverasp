import sys
import log
import json
import threading
from time import sleep
from hashlib import md5
from datetime import date
from get import getSchedule
from parser import findGroupSchedule

SUCCESS_CHECK_UPDATE_TIME = 60 * 5  # время сна после удачного обновления расписания
FAILURE_CHECK_UPDATE_TIME = 1800  # время сна после неудачного обновления расписания

find_gorup : int = 44

def main():
    schedule_old = ''
    while True:
        delay_time = 0

        log.log('Сheck schedule update')
        schedule = getSchedule()
        if schedule is None:
            log.errorLog('No schedule. Restart the program')
            break

        #старое расписание хранится в виде хэша
        if schedule_old != md5(schedule.text.encode().hexdigest()):
            schedule_old = md5(schedule.text.encode()).hexdigest()
            schedule_dict = findGroupSchedule(schedule, str(find_gorup))
            if schedule_dict is not None:
                log.successLog('New schedule')

                schedule_json = json.dumps(schedule_dict, ensure_ascii=False)
                delay_time = SUCCESS_CHECK_UPDATE_TIME

                # запись в файл
                with open(f'output/{date.today()}.json', 'w+', encoding='utf-8') as file:
                    file.write(schedule_json)
                    log.successLog('Schedule successfully written to file')
            else:
                log.warningLog('No schedule found for the selected group')
                delay_time = FAILURE_CHECK_UPDATE_TIME


        else:
            log.log('Nothing new')
            delay_time = FAILURE_CHECK_UPDATE_TIME

        sleep(delay_time)


if __name__ == '__main__':    
    while True:
        try:
            find_gorup = int(input('enter group number: '))
            break
        except:
            pass

    parse_thread = threading.Thread(target=main)
    parse_thread.daemon = True
    parse_thread.start()


    while True:
        cmd = input()
        if cmd.strip() in ['e', 'exit', 'q', 'quit']:
            sys.exit(0)
        elif cmd.split(' ')[0] == 'set':
            argv = cmd.split(' ')
            try:
                if argv[1] == 'SUT':
                    SUCCESS_CHECK_UPDATE_TIME = int(argv[2])
                    print(f'SUCCESS_CHECK_UPDATE_TIME = {argv[2]}')
                elif argv[1] == 'FUT':
                    FAILURE_CHECK_UPDATE_TIME = int(argv[2])
                    print(f'FAILURE_CHECK_UPDATE_TIME = {argv[2]}')
                elif argv[1] == 'group':
                    find_gorup = int(argv[2])
                    print(f'group = {argv[2]}')
                else:
                    print('unknown value')
            except IndexError:
                print('not enough parameters')
            except Exception as ex:
                print(ex)
        elif cmd == 'help':
            print('''
Type: "e" or "exit" to stop the process
Type "help" to get help
Type "set SUT(FUT, group) VAL" to set value SUCCESS_CHECK_UPDATE_TIME(FAILURE_CHECK_UPDATE_TIME, group)
''')
        else:
            print('unknown command')
