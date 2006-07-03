"""Comoonics modificationset module


here should be some more information about the module, that finds its way inot the onlinedoc

"""


# here is some internal information
# $Id: ComModificationset.py,v 1.4 2006-07-03 12:54:55 marc Exp $
#


__version__ = "$Revision: 1.4 $"
# $Source: /atix/ATIX/CVSROOT/nashead2004/management/comoonics-clustersuite/python/lib/Attic/ComModificationset.py,v $

import exceptions
import os

from ComDataObject import DataObject
import ComModification
import ComLog

log=ComLog.getLogger("ModificationSet")

def getModificationset(element, doc):
    """ Factory function to create Modificationset Objects"""
    __type=element.getAttribute("type")
    if __type == "filesystem":
        from ComFilesystemModificationset import FilesystemModificationset
        return FilesystemModificationset(element, doc)
    raise exceptions.NotImplementedError("Modifcicationset for type " + __type + " is not implemented")


class Modificationset(DataObject):
    TAGNAME = "modificationset"
    def __init__(self, element, doc):
        DataObject.__init__(self, element, doc)
        self.modifications=list()
        log.debug("Modificationset CWD: " + os.getcwd())
        
    def doModifications(self):
        """starts the modification process"""
        self.doPre()
        self.doRealModifications()
        self.doPost()

    def undoModifications(self):
        """undos all modifications """
        ComLog.getLogger(self.__logStrLevel__).debug("Modifications: %s" % self.modifications)
        self.modifications.reverse()
        for mod in self.modifications:
            try:
                mod.undoModification()
            except NotImplementedError, e:
                log.warning(e)
    
    def doPre(self):
        pass
    
    def doPost(self):
        pass
    
    def doRealModifications(self):
        for mod in self.modifications:
            try:
                mod.doModification()
            except NotImplementedError, e:
                log.warning(e)

    def getModifications(self):
        return self.modifications

    """
    privat methods
    """
    def createModificationsList(self, emods, doc):
        for i in range(len(emods)):
            self.modifications.append(ComModification.getModification(emods[i], doc))
        return self.modifications
   
# $Log: ComModificationset.py,v $
# Revision 1.4  2006-07-03 12:54:55  marc
# bugfixed undoing.
#
# Revision 1.3  2006/07/03 07:47:37  marc
# changed the list of modifications
#
# Revision 1.2  2006/06/30 12:38:35  marc
# added undo
#
# Revision 1.1  2006/06/30 08:04:41  mark
# initial checkin
#
