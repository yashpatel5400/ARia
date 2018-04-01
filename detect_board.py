import numpy as np
import cv2

def get_corners(frame):
    imcopy = color_img.copy()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(imcopy, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_orange = np.array([0,100,100])
    upper_orange = np.array([50,255,255])
    # Threshold the HSV image to get only orange colors
    mask = cv2.inRange(imcopy, lower_orange, upper_orange)
    imcopy = cv2.bitwise_and(imcopy,imcopy, mask=mask)

    # Get thresh into the correct cv2 readable format
    ret,thresh = cv2.threshold(imcopy, 0, 1, cv2.THRESH_BINARY)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_RGB2GRAY)
    # Find all the contours in the image
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Get the convex hull of all those contours
    convex_hulls = np.array(contours[:])
    # Find the area of all those convex hulls so we can take the largest
    contour_areas = [cv2.contourArea(c) for c in convex_hulls]
    # Get the indices of the 4 largest contours. 
    largest_contour_idxes = np.array(contour_areas).argsort()[-4:][::-1]
    # Get the 4 largest convex hulls
    largest_convex_hulls = [convex_hulls[i] for i in largest_contour_idxes]
    # TODO: Ensure the convex hulls are a minimum area
    
    moments = [cv2.moments(c) for c in largest_convex_hulls]
    centers = [(int(m['m10']/m['m00']), int(m['m01']/m['m00'])) for m in moments if m['m00'] != 0]
    
    return centers
