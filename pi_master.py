__author__ = 'carllipo'

import gps
import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
import datetime    # needed for timestamping outputfile

## this program will send the trigger for the multiple cameras (via pin 4)
## The trigger will be distance based using the GPS (ultimate GPS)
## this master computer must be set up as an access point (so the others can connect to it).
## The computer will look for files from the other PIs in the ftp directory
## and will bring them locally to assemble them into a GDAL, IMG file (multiband) (py_makeMultiSpectral.py)
## and then will trigger the creation of an NDVI (NDVI.py)

# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

OUTPUT_PIN = 4

GPIO.setup(OUTPUT_PIN, GPIO.OUT)

while True:
	try:
		report = session.next()
		# Wait for a 'TPV' report and display the current time
		# To see all report data, uncomment the line below
		# print report
		if report['class'] == 'TPV':
			if hasattr(report, 'time'):
				print report.time
	except KeyError:
		pass
	except KeyboardInterrupt:
		quit()
	except StopIteration:
		session = None
		print "GPSD has terminated"
