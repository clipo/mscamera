__author__ = 'carllipo'
import os
import commands
import re
from glob import glob

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))
    ##return list(sorted(glob(path+"*.JPG"),key=mtime))

pathsToImages = ["./Camera_1/","./Camera_2/","./Camera_3/"] ##, "./Camera_4/"]
outputPath = "/merged_images/"

disk = []
for path in pathsToImages:
    disk.append(sorted_ls(path))

fileCount = len(disk[0])
count=0

for p in pathsToImages:
    pdir = p+"*.img"
    for f in glob (pdir):
        os.remove (f)
    pdir = p+"*.aux.*"
    for f in glob (pdir):
        os.remove (f)
    pdir = p+"*.xml"
    for f in glob (pdir):
        os.remove (f)
    pdir = p+".DS_Store"
    for f in glob (pdir):
        os.remove (f)
    pdir = p+"*.img.aux.xml"
    for f in glob (pdir):
        os.remove (f)

while count<fileCount:
    print "now on: ", pathsToImages[0], disk[0][count]
    file_0 = pathsToImages[0]+disk[0][count]
    file_0_new = file_0+"_0.img"
    commandText='gdal_translate -of HFA -b 1 '+ str(file_0) + " " + str(file_0_new) + " " + "-a_ullr 0 0 640 480"
    output = commands.getstatusoutput(commandText)

    file_1 = pathsToImages[1]+disk[1][count]
    file_1_new = file_1+"_1.img"
    commandText='gdal_translate -of HFA -b 1 '+ str(file_1) + " " + str(file_1_new)+ " " + "-a_ullr -6 -49 634 441"
    output = commands.getstatusoutput(commandText)

    file_2 = pathsToImages[2]+disk[2][count]
    file_2_new = file_2 +"_2.img"
    commandText='gdal_translate -of HFA -b 1 ' + str(file_2) + " " + str(file_2_new)+ " " + "-a_ullr -7 0 633 480"  #11 29 629 451"
    ##print commandText
    output = commands.getstatusoutput(commandText)

   ## file_3 = pathsToImages[3]+disk[3][count]
   ## file_3_new = file_3 +"_3.img"
   ## commandText='gdal_translate -of HFA -b 1 ' + str(file_3) + " " + str(file_3_new) + " " + "-a_ullr 3 -2 643 478"  #11 29 629 451"
   ## ##print commandText
   ## output = commands.getstatusoutput(commandText)

    commandText = 'python ./gdal_merge.py -separate '+ file_0_new + " "+ file_1_new + " "+ file_2_new +  " -of HFA -o ./output/output_" +str(count)+".img" ##" "+ file_3_new +
    #print commandText
    output = commands.getstatusoutput(commandText)

    for p in pathsToImages:
        pdir = p+"*.img"
        for f in glob (pdir):
            os.unlink (f)
        pdir = p+"*.aux"
        for f in glob (pdir):
            os.unlink (f)
        pdir = p+"*.xml"
        for f in glob (pdir):
            os.unlink (f)
        pdir = p+".DS_Store"
        for f in glob (pdir):
            os.unlink (f)

    count += 1

    print "Done...!"

