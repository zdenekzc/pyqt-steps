#!/bin/env python -B

import os
import sipconfig
from PyQt5 import QtCore

sip_inc_fedora = "/usr/share/python3-sip/PyQt5"
sip_inc_debian = "/usr/share/sip/PyQt5"
sip_inc_archlinux = "/usr/lib/python3.9/site-packages/PyQt5/bindings"

basename = "designer"

# The name of the SIP build file generated by SIP and used by the build system.
build_file = basename + ".sbf"

# Get the SIP configuration information.
config = sipconfig.Configuration()

# Run SIP to generate the code.
os.system(" ".join([config.sip_bin, "-c", ".", "-b", build_file,
                    "-I" + sip_inc_fedora,
                    "-I" + sip_inc_debian,
                    "-I" + sip_inc_archlinux,
                    QtCore.PYQT_CONFIGURATION["sip_flags"],
                    basename + ".sip"]))

# Create the Makefile.
makefile = sipconfig.SIPModuleMakefile(config, build_file)

# makefile.extra_include_dirs = [ "/usr/include/qt5",
#                                 "/usr/include/qt5/QtCore",
#                                 "/usr/include/qt5/QtGui",
#                                 "/usr/include/qt5/QtWidgets",
#                                 "/usr/include/qt5/QtDesigner"
#                                 ]

# makefile.extra_libs = ["Qt5Widgets", "Qt5Gui", "Qt5Core", "Qt5Designer", "Qt5DesignerComponents" ]

cflags = os.popen ("pkg-config Qt5Widgets --cflags").read()
libs = os.popen ("pkg-config Qt5Widgets --libs").read()

makefile.extra_cxxflags = cflags.split ()
makefile.extra_lflags = libs.split ()
makefile.extra_libs = [ "Qt5Designer", "Qt5DesignerComponents" ]

# Generate the Makefile itself.
makefile.generate()

# /usr/lib/python3.6/site-packages/sipconfig.py
# /usr/include/qt5
# /usr/share/python3-sip/PyQt5

# https://github.com/zanton/hello-sip-pyqt5
