
def fifo(reference_string, frame_count):
    frames = []

    page_faults = 0
    page_hits = 0
    replacements = 0

    history = []

    for page in reference_string:

        if page in frames:
            # Page is already in memory
            page_hits += 1
            result = "Hit"

        else:
            # Page is not in memory
            page_faults += 1
            result = "Fault"

            if len(frames) < frame_count:
                # Fill an empty frame
                frames.append(page)

            else:
                # Remove the oldest-loaded page
                frames.pop(0)
                frames.append(page)
                replacements += 1

        # Save the state of memory after each request
        history.append({
            "page": page,
            "frames": frames.copy(),
            "result": result
        })

    total_requests = len(reference_string)

    page_fault_rate = (page_faults / total_requests) * 100
    page_hit_rate = (page_hits / total_requests) * 100

    return {
        "algorithm": "FIFO",
        "page_faults": page_faults,
        "page_hits": page_hits,
        "replacements": replacements,
        "page_fault_rate": page_fault_rate,
        "page_hit_rate": page_hit_rate,
        "history": history
    }


# Manual test
if __name__ == "__main__":

    test_string = [1, 2, 3, 1, 4, 1, 2, 5]

    result = fifo(test_string, 3)

    print("Algorithm:", result["algorithm"])
    print("Page Faults:", result["page_faults"])
    print("Page Hits:", result["page_hits"])
    print("Replacements:", result["replacements"])
    print("Page Fault Rate:", result["page_fault_rate"], "%")
    print("Page Hit Rate:", result["page_hit_rate"], "%")

    print("\nPage-by-page history:")

    for step in result["history"]:
        print(
            "Request:", step["page"],
            "| Frames:", step["frames"],
            "| Result:", step["result"]
        )
