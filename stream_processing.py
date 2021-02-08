import re

from datetime import datetime

def remote_controller_one(
            stream: str,
            set_time_amount: int = 4,
            set_time: int = 5,
            set_reverse_time: bool = False,
            set_sum_time: bool = False
        ):
    """
    Кастомная обработка потока
        с пульта Nr. BB329;
    Входные данные:
        часть потока типа str;
    """
    print(stream)
    # Берем время / счёт / количество взятых таймаутов
    tmp = datetime.today()
    time_info = re.findall(
            r'[\d\s]{2}:\d\d[\d\s]{2}\d[\d\s]{2}\d[\s\d]{2}[\d\s]{2}',
            stream,
            flags=re.ASCII
        )

    print(time_info)
    time_info = time_info[-1]

    time_part = re.findall(
            r'8a\d\d',
            stream,
            flags=re.ASCII
        )[-1][3] # Тайм

    # Обработаем полученные данные
    cur_time = time_info[:5] # Текущее время
    teams_scores = time_info[5:8].strip(), time_info[8:11].strip() # Счет команд
    taken_timeouts = time_info[-2:-1], time_info[-1:] # Количество взятых таймаутов

    m, s = cur_time.split(":")
    if len(m.strip()) == 0:
        cur_time = cur_time.replace(' ', '0')
    else:
        if set_sum_time is True:
            m = int(m) + (int(time_part)-1)*set_time
            cur_time = '{}:{}'.format(m,s)
            if set_reverse_time is True:
                minutes = int(set_time) * set_time_amount
                static_date = datetime(tmp.year, tmp.month, tmp.day, minutes//60, minutes%60, 0) # ВАЖНО! ТАЙМ НЕ ДОЛЖЕН БЫТЬ БОЛЬШЕ 59 МИНУТ!
                current_date = datetime(tmp.year, tmp.month, tmp.day, 0//60, int(m)%60, int(s))
                delta = static_date - current_date
                cur_time = '{}:{}'.format(delta.seconds//60, delta.seconds%60)
        else:
            if set_reverse_time is True:
                static_date = datetime(tmp.year, tmp.month, tmp.day, 0, int(set_time), 0) # ВАЖНО! ТАЙМ НЕ ДОЛЖЕН БЫТЬ БОЛЬШЕ 59 МИНУТ!
                current_date = datetime(tmp.year, tmp.month, tmp.day, 0, int(m), int(s))
                delta = static_date - current_date
                cur_time = '{}:{}'.format(delta.seconds//60, delta.seconds%60)

    plus = re.findall('x02O'+'.'*44, stream)
    if len(plus) != 0:
        plus = (plus[-1][0], plus[-1][1])
    else:
        plus = ['', '']

    remote_players = [[], []] # the area for collecting
    remote_players_info = re.findall('x02O'+'.'*42, stream)
    if len(remote_players_info) != 0:
        remote_players_info = remote_players_info[-1][4:]
        memory_cell = 0
        for i in range(0, 42, 7):
            memory_cell += 1
            info_about_remote_player = remote_players_info[i: i+7].strip()
            if info_about_remote_player != '':
                if memory_cell <= 3:
                    remote_players[0].append(info_about_remote_player)
                else:
                    remote_players[1].append(info_about_remote_player)

    return cur_time, teams_scores, taken_timeouts, time_part, remote_players, ['0', '0'], plus, ''

def remote_controller_two(
            stream: str,
            set_time_amount: int = 4,
            set_time: int = 5,
            set_reverse_time: bool = False,
            set_sum_time: bool = False
        ):
    """
    Кастомная обработка потока
        с пульта Nr. BB337;
    Входные данные:
        часть потока типа str;
    """
    # Берем время / счёт / количество взятых таймаутов
    tmp = datetime.today()
    time_info = re.findall(
            r'[\d\s]{2}:\d\d[\d\s]{2}\d[\d\s]{2}\d[\d\sE]{12}',
            stream,
            flags=re.ASCII
        )[-1]
    print(stream)
    # Обработаем полученные данные
    cur_time = time_info[:5] # Текущее время
    teams_scores = time_info[5:8].strip(), time_info[8:11].strip() # Счет команд
    taken_timeouts = time_info[13], time_info[14] # Количество взятых таймаутов
    foals = time_info[11], time_info[12] # Фолы
    timeout_time = time_info[19:21], time_info[21:23]
    print('Текущее:', cur_time, '\nСчет:', teams_scores, '\nТаймауты:', taken_timeouts, '\nФолы:', foals, '\nОставшееся время', timeout_time)

    time_part = re.findall(
            r'x880\d1',
            stream,
            flags=re.ASCII
        )[-1][4] # Тайм
    print('Taйм:', time_part)


    m, s = cur_time.split(":")
    if len(m.strip()) == 0:
        cur_time = cur_time.replace(' ', '0')
    else:
        if set_sum_time is True:
            m = int(m) + (int(time_part)-1)*set_time
            cur_time = '{}:{}'.format(m,s)
            if set_reverse_time is True:
                minutes = int(set_time) * set_time_amount
                static_date = datetime(tmp.year, tmp.month, tmp.day, minutes//60, minutes%60, 0) # ВАЖНО! ТАЙМ НЕ ДОЛЖЕН БЫТЬ БОЛЬШЕ 59 МИНУТ!
                current_date = datetime(tmp.year, tmp.month, tmp.day, 0//60, int(m)%60, int(s))
                delta = static_date - current_date
                cur_time = '{}:{}'.format(delta.seconds//60, delta.seconds%60)
        else:
            if set_reverse_time is True:
                static_date = datetime(tmp.year, tmp.month, tmp.day, 0, int(set_time), 0) # ВАЖНО! ТАЙМ НЕ ДОЛЖЕН БЫТЬ БОЛЬШЕ 59 МИНУТ!
                current_date = datetime(tmp.year, tmp.month, tmp.day, 0, int(m), int(s))
                delta = static_date - current_date
                cur_time = '{}:{}'.format(delta.seconds//60, delta.seconds%60)

    return cur_time, teams_scores, taken_timeouts, time_part, [[], []], foals

if __name__ == '__main__':
    example = r"\x02D 1:29 23 2000002010    \x03e\x02O                                          00\x03N\x02T27/08/2014:28.20\x8a322X   \x03\x82\x02D 1:29 23 2000002010    \x03e\x02F4                                \x03s\x02D 1:29 23 2000002010    \x03e\x02O                                          00\x03N\x02T27/08/2014:28.21\x8a322X   \x03\x83\x02D 1:29 23 2000002010    \x03e\x02F1`1 `5 `8 q0 q1 q3 q6 q7 q8 r1 r7 s4 t4 w7 x7 y1 \x03g\x02D 1:29 23 2000002010    \x03e\x02O 1:59                                     00\x03N\x02T27/08/2014:28.21\x8a322X   \x03\x83\x02D 1:29 23 2000002010    \x03e\x02F2`2 `3 q3 q6 q8 r1 r4 v3 w2 w3 w6 w7 w9 y7 y8 s7 \x03}\x02D 1:29 23 2000002010    \x03e\x02O                                          00\x03N\x02T27/08/2014:28.21\x8a322X   \x03\x83\x02D 1:30 23 2000002010    \x03m\x02F3                                \x03t\x02D 1:30 23 2000002010    \x03m\x02O                                          00\x03N\x02T27/08/2014:28.21\x8a322X   \x03\x83\x02D 1:30 23 2000002010    \x03m\x02F4                                \x03s"
    example_two = ' `4 `5 `6 `7 `8 `9 q0 q11q23            \x03d\x02D 9:44 15 1244321000  17\x03g\x02C4              4        00\x03B\x02T01/01/2015:47.06\x88011*   \x03\xf0\x02D 9:44 15 1244321000  17\x03g\x02F3                                \x03t\x02D 9:44 15 1244321000  17\x03g\x02C4              4        00\x03B\x02T01/01/2015:47.06\x88011*   \x03\xf0\x02D 9:44 15 1244321000  17\x03g\x02F4                                \x03s\x02D 9:44 15 1244321000  17\x03g\x02C4'

    print(remote_controller_one(example))
