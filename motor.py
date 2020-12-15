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

        # set motor PWM and range
        self.pi.set_PWM_range(self.ena_pin, 100)
        self.pi.set_PWM_frequency(self.ena_pin, 1000)

        # set initial state as stationary
        self.output(self.in1_pin, 0)
        self.output(self.in2_pin, 0)

    def set_speed(self, value: int):
        """
        pi.set_PWM_dutycycle(4, 0) # PWM off
        pi.set_PWM_dutycycle(4, 25) # PWM 1/4 on
        pi.set_PWM_dutycycle(4, 50) # PWM 1/2 on
        pi.set_PWM_dutycycle(4, 75) # PWM 3/4 on
        pi.set_PWM_dutycycle(4, 100) # PWM full on
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
        logging.info("FORWARD")

    def move_backwards(self, speed):
        self.output(self.in1_pin, gpio.LOW)
        self.output(self.in2_pin, gpio.HIGH)
        self.set_speed(speed)
        logging.info("BACKWARD")


def tu_dc_motor(_argv):
    dcMotor1 = DCMotor(ena_pin=24, in1_pin=13, in2_pin=19)
    dcMotor2 = DCMotor(ena_pin=23, in1_pin=20, in2_pin=21)

    while True:
        dcMotor1.move_forward(128)
        dcMotor2.move_forward(128)
        time.sleep(0.1)