#!/usr/bin/env python
import time
import math
from collections import namedtuple
import struct
import Adafruit_GPIO.FT232H as FT232H
import Adafruit_GPIO as GPIO

class MAXBOTIX_I2C():
    def __init__(self, ft232h, address=112):
        self.i2c = FT232H.I2CDevice(ft232h,112)

    def start_sensor(self):
        self.i2c.writeRaw8(81)

    def read_sensor(self):
        val = self.i2c.readU16(225)

        print(val >> 8), "cm"
        return val >> 8
