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
debuging = False

#for checking time
cht_start_time = datetime.now()

def print_working_time():
    working_time = (datetime.now() - cht_start_time) #total days for downloading
    return print('working time ::: %s' % (working_time))

print_working_time()
# Read the images to be aligned
base_dr = '../190505.JC_fossil.pentom4/'
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
    
    
def ecc_3_align_raws(raw_name1, raw_name2, raw_name3):
    #https://www.learnopencv.com/image-alignment-ecc-in-opencv-c-python/ 
    # Convert images to grayscale
    with rawpy.imread(raw_name1) as raw:
        im1 = raw.postprocess()
    with rawpy.imread(raw_name2) as raw:
        im2 = raw.postprocess()
    with rawpy.imread(raw_name3) as raw:
        im3 = raw.postprocess()
    
    im1_gray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
    im2_gray = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
    im3_gray = cv2.cvtColor(im3,cv2.COLOR_BGR2GRAY)
    
    # Find size of image1
    sz = im1.shape
     
    # Define the motion model
    #warp_mode = cv2.MOTION_TRANSLATION   #
    warp_mode = cv2.MOTION_EUCLIDEAN
    #warp_mode = cv2.MOTION_HOMOGRAPHY
     
    # Define 2x3 or 3x3 matrices and initialize the matrix to identity
    if debuging == True : 
        print("debugging::: # Define 2x3 or 3x3 matrices and initialize the matrix to identity")
    if warp_mode == cv2.MOTION_HOMOGRAPHY :
        warp_matrix12 = np.eye(3, 3, dtype=np.float32)
        warp_matrix13 = np.eye(3, 3, dtype=np.float32)
    else :
        warp_matrix12 = np.eye(2, 3, dtype=np.float32)
        warp_matrix13 = np.eye(2, 3, dtype=np.float32)
    
    # Specify the number of iterations.
    number_of_iterations = 1000;    #original value 5000
     
    # Specify the threshold of the increment
    # in the correlation coefficient between two iterations
    termination_eps = 1e-5;     #original value 1e-10
     
    # Define termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations, termination_eps)
     
    # Run the ECC algorithm. The results are stored in warp_matrix.
    if debuging == True : 
        print("debugging::: # Run the ECC algorithm. The results are stored in warp_matrix.")
    (cc, warp_matrix12) = cv2.findTransformECC (im1_gray,im2_gray,warp_matrix12, warp_mode, criteria)
    (cc, warp_matrix13) = cv2.findTransformECC (im1_gray,im3_gray,warp_matrix13, warp_mode, criteria)
    
    # Align images using warp_matrix.
    if debuging == True : 
        print("debugging::: # Align images using warp_matrix.")
    if warp_mode == cv2.MOTION_HOMOGRAPHY :
        # Use warpPerspective for Homography 
        im2_aligned = cv2.warpPerspective (im2, warp_matrix12, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        im3_aligned = cv2.warpPerspective (im3, warp_matrix13, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    else :
        # Use warpAffine for Translation, Euclidean and Affine
        im2_aligned = cv2.warpAffine(im2, warp_matrix12, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);
        im3_aligned = cv2.warpAffine(im3, warp_matrix13, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);
    return im1, im2_aligned, im3_aligned

def get_exp_time_raw(raw_name1, raw_name2, raw_name3):
    # Open image file for reading (binary mode)
     # Open image file for reading (binary mode)
    f1 = open(raw_name1, 'rb')
    f2 = open(raw_name2, 'rb')
    f3 = open(raw_name3, 'rb')
    tags1 = exifread.process_file(f1)
    tags2 = exifread.process_file(f2)
    tags3 = exifread.process_file(f3)
    
    exp_times = np.array([ tags1['EXIF ExposureTime'].values[0].num/tags1['EXIF ExposureTime'].values[0].den, \
                        tags2['EXIF ExposureTime'].values[0].num/tags2['EXIF ExposureTime'].values[0].den , \
                        tags3['EXIF ExposureTime'].values[0].num/tags3['EXIF ExposureTime'].values[0].den  ], dtype=np.float32)
    return exp_times

def bgr2rgb(bgr_image):
    RGB = np.zeros((bgr_image.shape[0], bgr_image.shape[1], 3), dtype=np.uint8)
    RGB[:,:,0] = bgr_image[:,:,2]
    RGB[:,:,1] = bgr_image[:,:,1]
    RGB[:,:,2] = bgr_image[:,:,0]
    return RGB

### Start process
img_lists = sorted(glob(os.path.join(base_dr, '*.dng')))

img_set_list = []
for i in range(0, len(img_lists), 3) :
    img_set_list.append([img_lists[i], img_lists[i+1], img_lists[i+2]])
    
for i in img_set_list :
    im1 =  cv2.imread(i[0])
    im2 =  cv2.imread(i[1])
    im3 =  cv2.imread(i[2])
    
    im1_aligned, im2_aligned, im3_aligned = ecc_3_align_raws(i[0], i[1], i[2])
    
    # Convert COVER_GBR2RGB
    if debuging == True : 
        print("debugging::: # Convert COVER_GBR2RGB")
    im1_aligned = bgr2rgb(im1_aligned)
    im2_aligned = bgr2rgb(im2_aligned)
    im3_aligned = bgr2rgb(im3_aligned)
    
    # Show aligned image
    if debuging == True : 
        print("debugging::: # Show final results")
    #cv2.imshow("%s%s%s_aligned.JPG" % (base_dr, save_dr, i[0][-12:-4]), im1)
    #cv2.imshow("%s%s%s_aligned.JPG" % (base_dr, save_dr, i[1][-12:-4]), im2_aligned)
    #cv2.imshow("%s%s%s_aligned.JPG" % (base_dr, save_dr, i[2][-12:-4]), im3_aligned)
    
    #save aligned image
    if debuging == True : 
        print("debugging::: # Save final results")
    
    cv2.imwrite("%s%s%s_aligned.JPG" % (base_dr, aligned_dr, i[0][-12:-4]), im1_aligned, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    print("%s%s%s_aligned.JPG is created"%(base_dr, aligned_dr, i[0][-21:-4]))
    
    cv2.imwrite("%s%s%s_aligned.JPG" % (base_dr, aligned_dr, i[1][-12:-4]), im2_aligned, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    print("%s%s%s_aligned.JPG is created" % (base_dr, aligned_dr, i[1][-21:-4]))
    
    cv2.imwrite("%s%s%s_aligned.JPG" % (base_dr, aligned_dr, i[2][-12:-4]), im3_aligned, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    print("%s%s%s_aligned.JPG is created" % (base_dr, aligned_dr, i[2][-21:-4]))
    
    # Start making HDR image using aligned images
    if debuging == True : 
        print("debugging::: # Start making HDR image using aligned images")
    exp_times = get_exp_time_raw(i[0], i[1], i[2])
    images = [im1_aligned, im2_aligned, im3_aligned]
    
    # Align input images
    #if debuging == True : 
    #    print("debugging::: # Align input images")
    #alignMTB = cv2.createAlignMTB()
    #alignMTB.process(images, images)
    
    # Obtain Camera Response Function (CRF)
    if debuging == True : 
        print("debugging::: # Obtain Camera Response Function (CRF)")
    calibrateDebevec = cv2.createCalibrateDebevec()
    responseDebevec = calibrateDebevec.process(images, exp_times)
    
    # Merge images into an HDR linear image
    if debuging == True : 
        print("debugging::: # Merge images into an HDR linear image")
    mergeDebevec = cv2.createMergeDebevec()
    hdrDebevec = mergeDebevec.process(images, exp_times, responseDebevec)
    
    # Tonemap HDR image
    if debuging == True : 
        print("debugging::: # Tonemap HDR image")
    tonemap1 = cv2.createTonemap(gamma=2.2)
    res_debevec = tonemap1.process(hdrDebevec.copy())
    
    # Exposure fusion using Mertens
    if debuging == True : 
        print("debugging::: # Exposure fusion using Mertens")
    merge_mertens = cv2.createMergeMertens()
    res_mertens = merge_mertens.process(images)
    
    # Convert datatype to 8-bit and save
    if debuging == True : 
        print("debugging::: # Convert datatype to 8-bit and save")
    res_mertens_8bit = np.clip(res_mertens*255, 0, 255).astype('uint8')
    
    # Save HDR image.
    cv2.imwrite("%s%s%s_%s_%s_HDR_Mertenes_Fusion.JPG"%(base_dr, hdr_dr, i[0][-12:-4], i[1][-12:-4], i[2][-12:-4]), res_mertens_8bit, [int(cv2.IMWRITE_JPEG_QUALITY), 100]) 
    print("%s%s%s_%s_%s_HDR_Mertenes_Fusion.JPG"%(base_dr, hdr_dr, i[0][-12:-4], i[1][-12:-4], i[2][-12:-4]))
    print_working_time()
    
print_working_time()