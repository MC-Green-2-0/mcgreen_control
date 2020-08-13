#!/usr/bin/env python3
import rospy
import RPi.GPIO as GPIO
import time
from mcgreen_control.msg import Array

MOTOR_TOPIC = "/upper_motors"

class Controller:
    def __init__ (self, side):
        pass

    def move_actuator(side, command):
        pass


class Linear_Actuator_Driver:
    def __init__ (self, side):
        self.motor_sub = rospy.Subscriber(self.MOTOR_TOPIC, Array, self.actuator_callback)
        self.side = side
        self.index = -1
        controller = Controller()

    def actuator_callback(self, data):
        if side == "left":
            self.index = 0
        else:
            self.index = 1

        motor_command = data[self.index]
        if motor_command == 1:
            controller.move_actuator(self.index, "out")
            #push self.index side up
        elif motor_command == -1:
            controller.move_actuator(self.index, "in")
            pass
            #push self.index side down
        else:
            controller.move_actuator(self.index, "stop")
            pass
            #don't move


if __name__ == "__main__":
    try:
        rospy.init_node("linear_actuator")
        args = {"side": rospy.get_param("~side")}
        actuator = Linear_Actuator_Driver(args["side"])
        rospy.spin()
    except KeyboardInterrupt:
		pass
	except rospy.ROSInterruptException:
		pass
