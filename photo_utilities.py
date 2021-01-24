# -*- coding: utf-8 -*-
"""
Spyder Editor

ModuleNotFoundError: No module named 'cv2' 
conda install opencv

pip install piexif

ModuleNotFoundError: No module named 'exifread'
pip install exifread

There are only just five functions.

load(filename) - Get exif data as dict.
dump(exif_dict) - Get exif as bytes.
insert(exif_bytes, filename) - Insert exif into JPEG, or WebP.
remove(filename) - Remove exif from JPEG, or WebP.
transplant(filename, filename) - Transplant exif from JPEG to JPEG.

created by guitar79@naver.com

"""

#for debugging
debuging = False
add_log = True
if add_log == True :
    log_file = 'python_log.txt'

def getFullnameListOfallFiles(dirName):
    ##############################################3
    import os
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = sorted(os.listdir(dirName))
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getFullnameListOfallFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles


def getFullnameListOfallsubDirs1(dirName):
    ##############################################3
    import os
    allFiles = list()
    for file in sorted(os.listdir(dirName)):
        d = os.path.join(dirName, file)
        allFiles.append(d)
        if os.path.isdir(d):
            allFiles.extend(getFullnameListOfallsubDirs1(d))

    return allFiles

def getFullnameListOfallsubDirs(dirName):
    ##############################################3
    import os
    allFiles = list()
    for it in os.scandir(dirName):
        if it.is_dir():
            allFiles.append(it.path)
            allFiles.extend(getFullnameListOfallsubDirs(it))

    return allFiles
                      
#for checking time
def print_working_time(cht_start_time):
    from datetime import datetime
    working_time = (datetime.now() - cht_start_time) #total days for downloading
    return print('working time ::: %s' % (working_time))

def get_image_datetime_str(fullname):
    import exifread
    f = open(fullname, 'rb')
    tags = exifread.process_file(f)
    f.close()
    if 'EXIF DateTimeOriginal' in tags :
        image_datetime = tags['EXIF DateTimeOriginal'].values.replace(':','')
        image_datetime = image_datetime.replace(' ','-')
    elif 'Image DateTime' in tags :
        image_datetime = tags['Image DateTime'].values.replace(':','')
        image_datetime = image_datetime.replace(' ','-')
    else : 
        image_datetime = '00000000-000000'
    return image_datetime


def get_image_Model_name(fullname):
    import exifread
    f = open(fullname, 'rb')
    tags = exifread.process_file(f)
    f.close()
    if 'Image Make' in tags and 'Image Model' in tags : 
        image_ModelID = tags['Image Make'].printable.replace(' ','')\
            +tags['Image Model'].printable.replace(' ','')
                
    elif 'MakerNote ModelID' in tags : 
        image_ModelID = tags['MakerNote ModelID'].printable.replace(' ','')
        
    else : 
        image_ModelID = 'NoModel'
    image_ModelID = image_ModelID.replace('CanonCanon','Canon')
    image_ModelID = image_ModelID.replace('/','')
    image_ModelID = image_ModelID.replace('\\','')
    image_ModelID = image_ModelID.replace('EASTMANKODAKCOMPANYKODAKDC3400ZOOMDIGITALCAMERA', 'KODAK-DC3400')
    image_ModelID = image_ModelID.replace('OLYMPUSOPTICALCO.,LTDC3100Z,C3020Z', 'OLYMPUS-C3100Z')
    image_ModelID = image_ModelID.replace('OLYMPUSCORPORATIONC-5000Z', 'OLYMPUS-C5000Z')
    image_ModelID = image_ModelID.replace('CanonEOSKissDigitalN', 'CANON-EOS-KissN')
    image_ModelID = image_ModelID.replace('CanonEOS350DDIGITAL', 'CANON-EOS-350D')
    image_ModelID = image_ModelID.replace('CanonEOS400DDIGITAL', 'CANON-EOS-400D')
    image_ModelID = image_ModelID.replace('CanonEOS', 'CANON-EOS')
    image_ModelID = image_ModelID.replace('EOS5DMarkII', 'EOS-5DMarkII')
    image_ModelID = image_ModelID.replace('EOS650D', 'EOS-650D')
    image_ModelID = image_ModelID.replace('CanonPowerShotS230', 'CANON-S230')
    image_ModelID = image_ModelID.replace('CanonPowerShotG', 'CANON-G')
    image_ModelID = image_ModelID.replace('CanonDIGITALIXUS50', 'CANON-IXUS50')
    image_ModelID = image_ModelID.replace('CanonIXYDIGITAL800IS', 'CANON-IXY800IS')
    image_ModelID = image_ModelID.replace('SONYDCR-TRV17', 'SONY-DCR-TRV17')
    image_ModelID = image_ModelID.replace('SONYCYBERSHOT', 'SONY-CYBERSHOT')
    image_ModelID = image_ModelID.replace('SONYDSC', 'SONY-DSC')
    image_ModelID = image_ModelID.replace('SONYNEX-5N', 'SONY-NEX-5N')
    image_ModelID = image_ModelID.replace('SONYILCE', 'SONY-ILCE')
    image_ModelID = image_ModelID.replace('NIKONE', 'NIKON-E')
    image_ModelID = image_ModelID.replace('NIKONCORPORATIONNIKOND', 'NIKON-D')
    image_ModelID = image_ModelID.replace('SAMSUNGELECTRONICSVM-C630', 'SAMSUNG-SVM-C630')
    image_ModelID = image_ModelID.replace('SAMSUNGTECHWINCO.,LTDDigimaxV5KenoxV5', 'SAMSUNG-DigimaxV5')
    image_ModelID = image_ModelID.replace('SamsungTechwinDigimax530KENOXD530', 'SAMSUNG-Digimax530')
    image_ModelID = image_ModelID.replace('SAMSUNGES95', 'SAMSUNG-ES95')
    image_ModelID = image_ModelID.replace('SAMSUNGWB150WB150FWB,...]', 'SAMSUNG-WB150')
    image_ModelID = image_ModelID.replace('SAMSUNGSM', 'SAMSUNG-SM')
    image_ModelID = image_ModelID.replace('SAMSUNGEK', 'SAMSUNG-EK')
    image_ModelID = image_ModelID.replace('SAMSUNGSH', 'SAMSUNG-SH')
    image_ModelID = image_ModelID.replace('SAMSUNGSSV', 'SAMSUNG-SHV')
    image_ModelID = image_ModelID.replace('SamsungTechwinDigimaxV4', 'SAMSUNG-DigimaxV4')
    image_ModelID = image_ModelID.replace('LGElectronicsLG', 'LG')
    image_ModelID = image_ModelID.replace('PanasonicDMC-LX2', 'PANASONIC-DMC-LX2')
    image_ModelID = image_ModelID.replace('ApplePhone', 'APPLE-iPhone')
    image_ModelID = image_ModelID.replace('Applei', 'APPLE-i')
    image_ModelID = image_ModelID.replace('DJIFC1102', 'DJI-FC1102')
    image_ModelID = image_ModelID.replace('DJIFC6310', 'DJI-FC6310')
    image_ModelID = image_ModelID.replace('XIAOYIYDXJ1', 'XIAOYI-YDXJ1')
    image_ModelID = image_ModelID.replace('PANTECH', 'PANTECH-')
        
    return image_ModelID

def get_mov_creation_date(fullname):
    from hachoir.parser import createParser
    from hachoir.metadata import extractMetadata

    parser = createParser(fullname)
    metadata = extractMetadata(parser)
    return metadata.get('creation_date').strftime("%Y%m%d-%H%M%S")



def get_image_Software(fullname):
    import exifread
    f = open(fullname, 'rb')
    tags = exifread.process_file(f)
    f.close()
    if 'Image Software' in tags : 
        image_Software = tags['Image Software'].printable.replace(' ','')
    else : 
        image_Software = 'NoSW'
    image_Software = image_Software.replace('DigitalPhotoProfessional', 'DPP')
    if 'ACDSystems' in image_Software : 
        image_Software = 'ACDSystems'
    return image_Software

def write_log(log_file, log_str):
    import os
    with open(log_file, 'a') as log_f:
        log_f.write("{}, {}\n".format(os.path.basename(__file__), log_str))
    return print ("{}, {}\n".format(os.path.basename(__file__), log_str))


def bgr2rgb(bgr_image):
    import numpy as np
    RGB = np.zeros((bgr_image.shape[0], bgr_image.shape[1], 3), dtype=np.uint8)
    RGB[:,:,0] = bgr_image[:,:,2]
    RGB[:,:,1] = bgr_image[:,:,1]
    RGB[:,:,2] = bgr_image[:,:,0]
    return RGB

def clahe_equalized(imgs):
    import cv2
    lab = cv2.cvtColor(imgs, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    lab_planes[0] = clahe.apply(lab_planes[0])
    lab = cv2.merge(lab_planes)
    bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return bgr


def readJpgPhoto_to_ImagesAndTimes(fullnames):
    # source : https://learnopencv.com/high-dynamic-range-hdr-imaging-using-opencv-cpp-python/
    import exifread
    import numpy as np
    #import rawpy
    import cv2
   
    images = []
    times = []
    for fullname in fullnames:
        #im = rawpy.imread(fullname)
        im = cv2.imread(fullname)
        images.append(im)
    
        f = open(fullname, 'rb')
        tags = exifread.process_file(f)
        f.close()
        if 'EXIF ExposureTime' in tags :
            image_ExposureTime = tags['EXIF ExposureTime'].values
        times.append(image_ExposureTime)
    #images = np.array(images, dtype=np.uint8)
    times = np.array(times, dtype=np.float32)
    return images, times
