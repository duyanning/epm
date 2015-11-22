from Action import *
import os

class Lex2CppAction(Action):

    def __init__(self, prj):
        Action.__init__(self)
        self.m_prj = prj

    def prj(self):
        return self.m_prj

    def execute(self, target, allPre, changedPre):
        Action.execute(self, target, allPre, changedPre)

        cpp_path = target.path()
        h_path = cpp_path.replace(".cpp", ".h")
        l_path = allPre[0].path()
        cmd = "flex" + " --outfile=" + cpp_path + " --header-file=" + h_path + " " + l_path

        print cmd
        os.system(cmd)

