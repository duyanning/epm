from Action import *
import os

class Yacc2CppAction(Action):

    def __init__(self, prj):
        Action.__init__(self)
        self.m_prj = prj

    def prj(self):
        return self.m_prj

    def execute(self, target, allPre, changedPre):
        Action.execute(self, target, allPre, changedPre)

        cpp_path = target.path()
        h_path = cpp_path.replace(".cpp", ".h")
        y_path = allPre[0].path()
        cmd = "bison" + " -o " + cpp_path + " --defines=" + h_path + " " + y_path

        print cmd
        os.system(cmd)

