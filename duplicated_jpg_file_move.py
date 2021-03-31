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

#for debugging
debuging = False
add_log = True
if add_log == True :
    log_file = 'duplicated_jpg_file_move.log'

base_dir_name = '../../jpgfile/'

fullnames = photo_utilities.getFullnameListOfallFiles(base_dir_name)

save_base_dir_name = '../duplicated/'

image_Num = 0

for i in range(len(fullnames[:])):
    if i < len(fullnames[:]) \
        and fullnames[i][-4:].lower() == ".jpg" \
        and fullnames[i+1][-4:].lower() == ".jpg":
        print("Trying with {}".format(fullnames[i]))
       
        image_Num += 1
        if photo_utilities.checkDuplicated_jpg(fullnames[i], fullnames[i+1]) :
            print("{} is duplicated with {}".format(fullnames[i], fullnames[i+1]))
        
            try :    
                image_datetime = photo_utilities.get_image_datetime_str(fullnames[i]).replace(':','')
                image_datetime = image_datetime.replace(' ','-')
                image_ModelID = photo_utilities.get_image_Model_name(fullnames[i]).replace(' ','')
                image_Software = photo_utilities.get_image_Software(fullnames[i])
                save_dir_name = '{0}{1}/{1}-{2}-{3}_{4}_{5}/'\
                      .format(save_base_dir_name, image_datetime[0:4], 
                      image_datetime[4:6], image_datetime[6:8], image_ModelID, image_Software)
                    
                while not os.path.exists(save_dir_name):
                    os.makedirs(save_dir_name)
                    print ('*'*80)
                    print ('{0} is created'.format(save_dir_name))
                        
                if not os.path.exists('{0}{1}_{2:08d}_py.jpg'.\
                          format(save_dir_name, image_datetime, image_Num)):
                    os.rename(fullnames[i], '{0}{1}_{2:08d}_{3}_py.jpg'.\
                          format(save_dir_name, image_datetime, image_Num, image_Software))
                    
                    photo_utilities.write_log(log_file, 
                          "{3} is moved to {0}{1}_{2:08d}_py.jpg".\
                          format(save_dir_name, image_datetime, image_Num, fullnames[i]))
                else : 
                    photo_utilities.write_log(log_file, \
                          "{3} is cannot moved because {0}{1}_{2:08d}_py.jpg is already exist..".\
                          format(save_dir_name, image_datetime, image_Num, fullnames[i]))
    
            except Exception as err :
                photo_utilities.write_log(log_file, 
                  "{2} ::: {0} error with {1}".format(err, fullnames[i], datetime.now()))
                                                   