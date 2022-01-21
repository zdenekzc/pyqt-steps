
/* designer.h */

#ifndef DESIGNER_H
#define DESIGNER_H

#include <QtDesigner/QtDesigner>
#include <QtDesigner/QDesignerComponents>
#include <QtDesigner/QDesignerIntegration>

/* ---------------------------------------------------------------------- */

class LocalDesignerIntegration : public QDesignerIntegration
{
   public:
      explicit LocalDesignerIntegration(QDesignerFormEditorInterface * core, QObject *parent = 0) :
         QDesignerIntegration (core, parent)
      {
         // setSlotNavigationEnabled (true);
         setFeatures (features () | SlotNavigationFeature);
      }
};

/* ---------------------------------------------------------------------- */

class Designer : public QObject
{
   private:
      QDesignerFormEditorInterface * core;
      QDesignerFormWindowInterface * form;
      QDesignerIntegration * integration;
      // LocalDesignerIntegration * integration;
      QWidget * resource_editor;
      QWidget * signal_slot_editor;

   public:

      Designer (QWidget * window = 0) :
         QObject (window),
         core (NULL),
         form (NULL),
         integration (NULL),
         resource_editor (NULL),
         signal_slot_editor (NULL)
      {
          // QDesignerComponents::initializeResources();

          core = QDesignerComponents::createFormEditor (window);

          core->setWidgetBox (QDesignerComponents::createWidgetBox (core, window));
          core->setObjectInspector (QDesignerComponents::createObjectInspector (core, window));

          core->setPropertyEditor (QDesignerComponents::createPropertyEditor (core, window));
          core->setActionEditor (QDesignerComponents::createActionEditor (core, window));

          resource_editor = QDesignerComponents::createResourceEditor (core, window);
          signal_slot_editor = QDesignerComponents::createSignalSlotEditor (core, window);

          // create propertyEditor before QDesignerIntegration
          // otherwise changes in propertyEditor are not displayed on designed form

          // create QDesignerIntegration before createFormWindow
          // otherwise propertyEditor and objectInspector are not updated when user selects designed widget

          // integration =  new QDesignerIntegration (core, window);
          integration = new LocalDesignerIntegration (core, window);
          QDesignerIntegration::initializePlugins (core);

          /*
          for (QObject * plugin : QPluginLoader::staticInstances())
          {
             QDesignerFormEditorPluginInterface *fep;
             fep = qobject_cast < QDesignerFormEditorPluginInterface * > (core);
             if (fep != NULL)
                 fep->initialize (core);
          }
          */

          form = core->formWindowManager()->createFormWindow();
 
          core->setTopLevel (window);
          core->formWindowManager()->setActiveFormWindow (form);
      }

      QWidget * getForm () { return form; }

      QWidget * widgetBox () { return core->widgetBox (); }
      QWidget * objectInspector () { return core->objectInspector (); }

      QWidget * propertyEditor () { return core->propertyEditor(); }
      QWidget * actionEditor () { return core->actionEditor(); }

      QWidget * resourceEditor () { return resource_editor; }
      QWidget * signalSlotEditor () { return signal_slot_editor; }

      void open (QString fileName)
      {
         QFile file (fileName);
         file.open (QFile::ReadOnly);
         form->setContents (&file);
      }

      void connectNavigation (QObject * target)
      {
          connect (integration, SIGNAL(navigateToSlot(QString, QString, QStringList)),
                   target, SLOT(navigateToSlot(QString, QString, QStringList)));
      }
};

/* ---------------------------------------------------------------------- */

#endif
