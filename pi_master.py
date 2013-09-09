__author__ = 'carllipo'

import gps
import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
import datetime    # needed for timestamping outputfile
import math

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
    rcurv1 = equatorial_radius*(1-eccentricity^2)/((1-(eccentricity*math.sin(latRad))^2)^(1.5))
    rcurv2 = equatorial_radius/((1-(eccentricity*math.sin(latRad))^2)^(0.5))
    merid_arc = A0*latRad - B0*math.sin(2*latRad) + C0*math.sin(4*latRad) - D0*math.sin(6*latRad) + E0*math.sin(8*latRad)
    k1= merid_arc * scale_factor
    k2= rcurv1*math.sin(latRad)*math.cos(latRad)/2
    k3=((rcurv2*math.sin(latRad)*(math.cos(latRad))^3)/24)*(5-math.tan(latRad)^2+9*eccentricity2*(math.cos(latRad))^2+(4*(eccentricity2)^2)*math.cos(latRad)^4)*scale_factor
    k4=rcurv2*math.cos(latRad)*scale_factor
    k5=math.cos(latRad)^3*(rcurv2/6)*(1-math.tan(latRad)^2+e1sq*math.cos(latRad)^2)*scale_factor
    a61=deltaLong*deltaLong*deltaLong*deltaLong*deltaLong*deltaLong*rcurv2*math.sin(latRad)*((math.cos(latRad))^5)/720
    a62=61-58*(math.tan(latRad)^2)+(math.tan(latRad)^4)+270*e1sq*(math.cos(latRad)^2)-330*e1sq*math.sin(latRad)^2
    a6=a61*a62*scale_factor
    raw_northing=(k1+k2*deltaLong*deltaLong+k3*deltaLong*deltaLong*deltaLong*deltaLong)
    northing = raw_northing
    if raw_northing < 0:
        northing = raw_northing + 10000000
    easting = 500000+(k4*deltaLong+k5*deltaLong*deltaLong*deltaLong)
    zone = longZone
    return northing, easting, zone

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
    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print "GPSD has terminated"
