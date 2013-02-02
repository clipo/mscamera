__author__ = 'clipo'

import VideoCapture as VC
from PIL import Image
from PIL import ImageOps
import time

def capture_image():
    cam = VC.Device()   # initialize the webcam
    img = cam.getImage() # in my testing the first getImage stays black.
    time.sleep(1) # give sometime for the device to come up
    img = cam.getImage() # capture the current image
    del cam # no longer need the cam. uninitialize
    return img

if __name__=="__main__":
    img = capture_image()

    # use ImageOps to convert to grayscale.
    # show() saves the image to disk and opens the image.
    # you can also take a look at Image.save() method to write image to disk.
    ImageOps.grayscale(img).show()
