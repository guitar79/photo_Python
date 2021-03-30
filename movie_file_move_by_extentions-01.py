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
from datetime import datetime
import photo_utilities

ext_name = "mp4"
#ext_name = "mov"
#ext_name = "3gp"

#for debugging
debuging = False
add_log = True
if add_log == True :
    log_file = "{}_file_rename.log".format(ext_name)

base_dir_name = "../New_Photo/"

fullnames = photo_utilities.getFullnameListOfallFiles(base_dir_name)

save_base_dir_name = "../../{}file/".format(ext_name)

Img_N = 0

for fullname in fullnames[:]:
#fullname = fullnames[0]
    if fullname[-4:].lower() == ".{}".format(ext_name) :
        mov_datetime = photo_utilities.get_mov_creation_date(fullname)
                
        try :
            print("Trying with {}...".format(fullname))
            
            save_dir_name = "{0}{1}/{1}-{2}-{3}/"\
                  .format(save_base_dir_name, mov_datetime[0:4], 
                          mov_datetime[4:6], mov_datetime[6:8])
            
            while not os.path.exists(save_dir_name):
                os.makedirs(save_dir_name)
                print ('*'*80)
                print ('{0} is created'.format(save_dir_name))
                    
            os.rename(fullname, '{0}{1}_{2:08d}_py.{3}'\
                      .format(save_dir_name, mov_datetime, Img_N, ext_name))
            #print(fullname, '{0}{1}_{2:08d}_py.jpg'.format(save_dir_name, image_datetime, Img_N))
            photo_utilities.write_log(log_file, \
                      '{4}:::{0}{1}_{2:08d}_py.{3}'.format(save_dir_name, \
                       mov_datetime, Img_N, ext_name, datetime.now()))
        
        except Exception as err :
            photo_utilities.write_log(log_file, 
                      '{2} ::: error {0} with {1}'.format(err, Img_N, datetime.now()))
        Img_N += 1
        
#############################################################################
#############################################################################
#############################################################################
fullnames = photo_utilities.getFullnameListOfallsubDirs(base_dir_name)
print ("fullnames: {}".format(fullnames))

import shutil 

for fullname in fullnames[:] :

    # Check is empty..
    if len(os.listdir(fullname)) == 0 :
        shutil.rmtree(r"{}".format(fullname)) # Delete..
        print ("rmtree {}\n".format(fullname))
                                                   