
%Module compiler

// Fedora: ModuleNotFoundError: No module named 'sip'
%Import QtGui/QtGuimod.sip

class Compiler
{

%TypeHeaderCode
#include <compiler.h>
%End

public:
      Compiler ();
      void compileFile (std::string fileName);
      void compile (std::vector <std::string> options, std::vector <std::string> libraries);
};

%ModuleCode
#include "compiler.cc"
%End

// from http://github.com/dboddie/python-diana/blob/master/sip/std/std.sip
// see http://stackoverflow.com/questions/38595200/extract-a-python-str-with-c-api-compatible-with-python-23
// see http://www.itopen.it/python-sip-c-bindings-experiments/

%MappedType std::string
{
    %TypeHeaderCode
    #include <string>
    %End

    %ConvertToTypeCode
    if (sipIsErr == NULL)
    {
        // if (!PyString_Check(sipPy))
        if (!PyUnicode_Check(sipPy))
            return 0;
        else
            return 1;
    }

    // std::string *s = new std::string(PyString_AsString(sipPy));
    std::string *s = new std::string(PyUnicode_AsUTF8(sipPy));
    *sipCppPtr = s;

    return sipGetState(sipTransferObj);
    %End

    %ConvertFromTypeCode
    // PyObject *s = PyString_FromString(sipCpp->c_str());
    PyObject *s = PyUnicode_FromString(sipCpp->c_str());

    return s;
    %End
};

// from http://github.com/shotgunsoftware/cplusplus-api/blob/master/plugins/python/sip/mappedTypes.sip
%MappedType std::vector<std::string>
{
%TypeHeaderCode
#include <vector>
%End

%ConvertFromTypeCode
    PyObject *pList = NULL;

    // Create the Python list of the correct length.
    if ((pList = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Go through each element in the C++ instance and convert it to the
    // corresponding Python object.
    for (SIP_SSIZE_T i = 0; i < SIP_SSIZE_T(sipCpp->size()); ++i)
    {
        PyObject *pObj;

        // if ((pObj = PyString_FromString((*sipCpp)[i].c_str())) == NULL)
        if ((pObj = PyUnicode_FromString((*sipCpp)[i].c_str())) == NULL)
        {
            Py_DECREF(pList);

            return NULL;
        }

        PyList_SET_ITEM(pList, i, pObj);
    }

    // Return the Python list.
    return pList;
%End

%ConvertToTypeCode
    if (sipIsErr == NULL)
    {
        return (PySequence_Check(sipPy) && PySequence_Size(sipPy) >= 0);
    }

    std::vector<std::string> *stdVector = new std::vector<std::string>;
    SIP_SSIZE_T len = PySequence_Size(sipPy);

    for (SIP_SSIZE_T i = 0; i < len; ++i)
    {
        PyObject *itm = PySequence_ITEM(sipPy, i);

        if (!itm)
        {
            delete stdVector;
            *sipIsErr = 1;

            return 0;
        }

        // stdVector->push_back(PyString_AS_STRING(itm));
        stdVector->push_back(PyUnicode_AsUTF8(itm));

        Py_DECREF(itm);
    }

    // Return the instance on the heap.
    *sipCppPtr = stdVector;

    // Apply the normal transfer.
    return sipGetState(sipTransferObj);
%End

};
