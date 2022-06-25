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

### activate �??��?���? ?��?��
conda activate photo_Python_win_env

### deactivate �??��?���? 종료
conda deactivate

### install module
conda install -c phygbu pyheif
conda install -c conda-forge python-dateutil
conda install -c conda-forge opencv piexif exifread 
pip install hachoir

### �??��?���? ?��보내�? (export)
conda env export > photo_Python_win_env.yaml

### .yaml ?��?���? ?��로운 �??��?���? 만들�?
conda env create -f photo_Python_win_env.yaml

### �??��?���? 리스?�� 출력
conda env list

### �??��?���? ?��거하�?
conda env remove -n photo_Python_win_env