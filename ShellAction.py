from Action import *
import os

class ShellAction(Action):

    def __init__(self, script):
        self.m_script = script

    def execute(self, target, allPre, changedPre):
        Action.execute(self, target, allPre, changedPre)
        print self.m_script
        os.system(self.m_script)
