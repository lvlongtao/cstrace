#/***************************************************************************
# * 
# * Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
# * 
# **************************************************************************/
 
 
 
#/**
# * @file test.py
# * @author lvlongtao(com@baidu.com)
# * @date 2014/12/23 17:48:49
# * @brief 
# *  
# **/
import xml.etree.cElementTree as ET




tree = ET.ElementTree(file='test.xml')
for item in tree.iter():
    print item.tag
















#/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
