__author__ = 'carllipo'

from time import sleep  # Allows us to call the sleep function to slow down our loop
import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
import subprocess  # needed to run external program raspistill
import datetime    # needed for timestamping outputfile

from subprocess import call
import datetime
import sys         # needed to get command line parameter which is time delay in seconds
import time        # nedeed to put program to sleep while waiting for next photo in low power
import picamera

## need to connect to the master computer via FTP.

print "Running..."

def takePicture():
    ts=datetime.datetime.now()          # get time step
    a= ts.strftime("%j%H%M%S")
    filename = "P-"+a+".jpg"   # give image file time-stamped name
    call(["python pi_takePhoto.py -awb sun --colfx 128:128 -o " + filename], shell=True) # call external program ro take a picture
    print "Taking a picture: %s " % filename
    #with picamera.PiCamera() as camera:
    #    camera.resolution = (1024, 768)
    #    camera.start_preview()
    #    camera.capture(filename, 'raw')

def takeAPhoto():
    ts=datetime.datetime.now()          # get time step
    a= ts.strftime("%j%H%M%S")
    filename = "P-"+a+".jpg"   # give image file time-stamped name
    call(["python pi_takePhoto.py -awb sun --colfx 128:128 -o " + filename], shell=True) # call external program ro take a picture
    ## now trigger the ftp of the image to the master computer. may need to encapsulate this so that it can be a subprocess


GPIO.cleanup()
GPIO.setmode(GPIO.BCM)  # Set's GPIO pins to BOARD numbering
INPUT_PIN = 23           # Pin 4
GPIO.setup(INPUT_PIN, GPIO.IN)
#GPIO.add_event_detect(INPUT_PIN, GPIO.RISING, callback=takePicture)
GPIO.add_event_detect(INPUT_PIN, GPIO.RISING, callback=lambda x: takePicture )
# Wait for the input to go high, run the function when it does

# Create a function to run when the input is high
wait=0
# Start a loop that never ends
while True:
    # basically do nothing but wait for the pin to go HIGH
    # do nothing.
    wait += 1








