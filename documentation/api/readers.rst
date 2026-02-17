Readers API
===========

Readers are responsible for loading and parsing Caliper performance files.

CaliReader
----------

.. class:: CaliReader(path="", pool_size=10, inclusive_strings=None)

   Primary reader for Caliper files with parallel processing support.

   :param path: Path to Caliper files. Can be:
                - A directory path (loads all .cali files recursively)
                - A single file path
                - A list of directory/file paths
   :type path: str or list[str]
   :param pool_size: Number of parallel processes for loading files (default: 10)
   :type pool_size: int
   :param inclusive_strings: Custom metric names to use instead of defaults.
                             Must provide 4 strings: [min, max, avg, sum]
   :type inclusive_strings: list[str] or None

   .. code-block:: python

      import treescape as ts

      # Load from a directory
      reader = ts.CaliReader("/path/to/cali/files")

      # Load from multiple sources
      reader = ts.CaliReader([
          "/path/to/dir1",
          "/path/to/dir2",
          "/path/to/file.cali"
      ])

      # Custom metrics
      reader = ts.CaliReader(
          path="/path/to/files",
          pool_size=8,
          inclusive_strings=[
              "min#inclusive#sum#my.timer",
              "max#inclusive#sum#my.timer",
              "avg#inclusive#sum#my.timer",
              "sum#inclusive#sum#my.timer"
          ]
      )

   **Attributes:**

   .. attribute:: inclusive_strings

      List of metric names used for min, max, avg, and sum.

      Default:
        - ``"min#inclusive#sum#time.duration"``
        - ``"max#inclusive#sum#time.duration"``
        - ``"avg#inclusive#sum#time.duration"``
        - ``"sum#inclusive#sum#time.duration"``


   .. attribute:: meta_globals

      Dictionary mapping metadata keys to their types.

   **Methods:**

   .. method:: get_entire()

      Get the complete dataset including nodes, children map, and metadata.

      :return: Dictionary with keys:
               - ``nodes``: Performance data for each node
               - ``childrenMap``: Parent-child relationships
               - ``meta_globals``: Metadata type information
      :rtype: dict

      .. code-block:: python

         reader = ts.CaliReader("/path/to/files")
         data = reader.get_entire()

         print(data["nodes"].keys())        # All function names
         print(data["childrenMap"]["main"]) # Children of main
         print(data["meta_globals"])        # Metadata types

   .. method:: __iter__()

      Iterate over drill levels (node names) in the dataset.

      :return: Iterator yielding (node_name, data) tuples
      :rtype: iterator

      .. code-block:: python

         reader = ts.CaliReader("/path/to/files")

         for node_name, data in reader:
             print(f"{node_name}: {data['xaxis']}")


ThicketReader
-------------

.. class:: ThicketReader(th_ens, profiles, xaxis)

   Reader that uses the Thicket library for data processing.

   :param th_ens: Thicket ensemble object
   :type th_ens: thicket.Thicket
   :param profiles: List of Caliper file paths
   :type profiles: list[str]
   :param xaxis: Metadata key to use as the x-axis
   :type xaxis: str

   .. code-block:: python

      import treescape as ts
      import thicket as tt

      # Load with Thicket
      profiles = ["/path/to/file1.cali", "/path/to/file2.cali"]
      th_ens = tt.Thicket.from_caliperreader(profiles)

      # Create reader
      reader = ts.ThicketReader(
          th_ens=th_ens,
          profiles=profiles,
          xaxis="launchdate"
      )

   **Methods:**

   .. method:: get_entire()

      Get the complete dataset in TreeScape format.

      :return: Dictionary with nodes, childrenMap, parentMap, and meta_globals
      :rtype: dict

   .. method:: get_entire_for_xaxis(xaxis_value)

      Get data for a specific x-axis value.

      :param xaxis_value: The x-axis value to filter by
      :type xaxis_value: any
      :return: List of node data dictionaries
      :rtype: list[dict]

      .. code-block:: python

         reader = ts.ThicketReader(th_ens, profiles, "launchdate")

         # Get data for a specific date
         data = reader.get_entire_for_xaxis(1609459200)

   .. method:: get_all_xaxis()

      Get all unique x-axis values in the dataset.

      :return: List of x-axis values
      :rtype: list

   .. method:: get_all_xaxis_meta()

      Get metadata for all runs.

      :return: List of metadata dictionaries
      :rtype: list[dict]

   .. method:: __iter__()

      Iterate over x-axis values and their data.

      :return: Iterator yielding (xaxis_value, metadata, node_data) tuples
      :rtype: iterator

      .. code-block:: python

         for xaxis_val, metadata, node_data in reader:
             print(f"X-axis: {xaxis_val}")
             print(f"Metadata: {metadata}")
             print(f"Nodes: {[n['name'] for n in node_data]}")

Reader Base Class
-----------------

.. class:: Reader()

   Abstract base class for all readers.

   All reader implementations must implement the ``get_entire()`` method.

   .. method:: get_entire(xaxis_name)

      Abstract method to retrieve the complete dataset.

      :param xaxis_name: Name of the x-axis metadata field
      :type xaxis_name: str
      :return: Complete dataset dictionary
      :rtype: dict

Helper Class: TH_ens
---------------------

.. class:: TH_ens()

   Helper class for managing Thicket ensemble creation.

   .. method:: get_th_ens(cali_files)

      Create or retrieve a cached Thicket ensemble.

      :param cali_files: Path(s) to Caliper files
      :type cali_files: str or list[str]
      :return: Tuple of (thicket_ensemble, profile_list)
      :rtype: tuple

      .. code-block:: python

         from treescape import TH_ens

         th = TH_ens()
         th_ens, profiles = th.get_th_ens("/path/to/cali/files")

Performance Considerations
--------------------------

**CaliReader Performance:**

* **pool_size**: Set to match your CPU core count for optimal parallel loading
* **Multiprocessing**: Files are loaded in parallel, significantly faster for large datasets
* **Per-file indexing**: Maintains separate indices for efficient data access
* **Memory usage**: Scales with number and size of Caliper files

**ThicketReader Performance:**

* **DataFrame operations**: Uses pandas for efficient data manipulation
* **Vectorized aggregation**: ~100x faster than row-by-row iteration
* **Memory overhead**: Higher than CaliReader due to Thicket's DataFrame structure
* **Best for**: Integration with existing Thicket workflows

Choosing a Reader
-----------------

**Use CaliReader when:**

* You have many Caliper files (100s to 1000s)
* You need maximum performance
* You're starting a new project
* You don't need Thicket's DataFrame features

**Use ThicketReader when:**

* You're already using Thicket in your workflow
* You need Thicket's data manipulation features
* You're migrating from existing Thicket code
* You want to leverage Thicket's filtering/aggregation

Examples
--------

**Loading from multiple sources:**

.. code-block:: python

   import treescape as ts

   reader = ts.CaliReader([
       "/nightly/2024-01-01/",
       "/nightly/2024-01-02/",
       "/nightly/2024-01-03/specific_test.cali"
   ])

   print(f"Loaded {len(reader.xy_idx_by_drill_level)} nodes")

**Custom metrics:**

.. code-block:: python

   reader = ts.CaliReader(
       path="/path/to/data",
       inclusive_strings=[
           "min#inclusive#sum#custom.metric",
           "max#inclusive#sum#custom.metric",
           "avg#inclusive#sum#custom.metric",
           "sum#inclusive#sum#custom.metric"
       ]
   )

**Iterating over data:**

.. code-block:: python

   reader = ts.CaliReader("/path/to/data")

   for node_name, node_data in reader:
       print(f"Node: {node_name}")
       print(f"  X-axis values: {node_data['xaxis']}")
       print(f"  Y-data points: {len(node_data['ydata'])}")

**Using ThicketReader:**

.. code-block:: python

   import thicket as tt
   import treescape as ts

   # Load with Thicket
   profiles = ["/path/to/file1.cali", "/path/to/file2.cali"]
   th_ens = tt.Thicket.from_caliperreader(profiles)

   # Create reader
   reader = ts.ThicketReader(th_ens, profiles, "problem_size")

   # Get all problem sizes
   sizes = reader.get_all_xaxis()
   print(f"Problem sizes: {sorted(set(sizes))}")

See Also
--------

* :doc:`models` - Working with TreeScapeModel and Run objects
* :doc:`visualizations` - Creating visualizations from reader data
* :doc:`../concepts` - Understanding TreeScape's architecture
