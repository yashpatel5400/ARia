"""
__authors__     = Yash, Peter, Jeff, Robert
__description__ = Main application file to be run
__name__ = app.py
"""

import cv2

from generate import generate_3d
from detect_board import get_corners
from midi import get_note_sequence
from postprocess import overlay_colors

def main(music_fn):
    music = get_note_sequence(music_fn)
    frame = 1
    while True:
        input_fn  = "stream/{}.jpg".format(frame)
        output_fn = "output/{}.jpg".format(frame)

        frame_img = cv2.imread(input_fn)
        board_corners = get_corners(frame_img)

        color_img = overlay_colors()
        cv2.imwrite(output_fn, color_img)
        generate_3d(output_fn)

        frame += 1
        print("Completed frame {}".format(frame))

if __name__ == "__main__":
    main("music/pirates.mid")