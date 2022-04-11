!ls -d /usr/local/cuda-*

# %%bash
# rm -rf /usr/local/cuda
# ln -s /usr/local/cuda-10.1 /usr/local/cuda

!sudo update-alternatives --install /usr/local/cuda cuda /usr/local/cuda-10.1 80
# !sudo update-alternatives --config cuda

# import os
# p = os.getenv('PATH')
# ld = os.getenv('LD_LIBRARY_PATH')
# os.environ['PATH'] = f"/usr/local/cuda-10.1/bin:{p}"
# os.environ['LD_LIBRARY_PATH'] = f"/usr/local/cuda-10.1/lib64:{ld}"
# !nvcc --version

# %%bash
# export CUDA_HOME=/usr/local/cuda-10.1
# # export CUDA_HOME=/usr/local/cuda-11.1

import os
os.environ['CUDA_HOME'] = '/usr/local/cuda-10.1'
os.environ['CUDA_PATH'] = '/usr/local/cuda-10.1'

print(os.environ.get('CUDA_HOME'))
print(os.environ.get('CUDA_PATH'))


!nvcc --version
!nvidia-smi
import torch; print(torch.version.cuda)
import torch; print(torch.__version__)
!python --version
cv2.__version__


















