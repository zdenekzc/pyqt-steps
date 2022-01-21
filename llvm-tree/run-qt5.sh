#!/bin/sh
python llvm-tree.py `python gcc_options.py` `pkg-config Qt5Widgets --cflags` test-qt.cc
