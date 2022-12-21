#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray 
import os
import pigpio

#define the pin of RPi
touch_l_pin = 5
touch_b_pin = 16 
touch_r_pin = 13
light_pin_d = 19

#initialize pinmode of rpi and give it a check
pi = pigpio.pi()
if not pi.connected:
    exit()

pi.set_mode(touch_r_pin, pigpio.INPUT)
pi.set_mode(touch_l_pin, pigpio.INPUT)
pi.set_mode(touch_b_pin, pigpio.INPUT)
pi.set_mode(light_pin_d, pigpio.INPUT)

rospy.init_node('sensor', anonymous=True) #node 
pub_touch_sensor = rospy.Publisher('touch_sensor', Float32MultiArray, queue_size=10) #topic name
pub_light = rospy.Publisher('light_sensor', Float32MultiArray, queue_size=10) #topic name
array = [1,1,1] # right/left/below
array_2 =[1] # find the light ball

def light_sensor():  
    if (pi.read(light_pin_d)==0):
        #print('Success!!!')
        return 0
    else:
        return 1

def collision():
    pub_touch_sensor.publish(data= array)
    pub_light.publish (data= array_2)
    rospy.sleep(0.3)
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        array[0] = pi.read(touch_r_pin)
        array[1] = pi.read(touch_l_pin)
        array[2] = pi.read(touch_b_pin)
        array_2[0] = light_sensor()
        pub_touch_sensor.publish(data= array)
        pub_light.publish (data = array_2)
        print('left/ right/ below/ light:', pi.read(touch_r_pin)," ", pi.read(touch_l_pin)," ",pi.read(touch_b_pin), " ", array_2[0])
        #print('light:_d', pi.read(light_pin_d))
        #print(array, array_2)
        r.sleep()

if __name__ == '__main__':
    
    try:
        collision()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

