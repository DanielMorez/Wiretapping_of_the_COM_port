import json
import time
import serial
import pathlib

from stream_processing import remote_controller_one, \
                              remote_controller_two

data = [
    {"time": " 0:00", "part": "1"},
    {
      "team": "A",
      "score": "0",
      "timeouts": "0",
      "remote": [
        {"num": " ", "time": " "},
        {"num": " ", "time": " "},
        {"num": " ", "time": " "}
      ],
      "foals": "0"
    },
    {
      "team": "B",
      "score": "0",
      "timeouts": "0",
      "remote": [
        {"num": " ", "time": " "},
        {"num": " ", "time": " "},
        {"num": " ", "time": " "}
      ],
      "foals": "0"
    }
  ] # output data

def init_time_thread(port='COM8', baudrate=9600, timeout=None):
    """
    Initialize stream
        params: port name, baudrate, timeout.
        return: serial.Serial obj.
    """
    ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
        )
    return ser

def listen_serial_port(ser: serial.Serial,
                       set_time_amount: int = 4,
                       set_time: int = 5,
                       set_reverse_time: bool = False,
                       set_sum_time: bool = False,
                       controller = remote_controller_one):
    """Get data stream and write current time in json file.
    params: serial.Serial obj.
    return: None."""

    if not ser.is_open:
        ser.open()
    else:
        ser.close(); ser.open()
    while True:
        size = ser.inWaiting()
        # print(size)
        while size:
            try:
                if size < 2048:
                    getting_size = size
                else:
                    getting_size = size
                stream = str(ser.read(getting_size)) # getting data
                for row in stream.split(): print((row))
                cur_time, scores, taken_timeouts, time_part, remote_players, foals, plus, plus_time = controller(
                        stream,
                        set_time_amount,
                        set_time,
                        set_reverse_time,
                        set_sum_time
                    )
            except IndexError:
                # print('Нет информации')
                pass
            else:
                # print(cur_time, scores, time_part, remote_players,
                #             taken_timeouts, foals, plus, plus_time)
                # write_json(cur_time, scores, time_part, remote_players,
                #             taken_timeouts, foals, plus, plus_time)
                pass
            finally:
                size -= getting_size
        else:
            time.sleep(0.5)

def write_json(current_time: str,
               scores: list,
               part: int,
               remote_players: list,
               timeouts: list,
               foals: list = ['0','0'],
               plus: list = ['0', '0'],
               plus_time: str = '',
               path: str = 'current_time.json'):
    global data
    # update time and timepart
    data[0].update(
            {
                'time': current_time,
                'part': part,
                'plus_time': plus_time
            }
        )

    for team_num in range(2):
        data[team_num+1].update(
                {
                    'score': scores[team_num]
                }
            )


        for i in range(len(remote_players[team_num])):
            data[team_num+1]['remote'][i] = dict(zip(["num", "time"], remote_players[team_num][i].split()))

        if len(remote_players[team_num]) == 0:
            for i in range(3):
                data[team_num+1]['remote'][i] = {"num": " ", "time": " "}
        if len(remote_players[team_num]) == 1:
            for i in range(2):
                data[team_num+1]['remote'][i+1] = {"num": " ", "time": " "}
        if len(remote_players[team_num]) == 2:
            data[team_num+1]['remote'][2] = {"num": " ", "time": " "}

        if timeouts[team_num] not in ('', ' '):
            data[team_num+1].update(
                {
                    'timeouts':timeouts[team_num]
                }
            )

        if '' not in plus:
            data[team_num+1].update(
                {'plusRemote': plus[team_num]}
            )

    with open(path, 'w', encoding = "utf-8") as outfile:
        json.dump({'response': data}, outfile)

    print('Записал')

if __name__ == '__main__':

    set_time_amount = 4 #int(input("Количество таймов: "))
    set_time = 20 #int(input("Время тайма:"))
    set_reverse_time = False #input("Реверс тайм (y/n):")
    set_sum_time = False #input("Суммировать таймы (y/n):")

    # example = r"\x02D 1:29 23 2000002010    \x03e\x02O                                          00\x03N\x02T27/08/2014:28.20\x8a322X   \x03\x82\x02D 1:29 23 2000002010    \x03e\x02F4                                \x03s\x02D 1:29 23 2000002010    \x03e\x02O                                          00\x03N\x02T27/08/2014:28.21\x8a322X   \x03\x83\x02D 1:29 23 2000002010    \x03e\x02F1`1 `5 `8 q0 q1 q3 q6 q7 q8 r1 r7 s4 t4 w7 x7 y1 \x03g\x02D 1:29 23 2000002010    \x03e\x02O 1:59                                     00\x03N\x02T27/08/2014:28.21\x8a322X   \x03\x83\x02D 1:29 23 2000002010    \x03e\x02F2`2 `3 q3 q6 q8 r1 r4 v3 w2 w3 w6 w7 w9 y7 y8 s7 \x03}\x02D 1:29 23 2000002010    \x03e\x02O                                          00\x03N\x02T27/08/2014:28.21\x8a322X   \x03\x83\x02D 1:30 23 2000002010    \x03m\x02F3                                \x03t\x02D 1:30 23 2000002010    \x03m\x02O                                          00\x03N\x02T27/08/2014:28.21\x8a322X   \x03\x83\x02D 1:30 23 2000002010    \x03m\x02F4                                \x03s"
    #
    #
    # cur_time, scores, taken_timeouts, time_part, remote_players, foals, plus = remote_controller_one(
    #         example,
    #         set_time_amount,
    #         set_time,
    #         set_reverse_time,
    #         set_sum_time
    #     )
    #
    # write_json(cur_time, scores, time_part, remote_players,
    #             taken_timeouts, foals, plus)

    ser = init_time_thread()
    listen_serial_port(ser, set_time_amount, set_time, set_reverse_time, set_sum_time, remote_controller_one)
