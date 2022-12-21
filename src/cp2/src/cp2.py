#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray
import time
import os

def speed():
    data= float(input('Please input the left speed:'))
    if(data==float(-100)):
        os._exit(0)
    pub = rospy.Publisher('num/raw', Float32MultiArray , queue_size=10)
    data1= float(input('Please input the right speed:'))
    array = [data,data1]
    pub.publish(Float32MultiArray(data=array))
    print('user\'s input(left/right):'+str(data) + '/' + str(data1))
    time.sleep(0.5)



def main():
    rospy.init_node('speed', anonymous=True)
    try:
        while(True):
            speed()
    except rospy.ROSInterruptException:
        pass
main()
