from Action import *
from OptionManager import *
import os
from subprocess import *

class Cpp2ObjAction(Action):

    def __init__(self, prj):
        Action.__init__(self)
        self.m_prj = prj

    def prj(self):
        return self.m_prj

    def execute(self, target, allPre, changedPre):
        Action.execute(self, target, allPre, changedPre)

        cpp_path = allPre[0].path()
        obj_path = target.path()
        dep_path = obj_path.replace(".o", ".d")

        if self.m_prj.type() == "dll":
            cmd = "g++ -Wall -c -fPIC -o"
        else:
            cmd = "g++ -Wall -c -o"

        cmd += " " + obj_path

        for p in allPre:
            if p.path().endswith(".cpp"):
                cmd += " " + p.path()

        optMgr = OptionManager()
        options = optMgr.getOptionFor(cpp_path, self.m_prj.activeConfig())

        if not options == "":
            cmd = cmd + " " + options

        cmd += " -fpch-deps -MMD -MF " + dep_path

        #print cmd
        print "Compiling " + os.path.basename(cpp_path) + " ..."
        #os.system(cmd)
        retcode = call(cmd, shell=True)
        if retcode != 0:
            self.m_prj.setCompileOk(False)
