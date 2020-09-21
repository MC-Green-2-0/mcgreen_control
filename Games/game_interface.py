#!/usr/bin/python
import rospy
from std_msgs.msg import Int16, String
from mcgreen_control.msg import Array

# 1-3 -> Happy Faces
# 4   -> Neutral
# 5-6 -> Sad Faces
class Game_Interface:
    FACE_EXPRESSION = "/game_face"
    HEAD_TOPIC = "/game_motors"
    GAME_TOPIC = "/current_game"

    def __init__ (self):
        self.face_pub=rospy.Publisher(self.FACE_EXPRESSION, Int16, queue_size=1)
        self.head_pub=rospy.Publisher(self.HEAD_TOPIC, Array, queue_size=1)
        self.game_pub=rospy.Publisher(self.GAME_TOPIC, String, queue_size=1)
        self.expression=Int16()
        self.expression.data=4
        self.head=Array()
        self.head.arr=[90,90]
        self.name=String()
        self.name.data = "None"
        self.game_pub.publish(self.name)
        self.head_pub.publish(self.head)
        self.face_pub.publish(self.expression)

    def face_update(self, face):
        self.expression.data = int(face)
        self.face_pub.publish(self.expression)

    def game_update(self, game):
        self.name.data = str(game)
        self.game_pub.publish(self.name)

    def head_update(self, angle):
        self.head.arr = angle
        self.head_pub.publish(self.head)

if __name__=="__main__":
    try:
        rospy.init_node("Game_Interface")
        face_controller = Game_Interface()
        rospy.spin()
    except KeyboardInterrupt:
        pass
    except rospy.ROSInterruptException:
        pass
