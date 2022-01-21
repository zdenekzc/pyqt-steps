
#ifndef CONNECTIONPLUGIN_H
#define CONNECTIONPLUGIN_H

#include <QtUiPlugin/QDesignerCustomWidgetInterface>

#include <QDesignerFormEditorInterface>
#include <QDesignerIntegration>

class ConnectionPlugin : public QObject, public QDesignerCustomWidgetInterface
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QDesignerCustomWidgetInterface")
    Q_INTERFACES(QDesignerCustomWidgetInterface)

public:
    explicit ConnectionPlugin (QObject *parent = nullptr);

    bool isContainer () const override;
    bool isInitialized () const override;
    QIcon icon () const override;
    QString domXml () const override;
    QString group () const override;
    QString includeFile () const override;
    QString name () const override;
    QString toolTip () const override;
    QString whatsThis () const override;
    QWidget * createWidget (QWidget *parent) override;
    void initialize (QDesignerFormEditorInterface * p_core) override;

private:
    bool initialized = false;

private:
    QDesignerFormEditorInterface * core;
    QDesignerIntegrationInterface * integration;
    QString message;

private slots:
    void setup ();
    void slotNavigateToSlot (const QString &objectName, const QString &signalSignature, const QStringList &parameterNames);
};

#endif
