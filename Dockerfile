FROM python:3.9-slim

LABEL authors="aschwanden1"
LABEL description="TreeScape - Jupyter-based visualization tool for performance data"

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the treescape source code
COPY treescape ./treescape

# Copy JavaScript files and CSS needed for visualization
COPY js ./js
COPY stacked.css ./stacked.css

# Copy treescape-media examples and datasets
COPY treescape-media/examples /app/examples
COPY treescape-media/datasets /app/datasets

# Copy example notebook
RUN mkdir -p /app/notebooks
COPY treescape_demo.ipynb /app/notebooks/

# Trust the notebooks to avoid kernel restart issues
RUN jupyter trust /app/notebooks/treescape_demo.ipynb && \
    jupyter trust /app/examples/*.ipynb 2>/dev/null || true

# Expose Jupyter port
EXPOSE 8888

# Set up Jupyter configuration
RUN mkdir -p /root/.jupyter && \
    echo "c.ServerApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_server_config.py && \
    echo "c.ServerApp.allow_root = True" >> /root/.jupyter/jupyter_server_config.py && \
    echo "c.ServerApp.token = ''" >> /root/.jupyter/jupyter_server_config.py && \
    echo "c.ServerApp.password = ''" >> /root/.jupyter/jupyter_server_config.py && \
    echo "c.ServerApp.terminado_settings = {'shell_command': ['/bin/bash']}" >> /root/.jupyter/jupyter_server_config.py && \
    echo "c.NotebookApp.tornado_settings = {'websocket_ping_interval': 30000, 'websocket_ping_timeout': 30000}" >> /root/.jupyter/jupyter_server_config.py

# Start JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--notebook-dir=/app"]
