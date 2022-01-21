#!/bin/sh
python llvm-tree.py `python gcc_options.py`  test-small.cc
