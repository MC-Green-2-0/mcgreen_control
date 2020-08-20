#!/usr/bin/env python3
import rospy
import RPi.GPIO as GPIO
import time
from mcgreen_control.msg import Array

class Head_Servo_Driver:
    MOTOR_TOPIC = "/lower_motors"

    def __init__ (self, LIN1, LIN2, LPWM, RIN1, RIN2, RPWM, threshold):
        self.motor_sub = rospy.Subscriber(self.MOTOR_TOPIC, Array, self.motor_callback)
        self.side = side
        self.LIN1 = LIN1
        self.LIN2 = LIN2
        self.LPWM = LPWM
        self.RIN1 = RIN1
        self.RIN2 = RIN2
        self.RPWM = RPWM
        self.threshold = threshold

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.LIN1,GPIO.OUT)
        GPIO.setup(self.LIN2,GPIO.OUT)
        GPIO.setup(self.RIN1,GPIO.OUT)
        GPIO.setup(self.RIN2,GPIO.OUT)
        GPIO.output(self.LIN1, False)
        GPIO.output(self.LIN2, False)
        GPIO.output(self.RIN1, False)
        GPIO.output(self.RIN2, False)

        GPIO.setup(self.LPWM,GPIO.OUT)
        self.LPWM_Controller = GPIO.PWM(self.LPWM,50)
        self.LPWM_Controller.start(0)

        GPIO.setup(self.RPWM,GPIO.OUT)
        self.RPWM_Controller = GPIO.PWM(self.RPWM,50)
        self.RPWM_Controller.start(0)

    def motor_callback(self, data):
        left_joy = data[0]#left value (1000-2000)
        right_joy = data[1]#right value (1000-2000)

        #example code for direction of motor
        if motor_command == 1: #motor move forward
            GPIO.output(self.IN1, False)
            GPIO.output(self.IN2, True)
        elif motor_command == -1:#motor move reverse
            GPIO.output(self.IN1, True)
            GPIO.output(self.IN2, False)
        else:#don't move
            GPIO.output(self.IN1, False)
            GPIO.output(self.IN2, False)

        #PWM example
        self.LPWM_Controller.ChangeDutyCycle(number)#0-100
        #remember to use threshold

if __name__ == "__main__":
    try:
        rospy.init_node("Drivetrain_Driver")
        args = {"LIN1": rospy.get_param("~LIN1"), "LIN2": rospy.get_param("~LIN2"), "LPWM": rospy.get_param("~LPWM"), "RIN1": rospy.get_param("~RIN1"), "RIN2": rospy.get_param("~RIN2"), "RPWM": rospy.get_param("~RPWM"), "threshold": rospy.get_param("threshold_joystick")}
        controller = Drivetrain_Driver(args["LIN1"], args["LIN2"], args["LPWM"], args["RIN1"], args["RIN2"], args["RPWM"], args["threshold"])
        rospy.spin()
    except KeyboardInterrupt:
		pass
	except rospy.ROSInterruptException:
		pass
