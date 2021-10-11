#!/usr/bin/env python3
from typing import List
import rospy
from rospy.core import is_shutdown
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan

j1 = rospy.Publisher('joint1_vel_controller/command',Float64,queue_size=10)
j2 = rospy.Publisher('joint2_vel_controller/command',Float64,queue_size=10)
j3 = rospy.Publisher('joint3_vel_controller/command',Float64,queue_size=10)
j4 = rospy.Publisher('joint4_vel_controller/command',Float64,queue_size=10)

data = LaserScan()
min_value = 0
s = 0
i = 0
checking_value = []
inf = float('inf')
def callback(data):
    global min_value, s, i, checking_value
    min_value = min(data.ranges)
    s = data.ranges
    i = s.index(min_value)
    checking_value = s[i-5:i+5]

    rospy.loginfo("Message received")


def wall_follow():
    rospy.init_node('wall_follower',anonymous=True)
    distance = rospy.Subscriber('/laser/scan',LaserScan,callback)
    while(not rospy.is_shutdown):
        if(min_value in checking_value and data.range_min<min_value<data.range_max):
            v = 50
            w = -50
            j1.publish(v)
            j2.publish(w)
            j3.publish(v)
            j4.publish(w)
        else:
            j1.publish(0)
            j2.publish(0)
            j3.publish(0)
            j4.publish(0)

    

 

if __name__ == '__main__':
    try:
        wall_follow()
    except rospy.ROSInterruptException:
        pass