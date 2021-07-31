# photo_Python

Anaconda environment

conda create -n photo_Python_env python=3.7
conda env list

# activate 가상환경 시작
mac/linux
source activate photo_Python_env

windows
activate photo_Python_env

# deactivate 가상환경 종료
mac/linux
conda deactivate

windows
deactivate

# install module
conda install -c phygbu pyheif
conda install -c conda-forge opencv piexif exifread

# 가상환경 내보내기 (export)
conda env export > photo_Python_env.yaml

# .yaml 파일로 새로운 가상환경 만들기
conda env create -f my_python_env.yaml

# 가상환경 리스트 출력
conda env list

#가상환경 제거하기
conda env remove -n photo_Python_env