#!/bin/sh

insert_first () {
   local NAME=$1
   local NEW=$2
   eval VALUE=\"\$$NAME\"

   if test -z "$VALUE" ; then
      export $NAME="$NEW"
   else
      export $NAME="$NEW:$VALUE"
   fi
}

insert_first QT_PLUGIN_PATH _output/plugins

designer-qt5 $*
