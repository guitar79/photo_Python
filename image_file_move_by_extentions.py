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
import shutil 
from datetime import datetime
import _photo_utilities

log_dir = "logs/"
log_file = "{}{}.log".format(log_dir, os.path.basename(__file__)[:-3])
err_log_file = "{}{}_err.log".format(log_dir, os.path.basename(__file__)[:-3])
print ("log_file: {}".format(log_file))
print ("err_log_file: {}".format(err_log_file))

ext_names = ["dng", "jpg", "png", "heic", "cr2"]
#ext_name = "dng"
#ext_name = "jpg"
#ext_name = "png"
#ext_name = "heic"
#ext_name = "cr2"
#ext_name = "dng"

base_dir_name = '../New_Photo/'

fullnames = _python_utilities.getFullnameListOfallFiles(base_dir_name)

for ext_name in ext_names :

    save_base_dir_name = "../../{}file/".format(ext_name)

    image_Num = 0
    for fullname in fullnames[:]:
    #fullname = fullnames[10]
        if fullname[-4:].lower() == ".{}".format(ext_name) :
            image_Num += 1
            print('#'*40,
                "\n{2:.01f}%  ({0}/{1}) {3}".format(image_Num, len(fullnames), (image_Num/len(fullnames))*100, os.path.basename(__file__)))
            print ("Starting...   fullname: {}".format(fullname))
            try :
                image_datetime = _photo_utilities.get_image_datetime_str(fullname)
                image_ModelID = _photo_utilities.get_image_Model_name(fullname).replace(' ','')
                image_Software = _photo_utilities.get_image_Software(fullname)

                save_dir_name = '{0}{1}/{1}-{2}-{3}_{4}_{5}/'\
                          .format(save_base_dir_name, image_datetime[0:4], \
                          image_datetime[4:6], image_datetime[6:8], image_ModelID, image_Software)

                while not os.path.exists(save_dir_name):
                    os.makedirs(save_dir_name)
                    print ("*"*80)
                    print ("{0} is created".format(save_dir_name))

                if not os.path.exists("{0}{1}_{2}_{3}_{4:08d}_py.{5}"\
                          .format(save_dir_name, image_datetime, \
                          image_ModelID, image_Software, image_Num, ext_name)):
                    os.rename(fullname,\
                          "{0}{1}_{2}_{3}_{4:08d}_py.{5}"\
                          .format(save_dir_name, image_datetime, \
                          image_ModelID, image_Software, image_Num, ext_name))
                    _photo_utilities.write_log(log_file, \
                          "{6} is moved to {0}{1}_{2}_{3}_{4:08d}_py.{5}"\
                          .format(save_dir_name, image_datetime, \
                          image_ModelID, image_Software, image_Num, ext_name, fullname))
                else :
                    _photo_utilities.write_log(log_file, \
                          "{6} cannot move to {0}{1}_{2}_{3}_{4:08d}_py.{5}"\
                          .format(save_dir_name, image_datetime, \
                          image_ModelID, image_Software, image_Num, ext_name, fullname))

            except Exception as err :
                _photo_utilities.write_log(log_file,
                  "{2} ::: {0} error with {1}".format(err, fullname, datetime.now()))

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
                                                   