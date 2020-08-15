#!/usr/bin/env python3
import time
import serial
import chardet
import rospy
from mcgreen_control.msg import Array
from binascii import hexlify
from binascii import unhexlify
from threading import Timer



class Remote_Control:
	RECIEVER_TOPIC = "/receiver_output"

	ser = serial.Serial(
		port='/dev/ttyS0',
		baudrate=115200,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1
	)
	counter=0
	ch = [1500 for i in range(10)]

	def __init__ (self, rate):
		self.pub = rospy.Publisher(self.RECIEVER_TOPIC, Array, queue_size=0)
		self.rate = rospy.Rate(rate)

	def bytes_to_int(self, bytes):
		result=0
		for b in bytes:
			result = result*256+int(b)
		return result

	def talker(self):
		while not rospy.is_shutdown():
			a = ser.read(1)
			x = hexlify(a)

			if x == "20":
				a = ser.read(1)
				x = hexlify(a)
				if x == "40":
					for i in range(10):
						b = ser.read(1)
						a = ser.read(1)
						global ch
						if hexlify(a+b) != "":
							ch[i] = int(hexlify(a+b),16)
						else:
							ch = [0,0,0,0,0,0,0,0,0,0]
			elif x == "":
				ch = [0,0,0,0,0,0,0,0,0,0]

			msg = Array()
			msg.arr = ch
			self.pub.publish(msg)

if __name__ == '__main__':
	try:
		rospy.init_node("Remote_Control_Reciever")
		args = {"rate": rospy.get_param("~rate")}
		face_controller = Remote_Control(args["rate"])
		face_controller.talker()
		rospy.spin()
	except KeyboardInterrupt:
		pass
	except rospy.ROSInterruptException:
		pass
