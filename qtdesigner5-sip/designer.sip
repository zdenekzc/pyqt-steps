
%Module designer

%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

class Designer : public QObject
{

%TypeHeaderCode
#include <designer.h>
%End

public:
      Designer (QWidget * window = 0);

      QWidget * getForm ();

      QWidget * widgetBox ();
      QWidget * objectInspector ();

      QWidget * propertyEditor ();
      QWidget * actionEditor ();

      QWidget * resourceEditor ();
      QWidget * signalSlotEditor ();

      void open (QString fileName);
      void connectNavigation (QObject * target);
};
