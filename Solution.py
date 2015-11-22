import pickle

from PhonyEntity import *
from FileEntity import *

from Project import *

class Solution:
    def __init__(self, path):
#        self.m_target_pres_dict = {}
        self.m_projectFilesPathList = []
        self.m_path = path

    def show(self):
        print "project files:"
        for f in self.m_target_pres_dict.keys():
            print f

    def loadPrjList(self):
        f = open('PROJECTFILES')
        for line in f:
            prjName = line.strip(' \n\t')
            if not len(prjName) == 0:
                self.m_projectFilesPathList.append(prjName)
        f.close()

    def savePrjList(self):
        f = open('PROJECTFILES', 'w')
        for prj in self.m_projectFilesPathList:
            f.write(prj)
            f.write('\n')
#        f.writelines(self.m_sourceFilesPathList)
        f.close()

    def load(self):
        f = open(self.m_path, "r")
        self.loadPrjList()

#        self.m_target_pres_dict = pickle.load(f)

        f.close()

    def save(self):
        f = open(self.m_path, "w")
        self.savePrjList()

 #       pickle.dump(self.m_target_pres_dict, f)

        f.close()
    def addProject(self, project):
        for f in self.m_projectFilesPathList:
            if f == project:
                return False
        self.m_projectFilesPathList.append(project)
        return True

    def removeProject(self, project):
        for f in self.m_projectFilesPathList:
            if f == project:
                self.m_projectFilesPathList.remove(project)
                return True
        return False

    def build(self, verbose):
        # todo: projects dependences
        sln_absdir = os.path.dirname(self.m_path)
        for prj_relpath in self.m_projectFilesPathList:
            prj_abspath = os.path.abspath(prj_relpath)
            prj_reldir = os.path.dirname(prj_relpath)
            prj_absdir = os.path.dirname(prj_abspath)
            if verbose:
                print "Entering directory " + prj_absdir
            os.chdir(prj_absdir)
            prj = Project(prj_abspath)
            prj.load()
            prj.build(verbose)
            if verbose:
                print "Leaving directory " + prj_absdir
            os.chdir(sln_absdir)

