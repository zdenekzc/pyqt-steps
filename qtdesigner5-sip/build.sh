#!/bin/sh

test -f Makefile && make clean
python3 configure.py || exit 1
make || exit 1
python3 run.py
# gdb -ex r --args python3 run.py

# dnf install python3-sip-devel
# dnf install python3-qt5-devel
# dnf install qt5-tools-devel

# apt-get install pyqt5-dev python3-sip-dev qttools5-dev

# pacman -S sip
# pacman -S python-sip
# pacman -S python-pyqt5
# pacman -S python-pyqt5-sip
# pacman -S pkgconf
