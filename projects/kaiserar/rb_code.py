#delegate needs to be robot (or able to use robot's methods)

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import tkinter
from tkinter import ttk


def mqtt_connect():
    delegate = Delagate()
    client = com.MqttClient(delegate)
    client.connect_to_pc()

class Delagate(object):
    def __init__(self):
        self.robot = robo.Snatch3r
    def forward(self, lspeed, rspeed):
        while True:
            self.robot.forward_drive(lspeed, rspeed)
            if self.robot.ir_sensor.proximity() < 50:
                break
            time.sleep(0.1)
        self.stop()
    def left(self, lspeed):
        self.robot.left_drive(lspeed)
    def right(self, rspeed):
        self.robot.right_drive(rspeed)
    def stop(self):
        self.robot.stop()
    def reverse(self, lspeed, rspeed):
        self.robot.reverse_drive(lspeed, rspeed)


def main():
    # mqtt connect
    delegate = Delagate()
    client = com.MqttClient(delegate)
    client.connect_to_pc()

    #