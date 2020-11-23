import unittest
import os
import numpy
from absl import app, flags, logging
import pigpio as gpio
from part import Part

class DCMotor(Part):
    def __init__(self, ena_pin = 18, in1_pin = 14, in2_pin = 15):
        self.ena_pin = ena_pin
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin

        # set pin modes
        self.set_pin_mode(self.ena_pin, self.gpio.OUTPUT)
        self.set_pin_mode(self.in1_pin, self.gpio.OUTPUT)
        self.set_pin_mode(self.in2_pin, self.gpio.OUTPUT)

        # set initial state as stationary
        self.output(self.in1_pin, 0)
        self.output(self.in2_pin, 0)

        # set motor PWM
        self.pi.set_PWM_frequency(self.ena_pin, 1000)

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

    def move_forward(self, speed):
        self.set_speed(speed)
        self.output(self.in1_pin, gpio.HIGH)
        self.output(self.in2_pin, gpio.LOW)
        logging.log("FORWARD")

    def move_backwards(self, speed):
        self.set_speed(speed)
        self.output(self.in1_pin, gpio.LOW)
        self.output(self.in2_pin, gpio.HIGH)
        logging.log("BACKWARD")