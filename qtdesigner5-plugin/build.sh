#!/bin/sh
test -f Makefile && make distclean
mkdir -p _output/plugins/designer
qmake-qt5 connectionplugin.pro || exit 1
make || exit 1
make install || exit 1
# sh designer.sh
