#!/usr/bin/python3
import rospy
import RPi.GPIO as GPIO
import time
from mcgreen_control.msg import Int16

class Face_Controller:
    FACE_TOPIC = "/facial_expression"

    def __init__(self):
        self.tog_sub = rospy.Subscriber(self.FACE_TOPIC, Int16, self.face_callback)
        #initialize all your face display parameters here

    def face_callback(self, data):
        face_number = data.data
        if face_number == 0:
        	pass#add code to display each face
        if face_number == 1:
        	pass
        if face_number == 2:
        	pass
        if face_number == 3:
        	pass
        if face_number == 4:
        	pass
        if face_number == 5:
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
