#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
import time

def talker():
    pub = rospy.Publisher('talk', Int32, queue_size=10)
    data=Int32 (input('please input a number: '))
    pub.publish(data)
    time.sleep(0.5)

def callback(msg):
    print('return value is: ' + str(msg.data))

def main():
    rospy.init_node('talker', anonymous=True)
    rospy.Subscriber('listen',Int32, callback)
    try:
        while (True):
            #print('hello')
            talker()
    except rospy.ROSInterruptException:
        pass
main()

