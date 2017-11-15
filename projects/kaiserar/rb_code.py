#delegate needs to be robot (or able to use robot's methods)

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo



class Delagate(object):
    def __init__(self, robot):
        self.mode = 'ir'
        self.robot = robot
        self.arm_state = ''
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
        self.arm_state = 'up'
        self.robot.arm_up()
    def down(self):
        self.robot.arm_down()
        self.arm_state = 'down'
    def cal(self):
        self.arm_state = 'up'
        self.robot.arm_calibration()
        self.arm_state = 'down'
    def switch_mode_ir(self):
        self.mode = 'ir'
        print("ir")
        ev3.Sound.speak('I r')
    def switch_mode_mqtt(self):
        self.mode = 'mqtt'
        print('mqtt')
        ev3.Sound.speak('m q t t')
    def switch_mode_off(self):
        self.mode = 'off'


def handle_left_drive(state, robot):
    if state:
        robot.left_motor.run_forever(speed_sp = 600)
    else:
        robot.left_motor.stop()


def handle_left_reverse(state, robot):
    if state:
        robot.left_motor.run_forever(speed_sp = -600)
    else:
        robot.left_motor.stop()


def handle_right_drive(state, robot):
    if state:
        robot.right_motor.run_forever(speed_sp = 600)
    else:
        robot.right_motor.stop()


def handle_right_reverse(state, robot):
    if state:
        robot.right_motor.run_forever(speed_sp=-600)
    else:
        robot.right_motor.stop()


def handle_arm_up_button(button_state, robot):
    if button_state:
        robot.arm_up()


def handle_arm_down_button(button_state, robot):
    if button_state:
        robot.arm_down()


def handle_calibrate_button(button_state, robot):
    if button_state:
        robot.arm_calibration()


def handle_mode_change(state, delegate):
    if state:
        delegate.switch_mode_mqtt()


def handle_turn_off(state, delegate):
    if state:
        delegate.switch_mode_off()


def main():

    robot = robo.Snatch3r()
    ev3.Sound.speak("Starting")

    # IR remote
    rc1 = ev3.RemoteControl(channel=1)
    rc4 = ev3.RemoteControl(channel=4)
    rc2 = ev3.RemoteControl(channel=2)
    rc1.on_red_up = lambda state: handle_left_drive(state, robot)
    rc1.on_red_down = lambda state: handle_left_reverse(state, robot)
    rc1.on_blue_up = lambda state: handle_right_drive(state, robot)
    rc1.on_blue_down = lambda state: handle_right_reverse(state, robot)
    rc2.on_red_up = lambda state: handle_arm_up_button(state, robot)
    rc2.on_red_down = lambda state: handle_arm_down_button(state, robot)
    rc2.on_blue_up = lambda state: handle_calibrate_button(state, robot)
    rc4.on_red_up = lambda state: handle_mode_change(state, delegate)
    rc4.on_blue_down = lambda state: handle_turn_off(state, delegate)

    # mqtt connect
    delegate = Delagate(robot)
    client = com.MqttClient(delegate)
    client.connect_to_pc()

    ev3.Leds.all_off()
    robot.arm_calibration()
    delegate.arm_state = 'down'

    while delegate.mode != 'off':
        # IR mode
        while delegate.mode == 'ir':
            rc1.process()
            rc2.process()
            rc4.process()
            time.sleep(0.01)
        # mqtt mode
        while delegate.mode == 'mqtt':
            if delegate.arm_state == 'down':
                if robot.ir_sensor.proximity < 50:
                    robot.stop()
                    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
                    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
                    ev3.Sound.speak("Backing up")
                    robot.drive_inches(-8, 800)
                    client.send_message("display_message", ["Too close to wall. Turn and continue."])
                    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
                    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
    robot.shutdown()


main()