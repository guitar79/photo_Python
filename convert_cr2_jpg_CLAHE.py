# -*- coding: utf-8 -*-
"""
Spyder Editor

ModuleNotFoundError: No module named 'cv2' 
conda install opencv

created by guitar79@naver.com

"""
from glob import glob
import os
from datetime import datetime
import rawpy
import cv2
import numpy as np

#for debugging
debuging = False

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

def bgr2rgb(bgr_image):
    RGB = np.zeros((bgr_image.shape[0], bgr_image.shape[1], 3), dtype=np.uint8)
    RGB[:,:,0] = bgr_image[:,:,2]
    RGB[:,:,1] = bgr_image[:,:,1]
    RGB[:,:,2] = bgr_image[:,:,0]
    return RGB

def clahe_equalized(imgs):
    lab = cv2.cvtColor(imgs, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    lab_planes[0] = clahe.apply(lab_planes[0])
    lab = cv2.merge(lab_planes)
    bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return bgr
save_dir_name = 'jpeg_CLAHE/'
base_dir_name = '../190504.WooUm_Island.5Dm2/'
base_dir_names = ['../190504.WooUm_Island.5Dm2/', '../190505.JC_fossil.5Dm2']

base_dir_names = []
list_dir = os.listdir('../')
for i in list_dir : 
    base_dir_names.append('../'+i+'/')

for base_dir_name in base_dir_names :

    if not os.path.exists(base_dir_name+save_dir_name):
        os.makedirs(base_dir_name+save_dir_name)
        write_log(log_file, '{0} ::: {1}{2} is created'.format(datetime.now(), base_dir_name, save_dir_name))
    else : 
        write_log(log_file, '{0} ::: {1}{2} is already exist'.format(datetime.now(), base_dir_name, save_dir_name))
    
    ### Start process
    img_lists = sorted(glob(os.path.join(base_dir_name, '*.cr2')))
    
    for raw_name in img_lists:
        if not os.path.isfile('{0}{1}{2}.jpg'.format(base_dir_name, save_dir_name, raw_name[-25:-4])):
            try : 
                with rawpy.imread(raw_name) as raw:
                    img = raw.postprocess()
                img = clahe_equalized(img)
                img = bgr2rgb(img)
                
                # Save final results
                write_log(log_file, '{0} ::: {1}{2}{3}.jpg is created'.format(datetime.now(), base_dir_name, save_dir_name, raw_name[-25:-4]))
                cv2.imwrite('{0}{1}{2}.jpg'.format(base_dir_name, save_dir_name, raw_name[-25:-4]), img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            except Exception as err :
                write_log(log_file, '{0} ::: {1} with {2}'.format(datetime.now(), err, raw_name))
        else :
            write_log(log_file, '{0} ::: {1}{2}{3}.jpg is already exist'.format(datetime.now(), base_dir_name, save_dir_name, raw_name[-25:-4]))
    
        print_working_time()
    print_working_time()
print_working_time()