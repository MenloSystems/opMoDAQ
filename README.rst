OpMoDAQ
=======

Python 3 package for monitoring, control and operation mode
configuration of Raspberry Pi DAQHATs.

Installation
------------

Clone this repository and install the following dependencies

For MCC DAQ device control:

* mcculw (Windows)
* daqhats (Raspberry Pi, Linux)

For DAQ device control on the RasPi (`opmodaq_srv.py`):

* numpy

For OpMoDAQ clients:

* numpy
* matplotlib
* tkinter (for native GUI `opmodaq_gui.py`) 
* jupyter (for interactive notebook `opmodaq_lab.jpys`)


Usage Quick Start
-----------------

Run, on the RasPi:

::

$ (raspi) python3 opmodaq_srv.py

This starts an instance of the device control backend.

