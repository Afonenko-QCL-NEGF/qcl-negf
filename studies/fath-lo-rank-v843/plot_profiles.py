#!/usr/bin/env python3
"""Plot resolved Fath and V843 current at every cut, including both seams."""
import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read(path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def profile_plot(directory, baseline, output):
    fath = read(directory / "fath-D-expanded-cell.json")
    v843 = [read(directory / f"v843-selected-{k}.json") for k in (5, 9, 17)]
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.0), layout="constrained")
    colors = ("#174999", "#B74425", "#007261")

    ax = axes[0]
    for index, (obs, label) in enumerate(((baseline["observed"], "7 мод"),
                                        (fath["observation"], "8 мод"))):
        current = obs["current"]
        centered = [j - current["mean_internal_A_cm2"] for j in obs["current_A_cm2"]]
        ax.plot(fath["cut_coordinates_nm"], centered, color=colors[index],
                label=label, linewidth=1.65, marker="o", markersize=3,
                markevery=[0, len(centered) - 1])
    target = baseline["observed"]["current"]["target_tolerance_A_cm2"]
    ax.axhspan(-target, target, color="#808080", alpha=0.15, label="Допуск 7 мод")
    ax.axhline(0, color="#555555", linewidth=0.75)
    ax.set(title="Fath, 54 мВ на период", xlabel="Координата сечения, нм",
           ylabel="Ток относительно среднего, А/см²")
    ax.legend(loc="upper left", frameon=False, fontsize=9)

    ax = axes[1]
    for index, sample in enumerate(v843):
        obs = sample["observation"]
        profile = obs["current_A_cm2"]
        mean = obs["current"]["mean_internal_A_cm2"]
        label = f"{sample['rings']} колец, средний {mean:.0f}"
        ax.plot(sample["cuts_nm"], profile, color=colors[index], label=label,
                linewidth=1.65, marker="o", markersize=3,
                markevery=[0, len(profile) - 1])
    ax.set(title="V843, 21 кВ/см", xlabel="Координата сечения, нм",
           ylabel="Ток вдоль +z, А/см²")
    ax.legend(loc="best", frameon=False, fontsize=9)

    for ax in axes:
        ax.grid(axis="y", alpha=0.16, linewidth=0.6)
        ax.spines[["top", "right"]].set_visible(False)
        ax.margins(x=0.035)
    fig.savefig(output, dpi=175, metadata={"Title": "Fath and V843 resolved current profiles"})
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    baseline = Path(__file__).resolve().parents[1] / "fath-v843" / "evidence" / "fath-F13-positive-long.json"
    if args.output.exists():
        raise FileExistsError(args.output)
    profile_plot(args.reports, read(baseline), args.output)
