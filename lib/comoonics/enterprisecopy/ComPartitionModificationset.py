""" Comoonics partition modificationset module


here should be some more information about the module, that finds its way inot the onlinedoc

"""


# here is some internal information
# $Id: ComPartitionModificationset.py,v 1.2 2007-03-26 08:02:23 marc Exp $
#


__version__ = "$Revision: 1.2 $"
# $Source: /atix/ATIX/CVSROOT/nashead2004/management/comoonics-clustersuite/python/lib/comoonics/enterprisecopy/ComPartitionModificationset.py,v $

import xml.dom
import exceptions
from xml import xpath
from xml.dom.ext import PrettyPrint
import os

from comoonics.ComExceptions import *
from ComModificationset import ModificationsetJournaled
from comoonics.ComDisk import HostDisk
from comoonics import ComLog

log=ComLog.getLogger("Modificationset")

class PartitionModificationset(ModificationsetJournaled):
    """ Base Class for all source and destination objects"""
    def __init__(self, element, doc):
        ModificationsetJournaled.__init__(self, element, doc)
        try:
            __disk=xpath.Evaluate('disk', element)[0]
            self.disk=HostDisk(__disk, doc)
        except Exception:
            raise ComException("disk for modificationset not defined")

        self.addToUndoMap(self.disk.__class__.__name__, "savePartitionTable", "restorePartitionTable")
        self.addToUndoMap(self.disk.__class__.__name__, "noPartitionTable", "deletePartitionTable")

    def doRealModifications(self):
        __tmp=os.tempnam("/tmp")
        for journal_command in self.disk.resolveDeviceName():
            self.journal(self.disk, journal_command)
        if self.disk.hasPartitionTable():
            self.disk.savePartitionTable(__tmp)
            self.journal(self.disk, "savePartitionTable", __tmp)
        else:
            self.journal(self.disk, "noPartitionTable")

        self.disk.createPartitions()


# $Log: ComPartitionModificationset.py,v $
# Revision 1.2  2007-03-26 08:02:23  marc
# - added support for resolvDeviceName()
# - changed Disk to HostDisk just for better understanding
#
# Revision 1.1  2006/12/08 09:43:08  mark
# initial check in - stable
#
