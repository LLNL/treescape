Models API
==========

TreeScape's data model consists of TreeScapeModel (collection of runs) and Run (individual performance measurements).

TreeScapeModel
--------------

.. class:: TreeScapeModel(reader, updated_list=None)

   Collection of Run objects representing performance data across multiple runs.

   Extends Python's list class, so all list operations are supported.

   :param reader: A Reader object (CaliReader or ThicketReader)
   :type reader: Reader
   :param updated_list: Optional list of Run objects to initialize with
   :type updated_list: list[Run] or None

   .. code-block:: python

      import treescape as ts

      # Create from reader
      reader = ts.CaliReader("/path/to/files")
      model = ts.TreeScapeModel(reader)

      # Create from filtered runs
      filtered_runs = [r for r in model if r.metadata["problem_size"] > 100]
      new_model = ts.TreeScapeModel(reader, filtered_runs)

   **Attributes:**

   .. attribute:: runs

      List of Run objects in the model.

      :type: list[Run]

   .. attribute:: childrenMap

      Global mapping of parent nodes to their children.

      :type: dict[str, list[str]]

      .. code-block:: python

         model = ts.TreeScapeModel(reader)
         print(model.childrenMap["main"])
         # Output: ["initialization", "computation", "finalization"]

   .. attribute:: meta_globals

      Metadata type information for all runs.

      :type: dict[str, str]

      .. code-block:: python

         print(model.meta_globals)
         # Output: {"launchdate": "int", "problem_size": "int", "test": "string"}

   **Methods:**

   .. method:: get_meta_globals()

      Get metadata type information.

      :return: Dictionary mapping metadata keys to types
      :rtype: dict[str, str]

      .. code-block:: python

         meta = model.get_meta_globals()
         if meta["launchdate"] == "int":
             print("Launch date is numeric")

   .. method:: get_children_map()

      Get the global children map.

      :return: Dictionary mapping parent nodes to children
      :rtype: dict[str, list[str]]

      .. code-block:: python

         children_map = model.get_children_map()
         for parent, children in children_map.items():
             print(f"{parent} -> {children}")

   .. method:: update(new_tsm_list)

      Replace the runs in the model with a new list.

      :param new_tsm_list: New list of Run objects
      :type new_tsm_list: list[Run]

      .. code-block:: python

         # Filter and update
         fast_runs = [r for r in model if r.perftree["main"]["avg"] < 10.0]
         model.update(fast_runs)

   .. method:: get_entire_tsm()

      Get the complete model as a dictionary.

      :return: Dictionary with nodes, childrenMap, and meta_globals
      :rtype: dict

      .. code-block:: python

         data = model.get_entire_tsm()
         print(data.keys())  # dict_keys(['nodes', 'childrenMap', 'meta_globals'])

   .. method:: sort(metadata_key)

      Sort runs by a metadata key (in-place).

      :param metadata_key: Metadata field to sort by
      :type metadata_key: str

      .. code-block:: python

         model.sort("launchdate")  # Sort by date
         model.sort("problem_size")  # Sort by size

   **List Operations:**

   Since TreeScapeModel extends list, you can use standard list operations:

   .. code-block:: python

      model = ts.TreeScapeModel(reader)

      # Length
      print(f"Number of runs: {len(model)}")

      # Indexing
      first_run = model[0]
      last_run = model[-1]

      # Slicing
      first_ten = model[:10]
      last_five = model[-5:]

      # Iteration
      for run in model:
          print(run.metadata)

      # List comprehension
      large_runs = [r for r in model if r.metadata["problem_size"] > 1000]

      # Filtering
      recent = [r for r in model if r.metadata["launchdate"] > 1609459200]

      # Sorting (returns new list)
      sorted_runs = sorted(model, key=lambda r: r.metadata["launchdate"])

      # Check membership
      if first_run in model:
          print("Run found")

Run
---

.. class:: Run(metadata, perftree, reader, childrenMap=None)

   Represents a single performance run.

   :param metadata: Dictionary of run metadata (launchdate, problem_size, etc.)
   :type metadata: dict
   :param perftree: Dictionary mapping node names to their metrics
   :type perftree: dict[str, dict]
   :param reader: Reference to the Reader that created this run
   :type reader: Reader
   :param childrenMap: Optional per-run children mapping
   :type childrenMap: dict[str, list[str]] or None

   **Attributes:**

   .. attribute:: metadata

      Dictionary of metadata for this run.

      :type: dict

      Common metadata keys:
        - ``launchdate`` / ``launchday``: Timestamp of the run
        - ``problem_size``: Problem size parameter
        - ``jobsize``: Number of MPI ranks or threads
        - ``test``: Test name or identifier
        - Custom fields from your Caliper instrumentation

      .. code-block:: python

         run = model[0]
         print(run.metadata["launchdate"])
         print(run.metadata["problem_size"])
         print(run.metadata.get("custom_field", "default"))

   .. attribute:: perftree

      Dictionary mapping node names to their performance metrics.

      :type: dict[str, dict]

      Each node's metrics include:
        - ``sum``: Total inclusive time
        - ``avg``: Average inclusive time
        - ``min``: Minimum inclusive time
        - ``max``: Maximum inclusive time

      .. code-block:: python

         run = model[0]
         main_metrics = run.perftree["main"]
         print(f"Average time: {main_metrics['avg']}")
         print(f"Total time: {main_metrics['sum']}")
         print(f"Min time: {main_metrics['min']}")
         print(f"Max time: {main_metrics['max']}")

   .. attribute:: childrenMap

      Dictionary mapping parent nodes to their children for this run.

      :type: dict[str, list[str]]

   .. attribute:: read_from

      Reference to the Reader that created this run.

      :type: Reader

   **Methods:**

   .. method:: getMetaData(key)

      Get a metadata value by key.

      :param key: Metadata key to retrieve
      :type key: str
      :return: Metadata value
      :rtype: any

      .. code-block:: python

         run = model[0]
         date = run.getMetaData("launchdate")
         size = run.getMetaData("problem_size")

   .. method:: getPerfTree(node, metric)

      Get a specific metric for a node.

      :param node: Node name (e.g., "main", "compute")
      :type node: str
      :param metric: Metric name ("sum", "avg", "min", or "max")
      :type metric: str
      :return: Metric value
      :rtype: float

      .. code-block:: python

         run = model[0]
         avg_time = run.getPerfTree("main", "avg")
         max_time = run.getPerfTree("compute", "max")

   .. method:: to_dict()

      Convert the run to a dictionary.

      :return: Dictionary with metadata, perftree, and childrenMap
      :rtype: dict

      .. code-block:: python

         run = model[0]
         data = run.to_dict()
         print(data.keys())  # dict_keys(['metadata', 'perftree', 'childrenMap'])

   .. method:: __str__()

      String representation of the run.

      :return: String representation
      :rtype: str

      .. code-block:: python

         run = model[0]
         print(run)  # Prints the dictionary representation

Common Patterns
---------------

Filtering Runs
~~~~~~~~~~~~~~

.. code-block:: python

   import treescape as ts

   reader = ts.CaliReader("/path/to/data")
   model = ts.TreeScapeModel(reader)

   # Filter by problem size
   large = [r for r in model if r.metadata.get("problem_size", 0) > 1000]

   # Filter by date range
   import datetime
   start = datetime.datetime(2024, 1, 1).timestamp()
   end = datetime.datetime(2024, 12, 31).timestamp()
   year_2024 = [r for r in model
                if start <= r.metadata["launchdate"] <= end]

   # Filter by multiple criteria
   filtered = [
       r for r in model
       if r.metadata.get("jobsize") == 64
       and r.metadata.get("test") == "baseline"
       and "main" in r.perftree
   ]

   # Create new model from filtered data
   new_model = ts.TreeScapeModel(reader, filtered)

Sorting Runs
~~~~~~~~~~~~

.. code-block:: python

   # Sort by date (ascending)
   by_date = sorted(model, key=lambda r: r.metadata["launchdate"])

   # Sort by problem size (descending)
   by_size = sorted(model, key=lambda r: r.metadata["problem_size"], reverse=True)

   # Sort by performance
   by_perf = sorted(model, key=lambda r: r.perftree.get("main", {}).get("avg", 0))

   # Multi-level sort
   sorted_runs = sorted(
       model,
       key=lambda r: (r.metadata["test"], r.metadata["launchdate"])
   )

Extracting Data
~~~~~~~~~~~~~~~

.. code-block:: python

   # Get all unique test names
   tests = set(r.metadata.get("test", "unknown") for r in model)

   # Get time series data for a node
   times = [
       (r.metadata["launchdate"], r.perftree["main"]["avg"])
       for r in model
       if "main" in r.perftree
   ]

   # Calculate statistics
   import statistics
   avg_times = [r.perftree["main"]["avg"] for r in model if "main" in r.perftree]
   mean_time = statistics.mean(avg_times)
   median_time = statistics.median(avg_times)
   std_dev = statistics.stdev(avg_times)

Grouping Runs
~~~~~~~~~~~~~

.. code-block:: python

   from collections import defaultdict

   # Group by test name
   by_test = defaultdict(list)
   for run in model:
       test_name = run.metadata.get("test", "unknown")
       by_test[test_name].append(run)

   # Group by problem size
   by_size = defaultdict(list)
   for run in model:
       size = run.metadata.get("problem_size")
       by_size[size].append(run)

   # Create models for each group
   test_models = {
       test: ts.TreeScapeModel(model.reader, runs)
       for test, runs in by_test.items()
   }

Analyzing Performance
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Find slowest runs
   slowest = sorted(
       model,
       key=lambda r: r.perftree.get("main", {}).get("avg", 0),
       reverse=True
   )[:10]

   # Find runs with high variance
   high_variance = [
       r for r in model
       if "main" in r.perftree
       and (r.perftree["main"]["max"] - r.perftree["main"]["min"]) > 10.0
   ]

   # Compare baseline vs optimized
   baseline = [r for r in model if r.metadata.get("version") == "baseline"]
   optimized = [r for r in model if r.metadata.get("version") == "optimized"]

   baseline_avg = statistics.mean(
       r.perftree["main"]["avg"] for r in baseline if "main" in r.perftree
   )
   optimized_avg = statistics.mean(
       r.perftree["main"]["avg"] for r in optimized if "main" in r.perftree
   )

   speedup = baseline_avg / optimized_avg
   print(f"Speedup: {speedup:.2f}x")

Integration with Pandas
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   import treescape as ts

   reader = ts.CaliReader("/path/to/data")
   model = ts.TreeScapeModel(reader)

   # Convert to DataFrame
   data = []
   for run in model:
       row = {**run.metadata}  # Start with all metadata
       # Add performance metrics for key nodes
       if "main" in run.perftree:
           row["main_avg"] = run.perftree["main"]["avg"]
           row["main_sum"] = run.perftree["main"]["sum"]
       data.append(row)

   df = pd.DataFrame(data)

   # Now use pandas operations
   print(df.describe())
   print(df.groupby("test")["main_avg"].mean())

   # Filter with pandas
   fast_runs_df = df[df["main_avg"] < 10.0]

   # Convert back to model
   fast_run_indices = fast_runs_df.index.tolist()
   fast_runs = [model[i] for i in fast_run_indices]
   fast_model = ts.TreeScapeModel(reader, fast_runs)

See Also
--------

* :doc:`readers` - Loading data with CaliReader and ThicketReader
* :doc:`visualizations` - Creating visualizations from models
* :doc:`../examples` - Practical examples of working with models
