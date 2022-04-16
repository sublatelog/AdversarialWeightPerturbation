


# OSの確認
!cat /etc/issue　
# Ubuntu 18.04.5 LTS \n \l


# GPUの利用状況確認
!nvidia-smi


# pythonのバージョンでぇんこう
# Choose one of the given alternatives:
!sudo update-alternatives --config python3

# This one used to work but now NOT(for me)!
# !sudo update-alternatives --config python

# Check the result
!python3 --version

# Attention: Install pip (... needed!)
!sudo apt install python3-pip


which python # /usr/local/bin/python


# python　一覧
ls /usr/bin/ | grep python
