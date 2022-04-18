# OSの確認
!cat /etc/issue　
# Ubuntu 18.04.5 LTS \n \l


# GPUの利用状況確認
!nvidia-smi

# pythonのバージョン確認
from platform import python_version   
import sys
print("sys.version:",sys.version)
print("Current Python Version-", python_version())

sys.version_info.major, sys.version_info.minor, sys.version_info.micro
!python --version


# pythonのバージョン変更
!update-alternatives --list python

!update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1

# Choose one of the given alternatives:
!sudo update-alternatives --config python3


!nvcc --version
!nvidia-smi
import torch; print(torch.version.cuda)
import torch; print(torch.__version__)
!python --version
cv2.__version__



# This one used to work but now NOT(for me)!
# !sudo update-alternatives --config python

# Check the result
!python3 --version

# Attention: Install pip (... needed!)
!sudo apt install python3-pip


which python # /usr/local/bin/python


# python　一覧
ls /usr/bin/ | grep python


# エイリアスの設定
!alias python='/usr/bin/python3.6'


# プロセスの確認
!ps


# システムパスの確認
sys.path


# リンク元の確認
!which python3


# パスの確認
import site
site.getsitepackages()

# exportの一覧
!export -p





