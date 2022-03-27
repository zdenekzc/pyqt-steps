#!/bin/sh

use_sip6=false

if test -f /etc/arch-release ; then
   use_sip6=true
fi

if $use_sip6 ; then

   sip-build --verbose --target-dir=. --no-make

   ( cd _build && make )
   cp _build/highlight/libhighlight.so highlight.so
   
   # required file pyproject.toml
   python run.py

   # pacman -S sip (python-pyqt5-sip) python-pyqt5 pyqt-builder
   # conflict with sip4 python-sip4

   # dnf install sip6 python3-devel python3-qt5-devel

   # ArchLinux and Fedora 35 : RuntimeError: the PyQt5.QtCore module failed to register with the sip module

else

   test -f Makefile && make clean
   python configure.py || exit 1
   make || exit 1
   python run.py

   # dnf install python3-sip-devel python3-qt5-devel qt5-tools-devel
   # apt-get install pyqt5-dev python3-sip-dev qttools5-dev
   # pacman -S sip4 python-sip4 (python-pyqt5-sip) python-pyqt5 pkgconf

fi
