# -*- coding: utf-8 -*-
import glob
import os
import os.path
from Project import *
from Solution import *
import settings

def findSlnFile():
    slnFilesList = glob.glob("*.epmsln")
    if slnFilesList:
        return os.path.abspath(slnFilesList[0])
    else:
        return None

def findPrjFile():
    topArrived = False
    cd = os.getcwd();
    while not topArrived:
        if settings.verbose:
            print "finding .epmprj in " + cd + " ... ", 
        # 在当前目录下找epmprj文件
        prjFilesList = glob.glob(os.path.join(cd, "*.epmprj"))
        # print glob.glob(os.path.join(cd, "*.epmprj"))
        # 如果找到就返回
        if prjFilesList:
            if settings.verbose:
                print "found." 
            os.chdir(cd)
            return os.path.abspath(prjFilesList[0])
        if settings.verbose:
            print ""                # 没找到也输出一个换行
        lastCd = cd
        # 否则就去父目录中找
        cd = os.path.normpath(os.path.join(cd, os.pardir))

        if (cd == lastCd):
            topArrived = True

    return None

def findFile(pattern):
    prjFilesList = glob.glob(pattern)
    if prjFilesList:
        return os.path.abspath(prjFilesList[0])
    else:
        return None

def list_prj(name):
    prj = Project(name)
    prj.load()
    prj.show()

def list_sln(name):
    sln = EpmSolution(name)
    sln.load()
    sln.show()

def list_prj_or_sln(name, isSln):
    if not isSln:
        list_prj(name)
    else:
        list_sln(name)

def build_solution():
    slnName = findSlnFile()
    if not slnName:
        print "cannot find a solution"
        return
    sln = Solution(slnName)
    sln.load()
    sln.build()

def build_project():
    prjName = findPrjFile()
    if not prjName:
        print "cannot find a project"
        return
    prj = Project(prjName)
    prj.load()
    return prj.build()

def build_gch():
    prjName = findPrjFile()
    if not prjName:
        print "cannot find a project"
        return
    prj = Project(prjName)
    prj.load()
    prj.buildGch()

def compile_sourcefile(srcfile):
    prjName = findPrjFile()
    if not prjName:
        print "cannot find a project"
        return
    prj = Project(prjName)
    prj.load()
    return prj.compile(srcfile)


def set_active_config(name):
    prjName = findPrjFile()
    prj = Project(prjName)
    prj.load()
    prj.setActiveConfig(name)
    prj.saveProjectFile()

def add_config(name):
    prjName = findPrjFile()
    prj = Project(prjName)
    prj.load()
    prj.addConfig(name)
    prj.save()

def add_source(srcList):
    prjName = findPrjFile()
    if not prjName:
        print "cannot find project"
        return
    prj = Project(prjName)
    prj.load()
    for f in srcList:
        if not prj.addSource(f):
            print f, "is already in project"
    prj.save()

def remove_source(srcList):
    prjName = findPrjFile()
    if not prjName:
        print "cannot find project"
        return
    prj = Project(prjName)
    prj.load()
    for f in srcList:
        if not prj.removeSource(f):
            print f, "is not in project"
    prj.save()

def add_project(prj):
    slnName = findSlnFile()
    if not slnName:
        print "cannot find solution"
        return
    sln = Solution(slnName)
    sln.load()
    sln.addProject(prj)
    sln.save()


def remove_project(prj):
    slnName = findSlnFile()
    if not slnName:
        print "cannot find solution"
        return
    sln = Solution(slnName)
    sln.load()
    sln.removeProject(prj)
    sln.save()

def new_project(prjName, type):
#    prjPath = os.path.abspath(prjName)
    prjName += ".epmprj"
    prj = Project(prjName)

    (name, ext) = os.path.splitext(prjName)
    if type == "dll":
        postfix = ".so"
    elif type == "lib":
        postfix = ".a"
    else:
        postfix = ""
    exeName = name + postfix

    prj.addConfig("debug")
    print 'exe name: ' + exeName
    prj.setExeName(exeName)
    prj.setType(type)
    prj.save()

def new_solution(slnName):
    slnName += ".epmsln"
    sln = Solution(slnName)
    sln.save()

def add_pch(headerList):
    prjName = findPrjFile()
    if not prjName:
        print "cannot find project"
        return
    prj = Project(prjName)
    prj.load()
    for f in headerList:
        if not prj.addPch(f):
            print f, "is already in project"
    prj.save()

def remove_pch(headerList):
    prjName = findPrjFile()
    if not prjName:
        print "cannot find project"
        return
    prj = Project(prjName)
    prj.load()
    for f in headerList:
        if not prj.removePch(f):
            print f, "is not in project"
    prj.save()

def open_gui():
    import epmapp
    app = epmapp.EpmApp()
    app.main()
