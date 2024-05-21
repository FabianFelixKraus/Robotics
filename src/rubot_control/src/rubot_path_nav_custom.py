#!/usr/bin/env python3
import rospy
from rubot_nav import move_rubot
from math import sqrt,sin,cos,radians


def square_path(v,td):
    move_rubot(v,0,0,td)
    move_rubot(0,v,0,td)
    move_rubot(-v,0,0,td)
    move_rubot(0,-v,0,td)


def triangular_path(v, td):
    move_rubot(v,0,0,td)
    move_rubot(-v,v,0,td/sqrt(2))
    move_rubot(-v,-v,0,td/sqrt(2))

def star_path(v, td):
    # Move right
    move_rubot(v, 0, 0, td*2)
    # Move left
    move_rubot(-v, 0, 0, td*2)
    # Move diagonally up and right
    move_rubot(v * sqrt(2)/2, v * sqrt(2)/2, 0, td*2)
    # Move diagonally down and left
    move_rubot(-v * sqrt(2)/2, -v * sqrt(2)/2, 0, td*2)
    # Move up
    move_rubot(0, v, 0, td*2)
    # Move down
    move_rubot(0, -v, 0, td*2)
    # Move diagonally up and left
    move_rubot(-v * sqrt(2)/2, v * sqrt(2)/2, 0, td*2)
    # Move diagonally down and right
    move_rubot(v * sqrt(2)/2, -v * sqrt(2)/2, 0, td*2)
    # Move left
    move_rubot(-v, 0, 0, td*2)
    # Move right
    move_rubot(v, 0, 0, td*2)
    # Move diagonally down and left
    move_rubot(-v * sqrt(2)/2, -v * sqrt(2)/2, 0, td*2)
    # Move diagonally up and right
    move_rubot(v * sqrt(2)/2, v * sqrt(2)/2, 0, td*2)
    # Move down
    move_rubot(0, -v, 0, td*2)
    # Move up
    move_rubot(0, v, 0, td*2)
    # Move diagonally down and right
    move_rubot(v * sqrt(2)/2, -v * sqrt(2)/2, 0, td*2)
    # Move diagonally up and left
    move_rubot(-v * sqrt(2)/2, v * sqrt(2)/2, 0, td*2)

def rombus_path(v,td):
    move_rubot(v,-v,0,td/sqrt(2))
    move_rubot(v,v,0,td/sqrt(2))
    move_rubot(-v,v,0,td/sqrt(2))
    move_rubot(-v,-v,0,td/sqrt(2))
    # I just added a final spin as a show off.
    move_rubot(0,0,4.5,td)


if __name__ == '__main__':
    try:
        rospy.init_node('rubot_nav', anonymous=False)
        v= rospy.get_param("~v")
        w= rospy.get_param("~w")
        td= rospy.get_param("~td")
        path= rospy.get_param("~path")

        if path == "Square":
            square_path(v, td)

        elif path == "Triangular":
            triangular_path(v, td)
        
        elif path == "Star":
            star_path(v,td)

        elif path == "Rombus":
            rombus_path(v,td)
        
        elif path == "test":
            star_path(v,td)
            rombus_path(v,td)
        else:
            print('Error: unknown movement')

    except rospy.ROSInterruptException:
        pass
