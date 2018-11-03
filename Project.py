import pickle
import os
import glob

from PhonyEntity import *
from FileEntity import *

from Obj2ExeAction import *
from Cpp2ObjAction import *
from C2ObjAction import *
from H2GchAction import *
from Lex2CppAction import *
from Yacc2CppAction import *
from UpdateDependencyGraphAction import *

from Configuration import *
# from settings import verbose
import settings

class Project:
    def __init__(self, path):
        self.m_sourceFilesPathList = []
        self.m_precompiledHeadersPathList = []
        self.m_path = path
        self.m_librariesList = []

        self.m_activeConfig = "debug"
        self.m_exeName = ''
        self.m_type = ''

        self.m_compileOk = True
        self.m_linkOk = True

    def setLinkOk(self, ok):
        self.m_linkOk = ok

    def getLinkOk(self):
        return self.m_linkOk

    def setCompileOk(self, ok):
        self.m_compileOk = ok

    def getCompileOk(self):
        return self.m_compileOk

#    def name(self):
#        return os.path.basename(self.m_path)

    def exeName(self):
        return self.m_exeName
    def setExeName(self, name):
        self.m_exeName = name

    def dirName(self):
        return os.path.dirname(self.m_path)

    def type(self):
        return self.m_type
    def setType(self, type):
        self.m_type = type

    def addConfig(self, name):
#        os.mkdir(name)
        pass

    def activeConfig(self):
        return self.m_activeConfig

    def setActiveConfig(self, config):
        self.m_activeConfig = config

    def path(self):
        return self.m_path

    def sourceFilesList(self):
        return self.m_sourceFilesPathList;

    def show(self):

        print "source files:"
        for f in self.m_sourceFilesPathList:
            print f

        print "libraries:"
        for f in self.m_librariesList:
            print f

    def loadPrecompiledHeaderList(self):
        if not os.path.exists("PRECOMPILEDHEADERS"):
            return
        cwdname = os.getcwd()
        f = open("PRECOMPILEDHEADERS")
        for line in f:
            headerName = line.strip(' \n\t')
            self.m_precompiledHeadersPathList.append(headerName)
        f.close()

    def savePrecompiledHeaderList(self):
        f = open('PRECOMPILEDHEADERS', 'w')
        for header in self.m_precompiledHeadersPathList:
            f.write(header)
            f.write('\n')
        f.close()

    def loadSrcList(self):
        cwdname = os.getcwd()
        f = open("SOURCEFILES")
        for line in f:
            srcName = line.strip(' \n\t')
            self.m_sourceFilesPathList.append(srcName)
        f.close()

    def saveSrcList(self):
        f = open('SOURCEFILES', 'w')
        for src in self.m_sourceFilesPathList:
            f.write(src)
            f.write('\n')
        f.close()

    def load(self):
        self.loadPrecompiledHeaderList()
        self.loadSrcList()
        self.loadProjectFile()

    def save(self):
        self.savePrecompiledHeaderList()
        self.saveSrcList()
        self.saveProjectFile()

    def loadProjectFile(self):
        f = open(self.m_path, "r")

        self.m_librariesList = pickle.load(f)

        self.m_activeConfig = pickle.load(f)
        self.m_exeName = pickle.load(f)
        self.m_type = pickle.load(f)

        f.close()


    def saveProjectFile(self):
        f = open(self.m_path, "w")

        pickle.dump(self.m_librariesList, f)

        pickle.dump(self.m_activeConfig, f)
        pickle.dump(self.m_exeName, f)
        pickle.dump(self.m_type, f)

        f.close()

    def addSource(self, source):
        for f in self.m_sourceFilesPathList:
            if f == source:
                return False
        self.m_sourceFilesPathList.append(source)
        return True

    def removeSource(self, source):
        for f in self.m_sourceFilesPathList:
            if f == source:
                self.m_sourceFilesPathList.remove(source)
                return True
        return False

    def addPch(self, header):
        for f in self.m_precompiledHeadersPathList:
            if f == header:
                return False
        self.m_precompiledHeadersPathList.append(header)
        return True

    def removePch(self, header):
        for f in self.m_precompiledHeadersPathList:
            if f == header:
                self.m_precompiledHeadersPathList.remove(header)
                return True
        return False

    def sourceFilesPathList(self):
        return self.m_sourceFilesPathList

    def addLibrary(self, library):
        for lib in self.m_librariesList:
            if lib == library:
                return False
        self.m_librariesList.append(library)
        return True

    def removeLibrary(self, library):
        for lib in self.m_librariesList:
            if lib == library:
                self.m_librariesList.remove(library)
                return True
        return False

    def librariesList(self):
        return self.m_librariesList

    def setOutputPath(self, outputPath):
        self.m_outputPath = outputPath

    def outputPath(self):
        return self.m_outputPath

    def compile(self, src_path):
        #global verbose
        outputDir = self.activeConfig()
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)

        update_dependency = PhonyEntity("update dependency graph")

        srcName = os.path.basename(src_path)
        if srcName.endswith(".cpp"):
            objName = srcName.replace(".cpp", ".o")
        elif srcName.endswith(".c"):
            objName = srcName.replace(".c", ".o")
        obj_path = outputDir + "/" + objName

        obj = FileEntity(obj_path, obj_path)
        if srcName.endswith(".cpp"):
            obj.addAction(Cpp2ObjAction(self))
        elif srcName.endswith(".c"):
            obj.addAction(C2ObjAction(self))

        src = FileEntity(src_path, src_path)
        obj.addPrerequisite(src)

        optMgr = OptionManager()
        srcopt_path = optMgr.getOptionFilePath(src_path, self.activeConfig())
        srcopt = FileEntity(srcopt_path, srcopt_path)
        obj.addPrerequisite(srcopt)

        if srcName.endswith(".cpp"):
            depName = srcName.replace(".cpp", ".d")
        elif srcName.endswith(".c"):
            depName = srcName.replace(".c", ".d")
        dep_path = outputDir + "/" + depName
        if os.path.exists(dep_path):
            obj_update = PhonyEntity("update for " + obj_path)
            obj_update.addAction(UpdateDependencyGraphAction(obj))
            update_dependency.addPrerequisite(obj_update)


            dep = FileEntity(dep_path, dep_path)
            obj_update.addPrerequisite(dep)

        self.buildGch()

        if settings.verbose:
            update_dependency.show()
        update_dependency.update()

        if settings.verbose:
            obj.show()
        obj.update()

        if self.getCompileOk():
            return 0
        else:
            return 1


    def build(self):
        #global verbose
        outputDir = self.activeConfig()
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        exe_path = outputDir + "/" + self.exeName()
        exe = FileEntity(exe_path, exe_path)
        exe.addAction(Obj2ExeAction(self))
        update_dependency = PhonyEntity("update dependency graph")

        srcListOneByOne = []
        for src_path in self.m_sourceFilesPathList:
            srcList = glob.glob(src_path)
            srcListOneByOne += srcList

        for src_path in srcListOneByOne:

            srcName = os.path.basename(src_path)
            if srcName.endswith(".cpp"):
                objName = srcName.replace(".cpp", ".o")
            elif srcName.endswith(".c"):
                objName = srcName.replace(".c", ".o")
            obj_path = outputDir + "/" + objName

            obj = FileEntity(obj_path, obj_path)
            if srcName.endswith(".cpp"):
                obj.addAction(Cpp2ObjAction(self))
            elif srcName.endswith(".c"):
                obj.addAction(C2ObjAction(self))

            exe.addPrerequisite(obj)

            src = FileEntity(src_path, src_path)
            obj.addPrerequisite(src)

            optMgr = OptionManager()
            srcopt_path = optMgr.getOptionFilePath(src_path, self.activeConfig())
            srcopt = FileEntity(srcopt_path, srcopt_path)
            obj.addPrerequisite(srcopt)

            if srcName.endswith(".cpp"):
                depName = srcName.replace(".cpp", ".d")
            elif srcName.endswith(".c"):
                depName = srcName.replace(".c", ".d")
            dep_path = outputDir + "/" + depName
            if os.path.exists(dep_path):
                obj_update = PhonyEntity("update for " + obj_path)
                obj_update.addAction(UpdateDependencyGraphAction(obj))
                update_dependency.addPrerequisite(obj_update)

                dep = FileEntity(dep_path, dep_path)
                obj_update.addPrerequisite(dep)

        optMgr = OptionManager()
        exeopt_path = optMgr.getOptionFilePath(exe_path, self.activeConfig())
        exeopt = FileEntity(exeopt_path, exeopt_path)
        exe.addPrerequisite(exeopt)

        srcListFile = FileEntity('SOURCEFILES', 'SOURCEFILES')
        exe.addPrerequisite(srcListFile)


        self.buildGch()
        #print settings.verbose
        if settings.verbose:
            update_dependency.show()
        update_dependency.update()

        if settings.verbose:
            exe.show()
        exe.update()

        if self.getCompileOk() and self.getLinkOk():
            return 0
        else:
            return 1

    def buildGch(self):
        #global verbose
        if not os.path.exists("PRECOMPILEDHEADERS"):
            return
			
        outputDir = self.activeConfig()
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)

        all_gch = PhonyEntity("generate all gch")
        update_dependency = PhonyEntity("update dependency graph")

        headerListOneByOne = []
        for header_path in self.m_precompiledHeadersPathList:
            headerList = glob.glob(header_path)
            headerListOneByOne += headerList

        for header_path in headerListOneByOne:
            headerName = os.path.basename(header_path)

            gchDir = header_path + ".gch"
            if not os.path.exists(gchDir):
                os.mkdir(gchDir)

            gchName = self.activeConfig()

            gch_path = gchDir + "/" + gchName

            gch = FileEntity(gch_path, gch_path)
            gch.addAction(H2GchAction(self))

            all_gch.addPrerequisite(gch)

            header = FileEntity(header_path, header_path)
            gch.addPrerequisite(header)

            optMgr = OptionManager()
            headeropt_path = optMgr.getOptionFilePath(header_path, self.activeConfig())
            headeropt = FileEntity(headeropt_path, headeropt_path)
            gch.addPrerequisite(headeropt)

            depName = gchName + ".d"
            dep_path = gchDir + "/" + depName
            if os.path.exists(dep_path):
                gch_update = PhonyEntity("update for " + gch_path)
                gch_update.addAction(UpdateDependencyGraphAction(gch))
                update_dependency.addPrerequisite(gch_update)

                dep = FileEntity(dep_path, dep_path)
                gch_update.addPrerequisite(dep)

        if settings.verbose:
            update_dependency.show()
        update_dependency.update()

        if settings.verbose:
            all_gch.show()
        all_gch.update()
