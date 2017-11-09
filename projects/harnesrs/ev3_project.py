#!/usr/bin/env python3

"""
This program does something
"""

import ev3dev.ev3 as ev3
import robot_controller as robo
import time
import mqtt_remote_method_calls as com

robot = robo.Snatch3r()
left_color = 5
right_color = 2

class MyDelegate(object):

    def __init__(self):
        self.direction = 0

    def drive_button(self):
        robot.forward_drive(300, 300)
        ev3.Sound.speak('Driving').wait()

    def stop_button(self):
        robot.stop()
        ev3.Sound.speak('Stopping').wait()

    def left_color(self, color):
        left_color = color

    def right_color(self, color):
        right_color = color

    def direction(self):
        return self.direction


def main():

    print('Starting Project')

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()

    btn = ev3.Button()

    direction = 0

    while True:
        if btn.up:
            print('Up button')
            handle_up_button(mqtt_client, direction)
            time.sleep(3)
        if btn.down:
            print('Down button')
            handle_down_button(mqtt_client, direction)
            time.sleep(3)
        if btn.right:
            print('Right button')
            handle_right_button(mqtt_client, direction)
            time.sleep(3)
        if btn.left:
            print('Left button')
            handle_left_button(mqtt_client, direction)
            time.sleep(3)

        if robot.color_sensor.color == left_color:
            print('Turning left')
            turn_left(mqtt_client, direction)
            time.sleep(3)
        if robot.color_sensor.color == right_color:
            print('Turning right')
            turn_right(mqtt_client, direction)
            time.sleep(3)

        if btn.backspace:
            print('Backspace')
            robot.shutdown()
            break

def handle_up_button(mqtt_client, direction):
    mqtt_client.send_message('turn_forward')
    degrees = (direction * 90) % 360
    robot.turn_degrees(-degrees, 300)
    direction = 0
    robot.forward_drive(300, 300)

def handle_down_button(mqtt_client, direction):
    mqtt_client.send_message('turn_backward')
    degrees = (direction * 90) % 360 + 180
    robot.turn_degrees(-degrees, 300)
    direction = 2
    robot.forward_drive(300, 300)

def handle_right_button(mqtt_client, direction):
    mqtt_client.send_message('turn_right')
    degrees = (direction * 90) % 360 + 90
    robot.turn_degrees(-degrees, 300)
    direction = 1
    robot.forward_drive(300, 300)

def handle_left_button(mqtt_client, direction):
    mqtt_client.send_message('turn_left')
    degrees = (direction * 90) % 360 + 270
    robot.turn_degrees(-degrees, 300)
    direction = 3
    robot.forward_drive(300, 300)

def turn_left(mqtt_client, direction):
    robot.turn_degrees(90, 300)
    direction = direction + 1

def turn_right(mqtt_client, direction):
    robot.turn_degrees(-90, 300)
    direction = direction - 1

main()