# this file is anoter interface to epm to be used in emacs
# this moudle is used by epmacs.el

import glob
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



def setactiveconfig(configname):
    epmaux.set_active_config(configname)
