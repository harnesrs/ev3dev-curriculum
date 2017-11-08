import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import tkinter
from tkinter import ttk


def tkinter_window():
    root = tkinter.Tk()
    root.title("Controller")
    frame1 = ttk.Frame(root, padding = 10)
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
    root.mainloop()

def mqtt_connect():
    client = com.MqttClient()
    client.connect_to_ev3()


def test_prox(): 
    robot = robo.Snatch3r()
    while not robot.touch_sensor:
        print(robot.ir_sensor.proximity)

test_prox()