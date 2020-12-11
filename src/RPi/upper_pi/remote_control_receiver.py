#!/usr/bin/python3
import serial
import rospy
from mcgreen_control.msg import Array
from binascii import hexlify

class Remote_Control:
	RECEIVER_TOPIC = "/receiver_output"
	ser = serial.Serial( port='/dev/ttyS0', baudrate=115200, timeout=1)
	counter = 0
	self.out = [1500] * 10

	def __init__ (self, rate):
		self.pub = rospy.Publisher(self.RECEIVER_TOPIC, Array, queue_size=1)
		self.rate = rospy.Rate(rate)

	def recieve(self):
		while not rospy.is_shutdown():
			hex = hexlify(ser.read(2))
			if hex == "2040":
				for i in range(10):
					lower_byte = ser.read(1)
					upper_byte = ser.read(1)
					if hexlify(a+b) != "":
						self.out[i] = int(hexlify(upper_byte+lower_byte),16)
			msg = Array()
			msg.arr = out
			self.pub.publish(msg)

if __name__ == '__main__':
	try:
		rospy.init_node("Remote_Control_Receiver")
		args = {"rate": rospy.get_param("~rate")}
		controller = Remote_Control(args["rate"])
		controller.recieve()
		rospy.spin()
	except KeyboardInterrupt:
		pass
	except rospy.ROSInterruptException:
		pass
