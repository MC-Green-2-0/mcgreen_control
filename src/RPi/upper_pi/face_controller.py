#!/usr/bin/python3
import rospy
import RPi.GPIO as GPIO
import time
from mcgreen_control.msg import Int16

class Face_Controller:
    FACE_TOPIC = "/facial_expression"

    def __init__(self):
        self.tog_sub = rospy.Subscriber(self.FACE_TOPIC, Int16, self.face_callback)

    def face_callback(self, data):
        pass

if __name__ == "__main__":
    try:
        rospy.init_node("Face_Controller")
        controller = Face_Controller()
        rospy.spin()
    except KeyboardInterrupt:
		pass
	except rospy.ROSInterruptException:
		pass
