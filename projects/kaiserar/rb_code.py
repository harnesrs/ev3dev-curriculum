#delegate needs to be robot (or able to use robot's methods)

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo



def mqtt_connect():
    delegate = Delagate()
    client = com.MqttClient(delegate)
    client.connect_to_pc()

class Delagate(object):
    def __init__(self, robot):
        self.mode = 'mqtt'
        self.robot = robot
    def forward(self, lspeed, rspeed):
        self.robot.forward_drive(lspeed, rspeed)
    def left(self, lspeed):
        self.robot.left_drive(lspeed)
    def right(self, rspeed):
        self.robot.right_drive(rspeed)
    def stop(self):
        self.robot.stop()
    def reverse(self, lspeed, rspeed):
        self.robot.reverse_drive(lspeed, rspeed)
    def up(self):
        self.robot.arm_up()
    def down(self):
        self.robot.arm_down()
    def cal(self):
        self.robot.arm_calibration()
    def switch_mode_ir(self):
        self.mode = 'ir'
    def switch_mode_mqtt(self):
        self.mode = 'mqtt'
    def switch_mode_off(self):
        self.mode = 'off'
    def off(self):
        pass


def main():

    # mqtt connect
    robot = robo.Snatch3r
    delegate = Delagate(robot)
    client = com.MqttClient(delegate)
    client.connect_to_pc()

    while True:
        #mqtt mode
        while delegate.mode == 'mqtt':
            if robot.ir_sensor.proximity < 50:
                robot.stop()
                robot.drive_inches(-8, 800)
                client.send_message("display_message", ["Too close to wall. Turn and continue."])
        while delegate.mode == 'ir':


main()