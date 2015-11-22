import os
import sys
import Helper

class OptionManager:

    def __init__(self):
        pass

    def readOption(self, f):
        options = ""
        for line in f:
            line = Helper.trim_comment(line)
            line = line.rstrip()
            if not line == "":
#                print "len: ", len(line)
                options += line + " "
        options = options.rstrip()
        return options

    def getOptionFilePath(self, filename, config):
        optionFilePath = filename + "-" + config + ".options"
        if os.access(optionFilePath, os.R_OK):
            return optionFilePath

        if filename.endswith(".cpp") or filename.endswith(".h"):
            optionFilePath = "generalcxx" + "-" + config + ".options"
            if os.access(optionFilePath, os.R_OK):
                return optionFilePath

            optionFilePath = "generalcxx" + "-" + "any" + ".options"
            if os.access(optionFilePath, os.R_OK):
                return optionFilePath

            epmdir = os.path.dirname(sys.argv[0]) + "/"
            optionFilePath = epmdir + "defaultcxx" + "-" + config + ".options"
            if os.access(optionFilePath, os.R_OK):
                return optionFilePath

            optionFilePath = epmdir + "defaultcxx" + "-" + "any" + ".options"
            if os.access(optionFilePath, os.R_OK):
                return optionFilePath

        elif filename.endswith(".c"):
            optionFilePath = "generalc" + "-" + config + ".options"
            if os.access(optionFilePath, os.R_OK):
                return optionFilePath

            optionFilePath = "generalc" + "-" + "any" + ".options"
            if os.access(optionFilePath, os.R_OK):
                return optionFilePath

            epmdir = os.path.dirname(sys.argv[0]) + "/"
            optionFilePath = epmdir + "defaultc" + "-" + config + ".options"
            if os.access(optionFilePath, os.R_OK):
                return optionFilePath

            optionFilePath = epmdir + "defaultc" + "-" + "any" + ".options"
            if os.access(optionFilePath, os.R_OK):
                return optionFilePath

        else:
            optionFilePath = "generallink" + "-" + config + ".options"
            if os.access(optionFilePath, os.R_OK):
                return optionFilePath

            optionFilePath = "generallink" + "-" + "any" + ".options"
            if os.access(optionFilePath, os.R_OK):
                return optionFilePath

            epmdir = os.path.dirname(sys.argv[0]) + "/"
            optionFilePath = epmdir + "defaultlink" + "-" + config + ".options"
            if os.access(optionFilePath, os.R_OK):
                return optionFilePath

            optionFilePath = epmdir + "defaultlink" + "-" + "any" + ".options"
            if os.access(optionFilePath, os.R_OK):
                return optionFilePath

        return ""

    def getOptionFor(self, filename, config):
        optionFilePath = self.getOptionFilePath(filename, config)
        f = open(optionFilePath, 'r')
        return self.readOption(f)
