
%Module highlight

%Import QtCore/QtCoremod.sip
%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

class Highlighter : public QObject
{

%TypeHeaderCode
#include <highlight.h>
%End

public:
      Highlighter (QTextDocument *parent = 0);
      bool enabled;
      bool isEnabled ();
      void setEnabled (bool value);
};
