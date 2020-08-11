#!/usr/bin/env python
import time
import rospy
from mcgreen_control.msg import Arm
import math
from collections import namedtuple
import struct
import Adafruit_GPIO.FT232H as FT232H
import Adafruit_GPIO as GPIO
from micropython import const
import maxbotix_deplib
import argparse

class arm_sensors:
    def __init__(self, side, topic):
        self.arm_pub = rospy.Publisher(topic, Arm, queue_size=1)
        self.data = Arm()
        self.data.arm = side
        FT232H.use_FT232H()
        self.ft232h = FT232H.FT232H(serial='black')
        self.address_lis = 0x18
        self.address_maxbotix = 112
        self.maxbotix = maxbotix_deplib.MAXBOTIX_I2C(self.ft232h, self.address_maxbotix)

    def data_publish(self):
        self.maxbotix.start_sensor()
        time.sleep(0.15)
        self.data.ultra = self.maxbotix.read_sensor()
        self.arm_pub.publish(self.data)

if __name__ == "__main__":
    rospy.init_node("right_arm_sensor")#Change this so it works for both sides
    args = {"side": rospy.get_param("~side"), "topic": rospy.get_param("~topic"), "rate": rospy.get_param("/peripheral/rate")}
    print(args["side"])
    sense = arm_sensors(args["side"], args["topic"])
    r = rospy.Rate(args["rate"])
    while not rospy.is_shutdown():
        sense.data_publish()
        r.sleep()
