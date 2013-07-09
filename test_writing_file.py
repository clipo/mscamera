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
import os, sys, gdal, utils
from gdalconst import *

filename = easygui.fileopenbox(msg='SQLLite Filename', title='select file', filetypes=['*.jpg','*.img'])
if filename is None:
    sys.exit(1)

print "opening... ", filename

# register all of the GDAL drivers
gdal.AllRegister()
# open the image
inDs = gdal.Open(filename, GA_ReadOnly)
if inDs is None:
  print 'Could not open ', filename
  sys.exit(1)

# get image size
rows = inDs.RasterYSize
cols = inDs.RasterXSize
bands = inDs.RasterCount

# get the bands and block sizes
inBand2 = inDs.GetRasterBand(2)
inBand3 = inDs.GetRasterBand(3)
blockSizes = utils.GetBlockSize(inBand2)
xBlockSize = blockSizes[0]
yBlockSize = blockSizes[1]
print yBlockSize, xBlockSize

# create the output image

fileout= easygui.filesavebox(msg="Save file as...", title="Save", default="Output.img")
driver = inDs.GetDriver()
outDs = driver.Create(fileout, cols, rows, 1, GDT_Float32)
if outDs is None:
  print 'Could not create ', fileout
  sys.exit(1)
outBand = outDs.GetRasterBand(1)

# loop through the rows
for i in range(0, rows, yBlockSize):
  if i + yBlockSize < rows:
    numRows = yBlockSize
  else:
    numRows = rows - i

  # loop through the columns
  for j in range(0, cols, xBlockSize):
    if j + xBlockSize < cols:
      numCols = xBlockSize
    else:
      numCols = cols - j

    # read the data in
    data2 = inBand2.ReadAsArray(j, i, numCols, numRows).astype(np.float16)
    data3 = inBand3.ReadAsArray(j, i, numCols, numRows).astype(np.float16)

    # do the calculations
    mask = np.greater(data2 + data3, 0)
    ndvi = np.choose(mask, (-99, (data3 - data2) / (data3 + data2+ 0.00000000001)))

    # write the data
    outBand.WriteArray(ndvi, j, i)

# flush data to disk, set the NoData value and calculate stats
outBand.FlushCache()
outBand.SetNoDataValue(-99)
stats = outBand.GetStatistics(0, 1)

# georeference the image and set the projection
outDs.SetGeoTransform(inDs.GetGeoTransform())
outDs.SetProjection(inDs.GetProjection())

# build pyramids
gdal.SetConfigOption('HFA_USE_RRD', 'YES')
outDs.BuildOverviews(overviewlist=[2,4,8,16,32,64,128])

inDs = None
outDs = None