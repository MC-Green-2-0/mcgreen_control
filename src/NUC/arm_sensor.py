#!/usr/bin/env python3
import time
import rospy
from mcgreen_control.msg import Arm
import math
from collections import namedtuple
import struct
import Adafruit_GPIO.FT232H as FT232H
import Adafruit_GPIO as GPIO
import argparse

class MAXBOTIX_I2C():
    def __init__(self, ft232h, address=112):
        self.i2c = FT232H.I2CDevice(ft232h,112)

    def start_sensor(self):
        self.i2c.writeRaw8(81)

    def read_sensor(self):
        val = self.i2c.readU16(225)

        print(val >> 8), "cm"
        return val >> 8

class Arm_Sensor:
    def __init__(self, topic):
        self.arm_pub = rospy.Publisher(topic, Arm, queue_size=1)
        self.data = Arm()
        FT232H.use_FT232H()
        self.ft232h = FT232H.FT232H(serial='black')
        self.address_lis = 0x18
        self.address_maxbotix = 112
        self.maxbotix = MAXBOTIX_I2C(self.ft232h, self.address_maxbotix)

    def data_publish(self):
        self.maxbotix.start_sensor()
        time.sleep(0.15)
        self.data.ultrasonic = self.maxbotix.read_sensor()
        self.arm_pub.publish(self.data)

if __name__ == "__main__":
    rospy.init_node("arm_sensor")
    args = {"topic": rospy.get_param("~topic"), "rate": rospy.get_param("/Sensors/rate")}
    sense = Arm_Sensor(args["topic"])
    r = rospy.Rate(args["rate"])
    while not rospy.is_shutdown():
        sense.data_publish()
        r.sleep()
