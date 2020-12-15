"""
    authors: Avesalon Razvan, Balog Istvan, Bita Robert, Bora Bogdan, Farkas Istvan, Horju Rares
"""

import unittest
import os
import time
import numpy as np
from absl import app, flags, logging
import pigpio as gpio
from part import Part


class ServoMotor(Part):
    def __init__(self, pi = gpio.pi(), gpio = gpio, steering_pin = 18):
        super().__init__()
        self.pi = pi
        self.gpio = gpio
        self.steering_pin = steering_pin

        # set pin mode
        self.set_pin_mode(self.steering_pin, self.gpio.OUTPUT)

        # set motor PWM
        self.pi.set_PWM_frequency(self.steering_pin, frequency=50)

        # set initial state as stationary
        self.output(self.steering_pin, 0)
        self.pi.set_PWM_dutycycle(self.steering_pin, 0)
        self.pi.set_servo_pulsewidth(self.steering_pin)

    def convert_radians_to_PW(self, rad_value: int):
        """
        pi.set_servo_pulsewidth(17, 0)    # off
        pi.set_servo_pulsewidth(17, 1000) # safe anti-clockwise (-pi/3)
        pi.set_servo_pulsewidth(17, 1500) # centre (0)
        pi.set_servo_pulsewidth(17, 2000) # safe clockwise (pi/3)
        """
        if rad_value < -np.pi / 3 or rad_value > np.pi / 3:
            raise ValueError

        rad_diff = abs(rad_value)
        pw_value = 1500 / np.pi * rad_diff
        new_pw_value = 1500 - pw_value if rad_value < 0 else 1500 + pw_value

        return new_pw_value

    def rotate(self, value):
        """
        Rotate the servo motor from -pi/3 to pi/3 radians.
        :param value: radians
        :return:
        """
        self.pi.set_servo_pulsewidth(self.steering_pin, self.convert_radians_to_PW(value))

    def stop_motor(self):
        """
        method to stop the servo motor.
        :return:
        """
        self.output(self.steering_pin, 0)
        self.pi.set_servo_pulsewidth(self.steering_pin, 0)


def tu_servo(_argv):
    servo = ServoMotor()
    PWM_value = servo.convert_radians_to_PWM(np.pi/4)
    print(PWM_value)
    servo.rotate(0)
    servo.rotate(1)


if __name__ == '__main__':
    app.run(tu_servo)