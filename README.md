
sMAP BACnet support
===================

This repository contains simple Python bindings for the Steve Karg's
bacnet-stack; in particular, it supports the use of the ReadProperty,
WriteProperty, and Who-Is BACnet services.

Build instructions
------------------
In order to build the python support, you must first build the BACnet
c library.  Download bacnet-stack-0.6 from here:
http://sourceforge.net/projects/bacnet/files/bacnet-stack/bacnet-stack-0.6.0/ and place it in src/.  We recommend using version 0.6.0; later versions may work too.  Build that source for your platform (on OSX, make sure you do everything with CC=gcc; none of this works wtih LLVM).

After that, you should be able to do the usual `python setup.py build` in order to swig and compile the python module.

Scanning instructions
---------------------
To use the sMAP driver, you first need to discover the points on your
subnet.  the ``bacnet-scan`` tool will help you with that.  Run with
no arguments, it will dump a list of all devices, as well as all
objects present in each device to the output file as a json data structure.

sMAP Driver
-----------
You can then use the ``pybacnet.driver.BACnetDriver`` module to poll
your BACnet points and send data to a sMAP server.  The driver contains several options for cleaning up BACnet names.