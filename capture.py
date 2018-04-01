"""
__authors__     = Yash, Peter, Jeff, Robert
__description__ = Captures video off the Raspberry Pi camera and saves
them to the specified directory (off of which analysis/display will follow)
__name__ = capture.py
"""

import config as c

import io
import time
import picamera

class SplitFrames(object):
    def __init__(self):
        self.frame_num = 0
        self.output = None

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; close the old one (if any) and
            # open a new output
            if self.output:
                self.output.close()
            self.frame_num += 1
            self.output = io.open('stream/{}.jpg'.format(self.frame_num), 'wb')
        self.output.write(buf)

def capture(sec):
	with picamera.PiCamera(resolution='720p', framerate=c.FRAME_RATE) as camera:
		camera.start_preview()
		# Give the camera some warm-up time
		time.sleep(2)
		output = SplitFrames()
		start = time.time()
		camera.start_recording(output, format='mjpeg')
		camera.wait_recording(sec)
		camera.stop_recording()
		finish = time.time()
	print('Captured %d frames at %.2ffps' % (
		output.frame_num,
		output.frame_num / (finish - start)))

if __name__ == "__main__":
	capture(sec=3)
