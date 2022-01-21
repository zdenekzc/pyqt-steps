#!/bin/sh
test -f Makefile && make distclean
rm -rf _output
rm -f .qmake.stash
rm -f moc_predefs.h
rm -f Makefile
