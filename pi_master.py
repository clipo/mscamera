__author__ = 'carllipo'
from subprocess import call
import gps
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

try:
    call(["sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock"])
except RuntimeError:
    print ("Cannot get the gps process to run. try: sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock" )
    sys.exit("quitting.")

import datetime    # needed for timestamping outputfile
import math
import csv
import datetime

import sys         # needed to get command line parameter which is time delay in seconds
import time        # nedeed to put program to sleep while waiting for next photo in low power
import picamera

## this program will send the trigger for the multiple cameras (via pin 4)
## The trigger will be distance based using the GPS (ultimate GPS)
## this master computer must be set up as an access point (so the others can connect to it).
## The computer will look for files from the other PIs in the ftp directory
## and will bring them locally to assemble them into a GDAL, IMG file (multiband) (py_makeMultiSpectral.py)
## and then will trigger the creation of an NDVI (NDVI.py)

ts=datetime.datetime.now()
oldTime=ts
a=ts.strftime("%j%H%M%S")+"-log.csv"
## log file
log = open(a, 'wb')
writer = csv.writer(log)
values= ["Time","Northing","Easting","Zone","Latitude", "Longitude", "Altitude", "Speed"]
writer.writerows(values)

OUTPUT_PIN=7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)

# minimum distance between shots (meters)
distanceForNewPhoto=30

# minimum time between shots  (seconds)
minTime = 15

## some constants for the gps conversion
equatorial_radius = 6373137
polar_radius=6356752
flattening=0.003353
inverse_flattening=298.2572
mean_radius=6367436
scale_factor=0.9996
eccentricity=0.081819
eccentricity2=0.006739
e1sq= 0.006739
eccentricity3=0.001679
# Meridonal Arc Constants
A0 = 6367449.1458008400000000000
B0 = 16038.4295531591000000000
C0 = 16.8326133343344000000
D0 = 0.0219844042737573000
E0 = 0.0003127052179504480
Sin1 = 0.0000048481368110954
oldEasting = 0
oldNorthing = 0
oldZone =0
altitude =0
currentEasting=0
currentNorthing=0
currentZone=0
altitude=0
speed=0


######
## takes lat/long returns Northing/Easting/Zone
## Assumes WGS 1984 datum
######

def latLongToUTM(latitude, longitude):
    latRad = latitude*math.pi/180
    longRad = longitude*math.pi/180
    longZone = 31+int(longitude/6)
    longZoneCM = 6*longZone-183
    deltaLong=(longitude-longZoneCM)*math.pi/180
    rcurv1 = equatorial_radius*(1-eccentricity**2)/((1-(eccentricity*math.sin(latRad))**2)**(1.5))
    rcurv2 = equatorial_radius/((1-(eccentricity*math.sin(latRad))**2)**(0.5))
    merid_arc = A0*latRad - B0*math.sin(2*latRad) + C0*math.sin(4*latRad) - D0*math.sin(6*latRad) + E0*math.sin(8*latRad)
    k1= merid_arc * scale_factor
    k2= rcurv1*math.sin(latRad)*math.cos(latRad)/2
    k3=((rcurv2*math.sin(latRad)*(math.cos(latRad))**3)/24)*(5-math.tan(latRad)**2+9*eccentricity2*(math.cos(latRad))**2+(4*(eccentricity2)**2)*math.cos(latRad)**4)*scale_factor
    k4=rcurv2*math.cos(latRad)*scale_factor
    k5=math.cos(latRad)**3*(rcurv2/6)*(1-math.tan(latRad)**2+e1sq*math.cos(latRad)**2)*scale_factor
    a61=deltaLong*deltaLong*deltaLong*deltaLong*deltaLong*deltaLong*rcurv2*math.sin(latRad)*((math.cos(latRad))**5)/720
    a62=61-58*(math.tan(latRad)**2)+(math.tan(latRad)**4)+270*e1sq*(math.cos(latRad)**2)-330*e1sq*math.sin(latRad)**2
    a6=a61*a62*scale_factor
    raw_northing=(k1+k2*deltaLong*deltaLong+k3*deltaLong*deltaLong*deltaLong*deltaLong)
    northing = raw_northing
    if raw_northing < 0:
        northing = raw_northing + 10000000
    easting = 500000+(k4*deltaLong+k5*deltaLong*deltaLong*deltaLong)
    zone = longZone
    return northing, easting, zone

def distanceBetweenPoints(n1, e1, n2, e2):
    distance = math.sqrt((n1-n2)**2 + (e1-e2)**2)
    return distance

def takeAPhoto(channel):
    ts=datetime.datetime.now()          # get time step
    a= ts.strftime("%j%H%M%S")
    filename = "P-"+a+".jpg"   # give image file time-stamped name
    call(["python pi_takePhoto.py -awb sun --colfx 128:128 -o " + filename], shell=True) # call external program ro take a picture
    ## now trigger the ftp of the image to the master computer. may need to encapsulate this so that it can be a subprocess


def setup():
    # Listen on port 2947 (gpsd) of localhost
    session = gps.gps("localhost", "2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    wait=0
    tryAttempt=0
    ## first get initial location ... wait until you get a report
    try:
        report = session.next()
        if report['class'] == 'TPV':
            if hasattr(report, 'time'):
                time = report.time
            if hasattr(report, 'latitude'):
                latitude = report.latitude
            if hasattr(report, 'longitude'):
                longitude = report.longitude
            if hasattr(report,'altitude'):
                altitude=report.altitude
            if hasattr(report,'speed'):
                speed=report.speed
            oldNorthing, oldEasting, oldZone = latLongToUTM(latitude,longitude)
            currentNorthing = oldNorthing
            currentEasting = oldNorthing
            currentZone=oldZone
            currentAltitude=altitude
            currentTime = datetime.datetime.now()
            oldTime=currentTime
            wait = 1 ## break if we get values...
    except KeyError:
      pass
    except KeyboardInterrupt:
      quit()
    except StopIteration:
      session = None
      print "GPSD has terminated"

def takePicture():
    ts=datetime.datetime.now()          # get time step
    a= ts.strftime("%j%H%M%S")
    filename = "P-"+a+".jpg"   # give image file time-stamped name
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        time.sleep(1)
        camera.capture(filename, 'raw')

def main():
    print ("Setup...")
    setup()
    print ("Setup complete... now starting loop.") 
    ## Now begin main loop. Keep doing this forever
    # Listen on port 2947 (gpsd) of localhost
    session = gps.gps("localhost", "2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)


    latitude=0.0
    longitude=0.0
    oldNorthing=0.0
    oldEasting=0.0
    currentEasting=0.0
    currentNorthing=0.0
    currentZone=0
    altitude=0.0
    speed=0.0
    time=0
    while True:
        try:
            report = session.next()
            # Wait for a 'TPV' report and display the current time
            # To see all report data, uncomment the line below
            # print report
            if report['class'] == 'TPV':
                if hasattr(report, 'time'):
                    time = report.time
                if hasattr(report, 'latitude'):
                    latitude = report.latitude
                if hasattr(report, 'longitude'):
                    longitude = report.longitude
                if hasattr(report,'altitude'):
                    altitude=report.altitude
                if hasattr(report,'speed'):
                    speed=report.speed
                currentNorthing, currentEasting, currentZone = latLongToUTM(latitude,longitude)
                currentDistance = distanceBetweenPoints(currentNorthing, oldNorthing, currentEasting, oldEasting)
                currentTime = datetime.datetime.now()
                diffTime = currentTime-oldTime

                if currentDistance > distanceForNewPhoto or diffTime.total_seconds()>minTime:
                    ### tell everyone to take the photo!
                    takePicture()
                    GPIO.output(OUTPUT_PIN, True)
                    ### now set oldpoints to the current location
                    oldNorthing = currentNorthing
                    oldEasting = currentEasting
                    oldZone = currentZone
                    writer.writerows([time,currentNorthing,currentEasting,currentZone,latitude, longitude, altitude,speed])
                    GPIO.output(4,False)

        except KeyError:
            pass
        except KeyboardInterrupt:
            quit()
        except StopIteration:
            session = None
            print "GPSD has terminated.."


if __name__ == "__main__":

    main()
