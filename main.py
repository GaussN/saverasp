import sys
import json
import threading
from time import sleep
from get import getSchedule
from datetime import datetime, date
from pkg_resources import parse_requirements
from parser import findGroupSchedule

# SUCCESS_CHECK_UPDATE_TIME = 43200   # время сна после удачного обновления расписания
SUCCESS_CHECK_UPDATE_TIME = 60 * 5  # время сна после удачного обновления расписания
FAILURE_CHECK_UPDATE_TIME = 1800  # время сна после неудачного обновления расписания
FIND_GROUP = 44
        
def main():  
    schedule_old = ''
    while True:
        now = datetime.now()
        delay_time = 0

        print(f' {now} Сheck schedule update')

        schedule = getSchedule()

        if schedule is None:
            print(f'\033[101;93m {now} No schedule. Restart the program\033[0m') 
            break
        

        if schedule_old != schedule.text:
            schedule_old = schedule.text
            schedule_dict = findGroupSchedule(schedule, str(FIND_GROUP))
            if schedule_dict is not None:
                print(f'\033[102;97m {now} New schedule\033[0m')

                schedule_json = json.dumps(schedule_dict, ensure_ascii=False)
                delay_time = SUCCESS_CHECK_UPDATE_TIME

                # запись в файл
                with open(f'output/{date.today()}.json', 'w+', encoding='utf-8') as file:
                    file.write(schedule_json)
                    print(f'\033[1092;97m Schedule successfully written to file\033[0m')
            else:
                print('\033[103;97m No schedule found for the selected group\033[0m')
                delay_time = FAILURE_CHECK_UPDATE_TIME


        else:
            print(now, '\033[3mnothing new\033[0m')
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