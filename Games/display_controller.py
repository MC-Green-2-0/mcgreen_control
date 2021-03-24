#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16, Bool

class Display_Controller:
    MODE_TOPIC = "/safety_status"
    SAFETY_TOPIC = "/mode_status"

    def __init__ (self):
        self.mode_sub = rospy.Subscriber(self.MODE_TOPIC, Int16, self.mode_update)
        self.sefety_sub = rospy.Subscriber(self.SAFETY_TOPIC, Bool, self.safety_update)

    # Called when the robot's mode is changed. Decides whether games can be played or not
    def mode_update(self, mode):
        if mode.data != 3:
            # display MCGreen Logo (Games team)
            pass
        else:
            pass
            # you can play games
            # call the game menu function (Games team)

    # Called when there is a change to the safety status. If unsafe, displays a "caution" picture
    def safety_update(self, safety):
        if safety.data == False:
            pass
            # display Caution Picture

if __name__=="__main__":
    try:
        rospy.init_node("Display_Controller")
        controller = Display_Controller()
        rospy.spin()
    except KeyboardInterrupt:
        pass
    except rospy.ROSInterruptException:
        pass
