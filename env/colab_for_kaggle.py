%%capture

# kaggleへ接続
!mkdir /root/.kaggle
!echo '{"username":"sublate","key":"761073a2dbca2a5da62c60e3fb39cd71"}' > /root/.kaggle/kaggle.json
!chmod 600 /root/.kaggle/kaggle.json

# # google driveへ接続
# from google.colab import drive
# drive.mount('/content/drive') # 
# # drive._mount('/content/gdrive', force_remount=True) 

# kaggleのインストール
!pip install --upgrade --force-reinstall --no-deps kaggle

# コンペデータのダウンロード
!mkdir data/
!kaggle competitions download -c image-matching-challenge-2022 -p /content/data
!unzip -n /content/data/*.zip -d /content/data
!rm /content/data/*.zip

# # kaggle notebook 出力データのダウンロード
# !mkdir -p k/oldufo/imc2022-dependencies
# !kaggle kernels output oldufo/imc2022-dependencies -p k/oldufo/imc2022-dependencies

# kaggleデータセットのダウンロード
!mkdir -p /content/tensorort7234
!kaggle datasets download -d httpwwwfszyc/tensorort7234 -p /content/tensorort7234
!unzip /content/tensorort7234/tensorort7234.zip -d /content/tensorort7234
!rm /content/tensorort7234/*.zip

# githubレポジトリのダウンロード
!git clone https://github.com/sublatelog/Coarse_LoFTR_TRT.git
# !cp -pR ./Coarse_LoFTR_TRT/* /content/
# !rm -r ./Coarse_LoFTR_TRT

import os
import sys

repo = 'Coarse_LoFTR_TRT'
device = 'cuda'

if not repo in sys.path:
    sys.path.insert(1, repo)
