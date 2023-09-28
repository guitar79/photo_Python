# -*- coding: utf-8 -*-
"""
Spyder Editor

created by guitar79@naver.com

"""

import os
from datetime import datetime
from pathlib import Path
import shutil

import _photo_utilities
import _Python_utilities

#%%
#######################################################
# for log file
log_dir = "logs/"
log_file = "{}{}.log".format(log_dir, os.path.basename(__file__)[:-3])
err_log_file = "{}{}_err.log".format(log_dir, os.path.basename(__file__)[:-3])
print ("log_file: {}".format(log_file))
print ("err_log_file: {}".format(err_log_file))
if not os.path.exists('{0}'.format(log_dir)):
    os.makedirs('{0}'.format(log_dir))
#######################################################
#%%
BASEDIR = Path("/mnt/photo/")
NEW_files = BASEDIR / "NEW_files"
fullnames = _Python_utilities.getFullnameListOfallFiles(NEW_files)
print("len(fullnames):", len(fullnames))
print("fullnames:", fullnames)

ext_names_mov = [".mp4", ".mov", ".3gp", ".avi"]
ext_names_img = [".dng", ".jpg", ".heic", ".cr2", ".png"]

#%%
for fullname in fullnames[:]:
    fpath = Path(fullname)
    if fpath.suffix.lower() in ext_names_mov :
        try: 
            mov_datetime = _photo_utilities.get_mov_creation_date(str(fpath))
            print("mov_datetime :", mov_datetime)
            mov_dt = datetime.strptime(mov_datetime, '%Y%m%d-%H%M%S')
            # print("mov_dt :", mov_dt)
            # print(f"mov_dt.month : {mov_dt.month:02d}")
            # print(f"mov_dt.day : {mov_dt.day:02d}")
            SAVEDIR = (BASEDIR/ str(mov_dt.year) / f'{(mov_dt.month):02d}' / f'{(mov_dt.day):02d}')
            new_fname = f'{mov_datetime}_py{fpath.suffix}'
            new_fpath = SAVEDIR / new_fname
            print("new_fpath :", new_fpath)
            for i in range(3, -1, -1):
                if not new_fpath.parents[i].exists() :
                    os.mkdir(str(new_fpath.parents[i]))
                    #print(f'{str(new_fpath.parents[i])} is created...')
                else :
                    #print(f'{str(new_fpath.parents[i])} is exist...')
                    pass
            
            if not new_fpath.exists() :
                print(f'{str(new_fpath)} is not exist...')
                shutil.move(str(fpath), str(new_fpath))
            else : 
                print(f'{str(new_fpath)} is already exist...')
                new_date = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
                new_fpath = new_fpath.parents[0] / f'{new_fpath.stem}_{new_date}{new_fpath.suffix}'
            shutil.move(str(fpath), str(new_fpath))
        except Exception as err :
            print(err)
            

    if fpath.suffix.lower() in ext_names_img :
        try: 
            image_datetime = _photo_utilities.get_image_datetime_str(fullname)
            image_ModelID = _photo_utilities.get_image_Model_name(fullname).replace(' ','')
            image_Software = _photo_utilities.get_image_Software(fullname)
            #print("image_datetime :", image_datetime)
            
            image_dt = datetime.strptime(image_datetime, '%Y%m%d-%H%M%S')
            # print("image_dt :", image_dt)
            # print(f"image_dt.month : {image_dt.month:02d}")
            # print(f"image_dt.day : {image_dt.day:02d}")
            SAVEDIR = (BASEDIR/ str(image_dt.year) / f'{(image_dt.month):02d}' / f'{(image_dt.day):02d}_{image_ModelID}')
            new_fname = f'{image_datetime}_{image_ModelID}_py{fpath.suffix}'
            new_fpath = SAVEDIR / new_fname
            print("new_fpath :", new_fpath)
            for i in range(3, -1, -1):
                if not new_fpath.parents[i].exists() :
                    os.mkdir(str(new_fpath.parents[i]))
                    #print(f'{str(new_fpath.parents[i])} is created...')
                else :
                    #print(f'{str(new_fpath.parents[i])} is exist...')
                    pass
            if not new_fpath.exists() :
                print(f'{str(new_fpath)} is not exist...')
            else : 
                print(f'{str(new_fpath)} is already exist...')
                new_date = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
                new_fpath = new_fpath.parents[0] / f'{new_fpath.stem}_{new_date}{new_fpath.suffix}'
            shutil.move(str(fpath), str(new_fpath))
        except Exception as err :
            print(err)  

#%%
#############################################################################
for i in range(4) :
    fullnames = _Python_utilities.getFullnameListOfallsubDirs(str(NEW_files))
    print ("fullnames: {}".format(fullnames))
    for fullname in fullnames[:] :
        # Check is empty..
        if len(os.listdir(fullname)) == 0 :
            shutil.rmtree(r"{}".format(fullname)) # Delete..
            print ("rmtree {}\n".format(fullname))