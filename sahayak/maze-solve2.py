#!/usr/bin/env python3
from typing import List
import rospy
from rospy.core import is_shutdown
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
from math import inf 
import time

class Wall():
    def __init__(self):
        rospy.init_node('wall',anonymous = True)
        self.msg = LaserScan()
        self.min_sec_1 = 0
        self.min_sec_2 = 0
        self.min_sec_3 = 0
        self.i = 0
        self.count_val = 0
        self.min1 = 0
        self.min2 = 0
        self.min_left = 0
        self.min_0_90 = 0
        self.min_36_72 = 0
        self.min_sec_mid = 0
        self.full_list = []
        self.list_sector_1 = []
        self.list_sector_2 = []
        self.list_sector_3 = []
        self.sub = rospy.Subscriber('/laser/scan',LaserScan,self.update,queue_size = 5)
        self.j1 = rospy.Publisher('joint1_vel_controller/command',Float64,queue_size=10)
        self.j2 = rospy.Publisher('joint2_vel_controller/command',Float64,queue_size=10)
        self.j3 = rospy.Publisher('joint3_vel_controller/command',Float64,queue_size=10)
        self.j4 = rospy.Publisher('joint4_vel_controller/command',Float64,queue_size=10)
    def update(self,data):
        self.msg = data
        self.count_val = self.count_val + 1
        self.full_list = self.msg.ranges
        self.min_0_10 = min(self.full_list[0:10])
        self.min_81_90 = min(self.full_list[81:90])
        self.min_0_90 = min(self.full_list[0:90])
        self.min_36_72 = min(self.full_list[36:72])
        self.list_sector_1 = self.full_list[0:38]
        self.list_sector_2 = self.full_list[75:105]
        self.list_sector_3 = self.full_list[145:180]
        self.min_sec_1 = min(self.list_sector_1)
        self.min_sec_2 = min(self.list_sector_2)
        self.min_sec_3 = min(self.list_sector_3)
        self.min_sec_mid = min(self.full_list[81:99])
        rospy.loginfo(self.full_list[0])

    def expr(self):
        rospy.loginfo('Start')
        rospy.loginfo(self.count_val)
        while self.count_val == 1 or self.count_val== 0:
            self.min1 = self.min_sec_1
            self.min2 = self.min_sec_3
            self.min_left = self.min_0_90 + 0.5

        if self.min_sec_mid < 1.411:
            vel1 = -4000
            vel2 = -4000
            self.j1.publish(vel1)
            self.j2.publish(vel2)
            self.j3.publish(vel1)
            self.j4.publish(vel2)
        elif self.min_left - 0.3 <= self.min_36_72 <= self.min_left + 0.3 and self.min_sec_2 > 1.411:
            vel1 = 9000
            vel2 = -9000
            self.j1.publish(vel1)
            self.j2.publish(vel2)
            self.j3.publish(vel1)
            self.j4.publish(vel2)
        
        elif self.min_36_72 > self.min_left + 0.5 and self.min_sec_2 > 1.411:
            vel1 = 4000
            vel2 = 4000
            self.j1.publish(vel1)
            self.j2.publish(vel2)
            self.j3.publish(vel1)
            self.j4.publish(vel2)
        
        elif self.min_36_72 < self.min_left - 0.5 and self.min_sec_2 < 1.411:
            vel1 = -4000
            vel2 = -4000
            self.j1.publish(vel1)
            self.j2.publish(vel2)
            self.j3.publish(vel2)
            self.j4.publish(vel1)

        else:
            vel1 = 9000
            vel2 = -9000
            self.j1.publish(vel1)
            self.j2.publish(vel2)
            self.j3.publish(vel1)
            self.j4.publish(vel2)



if __name__ == '__main__':
    try:
        robot1 = Wall()
        while not rospy.is_shutdown():
            robot1.expr()
            rospy.sleep(0.5)
    except rospy.ROSInterruptException:
        pass