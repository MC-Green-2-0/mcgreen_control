#!/usr/bin/python3
import rospy
import numpy as np
from mcgreen_control.msg import Remote, Array
from std_msgs.msg import Int16

class Mode_Selector:
    RECEIVER_TOPIC = "/receiver"
    UPPER_TOPIC = "/remote_upper"
    LOWER_TOPIC = "/remote_lower"
    GAME_TOPIC = "/game_motors"
    FEEDBACK_TOPIC = "/mode_status"

    def __init__(self, multiplier, threshold):
        self.rec_sub = rospy.Subscriber(self.RECEIVER_TOPIC, Remote, self.rec_update)
        self.game_sub = rospy.Subscriber(self.GAME_TOPIC, Array, self.game_update)
        self.upper_safety_pub = rospy.Publisher(self.UPPER_TOPIC, Array, queue_size = 1)
        self.lower_safety_pub = rospy.Publisher(self.LOWER_TOPIC, Array, queue_size = 1)
        self.mode_feedback_pub = rospy.Publisher(self.FEEDBACK_TOPIC, Int16, queue_size = 1)
        self.multiplier = multiplier
        self.threshold  = threshold
        self.mode = 1 #1 is normal 2 arms and legs are disabled 3 is everything
        self.up_down = 0
        self.game_data = [90] * 2 #PWM for head or arms?
        self.feedback = Int16()
        self.feedback.data = 1
        self.out_upper = Array()
        self.out_upper.arr = [0] * 2 + [90] * 2
        self.out_lower = Array()
        self.mode_feedback_pub.publish(self.feedback)

    def rec_update(self,data):
        try:
            self.mode = data.ts[1]/500 - 1
            self.reset = int(data.ts[5]/2000)
            self.up_down = data.ts[0]/1000 - 1
        except (ValueError, IndexError):
            print("Waiting for receiver data")
        #FIX THIS SO IT MAKES MORE SENSE
        self.receiver_joystick = list(data.xy)
        self.receiver_joystick = self.receiver_joystick + list(data.ts[3:5])
        self.update()

    def game_update (self, data):
        self.game_data = data.arr
        self.update()

    def update(self):
        upper_data = [1500] * 2 + [90] * 2
        lower_data = [1500] * 4
        #up_down == 1 -> control drivetrain
        #up_down == 0 -> control head/face
        try:
            if self.mode == 1:
                if self.up_down == 1:
                    lower_data=self.receiver_joystick[:4]
                    upper_data=self.out_upper.arr
                if self.up_down == 0:
                    upper_data=self.receiver_joystick[:-2]
                    #move data from scroll wheels to replace left joystick
                    #will have to change to 0 and 1 here
                    upper_data[:2] = self.receiver_joystick[-2:]
                    print("input: ", upper_data)
                    #convert values from 1000-2000 range to 0-180 range
                    upper_data[2] = ((float(upper_data[2]) - 1000) / (1000) * (180))
                    upper_data[3] = ((float(upper_data[3]) - 1000) / (1000) * (180))
                    for x in range(2,4):
                        if abs(upper_data[x] - 90) > self.threshold:
                            increment = self.multiplier*np.sign(upper_data[x] - 90)
                            if increment + self.out_upper.arr[x] > 180:
                                upper_data[x]=180
                            elif increment + self.out_upper.arr[x] < 0:
                                upper_data[x]=0
                            else:
                                upper_data[x] = self.out_upper.arr[x] + increment
                        else:
                            upper_data[x] = self.out_upper.arr[x]
                if self.reset == 1:#may have to update for drivetrain motors as well
                    upper_data[0:2] = [0,0]
                    upper_data[2:] = [90,90]
        except IndexError:
            print("Waiting for receiver data")
        if self.mode == 2:
            upper_data = upper_data[:2] + self.game_data
            if self.up_down == 1:
                lower_data = self.receiver_joystick[:4]
        if self.mode == 3:
            upper_data = upper_data[:2] + self.game_data
        if self.feedback.data != self.mode:#check if mode is updated
            self.feedback.data=self.mode
            self.mode_feedback_pub.publish(self.feedback)
        #move forward or backward
        print("final: ", upper_data)
        self.out_upper.arr = upper_data
        self.out_lower.arr = lower_data
        self.upper_safety_pub.publish(self.out_upper)
        self.lower_safety_pub.publish(self.out_lower)

if __name__ == "__main__":
    try:
        rospy.init_node("mode_select")
        multiplier = rospy.get_param("~speed_multiplier")
        threshold = rospy.get_param("~joystick_threshold")
        mode = Mode_Selector(multiplier, threshold)
        rospy.spin()
    except KeyboardInterrupt:
        pass
    except rospy.ROSInterruptException:
        pass
