class Configuration:
    def __init__(self):
        self.m_cxxOptions = {}
        pass

    def cxxOptions(self, item):
        if self.m_cxxOptions.has_key(item):
            return self.m_cxxOptions[item]
        else:
            return None

    def setCxxOptions(self, item, options):
        self.m_cxxOptions[item] = options
 
#     def linkOptions(self, item, options):
#         pass

#     def setLinkOptions(self, item, options):
#         pass
