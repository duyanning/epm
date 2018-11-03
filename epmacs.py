# this file is anoter interface to epm to be used in emacs
# this moudle is used by epmacs.el

import glob
import os
import epmaux
from Project import *

def foo(x):
    return 2 * x


# def getexename():
#     prjName = epmaux.findPrjFile()
#     prj = Project(prjName)
#     prj.load()
#     exeName = prj.exeName()
# #    return "gdb --annotate=3 -cd . --args debug/" + exeName
#     return exeName

def getexename():
    prjName = epmaux.findPrjFile()
    prj = Project(prjName)
    prj.load()
    exeName = prj.dirName() + "/debug/" + prj.exeName()
    return exeName

def getprjname():
    prjName = epmaux.findPrjFile()
    # return "/home/duyanning/hello"
    # print "aaaaaaaaaaa: " + prjName
    if not prjName:
        return os.getcwd()
    return os.path.dirname(prjName)


def setactiveconfig(configname):
    epmaux.set_active_config(configname)
