import mqtt_remote_method_calls as com
import robot_controller as robo

import ev3dev.ev3 as ev3
import time

class MyDelegate(object):

    def __init__(self):
        self.running = True

    def drive_to_color(self, robot, button_state, color_string):
        print("Received: {} , {}".format(button_state, color_string))
        if button_state:
            robot.forward_drive(300, 300)
            while True:
                if robot.color_sensor.color == color_string:
                    break
                time.sleep(0.01)
            robot.stop()


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
