#delegate needs to be able to rename label in tkinter

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import tkinter
from tkinter import ttk


def tkinter_window():
    root = tkinter.Tk()
    root.title("Controller")
    frame1 = ttk.Frame(root, padding = 30)
    frame1.grid()
    fbutton = ttk.Button(frame1, text = "Forward")
    fbutton.grid(row=0, column=1)
    lbutton = ttk.Button(frame1, text = "Left Turn")
    lbutton.grid(row=1, column=0)
    sbutton = ttk.Button(frame1, text = "Brake")
    sbutton.grid(row=1, column=1)
    rbutton = ttk.Button(frame1, text = "Right Turn")
    rbutton.grid(row=1, column=2)
    bbutton = ttk.Button(frame1, text = "Reverse")
    bbutton.grid(row=2, column=1)
    slabel = ttk.Label(frame1, text = "Speed:")
    slabel.grid(row=3, column=0)
    sbox = ttk.Entry(frame1)
    sbox.grid(row=3, column=1)
    root.mainloop()

def mqtt_connect():
    delegate = Delegate()
    client = com.MqttClient(delegate)
    client.connect_to_ev3()

class Delegate(object):
    def __init__(self):
        pass
    def display_message(self, root):
        pass



tkinter_window()




