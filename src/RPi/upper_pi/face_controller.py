#!/usr/bin/python3
import rospy
import RPi.GPIO as GPIO
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

from mcgreen_control.msg import Int16

class Face_Controller:
    FACE_TOPIC = "/facial_expression"

    def __init__(self):
        self.tog_sub = rospy.Subscriber(self.FACE_TOPIC, Int16, self.face_callback)
        
        # Configuration for the matrix
        self.options = RGBMatrixOptions()
        self.options.rows = 32
        self.options.cols = 32
        self.options.chain_length = 1
        self.options.parallel = 1
        self.matrix = RGBMatrix(options=options)

    # Called when the face matrix must be changed
    def face_callback(self, data):
        face_number = data.data

        image = Image.open("caution.bmp")

        if face_number == 0:
        	image = Image.open("caution.bmp")
        elif face_number == 1:
            image = Image.open("Grin.png")
        elif face_number == 2:
            image = Image.open("neut.png")
        elif face_number == 3:
            image = Image.open("Sad.png")
        elif face_number == 4:
            image = Image.open("Surprise.png")
        elif face_number == 5:
            image = Image.open("thumbs.png")
        
        image.thumbnail((self.matrix.width, self.matrix.height + 1), Image.ANTIALIAS)
        self.matrix.SetImage(image.convert('RGB'))


if __name__ == "__main__":
    try:
        rospy.init_node("Face_Controller")
        controller = Face_Controller()
        rospy.spin()
    except KeyboardInterrupt:
        pass
    except rospy.ROSInterruptException:
        pass
