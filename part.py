import unittest
import os
import numpy
from absl import app, flags, logging
import pigpio as gpio

class Part(object):
    def __init__(self, pi=gpio.pi()):
        self.pi = pi

    def set_pin_mode(self, pin, mode):
        self.pi.set_mode(pin, mode)

    def send_data(self):
        pass

    def get_data(self):
        pass