TreeScape Documentation
========================

TreeScape is a Jupyter-based visualization tool for performance data, enabling
users to programmatically render graphs. With TreeScape, you can load an
ensemble of `Caliper <https://github.com/LLNL/caliper>`_ performance files and
visualize the collective performance of an application across many runs.

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License

.. image:: https://img.shields.io/badge/Python-3.9+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

Features
--------

* **Multiple Data Readers**: Support for both CaliperReader and ThicketReader
* **Interactive Visualizations**: Stacked line charts with integrated flame graphs
* **Static Plotting**: Matplotlib-based multi-line charts for publication
* **Performance Tracking**: Track performance changes over time across multiple runs
* **Flexible Data Model**: Filter, sort, and analyze performance data programmatically
* **Export Capabilities**: Export visualizations to SVG format

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/LLNL/treescape.git
   cd treescape
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   import treescape as ts

   # Load Caliper performance files
   reader = ts.CaliReader("/path/to/cali/files")

   # Create a data model
   model = ts.TreeScapeModel(reader)

   # Create an interactive visualization
   viz = ts.StackedLine()
   viz.setXAxis("launchdate")
   viz.setYAxis("avg")
   viz.setDrillLevel(["main", "LagrangeLeapFrog"])
   viz.render(model)

.. code-block:: python

   # Or create a static matplotlib plot
   ml = ts.MultiLine(model)
   ml.plot_sums("launchdate", "main", "test")

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   concepts
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/readers
   api/models
   api/visualizations

.. toctree::
   :maxdepth: 1
   :caption: Additional Information

   contributing
   changelog
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
