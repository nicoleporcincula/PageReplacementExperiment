
from fifo import fifo
from lru import lru
from optimal import optimal


algorithms = {
    "FIFO": fifo,
    "LRU": lru,
    "Optimal": optimal
}


# Validation test cases
test_cases = [
    {
        "name": "Changed Frame Capacity",
        "reference_string": [1, 2, 3, 1, 4, 1, 2, 5],
        "frame_count": 4,
        "expected": (5, 3, 1)
    },
    {
        "name": "Repeated Page Requests",
        "reference_string": [1, 1, 1, 1],
        "frame_count": 3,
        "expected": (1, 3, 0)
    },
    {
        "name": "All Pages Different",
        "reference_string": [1, 2, 3, 4, 5],
        "frame_count": 3,
        "expected": (5, 0, 2)
    },
    {
        "name": "Frames Exceed Unique Pages",
        "reference_string": [1, 2, 1, 2, 3, 1],
        "frame_count": 5,
        "expected": (3, 3, 0)
    }
]


for test in test_cases:

    print("\n===================================")
    print("TEST:", test["name"])
    print("===================================")

    reference_string = test["reference_string"]
    frame_count = test["frame_count"]

    for name, algorithm in algorithms.items():

        result = algorithm(reference_string, frame_count)

        actual = (
            result["page_faults"],
            result["page_hits"],
            result["replacements"]
        )

        expected = test["expected"]

        # Check metrics against expected values
        metrics_pass = actual == expected

        # Check that hits and faults equal total requests
        count_pass = (
            result["page_faults"] + result["page_hits"]
            == len(reference_string)
        )

        # Check that rates sum to 100%
        rate_pass = abs(
            result["page_fault_rate"]
            + result["page_hit_rate"] - 100
        ) < 0.000001

        passed = metrics_pass and count_pass and rate_pass

        print("\nAlgorithm:", name)
        print("Faults:", result["page_faults"])
        print("Hits:", result["page_hits"])
        print("Replacements:", result["replacements"])
        print("Fault Rate:", result["page_fault_rate"], "%")
        print("Hit Rate:", result["page_hit_rate"], "%")
        print("Validation:", "PASS" if passed else "FAIL")
