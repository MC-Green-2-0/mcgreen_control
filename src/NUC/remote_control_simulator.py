#!/usr/bin/env python3
from __future__ import division
import rospy
from mcgreen_control.msg import Array
import rospy
import os
from tkinter import *

class ControlApp(Tk, object):
    def __init__(self):
        super(ControlApp, self).__init__()
        self.ts = [1000,1500,0,1500,1500,0]#index 1 is mode (1000,1500,2000) index 5 is reset (0,2000) index 0 is updown (1000,2000) index 3,4 is arms (1000,1500,2000)
        self.xy = [1500,1500,1500,1500]
        # Initialize the teleop node
        rospy.init_node("Remote Control Sim")
        self.RECIEVER_TOPIC = "/receiver_output"
        self.pub = rospy.Publisher(self.RECIEVER_TOPIC, Array, queue_size=1)
        self.data = Array()
        self.sub = rospy.Subscriber("/receiver_output", Array, self.display_sensor_data)
        # Set up the interface
        self.geometry("100x100")
        self.bind("<KeyPress>", self.keydown)
        self.sensorText = StringVar()
        self.sensorLabel = Label(self, textvariable=self.sensorText)
        self.sensorLabel.pack()
        self.mainloop()
    def display_sensor_data(self, msg):
        s = str(msg.arr)
        self.sensorText.set(s)
    def keydown(self, event):
        self.xy = [1500,1500,1500,1500]
        if event.keysym =="w":
            self.xy[3] = 2000
        if event.keysym == "a":
            self.xy[2] = 1000
        if event.keysym== "s":
            self.xy[3] = 1000
        if event.keysym=="d":
            self.xy[2] = 2000
        if event.keysym=="r":
            if(self.ts[5] == 0):
                self.ts[5] = 2000
            else:
                self.ts[5] = 0
        self.ts[3:5] = [1500,1500]
        if event.keysym=="j":
            self.ts[3] = 2000
        if event.keysym=="k":
            self.ts[4] = 2000
        if event.keysym=="n":
            self.ts[3] = 1000
        if event.keysym=="m":
            self.ts[4] = 1000
        if event.keysym=="1":
            self.ts[1] = 1000
        if event.keysym=="2":
            self.ts[1] = 1500
        if event.keysym=="3":
            self.ts[1] = 2000
        if event.keysym=="u":
            if(self.ts[0] == 0):
                self.ts[0] = 2000
            else:
                self.ts[0] = 0
        self.data.arr = self.xy + self.ts
        self.pub.publish(self.data)
if __name__ == '__main__':
    os.system('xset r off')
    control = ControlApp()
    os.system('xset r on')
