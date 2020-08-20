#!/usr/bin/env python3
#USING PWM, but maybe change to another rotate-type movement?
import rospy
import RPi.GPIO as GPIO
import time
from mcgreen_control.msg import Array

#vertical controller attached to GPIO 12
#horizontal controller attached to GPIO 13

class Head_Servo_Driver:
    SERVO_TOPIC = "/upper_motors"

    def __init__(self,vertical,horizontal):
        self.tog_sub = rospy.Subscriber(self.SERVO_TOPIC, Array, self.servo_callback)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)#set pin numbering system
        GPIO.setup(vertical,GPIO.OUT)
        GPIO.setup(horizontal, GPIO.OUT)
        self.vertical_controller = GPIO.PWM(7,50)		#create PWM instance with frequency
        self.horizontal_controller = GPIO.PWM(19, 50)
        self.vertical_controller.start(0)				#start PWM of required Duty Cycle
        self.horizontal_controller.start(0)

    def servo_callback(self, data):
        horizontal_angle = int(2 + (data.arr[2]/18))
        vertical_angle = int(2 + (data.arr[3]/18))
        self.vertical_controller.ChangeDutyCycle(vertical_angle)
        self.horizontal_controller.ChangeDutyCycle(horizontal_angle)

    def clean(self):
        self.vertical_controller.ChangeDutyCycle(7)
        self.horizontal_controller.ChangeDutyCycle(7)

if __name__ == "__main__":
    try:
        rospy.init_node("Head_Servo_Driver")
        args = {"vertical": rospy.get_param("~vertical"), "horizontal": rospy.get_param("horizontal")}
        controller = Head_Servo_Driver(vertical, horizontal)
        rospy.spin()
        rospy.on_shutdown(controller.clean)
    except KeyboardInterrupt:
        pass
    except rospy.ROSInterruptException:
        pass
