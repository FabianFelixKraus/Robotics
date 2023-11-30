#! /usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan

def callback(msg):
    total_beams_factor = len(msg.ranges)/360.0

    print ("Number of scan points: "+ str(len(msg.ranges)))
    print ("total_beams_factor" + str(total_beams_factor))
    # values at 0 degrees
    print ("Distance at 0deg: " + str(msg.ranges[0]))
    # values at 90 degrees
    print ("Distance at 90deg: " + str(msg.ranges[int(90*total_beams_factor)]))
    # values at 180 degrees
    print ("Distance at 180deg: " + str(msg.ranges[int(180*total_beams_factor)]))
    # values at 270 degrees
    print ("Distance at 270deg: " + str(msg.ranges[int(270*total_beams_factor)]))
    # values at 360 degrees
    # print ("Distance at 360deg: " + str(msg.ranges[int(360*total_beams_factor)]))

rospy.init_node('scan_values')
sub = rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()