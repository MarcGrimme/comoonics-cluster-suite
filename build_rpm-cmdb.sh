#!/bin/bash

# $Id: build_rpm-cmdb.sh,v 1.2 2007-03-06 07:11:25 marc Exp $

source ./build-lib.sh

RELEASE=4
REQUIRES="--requires=comoonics-cs-py,MySQL-python"
NOAUTO_REQ="--no-autoreq"
NAME="comoonics-cmdb-py"
VERSION="0.1"
DESCRIPTION="Comoonics Softwaremanagement CMDB utilities and libraries written in Python"
LONG_DESCRIPTION="
Comoonics Softwaremanagement CMDB utilities and libraries written in Python
"
AUTHOR="Marc Grimme"
AUTHOR_EMAIL="grimme@atix.de"
URL="http://www.atix.de/comoonics/"
PACKAGE_DIR='"comoonics.cmdb" : "lib/comoonics/cmdb"'
PACKAGES='"comoonics.cmdb"'
SCRIPTS='"bin/com-channel2db", "bin/com-rpm2db", "bin/com-sysinfo", "bin/com-rpmdiffs"'
#DOCFILES="lib/comoonics/cmdb/sqlscripts/create-tables.sql"

setup

##############
# $Log: build_rpm-cmdb.sh,v $
# Revision 1.2  2007-03-06 07:11:25  marc
# not needed
#
# Revision 1.1  2007/03/05 21:12:18  marc
# first rpm version
#
#
