# TreeScape Documentation

This directory contains the documentation for TreeScape, built using [Sphinx](https://www.sphinx-doc.org/).

## Building the Documentation Locally

### Prerequisites

Install the required packages:

```bash
pip install -r requirements.txt
```

### Build HTML Documentation

```bash
make html
```

The built documentation will be in `_build/html/`. Open `_build/html/index.html` in your browser to view it.

### Other Build Formats

```bash
make latexpdf  # Build PDF documentation
make epub      # Build EPUB documentation
make help      # See all available build targets
```

### Cleaning Build Artifacts

```bash
make clean
```

## Documentation Structure

* `index.rst` - Main landing page
* `installation.rst` - Installation instructions
* `quickstart.rst` - Quick start guide
* `concepts.rst` - Core concepts and architecture
* `examples.rst` - Usage examples
* `api/` - API reference documentation
  * `readers.rst` - CaliReader and ThicketReader API
  * `models.rst` - TreeScapeModel and Run API
  * `visualizations.rst` - StackedLine and MultiLine API
* `contributing.rst` - Contribution guidelines
* `changelog.rst` - Version history
* `license.rst` - License information

## Automatic Deployment

The documentation is automatically built and deployed to GitHub Pages when changes are pushed to the `main` branch. The workflow is defined in `.github/workflows/docs.yml`.

## Viewing Published Documentation

Once deployed, the documentation will be available at:
https://llnl.github.io/treescape/

## Contributing to Documentation

When adding new features or making changes:

1. Update the relevant RST files
2. Build locally to verify formatting
3. Commit your changes
4. Submit a pull request

Follow the reStructuredText (RST) format for all documentation files.

## Documentation Style Guide

* Use clear, concise language
* Include code examples for all APIs
* Add cross-references using `:doc:` and `:ref:` directives
* Keep line length reasonable (80-100 characters)
* Use proper RST syntax for code blocks, lists, and tables
