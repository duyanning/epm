from FileEntity import *
from Action import *
import os

class UpdateDependencyGraphAction(Action):

    def __init__(self, obj):
        Action.__init__(self)
        self.m_obj = obj

    def execute(self, target, allPre, changedPre):
        Action.execute(self, target, allPre, changedPre)

        # analyze dependency file
        dep_path = allPre[0].path()
        f = open(dep_path, "r")
        nameList = []
        content = f.read()
        nameList = content.split()

        # skip the first and second
        for t in nameList[2:]:
            if t != "\\":
                self.m_obj.addPrerequisite(FileEntity(t, t))
