from Action import Action
from datetime import datetime

class DependencyGraphEntity:
    def __init__(self, name):
        self.m_name = name
        self.prerequisiteList = []
        self.actions = []

    def addPrerequisite(self, p):
        self.prerequisiteList.append(p)
        return self

    def name(self):
        return self.m_name

    def show(self, level=0, indent="  "):
        print level*indent, self.name()

        for p in self.prerequisiteList:
            p.show(level+1)
#        self.action.show()

    def timestamp(self):
        pass

    def addAction(self, a):
        self.actions.append(a)

    def executeActions(self, target, allPre, changedPre):
        for a in self.actions:
            a.execute(target, allPre, changedPre)

    def updatePrerequisites(self, changed):
        for p in self.prerequisiteList:
            
            oldStamp = p.timestamp()
            p.update()
            if p.timestamp() > oldStamp:
                changed.append(p)

    def update(self):
        pass
