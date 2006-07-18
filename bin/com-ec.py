#!/usr/bin/python
"""Com.oonics Enterprisecopy

The comoonics Enterprisecopy binary parses an xml configfile and then goes through every copy and modificationset and
does it.

"""


# here is some internal information
# $Id: com-ec.py,v 1.3 2006-07-18 12:12:55 marc Exp $
#


__version__ = "$Revision: 1.3 $"
# $Source: /atix/ATIX/CVSROOT/nashead2004/management/comoonics-clustersuite/python/bin/Attic/com-ec.py,v $

from exceptions import Exception
import sys
import os
import xml.dom
from xml.dom.ext import PrettyPrint
from xml.dom.ext.reader import Sax2

sys.path.append("../lib")

import ComLVM
import ComSystem
import ComLog
import ComEnterpriseCopy
import ComCopyset
import ComModificationset
import getopt
import logging
import warnings

ComSystem.__EXEC_REALLY_DO=""

def line(str=None):
    print
    print "--------------------"+str+"---------------------------------"

def usage(argv):
    print "%s [-a|--ask] [-d|-debug] [-n|--novalidate] [-h|--help] xmlfilename" % argv[0]
    print '''
    executes all commands described in the <xmlfile>
    
    -a|--ask ask before any command is executed
    -d|--debug be more helpfull
    -n|--novalidate don't validate the xml. Handle with care!!!
    -c|--copset <name>|all only do all or the given modification set
    -m|--modificationset <name>|all only do all or the given modification set
    -h|--help: this helpscreen
    '''

def setWarnings():
    warnings.filterwarnings(action = 'ignore', message='tempnam.*', category=RuntimeWarning, module='Com*')
    
try:
    (opts, args_proper)=getopt.getopt(sys.argv[1:], 'hadnc:m:', [ 'help', 'ask', 'debug', 'novalidate', 'copyset', 'modificationset' ])
except getopt.GetoptError, goe:
    print "Error parsing params: %s", goe
    usage(sys.argv)
    sys.exit(1)

VALIDATE=True
DEBUG=False
ASK_MODE=False
ComLog.setLevel(logging.INFO)
copysetname=None
modsetname=None
for (opt, value) in opts:
#    print "Option %s" % opt
    if opt == "-a" or opt == "--ask":
        ASK_MODE=True
    elif opt == "-d" or opt == "--debug":
        DEBUG=True
        ComLog.setLevel(logging.DEBUG)
    elif opt == "-n" or opt == "--novalidate":
        VALIDATE=FALSE
    elif opt == "-c" or opt == "--copyset":
        copysetname=value
    elif opt == "-m" or opt == "--modificationset":
        modsetname=value
    elif opt == "-h" or opt == "--help":
        usage(sys.argv)
        sys.exit(0)

# filter warnings
setWarnings()

# create Reader object
if VALIDATE:
    reader = Sax2.Reader(validate=1)
else:
    reader = Sax2.Reader(validate=0)

if len(args_proper) > 0:
    filename=args_proper[0]
else:
    print "No file as input given exiting."
    usage(sys.argv)
    sys.exit(1)

try:
    file=os.fdopen(os.open(filename,os.O_RDONLY))
    line("Parsing document %s " % filename)
    doc = reader.fromStream(file)
    businesscopy=ComEnterpriseCopy.getEnterpriseCopy(doc.documentElement, doc)
    if ASK_MODE:
        ComSystem.__EXEC_REALLY_DO="ask"
except KeyboardInterrupt:
    ComLog.getLogger(ComEnterpriseCopy.EnterpriseCopy.__logStrLevel__).info("Leaving because of user signal")
    sys.exit(1)
    
try:
    if businesscopy.hasAttribute("name"):
        line("Execution of businesscopy %s" % (businesscopy.getAttribute("name")))
    else:
        line("Execution of businesscopy %s" % ("unknown"))

    if (not copysetname and not modsetname) or copysetname:
        line("Executing %s copysets %u" % (copysetname, len(businesscopy.copysets)))
        businesscopy.doCopysets(copysetname)

    if (not copysetname and not modsetname) or modsetname:
        line("Executing %s modificationsets %u" % (modsetname, len(businesscopy.modificationsets)))
        businesscopy.doModificationsets(modsetname)

    line("Successfully executed businesscopy.")
except KeyboardInterrupt:
    ComLog.getLogger(ComEnterpriseCopy.EnterpriseCopy.__logStrLevel__).info("Leaving because of user signal")
    sys.exit(1)
except Exception, e:
    ComLog.getLogger(ComEnterpriseCopy.EnterpriseCopy.__logStrLevel__).warn("Exception %s caught during copy." % e)
    import traceback
    traceback.print_exc()
    if not copysetname and not modsetname or modsetname:
        line("Undoing executing %s modificationsets %u" % (modsetname, len(businesscopy.modificationsets)))
        ComLog.getLogger(ComEnterpriseCopy.EnterpriseCopy.__logStrLevel__).warn("Undoing %s." % ComModificationset.Modificationset.TAGNAME)
        businesscopy.undoModificationsets(copysetname)
    if not copysetname and not modsetname or copysetname:
        line("Undoing executing %s copysets %u" % (copysetname, len(businesscopy.copysets)))
        ComLog.getLogger(ComEnterpriseCopy.EnterpriseCopy.__logStrLevel__).warn("Undoing %s." % ComCopyset.Copyset.TAGNAME)
        businesscopy.undoCopysets(modsetname)

    line("Errors during execution of enterprisecopy.")

##################
# $Log: com-ec.py,v $
# Revision 1.3  2006-07-18 12:12:55  marc
# minor change.
#
# Revision 1.2  2006/07/11 09:24:41  marc
# added commandswitches -m and -c
#
# Revision 1.1  2006/07/07 08:40:02  marc
# initial revision business is enterprise now.
#
# Revision 1.6  2006/07/05 13:06:50  marc
# support names on every tag.
#
# Revision 1.5  2006/07/04 11:38:21  mark
# added support for Ctrl-C interrupt
#
# Revision 1.4  2006/07/04 11:16:11  mark
# added setWarinings()
#
# Revision 1.3  2006/07/04 11:01:48  marc
# be a little more verbose
#
# Revision 1.2  2006/07/03 16:11:10  marc
# added commandline params
#
# Revision 1.1  2006/06/30 13:57:13  marc
# initial revision
#