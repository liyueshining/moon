class MocNode:
    def __init__(self):
        self.name = ''
        self.parent = ''
        self.refmoc = []

    def setName(self, name):
        self.name = name

    def setParent(self, parent):
        self.parent = parent

    def setRefmoc(self, refmoc):
        self.refmoc = refmoc
