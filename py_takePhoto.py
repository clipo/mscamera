__author__ = 'carllipo'

import subprocess  # needed to run external program raspistill
import datetime    # needed for timestamping outputfile
from subprocess import call
import time
import sys
import socket
host = socket.gethostname()

## get filename from command line
filename=sys.argv[1]  # get time delay between photos from command line

lapsef=float(filename)# change from string to floating polint real for later
call(["raspistill -o " + host+filename], shell=True) # call external program ro take a picture
time.sleep(6)  # take about 6 secons for the photo to be taken
call(["ftp ftp://RP_Master/ " +host+filename], shell=True)
time.sleep(6)  # wait