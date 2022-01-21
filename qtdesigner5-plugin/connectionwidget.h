
#ifndef CONNECTIONWIDGET_H
#define CONNECTIONWIDGET_H

#include <QPushButton>
#include <QtUiPlugin/QDesignerExportWidget>

class QDESIGNER_WIDGET_EXPORT ConnectionWidget : public QPushButton
{
Q_OBJECT
public:
    explicit ConnectionWidget (QWidget *parent = nullptr);
};

#endif
