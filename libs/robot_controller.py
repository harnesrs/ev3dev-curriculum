"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    
    # TODO: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor
        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor

    def drive_inches(self, inches, speed):
        self.left_motor.run_to_rel_pos(position_sp=90 * inches, speed_sp=speed, stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=90 * inches, speed_sp=speed, stop_action='brake')
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees, speed):
        if degrees > 0:
            self.left_motor.run_to_rel_pos(position_sp=-degrees * 5, speed_sp=speed)
            self.right_motor.run_to_rel_pos(position_sp=degrees * 5, speed_sp=speed)
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        else:
            self.left_motor.run_to_rel_pos(position_sp = degrees * 5, speed_sp = speed)
            self.right_motor.run_to_rel_pos(position_sp = -degrees * 5, speed_sp = speed)
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=900)
        while self.touch_sensor.is_pressed == False:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

        self.arm_motor.position = 0

    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=900)
        while self.touch_sensor.is_pressed == False:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_down(self):
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep().wait()

    def shutdown(self):
        self.running = False
        self.left_motor.stop(stop_action = ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.stop(stop_action = ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        print('Goodbye')
        ev3.Sound.speak('Goodbye').wait()

    def forward_drive(self, lspeed, rspeed):
        self.left_motor.run_forever(speed_sp=lspeed)
        self.right_motor.run_forever(speed_sp=rspeed)

    def left_drive(self, lspeed):
        self.left_motor.run_forever(speed_sp=lspeed)
        self.right_motor.stop()

    def right_drive(self, rspeed):
        self.right_motor.run_forever(speed_sp=rspeed)
        self.left_motor.stop()

    def reverse_drive(self, lspeed, rspeed):
        self.left_motor.run_forever(speed_sp=-lspeed)
        self.right_motor.run_forever(speed_sp=-rspeed)

    def stop(self):
        action = ev3.Motor.STOP_ACTION_BRAKE
        self.left_motor.stop(stop_action = action)
        self.right_motor.stop(stop_action = action)

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def turn(self, lspeed, rspeed):
        self.left_motor.run_forever(speed_sp = lspeed)
        self.right_motor.run_forever(speed_sp = rspeed)



