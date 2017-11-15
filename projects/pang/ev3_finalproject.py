import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time

robot = robo.Snatch3r()


class MyDelegate(object):

    def __init__(self):
        self.color = None

    def set_client(self, color):
        self.color = color
        robot.forward_drive(50, 50)


class DataContainer(object):
    def __init__(self):
        self.running = True



def main():
    my_delegate = MyDelegate
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    btn = ev3.Button()
    while True:
        if btn.up:
            print('move forward')
            forward(mqtt_client)
            time.sleep(0.01)
        if btn.down:
            print('to client 2')
            backward(mqtt_client)
            time.sleep(0.01)
        if btn.right:
            print('arm down')
            arm_down(mqtt_client)
            time.sleep(0.01)
        if btn.left:
            print('arm up')
            arm_up(mqtt_client)
            time.sleep(0.01)
        if btn.on_backspace:
            # digital input
            play_wav_file()
        if robot.color_sensor == my_delegate.color:
            # analogue sensor
            # interaction between color sensor and motion
            print('Dish is delivered to the client.')
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            robot.stop()
            break



def forward(mqtt_client):
    mqtt_client.send_message('forward')
    # robot to pc
    robot.forward_drive(20, 20)


def backward(mqtt_client):
    mqtt_client.send_message('backward')
    robot.reverse_drive(20, 20)

def arm_up(mqtt_client):
    mqtt_client.send_message('arm_up')
    robot.arm_up()


def arm_down(mqtt_client):
    mqtt_client.send_message('arm_down')
    robot.arm_down()


def play_wav_file():
    robot.arm_down()
    ev3.Sound.play("/home/robot/csse120/assets/sounds/awesome_pcm.wav")



main()
