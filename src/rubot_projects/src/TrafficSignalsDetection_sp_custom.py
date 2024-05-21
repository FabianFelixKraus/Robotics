import rospy
import cv2
import numpy as np

def signal_detected(photo):
    img = cv2.imread(photo)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours to find circular and arrow-like shapes
    circles = []
    arrows = []
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.03 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Calculate contour area and perimeter
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        # If the contour is circular
        if len(approx) > 8 and area > 100 and abs(1 - (area / (np.pi * (perimeter ** 2) / 4))) < 0.2:
            circles.append(contour)
        # If the contour is an arrow-like shape 
        elif len(approx) == 7:
            arrows.append(contour)

    # Sort circles by area
    circles = sorted(circles, key=cv2.contourArea, reverse=True)
    # Sort arrows by position (e.g., centroid x-coordinate)
    arrows = sorted(arrows, key=lambda x: cv2.moments(x)['m10'])

    # Drawing the contour of the main circle
    if circles:
        main_signal = circles[0]
        signal_area = cv2.contourArea(main_signal)
        cv2.drawContours(img, [main_signal], -1, (0, 255, 0), 2)
    else:
        rospy.loginfo("No circular signal detected")
        return "unknown"

    # Assuming the closest arrow to the main signal is the direction indicator
    if arrows:
        arrow = arrows[0]
        arrow_area = cv2.contourArea(arrow)
        cv2.drawContours(img, [arrow], -1, (0, 0, 255), 2)
    else:
        rospy.loginfo("No arrow-like shape detected")
        return "unknown"

    # Calculate centroids for the circle and arrow contours
    circle_moments = cv2.moments(main_signal)
    circle_cx = int(circle_moments['m10'] / circle_moments['m00'])
    arrow_moments = cv2.moments(arrow)
    arrow_cx = int(arrow_moments['m10'] / arrow_moments['m00'])

    # Determine the direction based on the relative position of the arrow to the circle
    if circle_cx < arrow_cx:
        signal = "right"
    else:
        signal = "left"

    cv2.imshow('Detected Signals', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    rospy.loginfo("Signal detected: " + signal)
    return signal

if __name__ == '__main__':
     # Read signal
    #image = cv2.imread('left.png')
    photo = "left.png"
    signal = signal_detected(photo)
    print("Signal detected: ", signal)
    #cv2.imshow('Signal',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
