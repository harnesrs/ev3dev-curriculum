#delegate needs to be robot (or able to use robot's methods)

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import tkinter
from tkinter import ttk


def mqtt_connect():
    client = com.MqttClient()
    client.connect_to_pc()