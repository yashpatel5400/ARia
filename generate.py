"""
__authors__     = Yash, Peter, Jeff, Robert
__description__ = Generates the 3D image from a 2D image (to be displayed in the Oculus)
__name__ = generate.py
"""

import config as c
from PIL import Image

def generate_3d(img_fn):
    output_fn = "output/result.jpg"
    left  = Image.open(img_fn)
    right = Image.open(img_fn)

    w, h = left.size
    left  = left.crop( (0, 0, int(.90 * w), h))
    right = right.crop((int(.10 * w), 0, w, h))

    left  = left.resize((c.SCREEN_SIZE[0] // 2, c.SCREEN_SIZE[1]), Image.ANTIALIAS)
    right = right.resize((c.SCREEN_SIZE[0] // 2, c.SCREEN_SIZE[1]), Image.ANTIALIAS)
    
    new_img = Image.new('RGB', c.SCREEN_SIZE)
    new_img.paste(left, (0,0))
    new_img.paste(right, (c.SCREEN_SIZE[0] // 2,0))
    new_img.save(output_fn)

if __name__ == "__main__":
    generate_3d("images/fps.jpg")
    generate_3d("images/bioshock.jpg")
    generate_3d("images/drive.jpg")
    generate_3d("images/feet.jpg")
    generate_3d("images/drive.jpg")
    generate_3d("images/waterski.jpg")