FROM openjdk:11-slim

# Install necessary tools
RUN apt-get update && apt-get install -y \
    sudo \
    docker.io \
    bash \
    jq \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install PySpark
RUN pip3 install --no-cache-dir pyspark

# Create a shared group with a specific GID
RUN groupadd -g 1000 sharedgroup

# Create a non-root user with a specific UID, add it to the shared group and the docker group
RUN useradd -m -s /bin/bash -u 1000 -g sharedgroup -G docker mainuser

# Allow mainuser to use sudo without password
RUN echo "mainuser ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/mainuser

WORKDIR /workspace

COPY process_fhir.sh /workspace/
COPY synthea_script.sh /workspace/
RUN chmod +x /workspace/process_fhir.sh
RUN chmod +x /workspace/synthea_script.sh

USER mainuser

CMD ["/bin/bash"]