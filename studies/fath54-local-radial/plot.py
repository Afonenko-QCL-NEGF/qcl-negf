"""Plot the measured section currents and radial density for the Fath report."""

from pathlib import Path
import csv
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def rows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def main(evidence):
    profiles = rows(evidence/"profiles.csv")
    charges = rows(evidence/"radial-charge.csv")
    present = {row["level"] for row in charges}
    plt.rcParams.update({"font.family":"DejaVu Sans", "axes.spines.top":False,
                         "axes.spines.right":False,"svg.fonttype":"none"})
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.5), layout="constrained")
    physical, centered, input_charge, fresh_charge = axes.flat
    z = [float(row["z_nm"]) for row in profiles]
    series = (
        ("K25", "#214f7c", "-", "K25"),
        ("K27", "#9d4521", "--", "K27"),
        ("K31", "#277052", "-.", "K31"),
        ("K31_shift", "#70459b", ":", "K31, сдвиг"),
    )
    local_peaks = {input_charge: 0., fresh_charge: 0.}
    for name, color, line, label in series:
        if name not in present:
            continue
        for axis, key in ((physical, "profile"), (centered, "centered")):
            y = [float(row[f"{name}_{key}_A_cm2"]) for row in profiles]
            axis.plot(z, y, color=color, linestyle=line, lw=1.65, label=label)
        cells = [row for row in charges if row["level"] == name]
        edges = [float(cells[0]["u_left_nm-2"])] + [float(row["u_right_nm-2"]) for row in cells]
        bounds = [x**.5 for x in edges]
        for axis, key in ((input_charge,"dyson_input_charge_cm-2"),(fresh_charge,"fresh_charge_cm-2")):
            density = [float(row[key])/(right-left)*1e-12
                       for row,left,right in zip(cells,edges[:-1],edges[1:],strict=True)]
            axis.stairs(density,bounds,color=color,linestyle=line,lw=1.65,baseline=None)
            local_peaks[axis]=max(local_peaks[axis],max(y for y,low,high in
                zip(density,bounds[:-1],bounds[1:],strict=True) if low<.225 and high>.125))
    for axis, title, y in ((physical,"Ток свежей карты","J, А/см²"),
                            (centered,"Форма пространственного профиля","J − ⟨J⟩, А/см²")):
        axis.axvspan(33.84729,39.64097,color="#d8ab56",alpha=.18,zorder=0)
        axis.set(title=title,xlabel="Продольная координата z, нм",ylabel=y)
    for axis, title in ((input_charge,"Сырой заряд на входе после Дайсона"),
                        (fresh_charge,"Сырой заряд свежей карты")):
        axis.axvspan(.15,.20,color="#d8ab56",alpha=.18,zorder=0)
        axis.set(title=title,xlabel="Поперечный импульс k, нм⁻¹",
                 ylabel="dN/d(k²), 10¹² см⁻² нм²",xlim=(.125,.225),
                 ylim=(0,1.10*local_peaks[axis]))
    for axis in axes.flat:
        axis.grid(axis="y",color="#dddddd",linewidth=.65)
        axis.set_axisbelow(True)
    physical.legend(frameon=False, loc="best")
    svg = evidence/"profiles.svg"
    fig.savefig(svg,metadata={"Date":None})
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines())+"\n")
    plt.close(fig)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
