__author__ = 'clipo'
import os
import commands
# GDAL Modules
from osgeo import gdal, gdal_array, osr

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

pathsToImages = ["./Image_1/","./Image_2/","./Image_3/","./Image_4"]
outputPath = "/output/"

disk = []
for path in pathsToImages:
    disk.append(sorted_ls(path))

fileCount = len(disk[0])
count=0

while count<fileCount:
    file_0 = pathsToImages[0]+disk[0][count]
    file_0_new = file_0+"_0.img"
    commandText='gdal_translate -of HFA -b 1 '+ str(file_0) + " " + str(file_0_new)
    output = commands.getstatusoutput(commandText)
    # Open file with GDAL
    data = gdal.Open( file_0_new, gdal.GA_ReadOnly )
    if (data == None):
        print "Failed to open", file_0_new, "for read."
        exit(1)
    # Get image size
    width = data.RasterXSize
    height = data.RasterYSize
    print "File:  ", file_0_new, " height: ", height, " width: ", width
    #new_lrx = width+10000
    #new_lry = -1*height+10000
    #commandText="python ./gdal_edit.py -a_ullr 1000 1000 " + str(new_lrx) + " " + str(new_lry) + " " + file_0_new
    #print commandText
    #output = commands.getstatusoutput(commandText)

    file_1 = pathsToImages[1]+disk[1][count]
    file_1_new = file_1+"_1.img"
    commandText='gdal_translate -of HFA -b 1 '+ str(file_1) + " " + str(file_1_new)
    output = commands.getstatusoutput(commandText)

    file_2 = pathsToImages[2]+disk[2][count]
    file_2_new = file_2 +"_2.img"
    commandText='gdal_translate -of HFA -b 1 ' + str(file_2) + " " + str(file_2_new)
    output = commands.getstatusoutput(commandText)

    file_3 = pathsToImages[3]+disk[3][count]
    file_3_new = file_3 +"_3.img"
    commandText='gdal_translate -of HFA -b 1 ' + str(file_3) + " " + str(file_3_new)
    output = commands.getstatusoutput(commandText)

    commandText = 'python ./gdal_merge.py -separate '+ file_0_new + " "+ file_1_new + " "+ file_2_new + " " + file_3_new + " -of HFA -o ./output/output_" +str(count)+".img"
    print commandText
    output = commands.getstatusoutput(commandText)
    #os.remove(file_0_new)
    #os.remove(file_1_new)
    #os.remove(file_2_new)
    #os.remove(file_3_new)
    print output
    count += 1
