# photo_Python

## ubuntu
Anaconda environment

conda create -n photo_Python_ubuntu_env
conda env list

### activate conda virtual environment
conda activate photo_Python_ubuntu_env

### deactivate conda virtual environment
conda deactivate

### install module
conda install -c phygbu pyheif spyder
conda install -c conda-forge opencv piexif exifread 
conda install -c conda-forge python-dateutil
pip install hachoir

### expert conda virtual environment 
conda env export > photo_Python_ubuntu_env.yaml

### create conda virtual environment from .yaml file
conda env create -f photo_Python_ubuntu_env.yaml

### remove conda envrionment
conda env remove -n photo_Python_ubuntu_env


## Windows
Anaconda environment

conda create -n photo_Python_win_env
conda env list

### activate conda virtual environment
conda activate photo_Python_win_env

### deactivate conda virtual environment
conda deactivate

### install module
conda install -c phygbu pyheif
conda install -c conda-forge python-dateutil
conda install -c conda-forge opencv piexif exifread 
pip install hachoir

### expert conda virtual environment 
conda env export > photo_Python_win_env.yaml

### create conda virtual environment from .yaml file
conda env create -f photo_Python_win_env.yaml


### remove conda virtual environment
conda env remove -n photo_Python_win_env