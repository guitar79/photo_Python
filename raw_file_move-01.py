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
from glob import glob
import os
from datetime import datetime
import photo_utility

mode = 1

#for debugging
debuging = False
add_log = True
if add_log == True :
    log_file = 'python_log.txt'

#for checking time
cht_start_time = datetime.now()
def print_working_time():
    working_time = (datetime.now() - cht_start_time) #total days for downloading
    return print('working time ::: %s' % (working_time))

def write_log(log_file, log_str):
    with open(log_file, 'a') as log_f:
        log_f.write(log_str+'\n')
    return print (log_str)

base_dir_names = []
year_dirs = [d for d in sorted(os.listdir('../'))\
             if os.path.isdir(os.path.join('../', d))]
year_dirs = ['etc']
for year_dir in year_dirs : 
    base_dir_names.append(base_dir_names.append('../{0}/'.format(year_dir)))
    month_dirs = [d for d in sorted(os.listdir('../{0}/'.format(year_dir))) \
                  if os.path.isdir(os.path.join('../{0}/'.format(year_dir), d))]
        
    for month_dir in month_dirs : 
        base_dir_names.append(base_dir_names.append('../{0}/{1}/'.format(year_dir, month_dir)))
        day_dirs = [d for d in sorted(os.listdir('../{0}/{1}/'.format(year_dir, month_dir))) \
                  if os.path.isdir(os.path.join('../{0}/{1}/'.format(year_dir, month_dir), d))]

        for day_dir in day_dirs : 
            base_dir_names.append('../{0}/{1}/{2}/'.format(year_dir, month_dir, day_dir))

for base_dir_name in base_dir_names : 
    if type(base_dir_name) == str :
        fullnames = sorted(glob(os.path.join(base_dir_name, '*.CR2')))
    
        ### Start process    
        j = 1000
        for fullname in fullnames :
            image_datetime = photo_utility.get_image_datetime_str(fullname)
            image_ModelID = photo_utility.get_image_Model_name(fullname)
            #image_Software = photo_utility.get_image_Software(fullname)
            
            try :
                print(fullname)
                if mode == 1 : 
                    save_dir_name = 'P:/cr2file/{0}/{0}-{1}-{2}_{3}/'\
                          .format(image_datetime[0:4], image_datetime[4:6], image_datetime[6:8], image_ModelID)
                elif mode == 2 : 
                     save_dir_name = base_dir_name
                
                if not os.path.exists(save_dir_name):
                    os.makedirs(save_dir_name)
                    print ('{0} is created'.format(save_dir_name))
                else :
                    print ('{0} is already exist'.format(save_dir_name))
                if not os.path.exists('{0}{1}_{2:4d}_py.cr2'.format(save_dir_name, image_datetime, j)) :                        
                    os.rename(fullname, '{0}{1}_{2:4d}_py.cr2'.format(save_dir_name, image_datetime, j))
                    print ('#'*60)
                    print(fullname, '{0}{1}_{2:4d}_py.cr2'.format(save_dir_name, image_datetime, j))
                    write_log(log_file, '{3}:::{0}{1}_{2:4d}_py.cr2 is moved...'\
                              .format(save_dir_name, image_datetime, j, datetime.now()))
            
            except Exception as err :
                write_log(log_file, '{2} ::: error {0} with {1}'.format(err, fullname, datetime.now()))
            j += 1
        else : 
            continue
        print_working_time()
    print_working_time()
print_working_time()