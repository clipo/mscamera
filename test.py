__author__ = 'clipo'
import gdal
from gdalconst import *
import sys
import time
import logging
import os
import sqlite3 as sqlite
from datetime import date
from datetime import datetime
import numpy as np
from scipy import stats
from lmfit import minimize, Parameters, Parameter, report_errors
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl import Workbook
from scipy import *
#from scipy.optimize import leastsq
#import scikits.datasmooth as ds
#from lmfit import minimize, Parameters, Parameter, report_errors
import easygui
# here's a comment
filename = easygui.fileopenbox(msg='SQLLite Filename', title='select file', filetypes=['*.jpg'])
if filename is None:
    sys.exit(1)

print "opening... ", filename

gdal.AllRegister()

ds = gdal.Open(filename, GA_ReadOnly)

if ds is None:
    print 'Could not open ' + filename
    sys.exit(1)

# start timing
startTime = time.time()
# coordinates to get pixel values for
xValues = [500.0, 501.0, 503.0]
yValues = [500.0, 502.0, 504.0]

# get image size
rows = ds.RasterYSize
cols = ds.RasterXSize
bands = ds.RasterCount

# get georeference info
transform = ds.GetGeoTransform()
xOrigin = transform[0]
yOrigin = transform[3]
pixelWidth = transform[1]
pixelHeight = transform[5]
# loop through the coordinates

for i in range(3):
    # get x,y
    x = xValues[i]
    y = yValues[i]
    # compute pixel offset
    xOffset = int((x - xOrigin) / pixelWidth)
    yOffset = int((y - yOrigin) / pixelHeight)
    # create a string to print out
    s = str(x) + ' ' + str(y) + ' ' + str(xOffset) + ' ' + str(yOffset) + ' '
    # loop through the bands
    for j in range(bands):
        band = ds.GetRasterBand(j+1) # 1-based index
        # read data and add the value to the string
        data = band.ReadAsArray(xOffset, yOffset, 1, 1)
        value = data[0,0]
        s = s + str(value) + ' '
        # print out the data string
    print s
# figure out how long the script took to run
endTime = time.time()
print 'The script took ' + str(endTime - startTime) + ' seconds'
