  
   3.安装virtualenv
   pip install virtualenv

  2.激活虚拟环境

    1.激活激活虚拟环境
         source 虚拟环境目录/bin/activate
       当虚拟环境被激活后，在命令前可以看到(虚拟环境名称)
  3.退出虚拟环境
     deactivate
     如果要删除虚拟环境，只需退出虚拟环境后，删除对应的虚拟环境目录即可。不影响其他环境。
     继续使用之前的虚拟环境： workon 虚拟环境名称 （该虚拟环境必须存在）
    删除虚拟环境
    rmvirtualenv 
    注意：如果目前的位置在虚拟环境中，需要先退出虚拟环境，然后才能执行删除

    注意：可以在任何目录执行删除操作，如果不知道名字，可以rmvirtualen + 两次Tab键，提示所有的虚拟环境


    cuda链接更改
    可以使用stat命令查看当前cuda软链接指向的哪个cuda版本，如下所示： 
    stat cuda
    sudo rm -rf cuda
    sudo ln -s /usr/local/cuda-9.1 /usr/local/cuda
    之后运行nvcc --version查看当前版本


常用virtualenvwrapper命令
命令  说明
mkvirtualenv (env name) 创建虚拟环境，会在WORKON_HOME路径中
# mkvirtualenv --python==pathto\python.exe (env name) 创建虚拟环境，并制定具体python路径
workon (env name)   切换到某个虚拟环境
deactivate   退出当前虚拟环境
rmvirtualenv (env name) 删除虚拟环境
lsvirtualenv    列出所有虚拟环境所在目录
cdvirtualenv    进入到虚拟环境所在目录


安装环境
# Linux 
# Python 3.7
# PyTorch 1.6
# CUDA 10.1 
# GCC 5+
# MMCV
MMDetection version
# MMDetection version         MMCV version
#      master               mmcv-full>=1.2.4, <1.3
#      2.8.0                mmcv-full>=1.2.4, <1.3

pytorch,torchvision
# CUDA 10.1
pip install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html


mmcv-full
to install the latest mmcv-full with CUDA 11 and PyTorch 1.7.0, use the following command:
pip install mmcv-full -f https://download.openmmlab.com/mmcv/dist/cu110/torch1.7.0/index.html

