"""

Init this package

"""
from exceptions import ImportError
try:
   import comoonics.backup.EMCLegato
   import comoonics.backup.SepSesam
except ImportError:
#    print "Could not import comoonics.backup.EMCLegato"
   pass
