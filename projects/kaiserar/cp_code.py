#delegate needs to be able to rename label in tkinter

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import tkinter
from tkinter import ttk



class Delegate(object):
    def __init__(self, y, root):
        self.y = y
        self.root = root
    def display_message(self, string):
        self.y.set(string)





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
    y = tkinter.StringVar()
    mlabel = ttk.Label(frame1, textvariable=y)
    y.set("")
    mlabel.grid(row=4, column=1)
    ibutton = ttk.Button(frame1, text="IR Mode")
    ibutton.grid(row=6, column=2)
    ubutton = ttk.Button(frame1, text="Arm Up")
    ubutton.grid(row=5, column=0)
    dbutton = ttk.Button(frame1, text="Arm Down")
    dbutton.grid(row=5, column=2)
    cbutton = ttk.Button(frame1, text="Calibrate Arm")
    cbutton.grid(row=5, column=1)
    obutton = ttk.Button(frame1, text="End")
    obutton.grid(row=6, column=0)


    # mqtt connect
    delegate = Delegate(y, root)
    client = com.MqttClient(delegate)
    client.connect_to_ev3()

    speed = sbox.get() * 100

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

    ubutton['command'] = lambda: hand_ubutton(client)
    root.bind('<u>', lambda event: hand_ubutton(client))

    dbutton['command'] = lambda: hand_dbutton(client)
    root.bind('<d>', lambda event: hand_dbutton(client))

    cbutton['command'] = lambda: hand_cbutton(client)
    root.bind('<c>', lambda event: hand_cbutton(client))

    ibutton['command'] = lambda: hand_ibutton(client)
    root.bind('<i>', lambda event: hand_ibutton(client))

    obutton['command'] = lambda: hand_obutton(client)
    root.bind('<o>', lambda event: hand_obutton(client))



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

def hand_ubutton(client):
    client.send_message("up", [])

def hand_dbutton(client):
    client.send_message("down", [])

def hand_cbutton(client):
    client.send_message("cal", [])

def hand_ibutton(client):
    client.send_message("switch_mode_ir", [])

def hand_obutton(client):
    client.send_message("switch_mode_off", [])


main()