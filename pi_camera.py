__author__ = 'carllipo'

from time import sleep  # Allows us to call the sleep function to slow down our loop
#import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
import wiringpi2 as wiringpi

import subprocess  # needed to run external program raspistill
import datetime    # needed for timestamping outputfile

from subprocess import call
import datetime
import sys         # needed to get command line parameter which is time delay in seconds
import time        # nedeed to put program to sleep while waiting for next photo in low power
import picamera

## need to connect to the master computer via FTP.
wiringpi.wiringPiSetupGpio()
INPUT_PIN=16
print "Running..."

def takePicture():
    ts=datetime.datetime.now()          # get time step
    a= ts.strftime("%j%H%M%S")
    filename = "P-"+a+".jpg"   # give image file time-stamped name
    #call(["raspistill -awb sun --colfx 128:128 -o " + filename], shell=True) # call external program ro take a picture
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        time.sleep(1)
        camera.capture(filename, 'raw')

def takeAPhoto():
    ts=datetime.datetime.now()          # get time step
    a= ts.strftime("%j%H%M%S")
    filename = "P-"+a+".jpg"   # give image file time-stamped name
    call(["python pi_takePhoto.py -awb sun --colfx 128:128 -o " + filename], shell=True) # call external program ro take a picture
    ## now trigger the ftp of the image to the master computer. may need to encapsulate this so that it can be a subprocess



# Create a function to run when the input is high
wait=0
# Start a loop that never ends
while True:
    # basically do nothing but wait for the pin to go HIGH
    # do nothing.
    wait += 1
    input=wiringpi.digitalRead(INPUT_PIN) # Read pin 1
    print "INPUT: ",input
    if input > 0:
        takePicture()









