# photo_Python

conda env list

## Anaconda environment
conda create -n photo_Python_env

### activate conda virtual environment
conda activate photo_Python_env

### deactivate conda virtual environment
conda deactivate

### install module
conda install -c phygbu pyheif spyder
conda install -c conda-forge opencv-python piexif exifread python-dateutil
pip install hachoir

### expert conda virtual environment 
conda env export > photo_Python_env.yaml

### create conda virtual environment from .yaml file
conda env create -f photo_Python_env.yaml

### remove conda envrionment
conda env remove -n photo_Python_env

