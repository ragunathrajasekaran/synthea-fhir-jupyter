#!/bin/bash

echo "Connecting to Jupyter notebook server..."

# Wait for Jupyter service to be ready
until curl -s http://jupyter:8888 > /dev/null; do
    echo "Waiting for Jupyter server to be ready..."
    sleep 5
done

echo "Jupyter server is ready. You can now access it at http://localhost:8888"
echo "To create a new notebook with PySpark, select 'Python 3 (PySpark)' kernel."

# Keep the script running to maintain the connection
tail -f /dev/null