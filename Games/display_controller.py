#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16, Bool
import time
import sys
import menu.py

class Display_Controller:
    MODE_TOPIC = "/safety_status"
    SAFETY_TOPIC = "/mode_status"
    FACE_TOPIC = "/facial_expression"



    def __init__ (self):
        self.mode_sub = rospy.Subscriber(self.MODE_TOPIC, Int16, self.mode_update)
        self.sefety_sub = rospy.Subscriber(self.SAFETY_TOPIC, Bool, self.safety_update)
        self.face_pub = rospy.Publisher(self.FACE_TOPIC, Int16, queue_size=1)

    # Called when the robot's mode is changed. Decides whether games can be played or not
    def mode_update(self, mode):
        if mode.data != 3:
            # display MCGreen Logo
            pass
        else:
            menu.run_menu()

    # Called when there is a change to the safety status. If unsafe, displays a "caution" picture
    def safety_update(self, safety):
        if safety.data == False:
            # display MCGreen Logo
            self.expression = Int16()
            self.expression.data = 0
            self.face_pub.publish(self.expression)

if __name__=="__main__":
    try:
        rospy.init_node("Display_Controller")
        controller = Display_Controller()
        rospy.spin()
    except KeyboardInterrupt:
        pass
    except rospy.ROSInterruptException:
        pass
