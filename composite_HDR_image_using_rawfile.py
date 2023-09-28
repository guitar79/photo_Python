# -*- coding: utf-8 -*-
"""
Spyder Editor

ModuleNotFoundError: No module named 'cv2' 
conda install opencv

pip install piexif
pip install exifread

There are only just five functions.

load(filename) - Get exif data as dict.
dump(exif_dict) - Get exif as bytes.
insert(exif_bytes, filename) - Insert exif into JPEG, or WebP.
remove(filename) - Remove exif from JPEG, or WebP.
transplant(filename, filename) - Transplant exif from JPEG to JPEG.

created by guitar79@naver.com

"""
import os
import cv2
import _photo_utilities

add_log = True
if add_log == True :
    log_file = 'HDR_image_using_rawfile.log'

base_dir_name = '../HDR_input/'
save_base_dir_name = '../HDR_output/'

dirnames = _python_utilities.getFullnameListOfallsubDirs(base_dir_name)

for dirname in dirnames[:1] :
    dirname_el = dirname.split(base_dir_name)
    save_dir_name = "{}{}".format(save_base_dir_name, dirname_el[1])
    
    if not os.path.exists(save_dir_name):
        os.makedirs(save_dir_name)
        print ('*'*80)
        print ('{0} is created'.format(save_dir_name))
    else :
        print ('*'*80)
        print ('{0} is already exist'.format(save_dir_name))
    
    fullnames = _python_utilities.getFullnameListOfallFiles(dirname)
    #fullname = fullnames[0]
    composite_lists = [fullnames[x:x+3] for x in range(0, len(fullnames), 3)]
    
    for fullnames in composite_lists[:] :
        fullname_el = fullnames[0].split("/")
        
        images, times = _photo_utilities.readJpgPhoto_to_ImagesAndTimes(fullnames)
    
        # Align input images
        alignMTB = cv2.createAlignMTB()
        alignMTB.process(images, images)
        
        # Obtain Camera Response Function (CRF)
        calibrateDebevec = cv2.createCalibrateDebevec()
        responseDebevec = calibrateDebevec.process(images, times)
        
        # Merge images into an HDR linear image
        mergeDebevec = cv2.createMergeDebevec()
        hdrDebevec = mergeDebevec.process(images, times, responseDebevec)
        cv2.imwrite("{}/{}_hdrDebevec.jpg".format(save_dir_name, fullname_el[-1][:-4]), hdrDebevec,
                    [cv2.IMWRITE_JPEG_QUALITY, 100])
        print("{}/{}_hdrDebevec.jpg is created...".format(save_dir_name, fullname_el[-1][:-4]))
        
        # Tonemap using Drago's method to obtain 24-bit color image
        tonemapDrago = cv2.createTonemapDrago(1.0, 0.7)
        ldrDrago = tonemapDrago.process(hdrDebevec)
        ldrDrago = 3 * ldrDrago
        cv2.imwrite("{}/{}_ldrDrago.jpg".format(save_dir_name, fullname_el[-1][:-4]), ldrDrago * 255,
                    [cv2.IMWRITE_JPEG_QUALITY, 100])
        print("{}/{}_ldrDrago.jpg is created...".format(save_dir_name, fullname_el[-1][:-4]))
        
        # Tonemap using Reinhard's method to obtain 24-bit color image
        tonemapReinhard = cv2.createTonemapReinhard(1.5, 0,0,0)
        ldrReinhard = tonemapReinhard.process(hdrDebevec)
        cv2.imwrite("{}/{}_ldrReinhard.jpg".format(save_dir_name, fullname_el[-1][:-4]), ldrReinhard * 255,
                    [cv2.IMWRITE_JPEG_QUALITY, 100])
        print("{}/{}_ldrReinhard.jpg is created...".format(save_dir_name, fullname_el[-1][:-4]))
