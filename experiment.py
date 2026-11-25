
import csv
from pathlib import Path

from fifo import fifo
from lru import lru
from optimal import optimal


# File locations
BASE_DIR = Path(__file__).parent
DATASET_FILE = BASE_DIR / "reference_strings.csv"
RESULTS_FILE = BASE_DIR / "results.csv"


# Algorithms to be tested
algorithms = {
    "FIFO": fifo,
    "LRU": lru,
    "Optimal": optimal
}


# Frame capacities to be tested
frame_capacities = [3, 4, 5]


# Store all experiment results
experiment_results = []


# Load the reference strings from CSV
with open(DATASET_FILE, "r", newline="") as file:

    reader = csv.DictReader(file)

    for row in reader:

        string_id = row["string_id"]
        workload = row["workload"]

        # Extract all page requests from the row
        reference_string = [
            int(row[column])
            for column in row
            if column.startswith("request_")
        ]

        # Run every algorithm using each frame capacity
        for frame_count in frame_capacities:

            for algorithm_name, algorithm_function in algorithms.items():

                result = algorithm_function(
                    reference_string,
                    frame_count
                )

                # Store the experiment results
                experiment_results.append({
                    "string_id": string_id,
                    "workload": workload,
                    "algorithm": algorithm_name,
                    "frame_count": frame_count,
                    "total_requests": len(reference_string),
                    "page_faults": result["page_faults"],
                    "page_hits": result["page_hits"],
                    "replacements": result["replacements"],
                    "page_fault_rate": result["page_fault_rate"],
                    "page_hit_rate": result["page_hit_rate"]
                })


# Export results to CSV
fieldnames = [
    "string_id",
    "workload",
    "algorithm",
    "frame_count",
    "total_requests",
    "page_faults",
    "page_hits",
    "replacements",
    "page_fault_rate",
    "page_hit_rate"
]

with open(RESULTS_FILE, "w", newline="") as file:

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(experiment_results)


# Display experiment summary
print("===================================")
print("EXPERIMENT COMPLETED")
print("===================================")

print("Reference strings:", 15)
print("Frame capacities:", frame_capacities)
print("Algorithms:", list(algorithms.keys()))
print("Total experiment runs:", len(experiment_results))

print("\nResults saved to:", RESULTS_FILE.name)
