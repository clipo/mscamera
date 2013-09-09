__author__ = 'carllipo'
import struct

# script to merge several individual Tiffs (bands) into one multiband GeoTiff
# and potentially do calculations like NDVI, albedo, etc...

# import the GDAL and numpy libraries
from osgeo import gdal
from numpy import *
import numpy
# ***************************************************************
# ok lets load in the first 4 bands of Landsat imagery into their own numpy arrays
# the numpy arrays are named band1, band2, etc.
# I'm using the Boulder images that I provided you, but -
# alternatively you could change these file names to be Landast imagery that you downloaded
gdal.AllRegister()
g = gdal.Open('photo.jpg',gdal.GA_ReadOnly)

b1 = g.GetRasterBand(1)
print 'Band Type=',gdal.GetDataTypeName(b1.DataType)
#band1 = b1.ReadAsArray(1, 0, g.RasterXSize, g.RasterYSize)
band1 = b1.ReadAsArray() ## blue band
b2 = g.GetRasterBand(2)
print 'Band Type=',gdal.GetDataTypeName(b2.DataType)
#band2 = b2.ReadAsArray(2, 0, g.RasterXSize, g.RasterYSize)
band2 = b2.ReadAsArray() ## green band
b3 = g.GetRasterBand(3)
print 'Band Type=',gdal.GetDataTypeName(b3.DataType)

#band3 = b3.ReadAsArray(3, 0, g.RasterXSize, g.RasterYSize)
band3 = b3.ReadAsArray() ## NIR band

rows = g.RasterYSize
cols = g.RasterXSize

print "42 x 94: ", band3[42, 94]
print "100 x 100", band3[100,100]
# ****************************************************************

# Lets do an NDVI calc
# NDVI = (nearInfrared - Red) / (nearInfrared + Red)

band3 = array(band3, dtype = float)  # change the array data type from integer to float to allow decimals
band1 = array(band2, dtype = float)

var1 = subtract(band3, band2)+1
var2 = add( band3, band2)+1

ndvi = divide(var1,var2)

# ****************************************************************

# these variables will get information about the input Tiff so we can
# write out our new Tiff into the correct geographic space and with correct row/column dimensions

#geo = g.GetGeoTransform()  # get the datum
#proj = g.GetProjection()   # get the projection
#shape = band1.shape        # get the image dimensions - format (row, col)

# ****************************************************************

# here we write out the new image, only one band to write out in this case

driver = gdal.GetDriverByName('GTiff')

dst_ds = driver.Create('ndvi-new.tif', g.RasterXSize, g.RasterYSize, 1, gdal.GDT_Float32)


#dst_ds.SetGeoTransform( geo ) # set the datum
#dst_ds.SetProjection( proj )  # set the projection


dst_ds.GetRasterBand(1).WriteArray( ndvi )  # write numpy array band1 as the first band of the multiTiff - this is the blue band
stat = dst_ds.GetRasterBand(1).GetStatistics(1,1)  # get the band statistics (min, max, mean, standard deviation)
dst_ds.GetRasterBand(1).SetStatistics(stat[0], stat[1], stat[2], stat[3]) # set the stats we just got to the band


# that's it, close Python and load your NDVI image into QGIS !!