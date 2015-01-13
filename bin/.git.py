#/***************************************************************************
# * 
# * Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
# * 
# **************************************************************************/
 
 
 
#/**
# * @file commands.py
# * @author lvlongtao(com@baidu.com)
# * @date 2014/12/10 11:48:56
# * @brief 
# *  
# **/
#
import re
import sys
import commands
import pexpect
import colors
import os
import os.path
import xml.etree.cElementTree as ET
from optparse import OptionParser


class GIT:
        
    def __init__(self):
        self.user = 'lvlongtao'
        self.password = 'last2014'
        
    def __execute__(self, cmd):
        status,output = commands.getstatusoutput(cmd)
        output = output.replace("git", "cst")
        result = colors.red('========================================')
        for line in output.split('\n'):
            if line.startswith('+'):
                line = colors.yellow(line)
            elif line.startswith('-'):
                line = colors.red(line)
            elif line.startswith('#'):
                line = colors.white(line)
            elif line.startswith('Author'):
                line = ''
            result = result + '\n' + line
        if output.startswith('fatal'):
            result = colors.red('========================================\nPlease goto master path, then use cst')
        if result != colors.red('========================================\n'):
            print result
        return status,result
    
    def check_path(self, filepath):
        for parent, dirnames, filenames in os.walk(filepath):
            xml_flag = 0
            for filename in filenames:
                if filename.endswith('.xml'):
                    xml_flag = 1
                    tree = ET.ElementTree(file=filepath+filename)
                    treelist = []
                    for item in tree.iter():
                        treelist.append(item.tag)
                    if treelist[0] == 'tool' and 'dependency' in treelist:
                        status = 1
                        result = colors.red('check ok')
                        return status,result
                    else:
                        status = 0
                        result = colors.red('%s has error'%(filepath+filename))
                        return status,result
            if xml_flag ==0 :
                status = 0
                result = colors.red('your tool should include a xml file to tell us how to use it')
                return status,result
    
    def status(self):
        cmd = 'git status'
        return self.__execute__(cmd)
    
    def log(self):
        cmd = 'git log'
        return self.__execute__(cmd)
    
    def diff(self):
        cmd = 'git diff'
        diff = self.__execute__(cmd)
        if diff[1] == '========================================\n':
            diff = '========================================:\n no diff content'
            print diff
        return diff 
    
    def list(self):
        cmd = 'git ls-tree -r --name-only HEAD'
        list = self.__execute__(cmd)
        return list
    
    def search(self, toolname):
        cmd = 'git ls-tree -r --name-only HEAD'
        status,output = commands.getstatusoutput(cmd)
        result = colors.red('========================================')
        pattern = toolname
        for line in output.split('\n'):
            m = re.search(pattern, line)
            if m:
                result = result + '\n' + line.replace(pattern,colors.magenta(pattern))
        if result == colors.red('========================================'):
            result = colors.red('========================================\n')
            result += colors.yellow('do not have this tool')
        print result
        return status,result
    
    def show(self):
        cmd = 'git show'
        return self.__execute__(cmd)
    
    def add(self, file):
        cmd = 'git add %s' % file
        check = self.check_path(file)
        if check[0]:
            add = self.__execute__(cmd)
            print check[1]
        else:
            add = colors.red('========================================:\n') + ' %s %s' % (file, check[1])
            print add
        return add 
                
    def rm(self, file):
        cmd = 'git rm -r %s' % file
        self.__execute__(cmd)
                
    def ci(self, msg):
        cmd = 'git commit -am \'%s\'' % msg
        self.__execute__(cmd)
        pushcmd = 'git push'
        child = pexpect.spawn(pushcmd)
        while True:
            i = child.expect(['Username:','Password:', pexpect.EOF, pexpect.TIMEOUT], timeout=10)
            if i == 0:
                child.sendline(self.user)
            elif i == 1:
                child.sendline(self.password)
            else:
                child.close()
                return False
    
    def co(self):
        cmd = 'git clone http://gitlab.baidu.com:lvlongtao/cstrace.git master '
        self.__execute__(cmd)

    def up(self):
        cmd = 'git pull'
        self.__execute__(cmd)

if __name__ == '__main__':
    helpInfo = """
    cst [--version][--help]
               <command> [<args>]

    The most commonly used git commands are:
        add        Add file contents to the index
        list    List the whole tools
        search  List the tools you search for
        co     Clone a repository into a new directory
        ci     Record changes to the repository and Update remote refs along with associated objects
        diff       Show changes between commits, commit and working tree, etc
        log        Show commit logs
        up       Fetch from and merge with another repository or a local branch
        rm         Remove files from the working tree and from the index
        show       Show various types of objects
        status     Show the working tree status
    """
    CST = GIT()
    optParser = OptionParser(usage = helpInfo, version="cst 1.0.0.0")
    (options,args) = optParser.parse_args()
    if len(sys.argv) == 1:
        print optParser.print_help()
    elif sys.argv[1] == "add":
        if len(sys.argv) == 2:
            print "Try cst -h for more info\ncst: Not enough arguments provided"
        elif len(sys.argv) == 3:
            CST.add(sys.argv[2])
        else:
            print 'too mush arguments'
    elif sys.argv[1] == "co":
        if len(sys.argv) == 2:
            CST.co()
        else:
            print 'too mush arguments'
    elif sys.argv[1] == "ci":
        if len(sys.argv) == 2:
            print "Try cst -h for more info\ncst: Not enough arguments provided"
        elif len(sys.argv) == 3:
            CST.ci(sys.argv[2])
        else:
            print 'too mush arguments'
    elif sys.argv[1] == "diff":
        if len(sys.argv) == 2:
            CST.diff()
        else:
            print 'too mush arguments'
    elif sys.argv[1] == "log":
        if len(sys.argv) == 2:
            CST.log()
        else:
            print 'too mush arguments'
    elif sys.argv[1] == "up":
        if len(sys.argv) == 2:
            CST.up()
        else:
            print 'too mush arguments'
    elif sys.argv[1] == "rm":
        if len(sys.argv) == 2:
            print "Try cst -h for more info\ncst: Not enough arguments provided"
        elif len(sys.argv) == 3:
            CST.rm(sys.argv[2])
        else:
            print 'too mush arguments'
    elif sys.argv[1] == "search":
        if len(sys.argv) == 2:
            print "Try cst -h for more info\ncst: Not enough arguments provided"
        elif len(sys.argv) == 3:
            CST.search(sys.argv[2])
        else:
            print 'too mush arguments'
    elif sys.argv[1] == "show":
        if len(sys.argv) == 2:
            CST.show()
        else:
            print 'too mush arguments'
    elif sys.argv[1] == "list":
        if len(sys.argv) == 2:
            CST.list()
        else:
            print 'too mush arguments'
    elif sys.argv[1] == "status":
        if len(sys.argv) == 2:
            CST.status()
        else:
            print 'too mush arguments'
    elif sys.argv[1] == "check":
        if len(sys.argv) == 2:
            print "Try cst -h for more info\ncst: Not enough arguments provided"
        elif len(sys.argv) == 3:
            CST.check_path(sys.argv[2])
        else:
            print 'too mush arguments'
    else:
        print 'U put wrong arguments\nTry cst -h for more info'
