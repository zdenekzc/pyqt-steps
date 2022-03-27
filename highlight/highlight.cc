
/* highlight.cc */

// #include "highlight.h"

#include <QSyntaxHighlighter>

/* ---------------------------------------------------------------------- */

Highlighter (QTextDocument *parent = nullptr)
      : QSyntaxHighlighter (parent)
{
   keywordFormat.setForeground (QColor ("darkRed"));
   identifierFormat.setForeground (QColor ("darkRed"));
   qidentifierFormat.setForeground (QColor ("green"));
   numberFormat.setForeground (QColor ("blue"));
   realFormat.setForeground (QColor ("magenta"));
   characterFormat.setForeground (QColor ("cornflowerblue"));
   stringFormat.setForeground (QColor ("blue"));
   separatorFormat.setForeground (QColor ("orange"));
   commentFormat.setForeground (QColor ("gray"));
}

/* ---------------------------------------------------------------------- */

inline bool isLetter (QChar c)
{
    return c >= 'A' && c <= 'Z' || c >= 'a' && c <= 'z' || c == '_';
}

inline bool isDigit (QChar c)
{
    return c >= '0' && c <= '9';
}

inline bool isLetterOrDigit (QChar c)
{
    return isLetter (c) || isDigit (c);
}

/* ---------------------------------------------------------------------- */

void highlightBlock (const QString & text)
{
    if (!enabled)
       return;

    bool use_cursor = true; // enable_info_property;
    QTextCursor cursor;
    int cursor_inx = 0;
    if (use_cursor)
    {
        cursor = QTextCursor (currentBlock ());
        cursor_inx = 0;
    }

    int cnt = text.length ();
    int inx = 0;
    bool inside_comment = previousBlockState () == 1;
    int start_comment = 0;

    while (inx < cnt)
    {
        if (inside_comment)
        {
            if (inx == 0)
                inx = 1;
            while (inx < cnt && (text[inx - 1] != '*' || text[inx] != '/')) inx++;
            if (inx < cnt)
            {
                inx = inx + 1;
                setFormat (start_comment, inx - start_comment, commentFormat);
                inside_comment = false;
            }
        }
        else
        {
            while (inx < cnt && text[inx] <= ' ') inx ++;
            int start = inx;
            if (inx < cnt)
            {
                QChar c = text [inx];
                QTextCharFormat fmt;
                if (use_cursor)
                {
                    cursor.movePosition (QTextCursor::NextCharacter, QTextCursor::MoveAnchor, inx + 1 - cursor_inx);
                    cursor_inx = inx + 1;
                    fmt = cursor.charFormat ();
                }
                if (isLetter (c))
                {
                    while (inx < cnt && isLetterOrDigit (text[inx])) inx ++;
                    if (use_cursor && fmt.hasProperty (infoProperty))
                       ; // nothing
                    else if (c == 'Q')
                       setFormat (start, inx - start, qidentifierFormat);
                    else
                       setFormat (start, inx - start, identifierFormat);
                }
                else if (isDigit (c))
                {
                    while (inx < cnt && isDigit (text[inx]))
                        inx = inx + 1;
                    if (use_cursor && fmt.hasProperty (infoProperty))
                        ; // nothing
                    else
                        setFormat (start, inx - start, numberFormat);
                }
                else if (c == '"')
                {
                    inx = inx + 1;
                    while (inx < cnt && text[inx] != '"') inx ++;
                    inx = inx + 1;
                    if (use_cursor && fmt.hasProperty (infoProperty))
                        ; // nothing
                    else
                        setFormat (start, inx - start, stringFormat);
                }
                else if (c == '\'')
                {
                    inx = inx + 1;
                    while (inx < cnt && text[inx] != '\'')
                        inx = inx + 1;
                    inx = inx + 1;
                    if (use_cursor && fmt.hasProperty (infoProperty))
                        ; // nothing
                    else
                        setFormat (start, inx - start, characterFormat);
                }
                else if (c == '/')
                {
                    inx = inx + 1;
                    if (inx < cnt && text[inx] == '/')
                    {
                        inx = cnt;
                        setFormat (start, inx - start, commentFormat);
                    }
                    else if (inx < cnt && text[inx] == '*')
                    {
                        inx = inx + 1;
                        inside_comment = true;
                        start_comment = inx - 2;
                    }
                    else if (use_cursor && fmt.hasProperty (infoProperty))
                        ; // nothing
                    else
                        setFormat (start, inx - start, separatorFormat);
                }
                else
                {
                    inx = inx + 1;
                    if (use_cursor && fmt.hasProperty (infoProperty))
                        ; // nothing
                    else
                        setFormat (start, inx - start, separatorFormat);
                }
            }
        }
    }

    if (inside_comment)
    {
        setFormat (start_comment, inx - start_comment, commentFormat);
        setCurrentBlockState (1);
    }
    else
    {
        setCurrentBlockState (0);
    }
}

/* ---------------------------------------------------------------------- */
