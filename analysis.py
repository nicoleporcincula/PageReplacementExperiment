import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================
# FILE LOCATIONS
# ==========================================

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "results.csv"

OUTPUT_DIR = BASE_DIR / "analysis_output"
GRAPH_DIR = OUTPUT_DIR / "graphs"

OUTPUT_DIR.mkdir(exist_ok=True)
GRAPH_DIR.mkdir(exist_ok=True)


# ==========================================
# LOAD EXPERIMENTAL DATA
# ==========================================

df = pd.read_csv(DATA_FILE)


# ==========================================
# CALCULATE AVERAGE RESULTS
# ==========================================

summary = (
    df.groupby(["workload", "frame_count", "algorithm"])
    .agg(
        average_page_faults=("page_faults", "mean"),
        average_page_hits=("page_hits", "mean"),
        average_replacements=("replacements", "mean"),
        average_page_fault_rate=("page_fault_rate", "mean"),
        average_page_hit_rate=("page_hit_rate", "mean")
    )
    .reset_index()
)


# ==========================================
# EXPORT SUMMARY TABLE
# ==========================================

summary_file = OUTPUT_DIR / "summary_tables.csv"

summary.to_csv(summary_file, index=False)


# ==========================================
# GRAPH GENERATION FUNCTION
# ==========================================

workloads = ["Locality", "Random", "Sequential"]

algorithms = ["FIFO", "LRU", "Optimal"]

frame_capacities = [3, 4, 5]


def generate_graph(metric, title, ylabel, filename):

    fig, axes = plt.subplots(
        1, 3,
        figsize=(16, 5)
    )

    for ax, workload in zip(axes, workloads):

        workload_data = summary[
            summary["workload"] == workload
        ]

        pivot_table = workload_data.pivot(
            index="frame_count",
            columns="algorithm",
            values=metric
        )

        pivot_table = pivot_table.reindex(
            index=frame_capacities,
            columns=algorithms
        )

        pivot_table.plot(
            kind="bar",
            ax=ax,
            width=0.75
        )

        ax.set_title(workload)
        ax.set_xlabel("Frame Capacity")
        ax.set_ylabel(ylabel)
        ax.set_xticks(range(len(frame_capacities)))
        ax.set_xticklabels(frame_capacities, rotation=0)
        ax.legend(title="Algorithm")
        ax.grid(axis="y", linestyle="--", alpha=0.5)

    fig.suptitle(title, fontsize=14)
    fig.tight_layout()

    graph_file = GRAPH_DIR / filename

    fig.savefig(graph_file, dpi=300)
    plt.close(fig)

    print("Graph saved:", graph_file.name)


# ==========================================
# GENERATE THREE GRAPHS
# ==========================================

generate_graph(
    "average_page_faults",
    "Average Page Faults by Workload and Frame Capacity",
    "Average Page Faults",
    "average_page_faults.png"
)

generate_graph(
    "average_page_fault_rate",
    "Average Page Fault Rate by Workload and Frame Capacity",
    "Page Fault Rate (%)",
    "average_page_fault_rate.png"
)

generate_graph(
    "average_page_hit_rate",
    "Average Page Hit Rate by Workload and Frame Capacity",
    "Page Hit Rate (%)",
    "average_page_hit_rate.png"
)


# ==========================================
# DISPLAY COMPLETION SUMMARY
# ==========================================

print("\n===================================")
print("ANALYSIS COMPLETED")
print("===================================")

print("Total experiment records:", len(df))
print("Summary records:", len(summary))
print("Summary table:", summary_file)
print("Graphs folder:", GRAPH_DIR)