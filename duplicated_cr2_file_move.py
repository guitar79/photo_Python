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

base_dir_name = '../../cr2file/2022/'

fullnames = _photo_utilities.getFullnameListOfallFiles(base_dir_name)

save_base_dir_name = '../duplicated/'

image_Num = 0

for i in range(len(fullnames[:])):
    if i < len(fullnames[:]) \
        and fullnames[i][-4:].lower() == ".cr2" \
        and fullnames[i+1][-4:].lower() == ".cr2":
        print('#'*40,
            "\n{2:.01f}%  ({0}/{1}) {3}".format(image_Num, len(fullnames), (image_Num/len(fullnames))*100, os.path.basename(__file__)))
        print ("Starting...   fullname: {}".format(fullnames[i]))
       
        image_Num += 1
        if _photo_utilities.checkDuplicated_cr2(fullnames[i], fullnames[i+1]) :
            print('*'*60)
            print("{} is duplicated with {}".format(fullnames[i], fullnames[i+1]))
            
            try :    
                image_datetime = _photo_utilities.get_image_datetime_str(fullnames[i]).replace(':','')
                image_datetime = image_datetime.replace(' ','-')
                image_ModelID = _photo_utilities.get_image_Model_name(fullnames[i]).replace(' ','')
                image_Software = _photo_utilities.get_image_Software(fullnames[i])
                save_dir_name = '{0}{1}/{1}-{2}-{3}_{4}_{5}/'\
                      .format(save_base_dir_name, image_datetime[0:4], 
                      image_datetime[4:6], image_datetime[6:8], image_ModelID, image_Software)
                    
                while not os.path.exists(save_dir_name):
                    os.makedirs(save_dir_name)
                    print ('*'*80)
                    print ('{0} is created'.format(save_dir_name))
                        
                if not os.path.exists('{0}{1}_{2:08d}_py.jpg'.\
                          format(save_dir_name, image_datetime, image_Num)):
                    shutil.move(r"{}".format(fullnames[i]), r"{0}{1}_{2:08d}_{3}_py.cr2".\
                          format(save_dir_name, image_datetime, image_Num, image_Software))
                    #os.rename(fullnames[i], '{0}{1}_{2:08d}_{3}_py.jpg'.\
                    #      format(save_dir_name, image_datetime, image_Num, image_Software))
                    
                    _photo_utilities.write_log(log_file, 
                          "{3} is moved to {0}{1}_{2:08d}_py.jpg".\
                          format(save_dir_name, image_datetime, image_Num, fullnames[i]))
                else : 
                    _photo_utilities.write_log(log_file, \
                          "{3} is cannot moved because {0}{1}_{2:08d}_py.jpg is already exist..".\
                          format(save_dir_name, image_datetime, image_Num, fullnames[i]))
    
            except Exception as err :
                _photo_utilities.write_log(log_file, 
                  "{2} ::: {0} error with {1}".format(err, fullnames[i], datetime.now()))