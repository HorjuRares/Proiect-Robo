"""
    Script to change the motor behaviour using keyboard commands.
    Authors: Avesalon Razvan, Horju Rares
"""

from absl import app, logging, flags
import numpy as np
import keyboard as kb
import sys
import os
import time
# from motor import DCMotor
# from servo_motor import ServoMotor


direction = {
    'forward': True,
    'backward': False
}


def convert_degrees_to_rad(degree_value):
    return np.pi * degree_value / 180


def regulate_increment_throttle(value, direction: bool):
    """
    Function to regulate the throttle.
    :param value:
    :param direction: True - forward; False - backward
    :return:
    """
    if value >= 100 or value <= -100:
        return 0

    if direction:
        if value < 50:
            return 10
        else:
            return 1
    else:
        if value > -50:
            return -10
        else:
            return -1


def control_robot(dcMotor1=None, dcMotor2=None, servoMotor=None):
    """
    Function used to control the robot via keyboard.
    :param dcMotor1: dcMotor left
    :param dcMotor2: dcMotor right
    :param servoMotor: servo used for steering
    :return:
    """

    STEERING_ANGLE = 0
    THROTTLE_1 = 0
    THROTTLE_2 = 0

    while True:
        if kb.read_key() == "esc":
            # dcMotor1.stop_motor()
            # dcMotor2.stop_motor()
            # servoMotor.stop_motor()
            print("Exiting...")
            return
        if kb.read_key() == "b":
            print("Braking...")
            # dcMotor1.stop_motor()
            # dcMotor2.stop_motor()
            # servoMotor.stop_motor()
        if kb.read_key() == "a":
            THROTTLE_1 += regulate_increment_throttle(THROTTLE_1, direction=direction['forward'])
            THROTTLE_2 += regulate_increment_throttle(THROTTLE_2, direction=direction['forward'])

            # dcMotor1.move_forward(THROTTLE_1)
            # dcMotor2.move_forward(THROTTLE_2)

            print("Accelerating...")
            print("Throttle for motor 1: {}".format(THROTTLE_1))
            print("Throttle for motor 2: {}".format(THROTTLE_2))
        if kb.read_key() == "d":
            THROTTLE_1 += regulate_increment_throttle(THROTTLE_1, direction=direction['backward'])
            THROTTLE_2 += regulate_increment_throttle(THROTTLE_2, direction=direction['backward'])

            # dcMotor1.move_backwards(THROTTLE_1)
            # dcMotor2.move_backwards(THROTTLE_2)

            print("Decelerating...")
            print("Throttle for motor 1: {}".format(THROTTLE_1))
            print("Throttle for motor 2: {}".format(THROTTLE_2))

        if kb.read_key() == "left":
            if STEERING_ANGLE <= -60:
                continue

            STEERING_ANGLE -= 2
            # servoMotor.rotate(convert_degrees_to_rad(STEERING_ANGLE))

            print("Steering left...")
            print("Current steering angle: {} rad".format(STEERING_ANGLE))

        if kb.read_key() == "right":
            if STEERING_ANGLE >= 60:
                continue

            STEERING_ANGLE += 2
            # servoMotor.rotate(convert_degrees_to_rad(STEERING_ANGLE))

            print("Steering right...")
            print("Current steering angle: {} degrees".format(STEERING_ANGLE))


def main(_argv):
    # dcMotor1 = DCMotor(ena_pin=24, in1_pin=13, in2_pin=19)
    # dcMotor2 = DCMotor(ena_pin=23, in1_pin=20, in2_pin=21)
    #

    # servoMotor = ServoMotor(steering_pin=18)
    print("Press esc to exit / enter to start program")

    while True:
        if kb.read_key() == "esc":
            print("Exiting...")
            return
        if kb.read_key() == "enter":
            print("Starting...")
            print("Commands:")
            break

    control_robot()


if __name__ == '__main__':
    app.run(main)