
#include "QApplication"
#include "QWidget"
#include "QPushButton"

int main (int argc, char * * argv)
{
     QApplication appl (argc, argv);

     QWidget * window = new QWidget ();
     window->resize (320, 240);
     window->show ();

     QPushButton * button = new QPushButton ("Press me", window);
     button->move (100, 100);
     button->show ();

     appl.exec ();
}
