import unittest
import os
import numpy
from absl import app, flags, logging
import pigpio as gpio

class Part(object):
    def __init__(self, pi=gpio.pi(), gpio = gpio):
        self.pi = pi
        self.gpio = gpio

    def set_pin_mode(self, pin, mode):
        self.pi.set_mode(pin, mode)

    def send_data(self):
        pass

    def get_data(self):
        pass

    def output(self, pin, value):
        self.pi.write(pin, value)

    def input(self, pin):
        self.pi.read(pin)

    def stop(self):
        self.pi.stop()