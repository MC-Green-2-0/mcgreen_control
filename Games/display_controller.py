#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16, Bool

class Display_Controller:
    MODE_TOPIC = "/safety_status"
    SAFETY_TOPIC = "/mode_status"

    def __init__ (self):
        self.mode_sub = rospy.Subscriber(self.MODE_TOPIC, Int16, self.mode_update)
        self.sefety_sub = rospy.Subscriber(self.SAFETY_TOPIC, Bool, self.safety_update)

    def mode_update(self, mode):
        if mode.data != 3:
            #display MCGreen Logo (Maybe kill games?)
            pass
        else:
            pass
            #you can play games
            #Perhaps call the game menu function?

    def safety_update(self, safety):
        if safety.data == False:
            pass
            #display Caution Picture

if __name__=="__main__":
    try:
        rospy.init_node("Display_Controller")
        controller = Display_Controller()
        rospy.spin()
    except KeyboardInterrupt:
        pass
    except rospy.ROSInterruptException:
        pass
