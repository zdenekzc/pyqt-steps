#!/bin/env python
import faulthandler
faulthandler.enable ()
import compiler
comp = compiler.Compiler ()
comp.compileFile ("sample.cc")
