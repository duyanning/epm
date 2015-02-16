from Action import *
from OptionManager import *
import os
from subprocess import *

class C2ObjAction(Action):

    def __init__(self, prj):
        Action.__init__(self)
        self.m_prj = prj

    def prj(self):
        return self.m_prj

    def execute(self, target, allPre, changedPre):
        Action.execute(self, target, allPre, changedPre)

        c_path = allPre[0].path()
        obj_path = target.path()
        dep_path = obj_path.replace(".o", ".d")

        if self.m_prj.type() == "dll":
            cmd = "gcc -Wall -c -fPIC -o"
        else:
            cmd = "gcc -Wall -c -o"

        cmd += " " + obj_path
        for p in allPre:
            if p.path().endswith(".c"):
                cmd += " " + p.path()

        optMgr = OptionManager()
        options = optMgr.getOptionFor(c_path, self.m_prj.activeConfig())

        if not options == "":
            cmd = cmd + " " + options

        cmd += " -fpch-deps -MMD -MF " + dep_path

        print "Compiling " + os.path.basename(c_path) + " ..."
        #print cmd
        #os.system(cmd)
        retcode = call(cmd, shell=True)
        if retcode != 0:
            self.m_prj.setCompileOk(False)

