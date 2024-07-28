FROM jupyter/pyspark-notebook:latest

USER root

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY requirements.txt /home/jovyan/work/

# Install Python dependencies
RUN pip install --no-cache-dir -r /home/jovyan/work/requirements.txt

# Copy your Python script and kernel setup script into the container
COPY *.py /home/jovyan/work/

# Set the working directory
WORKDIR /home/jovyan/work

# Run the kernel setup script
RUN /opt/conda/bin/python /home/jovyan/work/kernel_setup.py

# Create necessary directories and set permissions
RUN mkdir -p /home/jovyan/.local/share/jupyter/runtime && \
    chown -R jovyan:users /home/jovyan/.local && \
    chmod -R 755 /home/jovyan/.local

# Switch back to the jovyan user
USER jovyan

# Ensure the correct PATH is set
ENV PATH="/opt/conda/bin:$PATH"

# Expose the Jupyter port
EXPOSE 8888

# Start Jupyter Notebook with no token
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]