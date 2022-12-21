#!/usr/bin/env python
import rospy
from std_msgs.msg import String, Float32MultiArray, Float32, Int16
import os
import time
import threading
########### global variable ##########
array_touch = [0,0,0] # right/left/below
light_digital = 0  # far away/ find
light_analog = 0.0
forward = [40, 43]
backward = [-29, -35]
left = [-20, 20]
right = [20, -20]
stop = [0, 0]
next_state = 'start'
light_log = 1000
### checkpoint4 ###
ir_data = 0 # no/600/1500
catch = 0
goal = 0
############ function part ############
def callback_touch(data):
    global array_touch
    global next_state
    global catch 
    #print('touch_sensor:',data.data)
    array_touch = data.data
    if array_touch[0] == float(0.0) and array_touch[1] == float(0.0)  :#obstacle front
        if catch == 0:
            next_state = 'backward'
            print('obstacle front')
        elif catch ==1:
            next_state = 'ball_back'

    elif array_touch[0] == float(0.0):#obstacle front left
        if catch == 0:
            next_state = 'backward'
            print('obstacle left')
        elif catch ==1:
            next_state = 'ball_right'
    elif array_touch[1] == float(0.0):#obstacle front right
        if catch == 0:
            next_state = 'backward'
            print('obstacle right')
        elif catch==1:
            next_state = 'ball_left'
        ### checkpoint4 ###
    elif array_touch[2] == float(0.0):
        catch = 1
        print('ir =',ir_data,' ',type(ir_data))
        print('catch the ball !!!')
        if ir_data != goal_gate: # cannot find the correct gate
           next_state = 'search_gate'
        elif ir_data == goal_gate: # find the correct gate 
            next_state = 'gogo_gate'
        
    
def callback_light_digital(data):
    global light_digital
    #print('light_sensor)digital:',data.data)
    light_digital =  data.data[0]

def callback_light_analog(data):
    global light_analog
    #print('light_sensor)analog:',data.data)
    light_analog =  data.data    

def ir_sub(data):
    global ir_data
    #print('ir_sensor:',data.data)
    ir_data =  data.data    

############ movement controll part ############   
def go_forward():
    pub_motor.publish(data = forward)
    time.sleep(1.0)
    
def go_backward():
    pub_motor.publish(data = backward)
    time.sleep(2)
    pub_motor.publish(data = left)
    time.sleep(0.5)

def turnleft():
    pub_motor.publish(data = left)
    print('left')
    time.sleep(0.3)

def turnright():
    pub_motor.publish(data = right)
    print('right')
    time.sleep(0.3)

def right_gate():
    pub_motor.publish(data = [10,-10])
    print('right')
    time.sleep(0.1)

def left_gate():
    pub_motor.publish(data = [-10, 10])
    print(left)
    time.sleep(0.1)

def forward_gate():
    pub_motor.publish(data = [20,22])
    time.sleep(0.5)

def backward_gate():
    pub_motor.publish(data =[-20, -22])
    time.sleep(0.2)

######### main #############        
if __name__ == '__main__':
    global goal_gate
    goal_gate = int(input('Enter gate (1 or 2):'))
    try:
        rospy.init_node('car_controller', anonymous=True)
        rospy.Subscriber("/touch_sensor", Float32MultiArray, callback_touch)
        rospy.Subscriber("/light_sensor", Float32MultiArray, callback_light_digital)
        rospy.Subscriber("/light_analog", Float32, callback_light_analog)
        ### checkpoint4 ###
        rospy.Subscriber("/ir_sensor", Int16, ir_sub)
        pub_motor = rospy.Publisher('/num/raw', Float32MultiArray, queue_size=10)
        direction = 0
        count = 0
        while not rospy.is_shutdown():
            print('-----------------')
            print(next_state)
            if next_state == 'start':
                count += 1
                if count == 8 and next_state == 'start' :
                    next_state = 'search'
                    count = 0
                elif next_state == 'start' :
                    go_forward()
                    next_state = 'start'
                else:
                    count = 0
        
            elif next_state == 'search':
                if(light_digital==0 and next_state=='search'):
                    go_forward()
                    if(next_state == 'search'):
                        next_state == 'search'
                        direction = 0
               # elif (light_digital == 1 and direction==0 and next_state=='search'):
               #    next_state = 'search_left'
               #     print(['direction ',direction])
               #     direction = -1
                elif (light_digital == 1 and direction==0 and next_state=='search'):
                    next_state = 'search_right'
                    direction = 0
                else:# have obstacle
                    print('obstacle!!!')
                    pass
            
            elif next_state == 'search_left':
                print('turnleft')
                turnleft()
                if(next_state == 'search_left'):
                    next_state = 'search'
                else:
                    pass
        
            elif next_state == 'search_right':
                print('turnright')
                if count == 3:
                    for i in range(2):
                        if next_state == 'search_right':
                            go_forward()
                        else:
                            break
                    count = 0
                else:
                    count +=1
                    turnright()
                if(next_state=='search_right'):
                    next_state = 'search'
                else:
                    pass

            elif next_state == 'backward':
                print('go_back')
                go_backward()
                next_state = 'search'
        
            elif next_state == 'ball_back':
                print('ball_back')
                backward_gate()
                if next_state == 'ball_back':
                    next_state = 'search_gate'
                else:
                    pass

            elif next_state == 'ball_left':
                print('ball_left')
                left_gate()
                if next_state == 'ball_left':
                    next_state = 'search_gate'
                else:
                    pass
            elif next_state == 'ball_right':
                print('ball_right')
                right_gate()
                if next_state == 'ball_right':
                    next_state = 'search_gate'
                else:
                    pass


            ### checkpoint4 ###

                   
            elif next_state == 'search_gate': 
                right_gate()
                if ir_data == 1:
                    next_state = 'gogo_gate'
                else:
                    next_state = 'search_gate'
           #     go_forward()
           #     go_forward()
           #     next_state == 'goal'
                
            elif next_state == 'gogo_gate':
                forward_gate()
                if ir_data == 1:
                    next_state = 'gogo_gate'
                else:
                    next_state = 'search_gate'
                

                
    except:
        pass


