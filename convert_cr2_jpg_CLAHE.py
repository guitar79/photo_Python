# -*- coding: utf-8 -*-
"""
Spyder Editor

ModuleNotFoundError: No module named 'cv2' 
conda install opencv

ModuleNotFoundError: No module named 'rawpy'
pip install rawpy

created by guitar79@naver.com

"""
from glob import glob
import os
from datetime import datetime
import rawpy
import cv2
import _photo_utilities

#for debugging
debuging = False
contrast_adjust = False
add_log = True
if add_log == True :
    log_file = 'python_log.txt'
    
def write_log(log_file, log_str):
    with open(log_file, 'a') as log_f:
        log_f.write(log_str+'\n')
    return print (log_str)
        
#for checking time
cht_start_time = datetime.now()
def print_working_time():
    working_time = (datetime.now() - cht_start_time) #total days for downloading
    return print('working time ::: %s' % (working_time))

save_dir_name = 'jpeg_CLAHE/'
base_dir_name = '../190504.WooUm_Island.5Dm2/'
base_dir_names = ['../190504.WooUm_Island.5Dm2/', '../190505.JC_fossil.5Dm2']

base_dir_names = []
list_dirs = os.listdir('../')
for list_dir in list_dirs : 
    base_dir_names.append('../{0}/'.format(list_dir))

for base_dir_name in base_dir_names[31:40] :

    if not os.path.exists('{0}{1}'.format(base_dir_name, save_dir_name)):
        os.makedirs('{0}{1}'.format(base_dir_name, save_dir_name))
        write_log(log_file, '{2}:::{0}{1} is created...'\
                  .format(base_dir_name, save_dir_name, datetime.now()))
    else : 
        write_log(log_file, '{2}:::{0}{1} is already exist...'\
                  .format(base_dir_name, save_dir_name, datetime.now()))
    
    ### Start process
    img_lists = sorted(glob(os.path.join(base_dir_name, '*.cr2')))
    
    for raw_name in img_lists:
        if not os.path.isfile('{0}{1}{2}.jpg'\
                      .format(base_dir_name, save_dir_name, raw_name[-25:-4])) \
            or not os.path.isfile('{0}{1}{2}_contrast_adjust.jpg'\
                      .format(base_dir_name, save_dir_name, raw_name[-25:-4])):
            try : 
                # Save final results
                if not os.path.isfile('{0}{1}{2}.jpg'\
                      .format(base_dir_name, save_dir_name, raw_name[-25:-4])) :
                    with rawpy.imread(raw_name) as raw:
                        img = raw.postprocess()
                        img = _photo_utilities.clahe_equalized(img)
                        img = _photo_utilities.bgr2rgb(img)
                    cv2.imwrite('{0}{1}{2}.jpg'\
                            .format(base_dir_name, save_dir_name, raw_name[-25:-4]), \
                            img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                    write_log(log_file, '{0} ::: {1}{2}{3}.jpg is created'\
                          .format(datetime.now(), base_dir_name, save_dir_name, raw_name[-25:-4]))
                if not os.path.isfile('{0}{1}{2}_contrast_adjust.jpg'\
                      .format(base_dir_name, save_dir_name, raw_name[-25:-4])) \
                    and contrast_adjust == True :
                    alpha = 1.95 # Simple contrast control
                    beta = 0    # Simple brightness control
                    new_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
                    cv2.imwrite('{0}{1}{2}_contrast_adjust.jpg'\
                            .format(base_dir_name, save_dir_name, raw_name[-25:-4]), \
                            new_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                    write_log(log_file, '{0} ::: {1}{2}{3}_ed.jpg is created'\
                          .format(datetime.now(), base_dir_name, save_dir_name, raw_name[-25:-4]))
            except Exception as err :
                write_log(log_file, '{0} ::: {1} with {2}'.format(datetime.now(), err, raw_name))
        else :
            write_log(log_file, '{0} ::: {1}{2}{3}.jpg is already exist'\
                      .format(datetime.now(), base_dir_name, save_dir_name, raw_name[-25:-4]))
    
        print_working_time()
    print_working_time()
print_working_time()