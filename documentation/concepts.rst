Core Concepts
=============

Understanding TreeScape's architecture will help you use it effectively.

Readers
-------
Readers are responsible for loading and parsing Caliper performance files.  There are multiple readers and you need to choose the right one for your use case.


Data Flow
---------

TreeScape follows a simple data flow:

.. code-block:: text

   Caliper Files (.cali)
          ↓
      Reader (CaliReader or ThicketReader)
          ↓
      TreeScapeModel (collection of Runs)
          ↓
      Visualization (StackedLine or MultiLine)


CaliReader
~~~~~~~~~~

The primary reader, optimized for performance:

* Uses multiprocessing to load files in parallel
* Supports directories, single files, or lists of paths
* Automatically merges data from multiple runs
* Creates performance tree hierarchies

.. code-block:: python

   reader = ts.CaliReader(
       path="/path/to/files",
       pool_size=10,  # Number of parallel processes
       inclusive_strings=None  # Custom metric names
   )

ThicketReader
~~~~~~~~~~~~~

Alternative reader using the Thicket library:

* Leverages Thicket's DataFrame-based processing
* Good for integration with existing Thicket workflows
* Requires Thicket to be installed

.. code-block:: python

   import thicket as tt
   th_ens = tt.Thicket.from_caliperreader(profiles)
   reader = ts.ThicketReader(th_ens, profiles, xaxis="launchdate")

TreeScapeModel
--------------

The TreeScapeModel is a collection of Run objects representing individual performance runs.  You need a treescapeModel to use the visualizations.
It's purpose is to hold the data in a format that the visualizations can understand.  It's also iterable, so you can use it like a list.

Structure
~~~~~~~~~

.. code-block:: python

   model = TreeScapeModel(reader)

   # Access metadata types
   meta_globals = model.get_meta_globals()

   # Access call tree hierarchy
   children_map = model.get_children_map()

   # Iterate over runs
   for run in model:
       # Each run has:
       run.metadata    # Dict of run metadata (launchdate, problem_size, etc.)
       run.perftree    # Dict of node_name -> metrics
       run.childrenMap # Dict of parent -> children relationships

Run Objects
~~~~~~~~~~~

Each Run represents a single performance measurement:

.. code-block:: python

   run = model[0]

   # Access metadata
   launch_date = run.getMetaData("launchdate")

   # Access performance data
   main_avg = run.getPerfTree("main", "avg")

   # Get node relationships
   children = run.getChildrenForNode("main")

Performance Metrics
-------------------

TreeScape can track multiple metrics for each function.  For example, if you are using caliper, you can specify which metrics you want to track.  By default, Caliper uses the following:

.. code-block:: python

    # Specify custom inclusive metric strings
    custom_metrics = [
        "min#inclusive#sum#time.duration",
        "max#inclusive#sum#time.duration",
        "sum#inclusive#sum#time.duration",
        "avg#inclusive#sum#time.duration",
    ]

    reader = ts.CaliReader(
        path=cali_file_loc,
        inclusive_strings=custom_metrics
    )

    model = ts.TreeScapeModel(reader)

    viz = ts.StackedLine()
    viz.render(model)


You can pick whatever metrics you like.  The above are just the defaults.  Metrics (avg, max, min, sum) are across mpi Ranks.

* **sum**: Total inclusive time across all calls
* **avg**: Average inclusive time per call
* **min**: Minimum inclusive time observed
* **max**: Maximum inclusive time observed

These metrics are stored in the ``perftree`` dictionary:

.. code-block:: python

   run.perftree["main"] = {
       "sum": 150.5,
       "avg": 75.25,
       "min": 70.0,
       "max": 80.5
   }

Call Tree Hierarchy
-------------------

The data comes from Caliper.  TreeScape maintains parent-child relationships between functions using ``childrenMap``:

.. code-block:: python

   run.childrenMap = {
       "main": ["compute", "io", "finalize"],
       "compute": ["kernel_A", "kernel_B"],
       "io": ["read_data", "write_data"]
   }

This hierarchy enables:

* Flame graph visualization
* Drill-down analysis
* Call path reconstruction

X-Axis Metadata
---------------

The X-axis in TreeScape plots represents metadata from your Caliper runs:

* **launchdate/launchday**: Timestamp of the run
* **problem_size**: Size of the problem being solved
* **jobsize**: Number of MPI ranks or threads
* **iterations**: Number of iterations performed
* Custom metadata fields you've added to Caliper

Aggregation
-----------

When multiple runs share the same X-axis value, TreeScape aggregates them:

* **sum**: Add all values together
* **avg**: Take the average of all values
* **max**: Take the maximum value
* **min**: Take the minimum value
* **topmax**: Special aggregation for stacked visualizations

Visualizations
--------------

StackedLine
~~~~~~~~~~~

Interactive Jupyter visualization with:

* **Line graphs**: Show performance over X-axis
* **Flame graphs**: Show call tree hierarchy at selected point
* **Drill-down**: Click to explore deeper into call tree
* **Color coding**: Consistent colors across views

MultiLine
~~~~~~~~~

Static MultiLine plots for:

* Multiple test series on one plot
* Publication-quality figures
* Date-aware X-axis formatting
* Customizable appearance

Filtering and Sorting
----------------------

The TreeScapeModel is a Python list, so you can use standard operations:

.. code-block:: python

   # Filter by problem size
   large_runs = [r for r in model if r.metadata["problem_size"] > 1000]

   # Sort by date
   sorted_runs = sorted(model, key=lambda x: x.metadata["launchdate"])

   # Filter by date range
   recent = [r for r in model
             if r.metadata["launchdate"] > 1609459200]

   # Create new model with filtered data
   new_model = ts.TreeScapeModel(reader, filtered_runs)

Performance Optimization
------------------------

CaliReader uses several optimizations:

* **Multiprocessing**: Loads files in parallel (configurable with ``pool_size``)
* **Per-file indexing**: Maintains separate indices per X-axis value
* **Lazy evaluation**: Only computes childrenMap when needed
* **Efficient merging**: Combines data from multiple files efficiently

Best Practices
--------------

1. **Use appropriate pool_size**: Match to your CPU core count
2. **Filter early**: Apply filters before visualization for better performance
3. **Choose the right reader**: CaliReader for large datasets, ThicketReader for Thicket integration
4. **Cache models**: Store TreeScapeModel if you'll reuse it
5. **Sort data**: Sort by X-axis before plotting for better visualization

Next Steps
----------

* See :doc:`examples` for practical applications
* Read :doc:`api/readers` for detailed API documentation
