
import csv
import random

# Reproducible data generation
random.seed(42)

NUM_REQUESTS = 50
PAGE_POOL = list(range(1, 11))

data = []

# 1. Locality-based workloads
for i in range(1, 6):
    rng = random.Random(100 + i)

    requests = []

    for _ in range(NUM_REQUESTS):
        if rng.random() < 0.80:
            # Frequently access pages 1-4
            page = rng.choice([1, 2, 3, 4])
        else:
            # Occasionally access pages 5-10
            page = rng.choice([5, 6, 7, 8, 9, 10])

        requests.append(page)

    data.append({
        "string_id": f"L{i}",
        "workload": "Locality",
        "requests": requests
    })

# 2. Random workloads
for i in range(1, 6):
    rng = random.Random(200 + i)

    requests = [
        rng.choice(PAGE_POOL)
        for _ in range(NUM_REQUESTS)
    ]

    data.append({
        "string_id": f"R{i}",
        "workload": "Random",
        "requests": requests
    })

# 3. Sequential workloads
for i in range(1, 6):
    start = i - 1

    requests = [
        PAGE_POOL[(start + j) % len(PAGE_POOL)]
        for j in range(NUM_REQUESTS)
    ]

    data.append({
        "string_id": f"S{i}",
        "workload": "Sequential",
        "requests": requests
    })

# CSV column names
headers = (
    ["string_id", "workload"]
    + [f"request_{i}" for i in range(1, NUM_REQUESTS + 1)]
)

# Write data to CSV
with open("reference_strings.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(headers)

    for item in data:
        writer.writerow([
            item["string_id"],
            item["workload"],
            *item["requests"]
        ])

print("Dataset successfully generated!")
print("Total reference strings:", len(data))
print("Requests per string:", NUM_REQUESTS)
print("Output: reference_strings.csv")
