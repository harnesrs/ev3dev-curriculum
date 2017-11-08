#!/usr/bin/env python3

"""
This program does something
"""

import ev3dev.ev3 as ev3
import robot_controller as robo
import time
import mqtt_remote_method_calls as com

robot = robo.Snatch3r()
direction = 0

class MyDelegate(object):

    def __init__(self):
        pass

    def drive_button(self):
        ev3.Sound.speak('Driving')

    def stop_button(self):
        ev3.Sound.speak('Stopping')


def main():

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)

    btn = ev3.Button()


    while True:
        if btn.up:
            print('Up button')
            handle_up_button(mqtt_client)
        if btn.down:
            print('Down button')
            handle_down_button(mqtt_client)
        if btn.right:
            print('Right button')
            handle_right_button(mqtt_client)
        if btn.left:
            print('Left button')
            handle_left_button(mqtt_client)
        if btn.backspace:
            print('Backspace')
            robot.shutdown(mqtt_client)
            break

def handle_up_button(mqtt_client):
    direction = 0
    mqtt_client.send_message('turn_forward', [])

def handle_down_button(mqtt_client):
    direction = 2
    mqtt_client.send_message('turn_backward', [])

def handle_right_button(mqtt_client):
    direction = 1
    mqtt_client.send_message('turn_right', [])

def handle_left_button(mqtt_client):
    direction = 3
    mqtt_client.send_message('turn_left', [])

main()