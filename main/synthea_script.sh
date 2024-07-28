#!/bin/bash

echo "Starting Synthea data generation..."

docker exec -u synthea synthea java -jar synthea-with-dependencies.jar \
    -p 100 \
    -m diabetes \
    --exporter.baseDirectory /usr/src/app/output \
    --exporter.fhir.export true \
    --exporter.fhir.use_us_core_ig true \
    --exporter.fhir.r4.export true \
    -o diabetes_percentage=0.1

if [ $? -eq 0 ]; then
    echo "Synthea data generation completed successfully."
else
    echo "Error: Synthea data generation failed. Check the Synthea container logs for more information."
    docker logs synthea
fi