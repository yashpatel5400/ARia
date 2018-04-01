"""
__authors__     = Yash, Peter, Jeff, Robert
__description__ = Main application file to be run
__name__ = app.py
"""

import cv2

from generate import generate_3d
from detect_board import get_corners

def main():
    frame = 0
    while True:
        frame_img = cv2.imread("stream/{}.jpg".format(frame))
        board_corners = get_corners(frame_img)

if __name__ == "__main__":
    main()