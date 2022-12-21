#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray, String, Int16
import os
import pigpio

#define the pin of RPi
touch_l_pin = 5
touch_b_pin = 12
touch_r_pin = 13
light_pin_d = 19
light_pin_a = 26 #can't read 

#define threshold value of light sensor
threshold = 20
#initialize pinmode of rpi and give it a check
pi = pigpio.pi()
if not pi.connected:
    exit()

pi.set_mode(touch_r_pin, pigpio.OUTPUT)
pi.set_mode(touch_l_pin, pigpio.OUTPUT)
pi.set_mode(touch_b_pin, pigpio.OUTPUT)
pi.set_mode(light_pin_d, pigpio.INPUT)
pi.set_mode(light_pin_a, pigpio.INPUT)

rospy.init_node('sensor', anonymous=True) #node 
pub_touch_sensor = rospy.Publisher('touch_sensor', Float32MultiArray, queue_size=10) #topic name
pub_light = rospy.Publisher('light_sensor', Int16, queue_size=10) #topic name
#pub_state = rospy.Publisher('car_state', String, queue_size=1) #topic name
array = [0,0,0] # right/left/below
#array_2 = [0,0,0] # near/ far away/ find
light_value = 0

def collision():
    rospy.sleep(0.3)
    r = rospy.Rate(1) # 1hz
    print(array,light_value)
    while not rospy.is_shutdown():
        array[0] = touch_sensor_right()
        array[1] = touch_sensor_left ()
        array[2] = touch_sensor_below()
        pub_touch_sensor.publish(data= array)
        pub_light.publish (data= light_value)
        print('right/ left/ below:', pi.read(touch_r_pin),'/', pi.read(touch_l_pin),'/',pi.read(touch_b_pin))
        print('light_a:', pi.read(light_pin_a))
        print('light:_d', pi.read(light_pin_d))
        r.sleep()


def touch_sensor_right():
    if(((rospy.get_rostime()- last_time_right) > rospy.Duration(0.3,0)) & (pi.read(touch_r_pin)==0)):
        last_time_right=rospy.get_rostime()
        return 1
    else:
        return 0

def touch_sensor_left():
    if(((rospy.get_rostime()- last_time_left) > rospy.Duration(0.3,0)) & (pi.read(touch_l_pin)== 0)):
        last_time_left=rospy.get_rostime()
        return 1
    else:
        return 0

def touch_sensor_below():  
    if(((rospy.get_rostime()- last_time_below) > rospy.Duration(0.3,0)) & (pi.read(touch_b_pin)== 0)):
        last_time_below=rospy.get_rostime()
        return 1
    else:
        return 0

def light_sensor():  
    # lower value when closer 
    #toward the light
    #if ((pi.read(light_pin_a)-last_light_a) < 0.0):
    #    array_2 = [1, 0, 0] # near/ far away/ find
    #far away the light
    #if ((pi.read(light_pin_a)-last_light_a) > 0.0):
    #    array_2[1] = [0,1,0] # near/ far away/ find
    #find the light
    #if ((((pi.read(light_pin_d) == 0) & (pi.read(last_light_d) == 0)) ==1) | (pi.read(light_pin_a)<40)):
    #    array_2[2] = [0,0,1] # near/ far away/ find
    if ((pi.read(light_pin_d) == 0) & (pi.read(last_light_d) == 0)):
        light_value = 1 # near/ far away/ find
    else:
        last_light_d = pi.read(light_pin_d)
    #last_light_a = pi.read(light_pin_a)
    return light_value


if __name__ == '__main__':
    #data = String (input('Type q to exit:'))
    #if( data == 'q' ):
    #    os._exit(0)
    #else:
    #    data == 'g' 
    #    pub_state(data)
    try:
        collision()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

