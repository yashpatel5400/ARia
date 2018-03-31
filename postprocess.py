"""
__authors__     = Yash, Peter, Jeff, Robert
__description__ = Post-processing step on the image frames before being sent
to be displayed on the Oculus
__name__ = postprocess.py
"""

import numpy as np
import cv2

from config import STREAM_FRAME_FILE

def step(frame):
    contours, colors = read_music(frame)
    frame = overlay_colors(frame, contours, colors)
    return frame

def read_music(frame):
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # imgray = cv2.cvtColor(,cv2.COLOR_BGR2GRAY)
    # ret,thresh = cv2.threshold(imgray,127,255,0)

    img, contours, h = cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    colors = np.random.randint(256, size=(len(contours), 3))

    return contours, colors
    # print contours
    # final = np.zeros(frame.shape,np.uint8)
    # mask = np.zeros(gray.shape,np.uint8)
    # return contours, mask, final
    # cv2.imshow("sup", gray)

def overlay_colors(frame, contours, colors):
    for i in xrange(0,len(contours)):
        cv2.drawContours(frame,contours,i,colors[i],-1)
    return frame

if __name__ == "__main__":
    # contours, colors, length = read_music(None)
    frame = cv2.imread(STREAM_FRAME_FILE)
    final = step(frame)
    cv2.imshow('original_frame',frame)
    cv2.imshow('final_frame',final)
    cv2.waitKey(0)