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

mode = 1

#for debugging
debuging = False
add_log = True
if add_log == True :
    log_file = 'raw_file_move.log'

base_dir_name = '../New_Photo/'

fullnames = photo_utilities.getFullnameListOfallFiles(base_dir_name)

save_base_dir_name = '../cr2file/'

image_Num = 0
for fullname in fullnames[:]:
#fullname = fullnames[0]
    if fullname[-4:].lower() == ".cr2" :
        image_Num += 1
        try :
            print("Trying with {}...".format(fullname))
            image_datetime = photo_utilities.get_image_datetime_str(fullname)
            image_ModelID = photo_utilities.get_image_Model_name(fullname).replace(' ','')
            #image_Num = photo_utilities.get_image_number(fullname)

            if mode == 1 : 
                save_dir_name = '{0}{1}/{1}-{2}-{3}_{4}/'\
                      .format(save_base_dir_name, image_datetime[0:4], 
                      image_datetime[4:6], image_datetime[6:8], image_ModelID)
            elif mode == 2 : 
                 save_dir_name = base_dir_name
            
            while not os.path.exists(save_dir_name):
                os.makedirs(save_dir_name)
                print ('*'*80)
                print ('{0} is created'.format(save_dir_name))
                    
            if not os.path.exists('{0}{1}_{2:08d}_py.cr2'.format(save_dir_name, image_datetime, image_Num)):
                os.rename(fullname, '{0}{1}_{2:08d}_py.cr2'.format(save_dir_name, image_datetime, image_Num))
                photo_utilities.write_log(log_file, "{3} is moved to {0}{1}_{2:08d}_py.cr2".format(save_dir_name, image_datetime, image_Num, fullname))
            else : 
                photo_utilities.write_log(log_file, "{3} is cannot moved because {0}{1}_{2:08d}_py.cr2 is already exist..".format(save_dir_name, image_datetime, image_Num, fullname))

        except Exception as err :
            photo_utilities.write_log(log_file, 
              "{2} ::: {0} error with {1}".format(err, fullname, datetime.now()))

        
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
                                                   