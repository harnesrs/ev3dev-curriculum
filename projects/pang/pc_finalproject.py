import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()  # Delete this line, it was added temporarily so that the code we gave you had no errors.
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: handle_forward_button(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: handle_forward_button(mqtt_client, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button and '<Left>' key
    left_button['command'] = lambda: handle_left_button(mqtt_client, left_speed_entry)
    root.bind('<Left>', lambda event: handle_left_button(mqtt_client, left_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: handle_stop_button(mqtt_client)
    root.bind('<space>', lambda event: handle_stop_button(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button and '<Right>' key
    right_button['command'] = lambda: handle_right_button(mqtt_client, right_speed_entry)
    root.bind('<Right>', lambda event: handle_right_button(mqtt_client, right_speed_entry))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button and '<Down>' key
    back_button['command'] = lambda: handle_back_button(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Down>', lambda event: handle_back_button(mqtt_client, left_speed_entry, right_speed_entry))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    client_1 = ttk.Button(main_frame, text='Client1')
    client_1.grid(row=1, column=4)
    client_1['command'] = (lambda: drive_to_color(mqtt_client, True, "red"))

    client_2 = ttk.Button(main_frame, text='Client2')
    client_2.grid(row=3, column=4)
    client_2['command'] = (lambda: drive_to_color(mqtt_client, True, 'blue'))

    client_3 = ttk.Button(main_frame, text='Client3')
    client_3.grid(row=5, column=4)
    client_3['command'] = (lambda: drive_to_color(mqtt_client, True, 'black'))

    client_4 = ttk.Button(main_frame, text='Client4')
    client_4.grid(row=7, column=4)
    client_4['command'] = (lambda: drive_to_color(mqtt_client, True, 'white'))

    root.mainloop()


def handle_forward_button(mqtt_client, left_speed_entry, right_speed_entry):
    left_speed = int(left_speed_entry.get())
    right_speed = int(right_speed_entry.get())
    mqtt_client.send_message('forward_drive', [left_speed, right_speed])


def handle_right_button(mqtt_client, right_speed_entry):
    right_speed = int(right_speed_entry.get())
    mqtt_client.send_message('right_drive', [right_speed])


def handle_left_button(mqtt_client, left_speed_entry):
    left_speed = int(left_speed_entry.get())
    mqtt_client.send_message('left_drive', [left_speed])


def handle_back_button(mqtt_client, left_speed_entry, right_speed_entry):
    left_speed = int(left_speed_entry.get())
    right_speed = int(right_speed_entry.get())
    mqtt_client.send_message('reverse_drive', [left_speed, right_speed])


def handle_stop_button(mqtt_client):
    mqtt_client.send_message('stop')


def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def drive_to_color(mqtt_client, button_state, color):
    print("Sending color = {}, {}".format(button_state, color))
    mqtt_client.send_message("set_command", [button_state, color])


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()