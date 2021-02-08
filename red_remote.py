import re

def remote_controller_three(
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
    time_info = re.findall(
            r'[\d\s]{2}[:.]\d[\d\s][\d\s]{2}\d[\d\s]{2}\d[\s\d]{2}[\d\s]{10}',
            stream,
            flags=re.ASCII
        )

    if len(time_info) != 0:
        time_info = time_info[-1]
        print(len(time_info))
        cur_time = time_info[:5] # Текущее время
        teams_scores = time_info[5:8].strip(), time_info[8:11].strip() # Счет команд
        taken_timeouts = time_info[13], time_info[14] # Количество взятых таймаутов
        time_part = time_info[15]
        plus_time = time_info[-2:]
        foals = time_info[11], time_info[12] # Фолы
        timeout_time = time_info[19:21], time_info[21:23]
    else:
        time_info = ''

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


    return (cur_time, teams_scores, taken_timeouts, time_part, remote_players, foals, '', plus_time)

if __name__ == '__main__':

    example_one = r'        00\x03N\x02T31/08/2016:34.50\x820      \x03\xfe\x02D 1:59 13 14  201320  18\x03n\x02F1`1 `2 `3 `4 `5 `6 `7  8  9 10 11 12 13 14 15    \x03&\x02\x02D 1:59 13 14  201320  18\x03n\x02O                                          00\x03N\x02T31/08/2016:34.50\x820      \x03\xfe\x02D 1:59 13 14  201320  18\x03n\x02F2`1 `2 `3 `4 `5 `6 `7  8  9 10 11 12 13 14 15    \x03%\x02\x02D 1:59 13 14  201320  18\x03n\x02O                                          00\x03N\x02T31/08/2016:34.50\x820      \x03\xfe\x02D 1:59 13 14  201320  18\x03n\x02F3                                \x03t\x02\x02D 1:59 13 14  201320  18\x03n\x02O                                          00\x03N\x02T31/08/2016:34.50\x820      \x03\xfe\x02D 1:59 13 14  201320  18\x03n\x02F4                                \x03s\x02\x02D 1:59 13 14  201320  18\x03n\x02O                                          00\x03N\x02T31/08/2016:34.50\x820      \x03\xfe\x02D 1:59 13 14  201320  18\x03n\x02F1`1 `2 `3 `4 `5 `6 `7  8  9 10 11 12 13 14 15    \x03&\x02\x02D 1:59 13 14  201320  18\x03n\x02O'

    example_two = r'                      \x03t\x02\x02D 5:28  0  0  001300  30\x03a\x02O                                          00\x03N\x02T17/09/2016:00.54\x820      \x03\xf8\x02D 5:28  0  0  001300  30\x03a\x02F4                                \x03s\x02\x02D 5:28  0  0  001300  30\x03a\x02O                                          00\x03N\x02T17/09/2016:00.55\x820      \x03\xf9\x02D 5:28  0  0  001300  30\x03a\x02F1`1 `2 `3 `4 `5 `6 `7  8  9 10 11 12 13 14 15    \x03&\x02\x02D 5:28  0  0  001300  30\x03a\x02O                                          00\x03N\x02T17/09/2016:00.55\x820      \x03\xf9\x02D 5:28  0  0  001300  30\x03a\x02F2`1 `2 `3 `4 `5 `6 `7  8  9 10 11 12 13 14 15    \x03%\x02\x02D 5:28  0  0  001300  30\x03a\x02O                                          00\x03N\x02T17/09/2016:00.55\x820      \x03\xf9\x02D 5:28  0  0  001300  30\x03a\x02F3                                \x03t\x02\x02D 5:28  0  0  001300  30\x03a\x02O                                          00\x03N\x02T17/09/2016:00.55\x820      \x03\xf9\x02D 5:28  0  0  001300  3'

    print(remote_controller_three(
        example_two
        )
    )
