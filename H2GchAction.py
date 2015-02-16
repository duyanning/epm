from Action import *
from OptionManager import *
import os

class H2GchAction(Action):

    def __init__(self, prj):
        Action.__init__(self)
        self.m_prj = prj

    def prj(self):
        return self.m_prj

    def execute(self, target, allPre, changedPre):
        Action.execute(self, target, allPre, changedPre)

        h_path = allPre[0].path()
        gch_path = target.path()
        dep_path = gch_path + ".d"

        # we should remove old .d before generate new one
        # otherwise, we will get a warning message
        if os.path.exists(dep_path):
            os.remove(dep_path)

        cmd = "g++ -Wall -o"

        cmd += " " + gch_path

        cmd += " " + h_path

        optMgr = OptionManager()
        options = optMgr.getOptionFor(h_path, self.m_prj.activeConfig())

        if not options == "":
            cmd = cmd + " " + options

        cmd += " -fpch-deps -MMD -MF " + dep_path

        print "Precompiling " + os.path.basename(h_path) + " ..."
        #print cmd
        os.system(cmd)

