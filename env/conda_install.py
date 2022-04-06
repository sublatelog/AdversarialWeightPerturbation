!which python # /usr/local/bin/python

!python --version

!echo $PYTHONPATH # /env/python

%env PYTHONPATH=

%%bash
MINICONDA_INSTALLER_SCRIPT=Miniconda3-4.5.4-Linux-x86_64.sh
MINICONDA_PREFIX=/usr/local
wget https://repo.continuum.io/miniconda/$MINICONDA_INSTALLER_SCRIPT
chmod +x $MINICONDA_INSTALLER_SCRIPT
./$MINICONDA_INSTALLER_SCRIPT -b -f -p $MINICONDA_PREFIX

!which conda # should return /usr/local/bin/conda

!conda --version # should return 4.5.4

!which python # still returns /usr/local/bin/python

!python --version # now returns Python 3.6.5 :: Anaconda, Inc.

%%bash
conda install --channel defaults conda python=3.6 --yes
conda update --channel defaults --all --yes

!conda --version # now returns 4.8.3

!python --version # now returns Python 3.6.10 :: Anaconda, Inc.

import sys
sys.path

!ls /usr/local/lib/python3.6/dist-packages

import sys
_ = (sys.path
        .append("/usr/local/lib/python3.6/site-packages"))


!conda install --channel conda-forge featuretools --yes



