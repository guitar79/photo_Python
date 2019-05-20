# -*- coding: utf-8 -*-
"""
Spyder Editor

ModuleNotFoundError: No module named 'cv2' 
conda install opencv

ModuleNotFoundError: No module named 'rawpy'
pip install rawpy

No module named 'pyexiv2'
pip install pyexiv2  (no supprt windows)

created by guitar79@naver.com

"""
from glob import glob
import os
import cv2
import numpy as np
from datetime import datetime
import rawpy
import exifread

#for debugging
debuging = True

#for checking time
cht_start_time = datetime.now()

def print_working_time():
    working_time = (datetime.now() - cht_start_time) #total days for downloading
    return print('working time ::: %s' % (working_time))

print_working_time()
# Read the images to be aligned
base_dr = '../190505.JC_fossil.pentom4/'
base_dr = '../190504.WooUm_Island.Spark/'
aligned_dr = 'aligned/'

if not os.path.exists(base_dr+aligned_dr):
    os.makedirs(base_dr+aligned_dr)
    print ('*'*80)
    print (base_dr+aligned_dr, 'is created')
else : 
    print (base_dr+aligned_dr, 'is already exist')

hdr_dr = 'hdr/'   
if not os.path.exists(base_dr+hdr_dr):
    os.makedirs(base_dr+hdr_dr)
    print ('*'*80)
    print (base_dr+hdr_dr, 'is created')
else : 
    print (base_dr+hdr_dr, 'is already exist')

CLAHE_dr = 'CLAHE/'
if not os.path.exists(base_dr+CLAHE_dr):
    os.makedirs(base_dr+CLAHE_dr)
    print ('*'*80)
    print (base_dr+CLAHE_dr, 'is created')
else : 
    print (base_dr+CLAHE_dr, 'is already exist')

### Start process
img_lists = sorted(glob(os.path.join(base_dr+hdr_dr, '*.jpg')))

def clahe_equalized(imgs):
    lab = cv2.cvtColor(imgs, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    lab_planes[0] = clahe.apply(lab_planes[0])
    lab = cv2.merge(lab_planes)
    bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return bgr

for i in img_lists :
    img = cv2.imread(i)
    img = clahe_equalized(img)
    cv2.imwrite("%s%s%s_CLAHE.JPG" % (base_dr, CLAHE_dr, i[-50:-4]), img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])   
    print("%s%s%s_CLAHE.JPG" % (base_dr, CLAHE_dr, i[-50:-4]))
    
    print_working_time()
print_working_time()