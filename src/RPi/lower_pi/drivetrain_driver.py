#!/usr/bin/env python3
import rospy
import RPi.GPIO as GPIO
import time
from mcgreen_control.msg import Array

class Head_Servo_Driver:
    MOTOR_TOPIC = "/lower_motors"
    
    def __init__(self):
        self.tog_sub = rospy.Subscriber(self.MOTOR_TOPIC, Array, self.motor_callback)

    def motor_callback(self, data):
        pass

if __name__ == "__main__":
    try:
        rospy.init_node("Drivetrain_Driver")
        controller = Drivetrain_Driver()
        rospy.spin()
    except KeyboardInterrupt:
		pass
	except rospy.ROSInterruptException:
		pass
