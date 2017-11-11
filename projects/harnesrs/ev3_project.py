#!/usr/bin/env python3

"""
This program does something
"""

import ev3dev.ev3 as ev3
import robot_controller as robo
import time
import mqtt_remote_method_calls as com

robot = robo.Snatch3r()

class MyDelegate(object):

    def __init__(self):
        self.direction = 0
        self.drive = False
        self.left_color = 5
        self.right_color = 2
        self.direction_list = ['forward', 'right', 'backward', 'left']

    def drive_button(self):
        robot.forward_drive(300, 300)
        self.drive = True

    def stop_button(self):
        robot.stop()
        self.drive = False

    def set_left_color(self, color):
        self.left_color = color

    def set_right_color(self, color):
        self.right_color = color

    def find_direction(self):
        print('I am facing', self.direction_list[self.direction])


def main():

    print('Starting Project')

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()

    btn = ev3.Button()

    while True:
        if btn.up:
            print('Up button')
            handle_up_button(mqtt_client, my_delegate)
            time.sleep(1)
        if btn.down:
            print('Down button')
            handle_down_button(mqtt_client, my_delegate)
            time.sleep(1)
        if btn.right:
            print('Right button')
            handle_right_button(mqtt_client, my_delegate)
            time.sleep(1)
        if btn.left:
            print('Left button')
            handle_left_button(mqtt_client, my_delegate)
            time.sleep(1)

        if robot.color_sensor.color == my_delegate.left_color:
            # print('left color is:', my_delegate.left_color)
            print('Turning left')
            turn_left(mqtt_client, my_delegate)

        if robot.color_sensor.color == my_delegate.right_color:
            # print('right color is:', my_delegate.right_color)
            print('Turning right')
            turn_right(mqtt_client, my_delegate)

        if btn.backspace:
            print('Backspace')
            robot.shutdown()
            break

def handle_up_button(mqtt_client, my_delegate):
    mqtt_client.send_message('turn_forward')
    degrees = (my_delegate.direction * 90)
    robot.turn_degrees(degrees, 300)
    my_delegate.direction = 0
    if my_delegate.drive:
        robot.forward_drive(300, 300)

def handle_down_button(mqtt_client, my_delegate):
    mqtt_client.send_message('turn_backward')
    degrees = (my_delegate.direction * 90) + 180
    robot.turn_degrees(degrees, 300)
    my_delegate.direction = 2
    if my_delegate.drive:
        robot.forward_drive(300, 300)

def handle_right_button(mqtt_client, my_delegate):
    mqtt_client.send_message('turn_right')
    degrees = (my_delegate.direction * 90) - 90
    robot.turn_degrees(degrees, 300)
    my_delegate.direction = 1
    if my_delegate.drive:
        robot.forward_drive(300, 300)

def handle_left_button(mqtt_client, my_delegate):
    # print('before left button direction is:', my_delegate.direction)
    mqtt_client.send_message('turn_left')
    degrees = (my_delegate.direction * 90) + 90
    robot.turn_degrees(degrees, 300)
    my_delegate.direction = 3
    # print('after left button direction is:', my_delegate.direction)
    if my_delegate.drive:
        robot.forward_drive(300, 300)

def turn_left(mqtt_client, my_delegate):
    if my_delegate.drive:
        # print('before turning left direction is:', my_delegate.direction)
        my_delegate.direction = (my_delegate.direction + 3) % 4
        robot.turn_degrees(90, 300)
        # print('after turning left direction is:', my_delegate.direction)
        robot.forward_drive(300, 300)

def turn_right(mqtt_client, my_delegate):
    if my_delegate.drive:
        my_delegate.direction = (my_delegate.direction + 1) % 4
        robot.turn_degrees(-90, 300)
        robot.forward_drive(300, 300)

main()