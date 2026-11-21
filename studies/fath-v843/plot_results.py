#!/usr/bin/env python3
"""Reproduce the published figures from the compact terminal reports."""

import argparse
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np


ROOT = Path(__file__).resolve().parent
COLLISION_COLORS = {
    "LO": "#3458a8",
    "acoustic": "#a65b16",
    "impurity": "#a43532",
    "IFR": "#725292",
    "alloy": "#2d736d",
}


def load_json(path):
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def load_rows(path):
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def axes_style(ax):
    ax.spines[["right", "top"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#637181")
    ax.tick_params(color="#637181")
    ax.grid(which="major", color="#dce3e9", linewidth=0.65)
    ax.set_axisbelow(True)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())


def fath_profile(path, output):
    report = load_json(path)
    resolved = report["measured"]["resolved"]
    cuts = report["current_midpoints_nm"]
    figure, (current, sources) = plt.subplots(
        2, 1, figsize=(7.8, 6), sharex=True, layout="constrained",
        gridspec_kw={"height_ratios": [1, 1.15]},
    )
    raw = resolved["current_A_cm2"]
    current.plot(cuts, raw, color="#172d43", label="Физические связи BDD")
    current.scatter([cuts[0], cuts[-1]], [raw[0], raw[-1]], color="#172d43", zorder=5, clip_on=False)
    current.plot(cuts, resolved["coherent_projected_A_cm2"], color="#637b9b",
                 ls="--", label="Поднятый модовый коммутатор")
    current.set_ylabel(r"$J(z)$, А/см²")
    current.set_title("Fath при 54 мВ на период и 10 К", loc="left")
    current.legend(frameon=False, loc="best")
    labels = {"LO": "LO", "acoustic": "Акустика", "impurity": "Примеси",
              "IFR": "Шероховатость", "alloy": "Сплав"}
    for channel, values in resolved["collision_cumulative_A_cm2"].items():
        sources.plot(cuts, values, color=COLLISION_COLORS[channel], label=labels[channel])
    sources.plot(cuts, resolved["spatial_projection_gap_A_cm2"], ls="--",
                 color="#25384a", label="Разность BDD и проекции")
    sources.axhline(0, color="#8294a5", lw=0.8)
    sources.set_ylabel("Накопленный вклад, А/см²")
    sources.set_xlabel("Координата сечения, нм")
    sources.legend(frameon=False, ncol=2, loc="best")
    for ax in (current, sources):
        axes_style(ax)
        ax.set_xlim(cuts[0], cuts[-1])
    figure.savefig(output, dpi=200)
    plt.close(figure)


def v843_current(numerics, output):
    figure, ax = plt.subplots(figsize=(8.5, 5), layout="constrained")
    published = load_rows(ROOT / "jonasson-figure-2.csv")
    ax.axvspan(30/3.616, 60/3.616, alpha=0.12, color="#c5a471", label="Скачок напряжения")
    for series, label, style in (
        ("NEGF50", "Dupont NEGF, решётка 50 К", {"color": "#2e7764", "lw": 1.25}),
        ("DM50", "Jonasson DM, решётка 50 К", {"color": "#335da6", "lw": 1.25}),
        ("experiment10", "Измерение, теплоотвод 10 К",
         {"color": "#a64439", "marker": "s", "ms": 3.2, "lw": 0}),
    ):
        data = [row for row in published if row["series"] == series]
        ax.plot([float(x["field_kV_cm"]) for x in data],
                [float(x["current_A_cm2"])/1000 for x in data], label=label, **style)
        for case in numerics:
            target = case["published"][series]
            lo, hi = target["digitization_range_A_cm2"]
            if series == "NEGF50":
                lo, hi = case["published_negf_digitization_envelope_A_cm2"]
            left, right = target["interpolation_bracket_kV_cm"]
            x, y = case["field_kV_cm"], target["current_A_cm2"]
            ax.errorbar(x, y/1000, xerr=[[max(0, x-left)], [max(0, right-x)]],
                        yerr=[[max(0, y-lo)/1000], [max(0, hi-y)/1000]],
                        fmt="none", ecolor=style["color"], elinewidth=0.9, capsize=2, alpha=0.75)
    fields = [x["field_kV_cm"] for x in numerics]
    means = np.array([x["mean_internal_A_cm2"] for x in numerics])
    bounds = np.array([x["resolved_min_max_A_cm2"] for x in numerics])
    ax.errorbar(fields, means/1000, yerr=np.stack((means - bounds[:, 0], bounds[:, 1] - means))/1000,
                fmt="D", color="#192a3b", markersize=5, elinewidth=1.2, capsize=4,
                label="Связанная NEGF, пространственный диапазон")
    differences = np.array([x["observed_sensitivity_A_cm2"] for x in numerics])
    ax.errorbar(fields, means/1000, yerr=differences/1000, fmt="none",
                color="#6e5794", elinewidth=1.8, capsize=6, label="Численная чувствительность")
    ax.set(xlabel="Поле, кВ/см", ylabel="Плотность тока, кА/см²", xlim=(1, 25))
    ax.set_title("Тёмный расчёт V843 и опубликованная ВАХ", loc="left")
    axes_style(ax)
    ax.legend(frameon=False, fontsize=9, loc="best")
    figure.savefig(output, dpi=200)
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fath_report", type=Path)
    parser.add_argument("v843_comparison", type=Path)
    parser.add_argument("output_directory", type=Path)
    options = parser.parse_args()
    options.output_directory.mkdir(parents=True, exist_ok=True)
    fath_profile(options.fath_report, options.output_directory / "fath-spatial-balance.png")
    v843_current(load_json(options.v843_comparison)["cases"],
                 options.output_directory / "v843-current-field.png")


if __name__ == "__main__":
    main()
