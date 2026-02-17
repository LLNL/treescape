Examples
========

This page provides practical examples for common TreeScape use cases.

Scaling Study Analysis
----------------------

Track how performance scales with problem size:

.. code-block:: python

	import treescape as ts

	# Load all runs from a scaling study
	cali_file_loc = "../datasets/newdemo/test"
	reader = ts.CaliReader(cali_file_loc)
	model = ts.TreeScapeModel(reader)

	# Create visualization
	viz = ts.StackedLine()
	viz.setXAxis("launchdate")
	viz.setYAxis("avg")
	viz.setDrillLevel(["IntegrateStressForElems", "CalcHourglassControlForElems"])
	viz.render(model)

Performance Regression Testing
-------------------------------

Track performance changes over time:

.. code-block:: python

	from datetime import datetime

	reader = ts.CaliReader(cali_file_loc)
	model = ts.TreeScapeModel(reader)

	# Sort by date
	sorted_runs = sorted(model, key=lambda x: x.metadata["launchdate"])

	# Plot with matplotlib for cleaner view
	ml = ts.MultiLine(sorted_runs)
	ml.plot_sums("launchdate", "main", "branch")

Comparing Multiple Tests
-------------------------

Compare different test configurations:

.. code-block:: python

	cali_file_loc = "../datasets/newdemo/test"
	xaxis = "launchday"
	metadata_key = "test"
	processes_for_parallel_read = 15
	initial_regions = ["main"]

	caliReader = ts.CaliReader( cali_file_loc, processes_for_parallel_read )
	tsm = ts.TreeScapeModel( caliReader)
	#Always be sure to sort your data into some reasonable way. 
	alltests = sorted(tsm, key=lambda x: x.metadata[xaxis])

	sl = ts.StackedLine()

	##
	for testname in { t.metadata[metadata_key] for t in tsm }:
	    print(testname)
	    # render each test.  click on "Run Info" button to see flamegraph and metadata
	    all_tests = [t for t in tsm if t.metadata[metadata_key] == testname]
	    sl.exportSVG( "/Users/aschwanden1/svg_imgs/", all_tests,  "launchday", ["TimeIncrement", "LagrangeLeapFrog"], testname )


Exporting to SVG
----------------

Export visualizations for reports or presentations:

.. code-block:: python

	cali_file_loc = "../datasets/newdemo/test"
	xaxis = "launchday"
	metadata_key = "test"
	processes_for_parallel_read = 15
	initial_regions = ["main"]

	caliReader = ts.CaliReader( cali_file_loc, processes_for_parallel_read )
	tsm = ts.TreeScapeModel( caliReader)
	#Always be sure to sort your data into some reasonable way. 
	alltests = sorted(tsm, key=lambda x: x.metadata[xaxis])

	sl = ts.StackedLine()

	##
	for testname in { t.metadata[metadata_key] for t in tsm }:
	    print(testname)
	    # render each test.  click on "Run Info" button to see flamegraph and metadata
	    all_tests = [t for t in tsm if t.metadata[metadata_key] == testname]
	    sl.exportSVG( "/Users/aschwanden1/svg_imgs/", all_tests,  "launchday", ["TimeIncrement", "LagrangeLeapFrog"], testname )


Custom Metrics
--------------

Use custom metric names from your Caliper instrumentation:

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

Filtering by Metadata
----------------------

Analyze specific subsets of runs:

.. code-block:: python

   import treescape as ts

   reader = ts.CaliReader(cali_file_loc)
   model = ts.TreeScapeModel(reader)

   # Filter by multiple criteria
   filtered = [
       run for run in model
       if run.metadata.get("jobsize", 0) == 64
       and run.metadata.get("problem_size", 0) > 1000
       and "production" in run.metadata.get("tag", "")
   ]

   # Create model from filtered runs
   filtered_model = ts.TreeScapeModel(reader, filtered)

   viz = ts.StackedLine()
   viz.render(filtered_model)

Multi-Node Drill Down
----------------------

Examine multiple functions simultaneously:

.. code-block:: python

   import treescape as ts

   reader = ts.CaliReader(cali_file_loc)
   model = ts.TreeScapeModel(reader)

   viz = ts.StackedLine()
   viz.setXAxis("launchdate")
   viz.setYAxis("sum")

   # Show multiple functions
   viz.setDrillLevel([
       "main",
       "initialization",
       "computation",
       "io_operations",
       "finalization"
   ])

   # Use topmax aggregation for stacked view
   viz.setXAggregation("topmax")

   viz.render(model)

Custom Chart Dimensions
------------------------

Adjust visualization size for presentations or notebooks:

.. code-block:: python

   import treescape as ts

   reader = ts.CaliReader(cali_file_loc)
   model = ts.TreeScapeModel(reader)

   viz = ts.StackedLine()
   viz.setWidth(1600)   # Wider for presentations
   viz.setHeight(800)   # Taller for more detail
   viz.render(model)

Combining with Pandas
---------------------

Leverage pandas for advanced data manipulation:

.. code-block:: python

   import treescape as ts
   import pandas as pd

   reader = ts.CaliReader(cali_file_loc)
   model = ts.TreeScapeModel(reader)

   # Convert to DataFrame for analysis
   data = []
   for run in model:
       if "main" in run.perftree:
           data.append({
               "date": run.metadata.get("launchdate"),
               "problem_size": run.metadata.get("problem_size"),
               "time_avg": run.perftree["main"]["avg"],
               "time_max": run.perftree["main"]["max"],
           })

   df = pd.DataFrame(data)

   # Perform pandas operations
   print(df.describe())
   print(df.groupby("problem_size")["time_avg"].mean())

   # Filter with pandas
   recent = df[df["date"] > 1609459200]

   # Convert back to model for visualization
   recent_runs = [model[i] for i in recent.index]
   recent_model = ts.TreeScapeModel(reader, recent_runs)

Working with Multiple Axes
---------------------------

Compare different metadata dimensions:

.. code-block:: python

   import treescape as ts

   reader = ts.CaliReader(cali_file_loc)
   model = ts.TreeScapeModel(reader)

   # Plot vs time
   viz1 = ts.StackedLine()
   viz1.setXAxis("launchdate")
   viz1.render(model)

   # Plot vs problem size
   viz2 = ts.StackedLine()
   viz2.setXAxis("problem_size")
   viz2.render(model)

   # Plot vs job size
   viz3 = ts.StackedLine()
   viz3.setXAxis("jobsize")
   viz3.render(model)

Computing Statistics
--------------------

Calculate performance statistics across runs:

.. code-block:: python

   import treescape as ts
   import statistics

   reader = ts.CaliReader(cali_file_loc)
   model = ts.TreeScapeModel(reader)

   # Collect times for main function
   main_times = []
   for run in model:
       if "main" in run.perftree and "avg" in run.perftree["main"]:
           main_times.append(run.perftree["main"]["avg"])

   # Compute statistics
   print(f"Mean: {statistics.mean(main_times):.2f}")
   print(f"Median: {statistics.median(main_times):.2f}")
   print(f"Std Dev: {statistics.stdev(main_times):.2f}")
   print(f"Min: {min(main_times):.2f}")
   print(f"Max: {max(main_times):.2f}")

Detecting Performance Anomalies
--------------------------------

Identify outliers and performance regressions:

.. code-block:: python

   import treescape as ts
   import statistics

   reader = ts.CaliReader(cali_file_loc)
   model = ts.TreeScapeModel(reader)

   # Sort by date
   sorted_runs = sorted(model, key=lambda x: x.metadata["launchdate"])

   # Calculate baseline statistics (first 10 runs)
   baseline_times = [
       run.perftree["main"]["avg"]
       for run in sorted_runs[:10]
       if "main" in run.perftree
   ]

   baseline_mean = statistics.mean(baseline_times)
   baseline_stdev = statistics.stdev(baseline_times)
   threshold = baseline_mean + 2 * baseline_stdev

   # Find anomalies
   anomalies = []
   for run in sorted_runs[10:]:
       if "main" in run.perftree:
           time = run.perftree["main"]["avg"]
           if time > threshold:
               anomalies.append({
                   "date": run.metadata["launchdate"],
                   "time": time,
                   "deviation": (time - baseline_mean) / baseline_stdev
               })

   # Report anomalies
   for a in anomalies:
       print(f"Anomaly detected on {a['date']}: "
             f"{a['time']:.2f}s ({a['deviation']:.1f}σ)")

Integration with Jupyter Notebooks
-----------------------------------

Best practices for Jupyter notebook usage:

.. code-block:: python

   import treescape as ts
   import sys

   # Add treescape to path if needed
   sys.path.append("/path/to/treescape")

   # Load data once at the top of notebook
   reader = ts.CaliReader(cali_file_loc)
   model = ts.TreeScapeModel(reader)

   print(f"Loaded {len(model)} runs")
   print(f"Available metadata: {list(model[0].metadata.keys())}")
   print(f"Available nodes: {list(model[0].perftree.keys())}")

   # Create visualizations in separate cells
   viz = ts.StackedLine()
   viz.setXAxis("launchdate")
   viz.render(model)

Next Steps
----------

* Review the :doc:`api/readers` for complete API documentation
* See :doc:`contributing` to contribute your own examples
