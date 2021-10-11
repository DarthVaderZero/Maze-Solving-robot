#!/usr/bin/env python3
import rospy
from rospy.core import is_shutdown
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan


def callback(msg):
    rospy.loginfo("Inside callback")
    
    
    
    
def wall():
    #declaring publishers and subscribers
    rospy.init_node('wall_follower',anonymous=True)
    j1 = rospy.Publisher('joint1_vel_controller/command',Float64,queue_size=10)
    j2 = rospy.Publisher('joint2_vel_controller/command',Float64,queue_size=10)
    j3 = rospy.Publisher('joint3_vel_controller/command',Float64,queue_size=10)
    j4 = rospy.Publisher('joint4_vel_controller/command',Float64,queue_size=10)
    #r_wheel_back= Float64()
    #l_wheel_back= Float64()
    #r_wheel_front= Float64()
    #l_wheel_front= Float64()
    sub = rospy.Subscriber('/laser/scan', LaserScan, callback)
    while(not rospy.is_shutdown()):
        j1.publish(10)
        j2.publish(-10)
        j3.publish(10)
        j4.publish(-10)
        rospy.sleep(1)

    

if __name__ == '__main__':
    wall()