import json
import os
from jupyter_client.kernelspec import KernelSpecManager

def setup_kernel():
    kernel_name = "python3_pyspark"
    kernel_dir = os.path.join(KernelSpecManager().user_kernel_dir, kernel_name)

    # Ensure the kernel directory exists
    os.makedirs(kernel_dir, exist_ok=True)

    kernel_json = {
        "argv": ["/opt/conda/bin/python", "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        "display_name": "Python 3 (PySpark)",
        "language": "python",
        "env": {
            "SPARK_HOME": "/usr/local/spark",
            "PYTHONPATH": "/usr/local/spark/python:/usr/local/spark/python/lib/py4j-0.10.9-src.zip:/opt/conda/lib/python3.9/site-packages",
            "PYSPARK_PYTHON": "/opt/conda/bin/python",
            "PYSPARK_DRIVER_PYTHON": "/opt/conda/bin/python"
        }
    }

    # Write the kernel.json file
    with open(os.path.join(kernel_dir, "kernel.json"), "w") as f:
        json.dump(kernel_json, f, indent=2)

    print(f"Custom PySpark kernel '{kernel_name}' has been set up in {kernel_dir}")

if __name__ == "__main__":
    setup_kernel()
    print("Custom PySpark kernel setup complete.")