from DependencyGraphEntity import *
from datetime import datetime

class PhonyEntity(DependencyGraphEntity):
    def __init__(self, name):
        DependencyGraphEntity.__init__(self, name)

    def timestamp(self):
        return datetime.now()

    def update(self):
        changed = []
        self.updatePrerequisites(changed)

        self.executeActions(self, self.prerequisiteList, changed)
