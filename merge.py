__author__ = 'carllipo'
import os
import commands


def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

pathsToImages = ["./Camera_1/","./Camera_2/","./Camera_3/"]
outputPath = "/output/"

disk = []
for path in pathsToImages:
    disk.append(sorted_ls(path))

fileCount = len(disk[0])
count=0

while count<fileCount:
    file_0 = pathsToImages[0]+disk[0][count]
    file_0_new = file_0+"_0.img"
    commandText='gdal_translate -of HFA -b 1 '+ str(file_0) + " " + str(file_0_new) + " " + "-a_ullr 0 0 640 480"
    output = commands.getstatusoutput(commandText)

    file_1 = pathsToImages[1]+disk[1][count]
    file_1_new = file_1+"_1.img"
    commandText='gdal_translate -of HFA -b 1 '+ str(file_1) + " " + str(file_1_new)+ " " + "-a_ullr -4 -12 636 468"
    output = commands.getstatusoutput(commandText)

    file_2 = pathsToImages[2]+disk[2][count]
    file_2_new = file_2 +"_2.img"
    commandText='gdal_translate -of HFA -b 1 ' + str(file_2) + " " + str(file_2_new)+ " " + "-a_ullr -11 29 629 509"  #11 29 629 451"
    output = commands.getstatusoutput(commandText)


    commandText = 'python ./gdal_merge.py -separate '+ file_0_new + " "+ file_1_new + " "+ file_2_new + " -of HFA -o ./output/output_" +str(count)+".img"
    output = commands.getstatusoutput(commandText)
    os.remove(file_0_new)
    os.remove(file_1_new)
    os.remove(file_2_new)
    print output
    count += 1