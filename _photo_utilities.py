"""
Spyder Editor

ModuleNotFoundError: No module named 'cv2' 
conda install opencv

pip install piexif

ModuleNotFoundError: No module named 'exifread'
pip install exifread

There are only just five functions.

load(filename) - Get exif data as dict.
dump(exif_dict) - Get exif as bytes.
insert(exif_bytes, filename) - Insert exif into JPEG, or WebP.
remove(filename) - Remove exif from JPEG, or WebP.
transplant(filename, filename) - Transplant exif from JPEG to JPEG.

created by guitar79@naver.com

"""

#for debugging
import os
from datetime import datetime
from astropy.io import fits
import exifread
import pyheif
import piexif
from pathlib import Path
import cv2
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
# =============================================================================
        
def checkDuplicated_jpg(fullname1, fullname2):
    Duplicated_im = False
    try :         
        im1 = cv2.imread("{}".format(fullname1))
        im2 = cv2.imread("{}".format(fullname2))
    
        # 1) Check if 2 images are equals
        if im1.shape == im2.shape:
            #print("The images have same size and channels")
            difference = cv2.subtract(im1, im2)
            b, g, r = cv2.split(difference)
        
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                Duplicated_im = True
                #print("The images are completely Equal")

    except:
        print("reading error with {}, {}".format(fullname1, fullname2))
    return Duplicated_im


def checkDuplicated_cr2(fullname1, fullname2):
    #pip install opencv-python
    #pip install opencv-contrib-python
    Duplicated_im = False
    try :         
        im1 = cv2.imread("{}".format(fullname1))
        im2 = cv2.imread("{}".format(fullname2))
    
        # 1) Check if 2 images are equals
        if im1.shape == im2.shape:
            #print("The images have same size and channels")
            difference = cv2.subtract(im1, im2)
            b, g, r = cv2.split(difference)
        
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                Duplicated_im = True
                #print("The images are completely Equal")

    except:
        print("reading error with {}, {}".format(fullname1, fullname2))
    return Duplicated_im


def get_image_datetime_str(fullname):
    f = open(fullname, 'rb')
    tags = exifread.process_file(f)
    f.close()
    if 'EXIF DateTimeOriginal' in tags :
        image_datetime = tags['EXIF DateTimeOriginal'].values.replace(':','')
        image_datetime = image_datetime.replace(' ','-')
        image_datetime = image_datetime.replace('오후','')
        image_datetime = image_datetime.replace('오전','')
        image_datetime = image_datetime.replace('  ','00')
        
    elif 'Image DateTime' in tags :
        image_datetime = tags['Image DateTime'].values.replace(':','')
        image_datetime = image_datetime.replace(' ','-')
        image_datetime = image_datetime.replace('오후','')
        image_datetime = image_datetime.replace('오전','')
        image_datetime = image_datetime.replace('  ','00')
    else : 
        image_datetime = "19990101-000000"
    
    return image_datetime

def get_image_number(fullname):
    f = open(fullname, 'rb')
    tags = exifread.process_file(f)
    f.close()
    if 'MakerNote FileNumber' in tags :
        image_num = tags['MakerNote FileNumber'].printable
    else : 
        image_num = "00"
    return image_num

def get_fileInfo_from_heifexif(fullname):
    heif_file = pyheif.read_heif(fullname)

    # Retrive the metadata
    for metadata in heif_file.metadata or []:
        if metadata['type'] == 'Exif':
            exif_dict = piexif.load(metadata['data'])
    image_datetime = exif_dict['0th'][306].decode('utf-8').replace(':','')
    file_datetime = image_datetime.replace(' ','-')
    camera_company = exif_dict['0th'][271].decode('utf-8')
    camera_model = exif_dict['0th'][272].decode('utf-8').replace(' ','-')
    Software = "-"
    return file_datetime, camera_company, camera_model, Software


def get_fileInfo_from_exif(fpath):
    fpath = Path(fpath)

    f = open(Path(fpath), 'rb')
    tags = exifread.process_file(f)
    f.close()
    ##########################################################
    if 'EXIF DateTimeOriginal' in tags :
        image_datetime = tags['EXIF DateTimeOriginal'].values.replace(':','')
        image_datetime = image_datetime.replace(' ','-')
        
    elif 'Image DateTime' in tags :
        image_datetime = tags['Image DateTime'].values.replace(':','')
        image_datetime = image_datetime.replace(' ','-')
    else : 
        image_datetime = "19990101-000000"
    ##########################################################
    
    if 'Image Make' in tags and 'Image Model' in tags : 
        camera_model = tags['Image Make'].printable.replace(' ','')\
            +tags['Image Model'].printable.replace(' ','')
    elif 'MakerNote ModelID' in tags : 
        camera_model = tags['MakerNote ModelID'].printable.replace(' ','')        
    else : 
        camera_model = '-'
    ##########################################################    
    if 'Image Software' in tags : 
        Software = tags['Image Software'].printable.replace(' ','')
    else : 
        Software = '-'
    if 'ACDSystems' in Software : 
        Software = 'ACDSystems'

    Software = Software.replace('DigitalPhotoProfessional', 'DPP')
    
    camera_model = camera_model.replace('CanonCanon','Canon')
    camera_model = camera_model.replace('/','')
    camera_model = camera_model.replace('\\','')
    camera_model = camera_model.replace('EASTMANKODAKCOMPANYKODAKDC3400ZOOMDIGITALCAMERA', 'KODAK_DC3400')
    camera_model = camera_model.replace('OLYMPUSOPTICALCO.,LTDC3100Z,C3020Z', 'OLYMPUS_C3100Z')
    camera_model = camera_model.replace('OLYMPUSCORPORATIONC-5000Z', 'OLYMPUS_C5000Z')
    camera_model = camera_model.replace('CanonEOSKissDigitalN', 'CANON_EOS-KissN')
    camera_model = camera_model.replace('CanonEOS350DDIGITAL', 'CANON_EOS-350D')
    camera_model = camera_model.replace('CanonEOS400DDIGITAL', 'CANON_EOS-400D')
    camera_model = camera_model.replace('CanonEOS', 'CANON_EOS')
    camera_model = camera_model.replace('EOS5DMarkII', 'EOS-5DMarkII')
    camera_model = camera_model.replace('EOS650D', 'EOS-650D')
    camera_model = camera_model.replace('CanonPowerShotS230', 'CANON_S230')
    camera_model = camera_model.replace('CanonPowerShotG', 'CANON_G')
    camera_model = camera_model.replace('CanonDIGITALIXUS50', 'CANON_IXUS50')
    camera_model = camera_model.replace('CanonIXYDIGITAL800IS', 'CANON_IXY800IS')
    camera_model = camera_model.replace('SONYDCR-TRV17', 'SONY_DCR-TRV17')
    camera_model = camera_model.replace('SONYCYBERSHOT', 'SONY_CYBERSHOT')
    camera_model = camera_model.replace('SONYDSC', 'SONY_DSC')
    camera_model = camera_model.replace('SONYNEX-5N', 'SONY_NEX-5N')
    camera_model = camera_model.replace('SONYILCE', 'SONY_ILCE')
    camera_model = camera_model.replace('NIKONE', 'NIKON_E')
    camera_model = camera_model.replace('NIKONCORPORATIONNIKOND', 'NIKON_D')
    camera_model = camera_model.replace('SAMSUNGELECTRONICSVM-C630', 'SAMSUNG_SVM-C630')
    camera_model = camera_model.replace('SAMSUNGTECHWINCO.,LTDDigimaxV5KenoxV5', 'SAMSUNG_DigimaxV5')
    camera_model = camera_model.replace('SamsungTechwinDigimax530KENOXD530', 'SAMSUNG_Digimax530')
    camera_model = camera_model.replace('SAMSUNGES95', 'SAMSUNG-ES95')
    camera_model = camera_model.replace('SAMSUNGWB150WB150FWB,...]', 'SAMSUNG_WB150')
    camera_model = camera_model.replace('SAMSUNGSM', 'SAMSUNG_SM')
    camera_model = camera_model.replace('SAMSUNGEK', 'SAMSUNG_EK')
    camera_model = camera_model.replace('SAMSUNGSH', 'SAMSUNG_SH')
    camera_model = camera_model.replace('SAMSUNGSSV', 'SAMSUNG_SHV')
    camera_model = camera_model.replace('SamsungTechwinDigimaxV4', 'SAMSUNG_DigimaxV4')
    camera_model = camera_model.replace('LGElectronicsLG', 'LG')
    camera_model = camera_model.replace('PanasonicDMC-LX2', 'PANASONIC_DMC-LX2')
    camera_model = camera_model.replace('ApplePhone', 'APPLE_iPhone')
    camera_model = camera_model.replace('Applei', 'APPLE_i')
    camera_model = camera_model.replace('DJIFC1102', 'DJI_FC1102')
    camera_model = camera_model.replace('DJIFC6310', 'DJI_FC6310')
    camera_model = camera_model.replace('XIAOYIYDXJ1', 'XIAOYI_YDXJ1')
    camera_model = camera_model.replace('PANTECH', 'PANTECH_')
    
    return image_datetime, camera_model, Software

def get_fileInfo_from_file(fpath):
    fpath = Path(fpath)
    #fullname_el = fullname.split(".")
    if fpath.suffix.lower() == ".heic" :
        try: 
            file_datetime, camera_model, Software = \
                get_fileInfo_from_heifexif(Path(fpath))
        except Exception as err :
            print(err)
        
    if fpath.suffix.lower() == ".cr2" or \
        fpath.suffix.lower() == ".jpg" or \
        fpath.suffix.lower() == ".tif" or \
        fpath.suffix.lower() == ".tiff" :
        try: 
            file_datetime, camera_model, Software = \
                get_fileInfo_from_exif(Path(fpath))
        except Exception as err :
            print(err)

    return file_datetime, camera_model, Software




def get_mov_creation_date(fullname):

    parser = createParser(fullname)
    metadata = extractMetadata(parser)
    if 'creation_date' in metadata :
        creation_date = metadata.get('creation_date').strftime("%Y%m%d-%H%M%S")
    else : 
        import os.path, time
        from dateutil.parser import parse
        creation_date = parse(time.ctime(os.path.getctime(fullname))).strftime("%Y%m%d-%H%M%S")
    return creation_date


def get_image_Software(fullname):
    import exifread
    f = open(fullname, 'rb')
    tags = exifread.process_file(f)
    f.close()
    if 'Image Software' in tags : 
        image_Software = tags['Image Software'].printable.replace(' ','')
    else : 
        image_Software = '-'

    if 'ACDSystems' in image_Software : 
        image_Software = 'ACDSystems'
    image_Software = image_Software.replace('DigitalPhotoProfessional', 'DPP')
    return image_Software

def write_log(log_file, log_str):
    import os
    with open(log_file, 'a') as log_f:
        log_f.write("{}, {}\n".format(os.path.basename(__file__), log_str))
    return print ("{}, {}\n".format(os.path.basename(__file__), log_str))


def bgr2rgb(bgr_image):
    import numpy as np
    RGB = np.zeros((bgr_image.shape[0], bgr_image.shape[1], 3), dtype=np.uint8)
    RGB[:,:,0] = bgr_image[:,:,2]
    RGB[:,:,1] = bgr_image[:,:,1]
    RGB[:,:,2] = bgr_image[:,:,0]
    return RGB

def clahe_equalized(imgs):
    import cv2
    lab = cv2.cvtColor(imgs, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    lab_planes[0] = clahe.apply(lab_planes[0])
    lab = cv2.merge(lab_planes)
    bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return bgr


def readJpgPhoto_to_ImagesAndTimes(fullnames):
    # source : https://learnopencv.com/high-dynamic-range-hdr-imaging-using-opencv-cpp-python/
    import exifread
    import numpy as np
    #import rawpy
    import cv2
   
    images = []
    times = []
    for fullname in fullnames:
        #im = rawpy.imread(fullname)
        im = cv2.imread(fullname)
        images.append(im)
    
        f = open(fullname, 'rb')
        tags = exifread.process_file(f)
        f.close()
        if 'EXIF ExposureTime' in tags :
            image_ExposureTime = tags['EXIF ExposureTime'].values
        times.append(image_ExposureTime)
    #images = np.array(images, dtype=np.uint8)
    times = np.array(times, dtype=np.float32)
    return images, times
