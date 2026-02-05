Contributing
============

TreeScape is an open-source project, and we welcome contributions from the community!

Getting Started
---------------

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a branch for your changes
4. Make your changes
5. Test your changes
6. Submit a pull request

Development Setup
-----------------

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/LLNL/treescape.git
   cd treescape

   # Create a virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Install development dependencies (if any)
   pip install -e .

Types of Contributions
----------------------

Bug Reports
~~~~~~~~~~~

If you find a bug, please create an issue on GitHub with:

* A clear description of the problem
* Steps to reproduce the issue
* Expected vs actual behavior
* Your environment (OS, Python version, TreeScape version)
* Sample code or data if possible

Feature Requests
~~~~~~~~~~~~~~~~

We welcome feature requests! Please create an issue describing:

* The problem you're trying to solve
* How you envision the feature working
* Why this feature would be useful to the community
* Example use cases

Code Contributions
~~~~~~~~~~~~~~~~~~

We welcome code contributions including:

* **Bug fixes**: Fix reported issues
* **New features**: Add requested or novel functionality
* **Performance improvements**: Optimize existing code
* **Documentation**: Improve or expand documentation
* **Examples**: Add new example notebooks or scripts
* **Tests**: Add or improve test coverage

Pull Request Process
--------------------

1. **Create a branch** from ``main`` for your changes:

   .. code-block:: bash

      git checkout -b feature/my-new-feature

2. **Make your changes** following our coding standards (see below)

3. **Test your changes** to ensure they work correctly:

   .. code-block:: bash

      # Run any existing tests
      pytest tests/

      # Test manually with example notebooks
      jupyter notebook

4. **Commit your changes** with clear, descriptive commit messages:

   .. code-block:: bash

      git add .
      git commit -m "Add feature: description of what you did"

5. **Push to your fork**:

   .. code-block:: bash

      git push origin feature/my-new-feature

6. **Create a pull request** on GitHub targeting the ``main`` branch

7. **Respond to feedback** from maintainers during code review

Coding Standards
----------------

Python Style
~~~~~~~~~~~~

* Follow PEP 8 style guidelines
* Use 4 spaces for indentation (no tabs)
* Maximum line length: 88 characters (Black formatter default)
* Use descriptive variable and function names

Documentation Style
~~~~~~~~~~~~~~~~~~~

* Add docstrings to all public classes and methods
* Use Google-style or NumPy-style docstrings
* Include type hints where appropriate
* Update RST documentation for new features

Example docstring:

.. code-block:: python

   def my_function(param1, param2):
       """
       Brief description of the function.

       :param param1: Description of param1
       :type param1: type
       :param param2: Description of param2
       :type param2: type
       :return: Description of return value
       :rtype: type
       """
       pass

Commit Messages
~~~~~~~~~~~~~~~

Write clear, descriptive commit messages:

* Start with a verb in imperative mood ("Add", "Fix", "Update")
* Keep the first line under 72 characters
* Add detailed explanation in the body if needed
* Reference issues with ``#issue_number``

Example:

.. code-block:: text

   Add support for custom metric names in CaliReader

   - Allow users to specify custom inclusive_strings parameter
   - Update documentation with examples
   - Add validation for metric name format

   Fixes #123

Code Review Process
-------------------

All pull requests will be reviewed by maintainers. We look for:

* **Correctness**: Does the code do what it's supposed to?
* **Quality**: Is the code well-written and maintainable?
* **Documentation**: Is the code properly documented?
* **Tests**: Are there appropriate tests?
* **Style**: Does it follow our coding standards?

Be prepared to:

* Answer questions about your approach
* Make changes based on feedback
* Iterate on your implementation

Testing
-------

Running Tests
~~~~~~~~~~~~~

.. code-block:: bash

   # Run all tests
   pytest

   # Run specific test file
   pytest tests/test_calireader.py

   # Run with coverage
   pytest --cov=treescape

Writing Tests
~~~~~~~~~~~~~

When adding new features, please include tests:

* Unit tests for individual functions
* Integration tests for complete workflows
* Test edge cases and error conditions

Place tests in the ``tests/`` directory following the naming convention ``test_<module>.py``.

Documentation
-------------

Updating Documentation
~~~~~~~~~~~~~~~~~~~~~~

Documentation is written in reStructuredText (RST) format using Sphinx.

To build documentation locally:

.. code-block:: bash

   cd documentation
   pip install sphinx sphinx_rtd_theme
   make html
   open _build/html/index.html

Documentation files are located in ``documentation/``:

* ``index.rst``: Main landing page
* ``installation.rst``: Installation instructions
* ``quickstart.rst``: Quick start guide
* ``concepts.rst``: Core concepts
* ``examples.rst``: Usage examples
* ``api/``: API reference documentation

License
-------

By contributing to TreeScape, you agree that your contributions will be
licensed under the MIT License.

Code of Conduct
---------------

TreeScape follows a code of conduct to ensure a welcoming and inclusive
environment for all contributors:

* Be respectful and considerate
* Welcome newcomers and help them get started
* Focus on constructive feedback
* Assume good intentions
* Report inappropriate behavior to maintainers

Getting Help
------------

If you need help with development:

* Open a discussion on GitHub
* Ask questions in pull request comments
* Reach out to maintainers

Contact
-------

* **GitHub Issues**: https://github.com/LLNL/treescape/issues
* **Email**: Contact the maintainers listed in the AUTHORS file

Release Process
---------------

For maintainers releasing new versions:

1. Update version number in relevant files
2. Update CHANGELOG with release notes
3. Create a git tag: ``git tag -a v1.x.x -m "Release v1.x.x"``
4. Push tag: ``git push origin v1.x.x``
5. Create GitHub release from tag
6. Update documentation deployment

Thank You!
----------

Thank you for contributing to TreeScape! Your contributions help make
performance analysis better for everyone.
