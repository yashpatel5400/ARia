"""
__authors__     = Yash, Peter, Jeff, Robert
__description__ = Suuuuuuper jank way of getting the stream of the Raspberry Pi
camera images to the camera
__name__ = sync.py
"""

import subprocess
import time

cmd = ["rsync", "-a", "pi@10.24.190.99:~/Desktop/ARia/stream/", "stream/"]

def sync(terminate=None):
    cur_time = 0
    while True:
        if terminate is not None and cur_time > terminate:
            return
        subprocess.call(cmd)
        time.sleep(1.0)
        cur_time += 1

if __name__ == "__main__":
    sync(terminate=3)