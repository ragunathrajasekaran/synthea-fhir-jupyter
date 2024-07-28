from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit, udf
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import requests
import json
from pyspark.sql.types import StringType

# Initialize Spark session
spark = SparkSession.builder.appName("DiabetesPrediction").getOrCreate()

# Load FHIR data
patients = spark.read.json("fhir_data/Patient*.json")
observations = spark.read.json("fhir_data/Observation*.json")
conditions = spark.read.json("fhir_data/Condition*.json")

# Process Patient data
patient_data = patients.select("id", "gender", "birthDate")

# Process Observation data (focusing on glucose and HbA1c)
glucose_data = observations.filter(col("code.coding.code") == "2339-0") \
    .select("subject.reference", "valueQuantity.value") \
    .withColumnRenamed("value", "glucose_level")

hba1c_data = observations.filter(col("code.coding.code") == "4548-4") \
    .select("subject.reference", "valueQuantity.value") \
    .withColumnRenamed("value", "hba1c_level")

# Process Condition data (check for diabetes diagnosis)
diabetes_condition = conditions.filter(col("code.coding.code") == "44054006") \
    .select("subject.reference") \
    .withColumn("has_diabetes", lit(1))

# Join all data
joined_data = patient_data.join(glucose_data, patient_data.id == glucose_data.reference, "left") \
    .join(hba1c_data, patient_data.id == hba1c_data.reference, "left") \
    .join(diabetes_condition, patient_data.id == diabetes_condition.reference, "left") \
    .fillna(0, subset=["has_diabetes"])

# Prepare features
feature_cols = ["gender", "age", "glucose_level", "hba1c_level"]
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
final_data = assembler.transform(joined_data)

# Split data
train_data, test_data = final_data.randomSplit([0.7, 0.3])

# Train Random Forest model
rf = RandomForestClassifier(labelCol="has_diabetes", featuresCol="features", numTrees=10)
model = rf.fit(train_data)

# Make predictions
predictions = model.transform(test_data)

# Evaluate model
evaluator = BinaryClassificationEvaluator(labelCol="has_diabetes")
auc = evaluator.evaluate(predictions)

print(f"AUC: {auc}")

# Function to create FHIR Observation resource
def create_fhir_observation(patient_id, prediction_prob):
    return json.dumps({
        "resourceType": "Observation",
        "status": "final",
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "82710-2",
                "display": "Diabetes mellitus risk assessment"
            }]
        },
        "subject": {"reference": f"Patient/{patient_id}"},
        "valueQuantity": {
            "value": float(prediction_prob),
            "unit": "probability",
            "system": "http://unitsofmeasure.org",
            "code": "probability"
        }
    })

# UDF to save prediction to FHIR server
@udf(returnType=StringType())
def save_to_fhir(patient_id, prediction_prob):
    fhir_server_url = "http://fhir-server:8080/fhir"
    headers = {'Content-Type': 'application/fhir+json'}
    payload = create_fhir_observation(patient_id, prediction_prob)
    response = requests.post(f"{fhir_server_url}/Observation", headers=headers, data=payload)
    return response.json().get('id', '')  # Return the ID of the created resource

# Apply UDF to save predictions
predictions = predictions.withColumn("fhir_observation_id", save_to_fhir(col("id"), col("probability")[1]))

# Save predictions as CSV
predictions.select("id", "probability", "prediction", "fhir_observation_id").write.csv("diabetes_predictions.csv", header=True)