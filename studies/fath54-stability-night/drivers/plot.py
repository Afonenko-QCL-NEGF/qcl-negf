#!/usr/bin/env python3
"""Build a static figure from the published compact evidence."""
import argparse
from pathlib import Path
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence",type=Path)
    args = parser.parse_args()
    evidence = args.evidence
    with (evidence/"fresh-maps.csv").open(newline="") as stream:
        maps = list(csv.DictReader(stream))
    with (evidence/"profiles.csv").open(newline="") as stream:
        profiles = list(csv.DictReader(stream))
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10.5,
                         "axes.spines.top":False,"axes.spines.right":False,
                         "svg.fonttype":"none","axes.titleweight":"bold"})
    fig,axes = plt.subplots(1,2,figsize=(11.4,4.6),layout="constrained")
    colors = {"primary7":"#21618c", "expanded8":"#176847", "radial25":"#8a4923"}
    cases = {"primary7":"K13, 7 мод", "expanded8":"K13, 8 мод", "radial25":"K25, 7 мод"}
    z = [float(row["z_nm"]) for row in profiles]
    left,right = axes
    for run in cases:
        trace = [row for row in maps if row["run"]==run and row["kind"]=="map"]
        if not trace:
            continue
        latest = int(trace[-1]["step"])
        profile_key = "radial25_last" if run=="radial25" else f"{run}_{latest}"
        y = [float(row[profile_key]) for row in profiles]
        case_label = (f"{cases[run]}, {len(trace)} карт после переноса" if run=="radial25"
                      else f"{cases[run]}, карта {latest}")
        left.plot(z,y,lw=2.1,color=colors[run],label=case_label)
        if run!="radial25" and f"{run}_48" in profiles[0] and latest!=48:
            left.plot(z,[float(row[f"{run}_48"]) for row in profiles],lw=0.9,
                      color=colors[run],alpha=.5,ls="--")
        iterations = [int(row["step"]) for row in trace]
        right.semilogy(iterations,[max(float(row["rK"]),1e-16) for row in trace],
                       color=colors[run],lw=2.1,label=cases[run])
        right.semilogy(iterations,[max(float(row["rSigma"]),1e-16) for row in trace],
                       color=colors[run],lw=1,ls="--")
    left.axvspan(33.84729,39.64097,color="#d8ab56",alpha=.20)
    left.set(title="Ток через физические сечения",
             xlabel="Продольная координата z, нм", ylabel="J, А/см²")
    left.legend(frameon=False, loc="best",fontsize=9)
    right.axvline(48,color="#666666",lw=.8,ls=":")
    right.set(title="Свежие невязки до смешивания",
              xlabel="Номер карты",ylabel="rK (сплошная) и rΣ (пунктир)")
    right.legend(frameon=False,loc="best",fontsize=9)
    for ax in axes:
        ax.grid(axis="y",color="#dddddd",linewidth=.7)
        ax.set_axisbelow(True)
    fig.savefig(evidence/"profiles.svg",metadata={"Date":None})
    plt.close(fig)


if __name__=="__main__":
    main()
