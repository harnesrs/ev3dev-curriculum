import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class MyDelegate(object):
    def __init__(self):
        pass

    def turn_forward(self):
        print('Turning forward')

    def turn_backward(self):
        print('Turning backward')

    def turn_right(self):
        print('Turning right')

    def turn_left(self):
        print('Turning left')

def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    color_list = [0, 1, 'blue', 'green', 4, 'red']

    root = tkinter.Tk()
    root.title('Color')

    main_frame = ttk.Frame(root, padding = 20)
    main_frame.grid()

    left = tkinter.StringVar()
    right = tkinter.StringVar()

    red_left = ttk.Radiobutton(main_frame, text='Red', variable = left, value = 5)
    red_left.grid(row=0, column=0)
    red_left.invoke()

    blue_left = ttk.Radiobutton(main_frame, text='Blue', variable = left, value = 2)
    blue_left.grid(row=0, column=1)

    green_left = ttk.Radiobutton(main_frame, text='Green', variable = left, value = 3)
    green_left.grid(row=0, column=2)

    set_left_color = ttk.Button(main_frame, text = 'Set left color')
    set_left_color.grid(row = 2, column = 1)
    set_left_color['command'] = lambda: set_left_color_button(mqtt_client, int(left.get()), color_list)

    red_right = ttk.Radiobutton(main_frame, text='Red', variable = right, value = 5)
    red_right.grid(row=0, column=4)

    blue_right = ttk.Radiobutton(main_frame, text='Blue', variable = right, value = 2)
    blue_right.grid(row=0, column=5)
    blue_right.invoke()

    green_right = ttk.Radiobutton(main_frame, text='Green', variable = right, value = 3)
    green_right.grid(row=0, column=6)

    set_right_color = ttk.Button(main_frame, text = 'Set right color')
    set_right_color.grid(row = 2, column = 5)
    set_right_color['command'] = lambda: set_right_color_button(mqtt_client, int(right.get()), color_list)

    drive_button = ttk.Button(main_frame, text = 'Drive')
    drive_button.grid(row = 4, column = 2)
    drive_button['command'] = lambda: handle_drive_button(mqtt_client)

    stop_button = ttk.Button(main_frame, text = 'Stop')
    stop_button.grid(row = 4, column = 4)
    stop_button['command'] = lambda: handle_stop_button(mqtt_client)

    direction = ttk.Button(main_frame, text = 'Direction')
    direction.grid(row = 4, column = 3)
    direction['command'] = lambda: direction_button(mqtt_client)

    quit_button = ttk.Button(main_frame, text = 'Quit')
    quit_button.grid(row = 5, column = 4)
    quit_button['command'] = lambda: quit_program(mqtt_client, True)

    root.mainloop()

def handle_drive_button(mqtt_client):
    print('Driving')
    mqtt_client.send_message('drive_button')

def handle_stop_button(mqtt_client):
    print('Stopping')
    mqtt_client.send_message('stop_button')

def set_left_color_button(mqtt_client, color, color_list):
    print('Turn left color is:', color_list[color])
    mqtt_client.send_message('set_left_color', [color])

def set_right_color_button(mqtt_client, color, color_list):
    print('Turn right color is:', color_list[color])
    mqtt_client.send_message('set_right_color', [color])

def direction_button(mqtt_client):
    mqtt_client.send_message('find_direction', [])

def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("Shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()

main()