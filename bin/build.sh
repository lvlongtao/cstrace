#/***************************************************************************
# * 
# * Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
# * 
# **************************************************************************/
 
 
 
#/**
# * @file build.sh
# * @author lvlongtao(com@baidu.com)
# * @date 2014/12/12 14:47:18
# * @brief 
# *  
# **/

###############get file path
cd ~
git_path=`pwd`
cd -
now_path=`pwd`

###############compile git and add python-pexpect module
tar -jxvf git-1.7.5.1.tar.bz2
cd git-1.7.5.1;
./configure --prefix=$git_path/.cstrace/git
make install
cd -
tar -xzvf pexpect-3.3.tar.gz
cd pexpect-3.3
python setup.py install
cd -
tar -xzvf colors.tar.gz
cd colors
python setup.py install

###############set git env
echo "alias cst='python $now_path/.git.py'" >> $git_path/.bashrc
echo "export PATH=\$PATH:$git_path/.cstrace/git/bin" >> $git_path/.bashrc
source $git_path/.bashrc
cd -
git clone http://gitlab.baidu.com/lvlongtao/cstrace.git master
cd $now_path/master; git config http.postBuffer 524288000;
cd $now_path/master; git config --global user.email "lvlongtao@baidu.com"
cd $now_path/master; git config --global user.name "lvlongtao"
cd $now_path/master; git config credential.helper store
source $git_path/.bashrc









