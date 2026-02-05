Installation
============

Requirements
------------

TreeScape requires Python 3.9 or higher and the following dependencies:

* caliper-reader
* ipython
* llnl-hatchet
* llnl-thicket
* matplotlib
* numpy
* pandas
* jupyterlab

Installing from Source
----------------------

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/LLNL/treescape.git
   cd treescape

2. Create a virtual environment:

.. code-block:: bash

   python3 -m venv venv

3. Activate the virtual environment:

On Linux/macOS:

.. code-block:: bash

   source venv/bin/activate

On Windows:

.. code-block:: bash

   venv\Scripts\activate

4. Install the dependencies:

.. code-block:: bash

   pip install -r requirements.txt

5. Run Jupyter Lab:

.. code-block:: bash

   jupyter lab

Verifying Installation
----------------------

To verify that TreeScape is installed correctly, open a Python interpreter and try:

.. code-block:: python

   import treescape as ts
   print(ts.__file__)

This should print the path to the TreeScape installation directory without errors.

Development Installation
------------------------

For development, you may want to install in editable mode:

.. code-block:: bash

   pip install -e .

This allows you to modify the source code without reinstalling the package.
