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
import exifread

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

def get_image_datetime_str(raw_name):
    f = open(raw_name, 'rb')
    tags = exifread.process_file(f)
    f.close()
    return tags['Image DateTime'].values

def write_log(log_file, log_str):
    with open(log_file, 'a') as log_f:
        log_f.write(log_str+'\n')
    return print (log_str)

base_dir_name = '../190504.WooUm_Island.5Dm2/'
base_dir_names = ['../2019-02-11.GS_graduation.5dm2/', '../2019-02-22.GS_goodbye.5dm2/',\
                  '../2019-02-27.Gunsan_tour.5dm2/', '../2019-02-28.Gunsan_tour.5dm2/']
base_dir_names = ['../Recuva1/']
for base_dir_name in base_dir_names[0:1] :

### Start process
    fullnames = sorted(glob(os.path.join(base_dir_name, '*.CR2')))
    
    j = 1000
    for fullname in fullnames :
        image_datetime = get_image_datetime_str(fullname).replace(':','')
        image_datetime = image_datetime.replace(' ','')
        
        try :
            print(fullname)
            save_dir_name = '../{0}-{1}-{2}/'\
                  .format(image_datetime[0:4], image_datetime[4:6], image_datetime[6:8])
            if not os.path.exists(save_dir_name):
                os.makedirs(save_dir_name)
                print ('*'*80)
                print ('{0} is created'.format(save_dir_name))
            else :
                print ('*'*80)
                print ('{0} is already exist'.format(save_dir_name))
                
            if not os.path.isfile('{0}{1}_py{2:4d}.cr2'.format(save_dir_name, image_datetime, j))
                os.rename(fullname, '{0}{1}_py{2:4d}.cr2'.format(save_dir_name, image_datetime, j))
            write_log(log_file, '{3}:::{0}{1}_py{2:4d}.cr2'.format(save_dir_name, image_datetime, j, datetime.now()))
        
        except Exception as err :
            write_log(log_file, '{2} ::: error {0} with {1}'.format(err, j, datetime.now()))
        j += 1
        print_working_time()
    print_working_time()
print_working_time()