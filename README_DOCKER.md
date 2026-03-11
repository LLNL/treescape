# TreeScape Docker Setup

This repository contains a Dockerfile that sets up a complete TreeScape environment with JupyterLab.

## Building the Docker Image

First, make sure the git submodule is initialized (this includes example notebooks and datasets):

```bash
git submodule update --init --recursive
```

Then build the Docker image from the repository root directory:

```bash
docker build -t treescape:latest .
```

## Running the Container

**Important**: You need to mount a directory containing Caliper data files:

```bash
docker run -p 8888:8888 -v /path/to/your/caliper/data:/app/data treescape:latest
```

For example:

```bash
docker run -p 8888:8888 -v /Users/aschwanden1/datasets/newdemo/test:/app/data treescape:latest
```

## Accessing JupyterLab

After starting the container, open your browser and navigate to:

```
http://localhost:8888
```

You'll find a demo notebook at `treescape_demo.ipynb` that demonstrates basic TreeScape functionality.

## What's Included

- Python 3.9
- All TreeScape dependencies (from requirements.txt)
- TreeScape source code
- Example notebooks from treescape-media (in `/app/examples`)
- Example datasets from treescape-media (in `/app/datasets`)
- JupyterLab environment
- Demo notebook showing basic usage

## Customizing

### Using Your Own Caliper Data

To use your own Caliper data, mount your data directory when running the container:

```bash
docker run -p 8888:8888 -v /path/to/your/data:/app/data treescape:latest
```

For example, to use the newdemo test data:

```bash
docker run -p 8888:8888 -v /Users/aschwanden1/datasets/newdemo/test:/app/data treescape:latest
```

**Note**: TreeScape requires native Caliper format files (text files with `__rec=` entries), not JSON-formatted Caliper files. The demo notebook is configured to read from `/app/data` inside the container.

### Persisting Notebooks

To save your work:

```bash
docker run -p 8888:8888 -v $(pwd)/notebooks:/app/notebooks treescape:latest
```

This saves any notebooks you create to a local `notebooks` directory.

### Running with Both Custom Data and Persistent Notebooks

```bash
docker run -p 8888:8888 \
  -v /path/to/your/data:/app/data \
  -v $(pwd)/notebooks:/app/notebooks \
  treescape:latest
```

## Demo Notebook

The included demo notebook (`treescape_demo.ipynb`) shows:

1. Importing TreeScape library
2. Loading Caliper data files
3. Creating a TreeScapeModel
4. Next steps for creating visualizations

You can extend this notebook or create your own to explore your performance data.

## Example Notebooks

The container includes example notebooks from the treescape-media repository:

- **DocuExamples.ipynb** - Comprehensive examples demonstrating TreeScape features
- **NightlyTestDemo.ipynb** - Nightly test demonstrations
- **NightlyTestDemo_local.ipynb** - Local version of nightly test demos

These examples are located in `/app/examples` within the container. The corresponding datasets are in `/app/datasets`.

## Troubleshooting

If you encounter issues:

- Make sure Docker is running
- Check that port 8888 is not already in use
- Verify your data files are valid Caliper format (.cali files)
- Check container logs: `docker logs <container-id>`
