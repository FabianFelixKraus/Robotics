#!/usr/bin/env python3

import rospy
import sys
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class rUBot:

    def __init__(self):

        rospy.init_node("rubot_nav", anonymous=False)
        self._distanceLaser = rospy.get_param("~distance_laser")
        self._speedFactor = rospy.get_param("~speed_factor")
        self._forwardSpeed = rospy.get_param("~forward_speed")
        self._backwardSpeed = rospy.get_param("~backward_speed")
        self._rotationSpeed = rospy.get_param("~rotation_speed")

        self._msg = Twist()
        self._cmdVel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        rospy.Subscriber("/scan", LaserScan, self.callbackLaser)
        rospy.on_shutdown(self.shutdown)

        self._r = rospy.Rate(25)

    def start(self):

        while not rospy.is_shutdown():
            self._cmdVel.publish(self._msg)
            self._r.sleep()

    def callbackLaser(self, scan):
        """Function executed each time a message is received on /scan topic."""
        
        # Find the closest distance and its corresponding angle
        closestDistance, elementIndex = min((val, idx) for (idx, val) in enumerate(scan.ranges) if scan.range_min < val < scan.range_max)
        angleClosestDistance = (elementIndex / 2)  

        # Ensure angle is within the range [-180, 180)
        angleClosestDistance = self.__wrapAngle(angleClosestDistance)
        rospy.loginfo("Degree wrapped %5.2f ", angleClosestDistance)

        if angleClosestDistance > 0:
            angleClosestDistance=(angleClosestDistance-180)

        else:
            angleClosestDistance=(angleClosestDistance+180)

        # Check if the closest distance is within the specified range and adjust robot movement accordingly
        if closestDistance < self._distanceLaser and -80 < angleClosestDistance < 80:
            if angleClosestDistance > 45:
                # Move left if closest obstacle is on the right side
                self._msg.linear.x = 0
                self._msg.linear.y =  self._speedFactor * -self._forwardSpeed   # Move left to avoid obstacle
                self._msg.angular.z = 0
                rospy.logwarn("Within laser distance threshold. Moving the robot left...")
            if angleClosestDistance < -45:
                # Move right if closest obstacle is on the left side
                self._msg.linear.x = 0
                self._msg.linear.y =  self._speedFactor * self._forwardSpeed 
                self._msg.angular.z = 0
                rospy.logwarn("Within laser distance threshold. Moving the robot right...")

            if angleClosestDistance <= 45 and angleClosestDistance >= -45: 
                # Obstacle in front 
                self._msg.linear.x = 0
                self._msg.linear.y = 0
                self._msg.angular.z = self._rotationSpeed * self._speedFactor
        else:
            # Move forward if no obstacles within the specified range
            self._msg.linear.x = self._forwardSpeed * self._speedFactor
            self._msg.angular.z = 0
            self._msg.linear.y = 0

    def __sign(self, val):

        if val >= 0:
            return 1
        else:
            return -1
    

    def __wrapAngle(self, angle):
        if -180 <= angle <= 180:
            return angle
        else:
            return angle % 180

    def shutdown(self):
        self._msg.linear.x = 0
        self._msg.linear.y = 0
        self._msg.angular.z = 0
        self._cmdVel.publish(self._msg)
        rospy.loginfo("Stopping rUBot")

if __name__ == '__main__':
    try:
        rUBot1 = rUBot()
        rUBot1.start()
        rospy.spin()
        rUBot1.shutdown()
    except rospy.ROSInterruptException:
        pass
