#!/usr/bin/env python3
import time
import rospy
from mcgreen_control.msg import Arm
import argparse
import RPi.GPIO as GPIO

class Arm_Sensor:

    def __init__(self, topic, trigger, echo):
        self.arm_pub = rospy.Publisher(topic, Arm, queue_size=1)
        self.data = Arm()
        GPIO.setmode(GPIO.BOARD)
        self.GPIO_TRIGGER = trigger
        self.GPIO_ECHO = echo
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

    def sense(self):
        GPIO.output(self.GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()

        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2

        self.data.ultrasonic = int(distance)
        self.arm_pub.publish(self.data)

if __name__ == "__main__":
    rospy.init_node("arm_sensor")
    args = {"topic": rospy.get_param("~topic"), "rate": rospy.get_param("/Sensors/rate"), "trigger": rospy.get_param("~trigger"), "echo": rospy.get_param("~echo")}
    sensor = Arm_Sensor(args["topic"], args["trigger"], args["echo"])
    r = rospy.Rate(args["rate"])
    while not rospy.is_shutdown():
        sensor.sense()
        r.sleep()
    GPIO.cleanup()
