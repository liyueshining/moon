from xml.dom.minidom import parseString
from xml.dom import minidom
from MocNode import MocNode
import os
import sys

radioTypes = ['GSM', 'UMTS', 'TD', 'AG', 'MCE']


def getMocOrder(path):
    files = os.listdir(path)
    for afile in files:
        if afile.lower().endswith("-mocinfo-sdrm.xml"):
            mocinfoXML = open(afile, "r").read()
            mocinfoXML = mocinfoXML.replace('encoding="GBK"', 'encoding="utf-8"')
            mocOrder = MocOrder(mocinfoXML, path)
            mocOrder.generateMocOrderXML()


def getType(version):
    if version in radioTypes:
        return "radio"
    return "ground"


class MocOrder:
    def __init__(self, mocinfoxml, path):
        self.mocinfoxml = mocinfoxml
        self.filePath = path
        self.radioType = ''
        self.mocs = []
        self.mocNodes = {}

    def parsexml(self):
        domtree = parseString(self.mocinfoxml)
        domcument = domtree.documentElement

        if domcument.hasAttribute("version"):
            self.radioType = domcument.getAttribute("version")
        print "radioType is %s" % self.radioType

        mocinfos = domcument.getElementsByTagName("mocinfo")
        for mocinfo in mocinfos:
            mocNode = MocNode()
            name = mocinfo.getAttribute('name')
            parent = mocinfo.getAttribute('parent')
            self.mocs.append(name)
            mocNode.setName(name)
            mocNode.setParent(parent)
            print "mocInfo name is %s  parent is %s " % (name, parent)

            fields = mocinfo.getElementsByTagName("field")
            refmocs = []
            for field in fields:
                fieldName = field.getAttribute('name')
                if fieldName[0 : 3] == "ref":
                    if fieldName[3].isnumeric():
                        refmoc = fieldName[4:]
                    else:
                        refmoc = fieldName[3:]

                    if refmoc not in refmocs:
                        refmocs.append(refmoc)

            print "    ref field is %s" % refmocs
            mocNode.setRefmoc(refmocs)
            self.mocNodes[name] = mocNode

    def dealWithMocs(self):
        for mocNode in self.mocNodes:
            name = self.mocNodes[mocNode].name
            refmocs = self.mocNodes[mocNode].refmoc

            if len(refmocs) == 0:
                continue
            for refmoc in refmocs:
                if refmoc not in self.mocs:
                    continue
                if self.mocs.index(refmoc) < self.mocs.index(name):
                    continue
                if self.mocNodes[refmoc].parent == name:
                    continue
                selfIndex = self.mocs.index(name)
                refIndex = self.mocs.index(refmoc)
                self.mocs.remove(name)
                self.mocs.insert(selfIndex, refmoc)
                self.mocs.remove(refmoc)
                self.mocs.insert(refIndex, name)
        self.mocs.reverse()

    def generateMocOrderXML(self):
        self.parsexml()
        self.dealWithMocs()

        doc = minidom.Document()
        root = doc.createElement("root")
        doc.appendChild(root)

        orderedMocList = doc.createElement("orderedMocList")
        orderedMocList.setAttribute("mocType", getType(self.radioType))
        orderedMocList.setAttribute("version", self.radioType)
        for mo in self.mocs:
            moc = doc.createElement("moc")
            moc.setAttribute("name", mo)
            orderedMocList.appendChild(moc)

        root.appendChild(orderedMocList)

        if self.radioType in radioTypes:
            xmlName = self.radioType + "-" + getType(self.radioType) + "-cm-mocorder.xml"
        else:
            xmlName = self.radioType + "-cm-mocorder.xml"
        absoluteFilePath = self.filePath + "/" + xmlName
        xmlFile = file(absoluteFilePath, "w")
        doc.writexml(xmlFile, "\t", "  ", "\n", "UTF-8")
        xmlFile.close()

if __name__ == "__main__":
    print 'arguments passed is: ' + sys.argv[1]
    getMocOrder(sys.argv[1])
