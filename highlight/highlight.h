
/* highlight.h */

#ifndef HIGHLIGHT_H
#define HIGHLIGHT_H

#include <QSyntaxHighlighter>

/* ---------------------------------------------------------------------- */

class Highlighter : public QSyntaxHighlighter
{
   private:
      const int infoProperty = QTextFormat::UserProperty + 2;

      QTextCharFormat keywordFormat;
      QTextCharFormat identifierFormat;
      QTextCharFormat qidentifierFormat;
      QTextCharFormat numberFormat;
      QTextCharFormat realFormat;
      QTextCharFormat characterFormat;
      QTextCharFormat stringFormat;
      QTextCharFormat separatorFormat;
      QTextCharFormat commentFormat;

   public:
      // Highlighter (QTextDocument *parent = 0);
      bool enabled = true;
      bool isEnabled () { return enabled; }
      void setEnabled (bool value) { enabled = value; }
      #include "highlight.cc"
};

// kate: indent-width 1; show-tabs true; replace-tabs true; remove-trailing-spaces all

#endif // HIGHLIGHT_H
