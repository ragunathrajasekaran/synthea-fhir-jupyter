# Build stage
FROM openjdk:11-jdk AS build

# Set the working directory
WORKDIR /usr/src/app

# Install git and other necessary tools
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Clone Synthea repository
RUN git clone https://github.com/synthetichealth/synthea.git .

# Copy custom modules from host to the modules directory
COPY ./custom_modules/*.json src/main/resources/modules/

# Build Synthea without running tests
RUN ./gradlew build -x test

# Runtime stage
FROM openjdk:11-jre

WORKDIR /usr/src/app

# Copy the built JAR from the build stage
COPY --from=build /usr/src/app/build/libs/synthea-with-dependencies.jar .

# Create a shared group, non-root user, and set up the output directory
RUN groupadd -r sharedgroup && \
    useradd -r -g sharedgroup synthea && \
    mkdir -p /usr/src/app/output && \
    chown synthea:sharedgroup /usr/src/app/output && \
    chmod 775 /usr/src/app/output

USER synthea

# Set the entrypoint to bash
ENTRYPOINT ["/bin/bash"]

# By default, just keep the container running
CMD ["-c", "tail -f /dev/null"]