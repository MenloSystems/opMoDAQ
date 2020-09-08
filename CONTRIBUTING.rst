
Contributing
------------


Editable Installation
=====================

For an editable installation, change to the opmodaq root
directory where setup.py is located. From there, create a
virtual environment:

::
    
    python -m venv venv

Install opmodaq in editable mode:

::

    pip install -e .


Packaging
=========

The Python Packaging Tutorial is a good starting point:

https://packaging.python.org/tutorials/installing-packages/


Make sure you have the latest versions of setuptools and
wheel installed:

::

    python3 -m pip install --user --upgrade setuptools wheel


Now run this command from the same directory where *setup.py*
is located:

::

    python3 setup.py sdist bdist_wheel

