import time_util

from stream_processing import remote_controller_one, \
                              remote_controller_two

from red_remote import remote_controller_three


def set_model_on_stream(controller):
    time_util.listen_serial_port(ser, set_time_amount, set_time, set_reverse_time, set_sum_time, controller)


if __name__ == '__main__':
    try:
        set_port = str(input("Название порта (пример, COM3): "))
        set_time_amount = int(input("Количество таймов: "))
        set_time = int(input("Время тайма:"))
        set_reverse_time = input("Реверс тайм (y/n): ").lower() in ('y', 'yes', 'н', 'да', 1)
        set_sum_time = input("Суммировать таймы (y/n): ").lower() in ('y', 'yes', 'н', 'да', 1)
        set_model = int(input('Выберите модель пульта\
        \n 1 - Nr. BB329 (Старый серый)\
        \n 2 - Nr. BB337 (Новый серый)\
        \n 3 - Красный (водное поло, пока не работает): '))

        ser = time_util.init_time_thread(port="COM"+set_port)

        if set_model == 1:
            print('Подключение к серому старому пульту')
            set_model_on_stream(remote_controller_one)
        elif set_model == 2:
            print('Подключение к серому новому пульту')
            set_model_on_stream(remote_controller_two)
        elif set_model == 3:
            print('Подключение к красному новому пульту')
            set_model_on_stream(remote_controller_three)
        else:
            pass
    except Exception as e:
        print(e)
        input("Нажмите Enter, чтобы выйти")
