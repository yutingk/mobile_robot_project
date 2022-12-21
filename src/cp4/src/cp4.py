#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray, Int16 

import os
import pigpio
import threading

#define the pin of RPi
touch_l_pin = 5
touch_b_pin = 16 
touch_r_pin = 13
light_pin_d = 19
ir_sensor_pin = 12
#initialize pinmode of rpi and give it a check
pi = pigpio.pi()
if not pi.connected:
    exit()

pi.set_mode(touch_r_pin, pigpio.INPUT)
pi.set_mode(touch_l_pin, pigpio.INPUT)
pi.set_mode(touch_b_pin, pigpio.INPUT)
pi.set_mode(light_pin_d, pigpio.INPUT)
pi.set_mode(ir_sensor_pin, pigpio.INPUT)

rospy.init_node('sensor', anonymous=True) #node 
pub_touch_sensor = rospy.Publisher('touch_sensor', Float32MultiArray, queue_size=10) #topic name
pub_light = rospy.Publisher('light_sensor', Float32MultiArray, queue_size=10) #topic name
pub_ir = rospy.Publisher('ir_sensor', Int16, queue_size=10)
array = [1,1,1] # right/left/below
array_2 =[1] # find the light ball
last_ir_time = rospy.Time()
cnt_beacon1500 = 0
cnt_beacon600 = 0
gate = 0
flag_busy = False
def light_sensor():  
    if (pi.read(light_pin_d)==0):
        #print('Success!!!')
        return 0
    else:
        return 1
def ir_cb():
    global flag_busy
    global last_ir_time
    global cnt_beacon600
    global cnt_beacon1500
    while True:
        #print('123')
        if(flag_busy == False):
            #print('ir_start')
            diff_time = rospy.Time.now() - last_ir_time
            print('diff_time = ', diff_time)
            if(diff_time > rospy.Duration(0.001)):
                diff_time = rospy.Time.now() - last_ir_time
                if(diff_time > rospy.Duration(0.0007) and diff_time < rospy.Duration(0.002)):
                    print(cnt_beacon600)
                    cnt_beacon600 +=1
                elif(diff_time > rospy.Duration(0.002) and diff_time < rospy.Duration(0.004)):
                    cnt_beacon1500 +=1
        last_ir_time = rospy.Time.now()
    
def collision():
    global flag_busy
    global cnt_beacon600
    global cnt_beacon1500
    pub_touch_sensor.publish(data= array)
    pub_light.publish (data= array_2)
    rospy.sleep(0.3)
    r = rospy.Rate(4) # 4hz
    #ir = pi.callback(ir_sensor_pin,pigpio.EITHER_EDGE, ir_cb())
    while not rospy.is_shutdown():
        array[0] = pi.read(touch_r_pin)
        array[1] = pi.read(touch_l_pin)
        array[2] = pi.read(touch_b_pin)
        array_2[0] = light_sensor()
        pub_touch_sensor.publish(data= array)
        pub_light.publish (data = array_2)
        #print('left/ right/ below/ light:', pi.read(touch_r_pin)," ", pi.read(touch_l_pin)," ",pi.read(touch_b_pin), " ", array_2[0])
        #print('light:_d', pi.read(light_pin_d))
        #print(array, array_2)
        flag_busy = True
        if(cnt_beacon600 - cnt_beacon1500 >=5):
            gate = 1
        elif (cnt_beacon1500 - cnt_beacon600 >=5):
            gate = 2
        else:
            gate = 0
        pub_ir.publish(data = gate)
        cnt_beacon600 = 0
        cnt_beacon1500 = 0
        flag_busy = False
        #print(flag_busy)
        #print(pi.read(ir_sensor_pin))
        print('left/ right/ below/ ligjt/ gate:', pi.read(touch_r_pin)," ", pi.read(touch_l_pin)," ",pi.read(touch_b_pin)," ", array_2[0], " ", gate)
        r.sleep()


if __name__ == '__main__':
    
    try:
        t = threading.Thread(target=ir_cb)
        t.setDaemon(True)
        t.start()
        collision()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass


