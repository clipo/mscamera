__author__ = 'clipo'

from imgproc import *
import time

imageWidth = 640
imageHeight = 480
camera_1 = Camera(imageWidth,imageHeight)
camera_2 = Camera(imageWidth,imageHeight)
camera_3 = Camera(imageWidth,imageHeight)

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




# open the webcam
my_camera = Camera(320, 240)
# grab an image from the camera
my_image = my_camera.grabImage()

# open a view, setting the view to the size of the captured image
my_view = Viewer(“Basic image processing”, my_image.width, my_image.height)

# display the image on the screen
my_view.displayImage(my_image)

# wait for 5 seconds, so we can see the image
delay(5000)


==============
import cv

cv.NamedWindow("Camera 1")
cv.NamedWindow("Camera 2")
video1 = cv.CaptureFromCAM(0)
cv.SetCaptureProperty(video1, cv.CV_CAP_PROP_FRAME_WIDTH, 800)
cv.SetCaptureProperty(video1, cv.CV_CAP_PROP_FRAME_HEIGHT, 600)

video2 = cv.CaptureFromCAM(1)
cv.SetCaptureProperty(video2, cv.CV_CAP_PROP_FRAME_WIDTH, 800)
cv.SetCaptureProperty(video2, cv.CV_CAP_PROP_FRAME_HEIGHT, 600)

loop = True
while(loop == True):
    frame1 = cv.QueryFrame(video1)
    frame2 = cv.QueryFrame(video2)
    cv.ShowImage("Camera 1", frame1)
    cv.ShowImage("Camera 2", frame2)
    char = cv.WaitKey(99)
    if (char == 27):
        loop = False

cv.DestroyWindow("Camera 1")
cv.DestroyWindow("Camera 2")