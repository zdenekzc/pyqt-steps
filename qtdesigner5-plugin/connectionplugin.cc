
#include "connectionwidget.h"
#include "connectionplugin.h"

#include <QtPlugin>

#include <QDBusConnection>
#include <QDBusInterface>
#include <QDBusReply>

#include <abstractintegration.h>

#include <iostream>
using namespace std;

ConnectionPlugin::ConnectionPlugin (QObject *parent) :
   QObject(parent) ,
   core (NULL),
   integration (NULL)
{
    cout << "PLUGIN CONSTRUCTOR" << endl;
}

void ConnectionPlugin::initialize (QDesignerFormEditorInterface * p_core)
{
    core = p_core;

    if (! initialized)
    {
        initialized = true;
        message = "initialized";
        connect ( core->parent(), SIGNAL (initialized ()), this, SLOT (setup ()) );
    }
}

void ConnectionPlugin::setup()
{
    cout << "SETUP" << endl;
    message = "setup";
    if (integration == NULL)
    {
        integration = core->integration();
        message = "integration";
        if (integration != NULL)
        {
           cout << "INTEGRATION" << endl;

           // integration->setSlotNavigationEnabled (true);

           integration->setFeatures (integration->features () | QDesignerIntegrationInterface::SlotNavigationFeature);

           // connect (integration, SIGNAL(navigateToSlot(QString, QString, QStringList)),
           //          this, SLOT(slotNavigateToSlot(QString, QString, QStringList)));


           typedef void (QDesignerIntegrationInterface::* F ) (const QString & objectName, const QString & signalSignature, const QStringList & parameterNames);

           QObject::connect (integration, (F) &QDesignerIntegrationInterface::navigateToSlot,
                             this, &ConnectionPlugin::slotNavigateToSlot);

           message = "ready";
        }
    }
}

void ConnectionPlugin::slotNavigateToSlot (const QString & objectName, const QString & signalSignature, const QStringList & parameterNames)
{
    cout << "SLOT" << endl;
    QDBusConnection bus = QDBusConnection::sessionBus();
    if (bus.isConnected ())
    {
        cout << "BUS" << endl;
        QDBusInterface ifc ("org.example.receiver", "/org/example/ReceiverObject", "org.example.ReceiverInterface", bus);
        if (ifc.isValid())
        {
            cout << "INTERFACE" << endl;
            ifc.call ("navigateToSlot", objectName, signalSignature, parameterNames);
            message = "sent";
        }
    }
}

bool ConnectionPlugin::isInitialized() const
{
    return initialized;
}

QWidget *ConnectionPlugin::createWidget(QWidget *parent)
{
    // setup ();
    ConnectionWidget * widget = new ConnectionWidget (parent);
    widget->setText (message);
    return widget;
}

QString ConnectionPlugin::name() const
{
    return "ConnectionWidget";
}

QString ConnectionPlugin::group() const
{
    return "Designer Connection";
}

QIcon ConnectionPlugin::icon() const
{
    return QIcon ();
}

QString ConnectionPlugin::toolTip() const
{
    return "Qt Designer plugin with DBus connection (Qt5)";
}

QString ConnectionPlugin::whatsThis() const
{
    return "";
}

bool ConnectionPlugin::isContainer() const
{
    return false;
}

QString ConnectionPlugin::domXml() const
{
    return "<ui language=\"c++\">\n"
           " <widget class=\"ConnectionWidget\" name=\"connectionWidget\">\n"
           " </widget>\n"
           "</ui>\n";
}

QString ConnectionPlugin::includeFile() const
{
    return "connectionplugin.h";
}
