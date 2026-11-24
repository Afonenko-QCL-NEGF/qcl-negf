"""Render compact Fath profiles or the LiEL2014 spatial energy density."""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


RANKS = {7: ("7/Q21", "#166997"), 8: ("8/Q25", "#b74728")}


def fath(path, output):
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    z = rows[0]["cuts"]
    maps = {(r["rank"], r["step"]): r["row"] for r in rows if r["kind"] == "map"}
    obs = {(r["rank"], r["step"]): r["observation"]["GL20"] for r in rows if r["kind"] == "GL20"}
    last = max(step for rank, step in obs if (15-rank, step) in obs)
    fig, ((ax_raw, ax_cent), (ax_jump, ax_err)) = plt.subplots(2, 2, layout="constrained", figsize=(10, 7))
    for rank, (label, color) in RANKS.items():
        first, end = [obs[rank, step] for step in (1, last)]
        ax_raw.plot(z, end["profile"], color=color, label=label)
        ax_cent.plot(z, first["centered"], color=color, linestyle="--", alpha=0.65)
        ax_cent.plot(z, end["centered"], color=color)
        indices = sorted(step for current_rank, step in maps if current_rank == rank)
        for key, style, suffix in (("rK", "-", r"$r_K$"), ("rSigma", "--", r"$r_\Sigma$")):
            ax_err.semilogy(indices, [maps[rank, step][key] for step in indices],
                            color=color, linestyle=style, label=f"{label} {suffix}")
        ax_jump.plot(indices, [maps[rank, step]["fixed_segment_A_cm2"] for step in indices], color=color)
    for axis in (ax_raw, ax_cent):
        axis.set(xlabel="z, нм")
        for cut in (33.8473, 39.6410):
            axis.axvline(cut, color="#666666", linewidth=0.6)
    ax_raw.set(title=f"GL20, карта {last}", ylabel="J, А/см²")
    ax_cent.set(title="Первая карта пунктиром", ylabel="J − среднее, А/см²")
    ax_jump.set(xlabel="Свежая карта", ylabel="ΔJ (33,85–39,64 нм), А/см²")
    ax_err.set(xlabel="Свежая карта", ylabel="Свежая невязка")
    for axis in (ax_raw, ax_err):
        axis.legend(frameon=False)
    for axis in (ax_raw, ax_cent, ax_jump, ax_err):
        axis.grid(axis="y", alpha=0.18)
    fig.savefig(output, dpi=175, metadata={"Creator": "QCL NEGF"})
    if output.suffix == ".svg":
        output.write_text("\n".join(line.rstrip() for line in output.read_text().splitlines())+"\n")


def liel(path, output):
    r = np.genfromtxt(path, delimiter=",", names=True)
    energy = np.unique(r["energy_meV"])
    z = np.unique(r["z_nm"])
    form = (len(energy), len(z))
    z_weight = r["z_weight_nm"].reshape(form)[0]
    energy_weight = r["energy_weight_meV"].reshape(form)[:, 0]
    z_left = z[0] - z_weight[0]/2
    energy_left = energy[0] - energy_weight[0]/2
    z_edges = z_left + np.insert(np.cumsum(z_weight), 0, 0)
    energy_edges = energy_left + np.insert(np.cumsum(energy_weight), 0, 0)
    n = r["n_per_meV_nm3"].reshape(form)
    fig, ax = plt.subplots(layout="constrained", figsize=(8, 5))
    mesh = ax.pcolormesh(z_edges, energy_edges, n, cmap="magma",
                         shading="flat", rasterized=True)
    for wall in (5.20, 15.50, 17.20, 27.95, 31.55, 40.35, 44.30):
        ax.axvline(wall, color="white", alpha=0.42, linewidth=0.65)
    ax.set(xlabel="z, нм", ylabel="E, мэВ", ylim=(-60, 100),
           title="LiEL2014 · 50 мВ на период · 77 К")
    fig.colorbar(mesh, ax=ax, label="n(z, E), нм⁻³ мэВ⁻¹")
    fig.savefig(output, dpi=175, metadata={"Creator": "QCL NEGF"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("device", choices=("fath", "liel"))
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    {"fath": fath, "liel": liel}[args.device](args.input, args.output)
