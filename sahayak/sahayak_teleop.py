#!/usr/bin/env python3
import rospy
import sys, termios, tty, os, time
from std_msgs.msg import Float64
from rospy.timer import Rate
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
def velocity():
    pub1 = rospy.Publisher('/joint1_vel_controller/command', Float64, queue_size=10)
    pub2 = rospy.Publisher('/joint2_vel_controller/command', Float64, queue_size=10)
    pub3 = rospy.Publisher('/joint3_vel_controller/command', Float64, queue_size=10)
    pub4 = rospy.Publisher('/joint4_vel_controller/command', Float64, queue_size=10)
    rospy.init_node('teleopsahayak', anonymous=True)
    rate = rospy.Rate(1)
    r_wheel_back= Float64()
    l_wheel_back= Float64()
    r_wheel_front= Float64()
    l_wheel_front= Float64()
    while not rospy.is_shutdown():
        key_value = getch()
        r_wheel_back.data= 0
        l_wheel_back.data= 0
        r_wheel_front.data= 0
        l_wheel_front.data= 0
        if key_value == 'w':
            r_wheel_back.data=1
            l_wheel_back.data=-1
            r_wheel_front.data=1
            l_wheel_front.data=-1
        elif key_value == 's':
            r_wheel_back.data= -1
            l_wheel_back.data= 1
            r_wheel_front.data= -1
            l_wheel_front.data= 1
        elif key_value == 'a':
            r_wheel_back.data= 1
            l_wheel_back.data= 1
            r_wheel_front.data= 1
            l_wheel_front.data= 1
        elif key_value == 'd':
            r_wheel_back.data= -1
            l_wheel_back.data= -1
            r_wheel_front.data= -1
            l_wheel_front.data= -1
        else:
            print("Invalid input")
        pub1.publish(r_wheel_back)
        pub2.publish(l_wheel_back)
        pub3.publish(r_wheel_front)
        pub4.publish(l_wheel_front)
        rate.sleep()
if __name__ == '__main__':
    try:
        velocity()
    except rospy.ROSInterruptException:
        pass