# -*- coding: utf-8 -*-
"""
Spyder Editor
created by guitar79@naver.com
https://stackoverflow.com/questions/33031663/how-to-change-image-captured-date-in-python
"""

import os
from datetime import datetime
from pathlib import Path
import shutil
import filecmp
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
DOINGDIR = BASEDIR / "NEW_files"
DUPLICATEDIR =  BASEDIR / "dupulicate_files"
fullnames = _Python_utilities.getFullnameListOfallFiles(DOINGDIR)
#print("fullnames:", fullnames)
print("len(fullnames):", len(fullnames))

ext_lst = [".mpg", ".wmv", ".mp4", ".mov", ".3gp", ".avi", ".dng", 
           "heic", ".jpg", "jpeg", ".cr2", ".png"]

#%%
for fullname in fullnames[:]:
    fpath = Path(fullname)
    print(fpath)
    print(fpath.suffix.lower())
    if fpath.suffix.lower() in ext_lst :

        try :     
            file_datetime, camera_ModelID, Software = \
                _photo_utilities.get_fileInfo(str(fpath))
            
            print(file_datetime, camera_ModelID, Software)
            
            file_dt = datetime.strptime(file_datetime, r'%Y%m%d-%H%M%S')
            print("file_dt :", file_dt)
            print(f"file_dt.month : {file_dt.month:02d}")
            print(f"file_dt.day : {file_dt.day:02d}")
            SAVEDIR = (BASEDIR/ str(file_dt.year) / f'{(file_dt.month):02d}' / f'{(file_dt.day):02d}_{camera_ModelID}')
            new_fname = f'{file_datetime}_{camera_ModelID}_py{fpath.suffix}'
            new_fpath = SAVEDIR / new_fname
            print("new_fpath :", new_fpath)
            for i in range(3, -1, -1):
                if not new_fpath.parents[i].exists() :
                    os.mkdir(str(new_fpath.parents[i]))
                    #print(f'{str(new_fpath.parents[i])} is created...')
                else :
                    #print(f'{str(new_fpath.parents[i])} is exist...')
                    pass

            if new_fpath.exists() :
                print(f'{str(new_fpath)} is already exist...')
                if filecmp.cmp(str(new_fpath), str(fpath)) :
                    now_dt = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f')
                    new_fpath = DUPLICATEDIR / f'{new_fpath.stem}_{now_dt}{new_fpath.suffix}'
                else :
                    now_dt = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f')
                    new_fpath = new_fpath.parents[0] / f'{new_fpath.stem}_{now_dt}{new_fpath.suffix}'
            else : 
                print(f'{str(new_fpath)} is not exist...')
                
            shutil.move(str(fpath), str(new_fpath))
            print(str(fpath), str(new_fpath))
        except Exception as err :
            print(err)


#%%
#############################################################################
for i in range(10):
    BASEDIR = Path("/mnt/photo/")
    DOINGDIR = BASEDIR / "NEW_files"
    DOINGDIRs = sorted(_Python_utilities.getFullnameListOfallsubDirs(DOINGDIR))
    #print ("DOINGDIRs: ", format(DOINGDIRs))
    print ("len(DOINGDIRs): ", format(len(DOINGDIRs)))
    
    for DOINGDIR in DOINGDIRs : 
        if len(os.listdir(str(DOINGDIR))) == 0 :
            shutil.rmtree(f"{str(DOINGDIR)}") # Delete..
            print (f"rmtree {str(DOINGDIR)}")
        else : 
            try: 
                fpaths = _Python_utilities.getFullnameListOfallFiles(str(DOINGDIR))
                print("fpaths", fpaths)

                for fpath in fpaths[:]:
                    print("fpath", fpath)

                    if fpath[-4:].lower() in [".txt", ".log", ".ini", "json", "info",
                                            ".csv", ".thm", "proj", ".pp3", "s.db"] \
                                            and os.path.isfile(fpath):
                        os.remove("{}".format(fpath))
                        print("{} is removed...".format(fpath))
            except Exception as err :
                    print(err) 