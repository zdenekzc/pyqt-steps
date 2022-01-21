#!/bin/sh

test -f Makefile && make clean
python3 configure.py || exit 1
make || exit 1
python3 run.py

# dnf install python3-sip-devel
# dnf install clang-devel llvm-devel

# apt-get install python3-sip-dev
# apt-get install llvm clang libclang-dev

# pacman -S sip
# pacman -S python-sip
# pacman -S clang

# Fedora: ModuleNotFoundError: No module named 'sip'
#  or Unable to find file "QtGui/QtGuimod.sip"
# dnf install python3-qt5-devel
# apt-get install pyqt5-dev
# pacman -S python-pyqt5 python-pyqt5-sip

# Debian 10, clang 6
# apt-get install libclang-6.0-dev

# Debian 10, clang 8 from backports
# apt-get install libclang-8-dev clang-8
