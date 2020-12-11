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


class DCMotor(Part):
    def __init__(self, ena_pin = 18, in1_pin = 14, in2_pin = 15):
        super().__init__()
        self.ena_pin = ena_pin
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin

        # set pin modes
        self.set_pin_mode(self.ena_pin, self.gpio.OUTPUT)
        self.set_pin_mode(self.in1_pin, self.gpio.OUTPUT)
        self.set_pin_mode(self.in2_pin, self.gpio.OUTPUT)

        # set motor PWM
        self.pi.set_PWM_frequency(self.ena_pin, 1000)

        # set initial state as stationary
        self.output(self.in1_pin, 0)
        self.output(self.in2_pin, 0)

    def set_speed(self, value: int):
        """
        pi.set_PWM_dutycycle(4,   0) # PWM off
        pi.set_PWM_dutycycle(4,  64) # PWM 1/4 on
        pi.set_PWM_dutycycle(4, 128) # PWM 1/2 on
        pi.set_PWM_dutycycle(4, 192) # PWM 3/4 on
        pi.set_PWM_dutycycle(4, 255) # PWM full on
        :param value:
        :return:
        """
        self.pi.set_PWM_dutycycle(self.ena_pin, value)

    def stop_motor(self):
        self.output(self.in1_pin, gpio.LOW)
        self.output(self.in2_pin, gpio.LOW)
        self.set_speed(0)

    def move_forward(self, speed):
        self.output(self.in1_pin, gpio.HIGH)
        self.output(self.in2_pin, gpio.LOW)
        self.set_speed(speed)
        logging.log("FORWARD")

    def move_backwards(self, speed):
        self.output(self.in1_pin, gpio.LOW)
        self.output(self.in2_pin, gpio.HIGH)
        self.set_speed(speed)
        logging.log("BACKWARD")


class ServoMotor(Part):
    def __init__(self, pi = gpio.pi(), gpio = gpio, steering_pin = 23):
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
        # self.pi.set_PWM_range()

    def convert_radians_to_PWM(self, rad_value: int):
        """
        pi.set_PWM_dutycycle(4,   0) # PWM off
        pi.set_PWM_dutycycle(4,  25) # PWM 1/4 on
        pi.set_PWM_dutycycle(4, 50) # PWM 1/2 on
        pi.set_PWM_dutycycle(4, 75) # PWM 3/4 on
        pi.set_PWM_dutycycle(4, 100) # PWM full on
        """
        if rad_value < 0 or rad_value > np.pi:
            raise ValueError

        # (PWM_value - 1) * np.pi / 254
        return rad_value * 255 / np.pi

    def rotate(self, value):
        """
        Rotate the servo motor from 0 to pi radians.
        :param value: radians
        :return:
        """
        self.pi.set_PWM_dutycycle(self.steering_pin, self.convert_radians_to_PWM(value))

    def stop_motor(self):
        """
        method to stop the servo motor.
        :return:
        """
        self.output(self.steering_pin, 0)
        self.pi.set_PWM_dutycycle(self.steering_pin, 0)


def tu_dc_motor(_argv):
    dcMotor1 = DCMotor(ena_pin=24, in1_pin=13, in2_pin=19)
    dcMotor2 = DCMotor(ena_pin=23, in1_pin=20, in2_pin=21)

    while True:
        dcMotor1.move_forward(128)
        dcMotor2.move_forward(128)
        time.sleep(0.1)


def tu_servo(_argv):
    servo = ServoMotor()
    PWM_value = servo.convert_radians_to_PWM(np.pi/4)
    print(PWM_value)
    servo.rotate(0)
    servo.rotate(1)


if __name__ == '__main__':
    app.run(tu_servo)