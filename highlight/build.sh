#!/bin/sh

test -f Makefile && make clean
python configure.py || exit 1
make || exit 1
python run.py

# dnf install python3-sip-devel python3-qt5-devel qt5-tools-devel
# apt-get install pyqt5-dev python3-sip-dev qttools5-dev
# pacman -S sip python-sip python-pyqt5 python-pyqt5-sip pkgconf
