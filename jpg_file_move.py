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
import _photo_utilities

mode = 1

#for debugging
debuging = False
add_log = True
if add_log == True :
    log_file = 'jpg_file_rename.log'

base_dir_name = '../New_Photo/'

fullnames = _python_utilities.getFullnameListOfallFiles(base_dir_name)

save_base_dir_name = '../jpgfile/'

Img_N = 0
for fullname in fullnames[:]:
#fullname = fullnames[0]
    if fullname[-4:].lower() == ".jpg" or fullname[-5:].lower() == ".jpeg" :

        image_datetime = _photo_utilities.get_image_datetime_str(fullname).replace(':','')
        image_datetime = image_datetime.replace(' ','-')
        image_ModelID = _photo_utilities.get_image_Model_name(fullname).replace(' ','')
        image_Software = _photo_utilities.get_image_Software(fullname)
        
        try :
            print("Trying with {}...".format(fullname))
            if mode == 1 : 
                save_dir_name = '{0}{1}/{1}-{2}-{3}_{4}_{5}/'\
                      .format(save_base_dir_name, image_datetime[0:4], 
                              image_datetime[4:6], image_datetime[6:8], image_ModelID, image_Software)
            elif mode == 2 : 
                 save_dir_name = base_dir_name
            
            if not os.path.exists(save_dir_name):
                os.makedirs(save_dir_name)
                print ('*'*80)
                print ('{0} is created'.format(save_dir_name))
            else :
                print ('*'*80)
                print ('{0} is already exist'.format(save_dir_name))
                    
            os.rename(fullname, '{0}{1}_{2:08d}_{3}_py.jpg'.format(save_dir_name, image_datetime, Img_N, image_Software))
            #print(fullname, '{0}{1}_{2:08d}_{3}_py.jpg'.format(save_dir_name, image_datetime, Img_N, image_Software))
            _photo_utilities.write_log(log_file, '{3}:::{0}{1}_{2:08d}_py.jpg'.format(save_dir_name, image_datetime, Img_N, datetime.now()))
        
        except Exception as err :
            _photo_utilities.write_log(log_file, '{2} ::: error {0} with {1}'.format(err, Img_N, datetime.now()))
        Img_N += 1
        
#############################################################################
#############################################################################
#############################################################################
fullnames = _python_utilities.getFullnameListOfallsubDirs(base_dir_name)
print ("fullnames: {}".format(fullnames))

import shutil 

for fullname in fullnames[:] :

    # Check is empty..
    if len(os.listdir(fullname)) == 0 :
        shutil.rmtree(r"{}".format(fullname)) # Delete..
        print ("rmtree {}\n".format(fullname))
                                                   
