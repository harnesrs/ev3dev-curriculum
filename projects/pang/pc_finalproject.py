import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegate():
    def __init__(self):
        pass

    def drive_to_client(self):
        print('drive_to_client')

    def forward(self):
        print('go forward')

    def backward(self):
        print('go backward')

    def arm_up(self):
        print('arm up')

    def arm_down(self):
        print('arm down')

def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()
    # tkinter
    # human interaction
    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: handle_forward_button(mqtt_client)

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: handle_stop_button(mqtt_client)
    root.bind('<space>', lambda event: handle_stop_button(mqtt_client))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: handle_backward_button(mqtt_client)

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=3, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=3, column=2)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=5, column=0)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    color=tkinter.StringVar()
    color_list = ['ev3.ColorSensor.COLOR_RED', 'ev3.ColorSensor.COLOR_BLUE',
                  'ev3.ColorSensor.COLOR_BLACK', 'ev3.ColorSensor.COLOR_WHITE']

    client_1 = ttk.Radiobutton(main_frame, text='Client1', variable=color, value=0)
    client_1.grid(row=7, column=0)

    client_2 = ttk.Radiobutton(main_frame, text='Client2', variable=color, value=1)
    client_2.grid(row=7, column=1)

    client_3 = ttk.Radiobutton(main_frame, text='Client3', variable=color, value=2)
    client_3.grid(row=7, column=2)

    client_4 = ttk.Radiobutton(main_frame, text='Client4', variable=color, value=3)
    client_4.grid(row=7, column=3)

    set_client_button = ttk.Button(main_frame, text='set_client')
    set_client_button.grid(row=8, column=2)
    set_client_button['command'] = lambda: set_client(mqtt_client, color_list, int(color.get()))


    root.mainloop()


def handle_forward_button(mqtt_client):
    print('forward')
    mqtt_client.send_message('forward_drive',[300, 300])
    # pc to robot
    # motor


def handle_backward_button(mqtt_client):
    print('backward')
    mqtt_client.send_message('reverse_drive',[300, 300])


def handle_stop_button(mqtt_client):
    mqtt_client.send_message('stop')


def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def set_client(mqtt_client, color_list, color):
    print("Sending to client = {}", color)
    mqtt_client.send_message("set_color", [color_list[color]])


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()