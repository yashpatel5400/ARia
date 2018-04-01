import numpy as np
import cv2

def rectify(h):
    if h.shape[0] * h.shape[1] != 8:
        return None

    h = h.reshape((4,2))
    hnew = np.zeros((4,2))

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h,axis=1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew


def get_corners(frame):

    imcopy = frame.copy()
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(imcopy, cv2.COLOR_BGR2HSV)
    # define range of orange color in HSV
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

    centers = np.array(centers)
    if centers.shape == (0,):
        return None

    centers = rectify(centers)
    return centers

def get_C_key(frame,corners):

    imcopy = frame.copy()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(imcopy, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([150,0,0])
    upper_blue = np.array([255,100,100])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(imcopy, lower_blue, upper_blue)
    imcopy = cv2.bitwise_and(imcopy,imcopy, mask=mask)

    # Get thresh into the correct cv2 readable format
    ret,thresh = cv2.threshold(imcopy, 0, 1, cv2.THRESH_BINARY)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_RGB2GRAY)
    # Find all the contours in the image
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Get the convex hull of all those contours
    convex_hulls = np.array(contours)
    # Find the area of all those convex hulls so we can take the largest
    contour_areas = [cv2.contourArea(c) for c in convex_hulls]
    # Get the indices of the largest contours. 
    largest_contour_idxes = np.array(contour_areas).argsort()[-1:][::-1]
    # Get the largest convex hull
    largest_convex_hulls = [convex_hulls[i] for i in largest_contour_idxes]
    # TODO: Ensure the convex hull are a minimum area

    # approximate the contour with a quadrangle
    if len(largest_convex_hulls) == 0:
        return None

    peri = cv2.arcLength(largest_convex_hulls[0],True)
    approx = cv2.approxPolyDP(largest_convex_hulls[0],0.02*peri,True)
    approx = rectify(approx)

    if approx is None:
        return None

    # get midpoints of corners
    left_mdpt = [(corners[0,0]+corners[3,0])/2,(corners[0,1]+corners[3,1])/2]
    right_mdpt = [(corners[1,0]+corners[2,0])/2,(corners[1,1]+corners[2,1])/2]
    top_mdpt = [(corners[0,0]+corners[1,0])/2,(corners[0,1]+corners[1,1])/2]
    bot_mdpt = [(corners[2,0]+corners[3,0])/2,(corners[2,1]+corners[3,1])/2]
    # get bounding coordinates
    board_left_x = left_mdpt[0]
    board_right_x = right_mdpt[0]
    board_top_y = top_mdpt[1]
    board_bot_y = bot_mdpt[1]

    # get top line of box which will be bottom of black key
    top = (approx[0,1]+approx[1,1])/2
    
    # get width of box, which will be width of a white key
    # black keys will be 2/3 as wide as a white key
    left_mdpt = [(approx[0,0]+approx[3,0])/2,(approx[0,1]+approx[3,1])/2]
    right_mdpt = [(approx[1,0]+approx[2,0])/2,(approx[1,1]+approx[2,1])/2]
    left_x = left_mdpt[0]
    right_x = right_mdpt[0]
    width = right_x - left_x

    # get corners of key
    ckey = [[left_x,board_top_y],[right_x,board_top_y],[right_x,board_bot_y],[left_x,board_bot_y]]

    return(ckey,width,top,[board_left_x,board_right_x])

def remainder_black_keys(remainder,higher):
    if higher:
        if remainder == 1:
            return 1
        elif remainder == 2:
            return 2
        elif remainder == 3:
            return 2
        elif remainder == 4:
            return 3
        elif remainder == 5:
            return 4
        elif remainder == 6:
            return 5
        else:
            return 0
    else:
        if remainder == 1:
            return 0
        elif remainder == 2:
            return 1
        elif remainder == 3:
            return 2
        elif remainder == 4:
            return 3
        elif remainder == 5:
            return 3
        elif remainder == 6:
            return 4
        else:
            return 0

def get_all_keys(frame,corners):

    # get the C key
    C_key_output = get_C_key(frame,corners)
    if C_key_output is None:
        return {}

    ckey = C_key_output[0]
    key_width = C_key_output[1]
    black_bot = C_key_output[2]
    board_bounds = C_key_output[3]

    # extrapolate positions of other keys
    num_higher_white_keys = np.around((board_bounds[1] - ckey[1][0])/key_width,decimals=0)
    higher_remainder = num_higher_white_keys % 7
    higher_remainder = remainder_black_keys(higher_remainder,True)
    num_higher_black_keys = (num_higher_white_keys//7)*5
    keys = [(ckey[0][0],ckey)]

    # white keys
    repeats = np.arange(num_higher_white_keys)
    higher_keys = [ (ckey[0][0]+shift*key_width,[[ckey[0][0]+shift*key_width,ckey[0][1]],[ckey[1][0]+shift*key_width,ckey[1][1]],[ckey[2][0]+shift*key_width,ckey[2][1]],[ckey[3][0]+shift*key_width,ckey[3][1]]]) for shift in repeats ]

    # black keys
    black_keys = []
    key = [[ckey[0][0]+2*key_width/3,ckey[0][1]],[ckey[1][0]+key_width/3,ckey[1][1]],[ckey[2][0]+2*key_width/3,black_bot],[ckey[3][0]+key_width/3,black_bot]]
    black_keys.append((key[0][0],key))
    last_key = black_keys[-1][1]
    key = [[last_key[0][0]+key_width,last_key[0][1]],[last_key[1][0]+key_width,last_key[1][1]],[last_key[2][0]+key_width,last_key[2][1]],[last_key[3][0]+key_width,last_key[3][1]]]
    black_keys.append((key[0][0],key))
    last_key = black_keys[-1][1]
    key = [[last_key[0][0]+2*key_width,last_key[0][1]],[last_key[1][0]+2*key_width,last_key[1][1]],[last_key[2][0]+2*key_width,last_key[2][1]],[last_key[3][0]+2*key_width,last_key[3][1]]]
    black_keys.append((key[0][0],key))
    last_key = black_keys[-1][1]
    key = [[last_key[0][0]+key_width,last_key[0][1]],[last_key[1][0]+key_width,last_key[1][1]],[last_key[2][0]+key_width,last_key[2][1]],[last_key[3][0]+key_width,last_key[3][1]]]
    black_keys.append((key[0][0],key))
    last_key = black_keys[-1][1]
    key = [[last_key[0][0]+key_width,last_key[0][1]],[last_key[1][0]+key_width,last_key[1][1]],[last_key[2][0]+key_width,last_key[2][1]],[last_key[3][0]+key_width,last_key[3][1]]]
    black_keys.append((key[0][0],key))
    for i in range(int(num_higher_black_keys/5-1)):
        last_key = black_keys[-1][1]
        key = [[last_key[0][0]+2*key_width,last_key[0][1]],[last_key[1][0]+2*key_width,last_key[1][1]],[last_key[2][0]+2*key_width,last_key[2][1]],[last_key[3][0]+2*key_width,last_key[3][1]]]
        black_keys.append((key[0][0],key))
        last_key = black_keys[-1][1]
        key = [[last_key[0][0]+key_width,last_key[0][1]],[last_key[1][0]+key_width,last_key[1][1]],[last_key[2][0]+key_width,last_key[2][1]],[last_key[3][0]+key_width,last_key[3][1]]]
        black_keys.append((key[0][0],key))
        last_key = black_keys[-1][1]
        key = [[last_key[0][0]+2*key_width,last_key[0][1]],[last_key[1][0]+2*key_width,last_key[1][1]],[last_key[2][0]+2*key_width,last_key[2][1]],[last_key[3][0]+2*key_width,last_key[3][1]]]
        black_keys.append((key[0][0],key))
        last_key = black_keys[-1][1]
        key = [[last_key[0][0]+key_width,last_key[0][1]],[last_key[1][0]+key_width,last_key[1][1]],[last_key[2][0]+key_width,last_key[2][1]],[last_key[3][0]+key_width,last_key[3][1]]]
        black_keys.append((key[0][0],key))
        last_key = black_keys[-1][1]
        key = [[last_key[0][0]+key_width,last_key[0][1]],[last_key[1][0]+key_width,last_key[1][1]],[last_key[2][0]+key_width,last_key[2][1]],[last_key[3][0]+key_width,last_key[3][1]]]
        black_keys.append((key[0][0],key))
    count = 0
    for i in range(1):
        if count >= higher_remainder:
            break
        last_key = black_keys[-1][1]
        key = [[last_key[0][0]+2*key_width,last_key[0][1]],[last_key[1][0]+2*key_width,last_key[1][1]],[last_key[2][0]+2*key_width,last_key[2][1]],[last_key[3][0]+2*key_width,last_key[3][1]]]
        black_keys.append((key[0][0],key))
        count = count + 1
        if count >= higher_remainder:
            break
        last_key = black_keys[-1][1]
        key = [[last_key[0][0]+key_width,last_key[0][1]],[last_key[1][0]+key_width,last_key[1][1]],[last_key[2][0]+key_width,last_key[2][1]],[last_key[3][0]+key_width,last_key[3][1]]]
        black_keys.append((key[0][0],key))
        count = count + 1
        if count >= higher_remainder:
            break
        last_key = black_keys[-1][1]
        key = [[last_key[0][0]+2*key_width,last_key[0][1]],[last_key[1][0]+2*key_width,last_key[1][1]],[last_key[2][0]+2*key_width,last_key[2][1]],[last_key[3][0]+2*key_width,last_key[3][1]]]
        black_keys.append((key[0][0],key))
        count = count + 1
        if count >= higher_remainder:
            break
        last_key = black_keys[-1][1]
        key = [[last_key[0][0]+key_width,last_key[0][1]],[last_key[1][0]+key_width,last_key[1][1]],[last_key[2][0]+key_width,last_key[2][1]],[last_key[3][0]+key_width,last_key[3][1]]]
        black_keys.append((key[0][0],key))
        count = count + 1
        if count >= higher_remainder:
            break
        last_key = black_keys[-1][1]
        key = [[last_key[0][0]+key_width,last_key[0][1]],[last_key[1][0]+key_width,last_key[1][1]],[last_key[2][0]+key_width,last_key[2][1]],[last_key[3][0]+key_width,last_key[3][1]]]
        black_keys.append((key[0][0],key))

    # sort by left x coordinate
    for black_key in black_keys:
        higher_keys.append(black_key)
    higher_keys.sort()
    key_boxes = [x for y,x in higher_keys]
    notes = range(len(key_boxes))
    key_dict = dict(zip(notes,key_boxes))

    return key_dict

def get_board(frame):

    corners = get_corners(frame)
    if corners is None:
        return {}

    key_dict = get_all_keys(frame,corners)
    return key_dict
