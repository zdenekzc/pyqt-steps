/* ---------------------------------------------------------------------- */

#if 0

#include <stdio.h>
#include <execinfo.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>

extern "C" void handler (int sig)
{
  void *array [10];
  size_t size;

  // get void*'s for all entries on the stack
  size = backtrace (array, 10);

  // print out all the frames to stderr
  fprintf (stderr, "Error: signal %d:\n", sig);
  backtrace_symbols_fd (array, size, STDERR_FILENO);
  exit (1);
}

#endif

/* ---------------------------------------------------------------------- */

#include <iostream>
using namespace std;
extern "C" int __dso_handle () { return 0; } // required when linking -lstdc++

/* ---------------------------------------------------------------------- */

#include "QApplication"
#include "QWidget"
#include "QPushButton"
#include "QStringList"
#include "QTreeWidget"

int main (int argc, char * * argv)
{
     // signal(SIGSEGV, handler);

     printf ("point 1 \n");

     // QApplication appl (argc, argv); // already done by PyQt

     cout << "point 2" << endl;

     QWidget * window = new QWidget ();
     window->resize (320, 240);
     window->show ();

     QPushButton * button = new QPushButton ("Press me", window);
     button->move (100, 100);
     button->show ();

     // appl.exec (); // PyQt
}
