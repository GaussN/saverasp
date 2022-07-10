import json
from time import sleep
from datetime import datetime, date
from get import getSchedule
from parser import findGroupSchedule

# SUCCESS_CHECK_UPDATE_TIME = 43200   # время сна после удачного обновления расписания
SUCCESS_CHECK_UPDATE_TIME = 60 * 5  # время сна после удачного обновления расписания
FAILURE_CHECK_UPDATE_TIME = 1800  # время сна после неудачного обновления расписания
FIND_GROUP = 46


def main():
    schedule_old = ''
    while True:
        now = datetime.now()
        delay_time = 0

        print(now, 'Сheck schedule update')

        schedule = getSchedule()

        if schedule_old != schedule.text:
            schedule_old = schedule.text
            schedule_dict = findGroupSchedule(schedule, str(FIND_GROUP))
            if schedule_dict is not None:
                print(now, 'new schedule')

                schedule_json = json.dumps(schedule_dict, ensure_ascii=False)

                # запись в файл
                with open(f'output/{date.today()}.json', 'w+', encoding='utf-8') as file:
                    file.write(schedule_json)
                    print(now, 'schedule successfully written to file')

            delay_time = SUCCESS_CHECK_UPDATE_TIME

        else:
            print(now, 'nothing new')
            delay_time = FAILURE_CHECK_UPDATE_TIME

        sleep(delay_time)


if __name__ == '__main__':
    main()
