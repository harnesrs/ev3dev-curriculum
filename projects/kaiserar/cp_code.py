#delegate needs to be able to rename label in tkinter

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import tkinter
from tkinter import ttk



def mqtt_connect():
    delegate = Delegate()
    client = com.MqttClient(delegate)
    client.connect_to_ev3()

class Delegate(object):
    def __init__(self):
        pass
    def display_message(self, mlabel):
        pass



def main():
    # tkinter construction
    root = tkinter.Tk()
    root.title("Controller")
    frame1 = ttk.Frame(root, padding=30)
    frame1.grid()
    fbutton = ttk.Button(frame1, text="Forward")
    fbutton.grid(row=0, column=1)
    lbutton = ttk.Button(frame1, text="Left Turn")
    lbutton.grid(row=1, column=0)
    sbutton = ttk.Button(frame1, text="Brake")
    sbutton.grid(row=1, column=1)
    rbutton = ttk.Button(frame1, text="Right Turn")
    rbutton.grid(row=1, column=2)
    bbutton = ttk.Button(frame1, text="Reverse")
    bbutton.grid(row=2, column=1)
    slabel = ttk.Label(frame1, text="Speed:")
    slabel.grid(row=3, column=0)
    x = tkinter.IntVar()
    sbox = ttk.Scale(frame1, from_=0, to=8, variable=x)
    sbox.grid(row=3, column=1)
    sread = ttk.Label(frame1, textvariable=x)
    sread.grid(row=3, column=2)
    mlabel = ttk.Label(frame1, text="")
    mlabel.grid(row=4, column=1)


    # mqtt connect
    delegate = Delegate()
    client = com.MqttClient(delegate)
    client.connect_to_ev3()

    speed = sbox.get()

    # tkinter buttons
    fbutton['command'] = lambda: hand_fbutton(client, speed)
    root.bind('<Up>', lambda event: hand_fbutton(client, speed))
    lbutton['command'] = lambda: hand_lbutton(client, speed)
    root.bind('<Left>', lambda event: hand_lbutton(client, speed))
    sbutton['command'] = lambda: hand_sbutton(client)
    root.bind('<space>', lambda event: hand_sbutton(client))
    rbutton['command'] = lambda: hand_rbutton(client, speed)
    root.bind('<Right>', lambda event: hand_rbutton(client, speed))
    bbutton['command'] = lambda: hand_bbutton(client, speed)
    root.bind('<Down>', lambda event: hand_bbutton(client, speed))


    root.mainloop()



# handle functions
def hand_fbutton(client, speed):
    client.send_message("forward", [speed, speed])

def hand_lbutton(client, speed):
    client.send_message("left", [speed])

def hand_sbutton(client):
    client.send_message("stop", [])

def hand_rbutton(client, speed):
    client.send_message("right", [speed])

def hand_bbutton(client, speed):
    client.send_message("reverse", [speed, speed])


main()