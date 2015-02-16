from DependencyGraphEntity import *
import os
from stat import *

class FileEntity(DependencyGraphEntity):

    def __init__(self, name, path):
        DependencyGraphEntity.__init__(self, name)
        self.m_path = path

    def path(self):
        return self.m_path

    def actualFileTimestamp(self):
        if not os.path.exists(self.m_path):
            timestamp = 0
        else:
            # timestamp is the modification time of file
            timestamp = os.stat(self.m_path)[ST_MTIME]
        return datetime.fromtimestamp(timestamp)


    def timestamp(self):
        return self.actualFileTimestamp()

    def update(self):
        # make all prerequisites
        changed = []
        self.updatePrerequisites(changed)

        # check to see if execution is needed
        needExecute = False
        for p in self.prerequisiteList:
            if p.timestamp() == datetime.fromtimestamp(0):
                # errMsg = "Cannot make `" + p.name() + "', needed by `" + self.name() + "'."
                errMsg = self.name() + ": cannot make `" + p.name() + "'"
                print errMsg
            if self.timestamp() < p.timestamp():
                needExecute = True
                break

        # execute action
        if needExecute:
            self.executeActions(self, self.prerequisiteList, changed)
