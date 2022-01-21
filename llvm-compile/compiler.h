
/* compiler.h */

#ifndef COMPILER_H
#define COMPILER_H

#include <string>
#include <vector>
using namespace std;

class Compiler
{
   public:
      Compiler () { }
      void compileFile (string fileName);
      void compile (vector <string> options, vector <string> libraries);
   // private:
   //      void info (string msg);
   //      void error (string msg);
};

#endif

