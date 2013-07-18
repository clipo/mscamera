__author__ = 'carllipo'


import subprocess  # needed to run external program raspistill
import datetime    # needed for timestamping outputfile

from subprocess import call
from datetime import datetime
import sys         # needed to get command line parameter which is time delay in seconds
import time        # nedeed to put program to sleep while waiting for next photo in low power

lapse=sys.argv[1]  # get time delay between photos from command line
print "Time lapse camera running with interval in seconds of"
print lapse        # echo input to screen
lapsef=float(lapse)# change from string to floating polint real for later

loop=True          # loop for ever - stop with CTRL C
while loop is True:
    ts=datetime.now()          # get time step
    a= ts.strftime("%j%H%M%S")
    print a                    # keep auidence amused
    print "picture in 5 sec"
    filename = "tl"+a+".jpg"   # give image file time-stamped name
    call(["raspistill -o " + filename], shell=True) # call external program ro take a picture
    print "done"
    time.sleep(lapsef-6.0)     # 6 sec roughly time to take a picture