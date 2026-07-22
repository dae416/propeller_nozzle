#!/usr/bin/env python3
"""Performance map for the README: normalized thrust vs normalized power.

X axis is reversed so that "better" (less power) is to the right, matching the
MATLAB C07a plot. Colors follow the same generation scheme as the pipeline.
"""
import csv, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

S = sys.argv[1]
allrows = list(csv.DictReader(open(f"{S}/nozzle_performance.csv")))
rows = [r for r in allrows if r["Representative"]]   # labelled in full; rest are context

STYLE = {                       # (generation, type) -> color, marker
    (1, "F"): ("#ff8080", "o"), (1, "R"): ("#9a9a9a", "s"),
    (2, "F"): ("#8c0d0d", "o"), (2, "R"): ("#262626", "s"),
    (3, "F"): ("#5a005a", "o"), (3, "R"): ("#00264d", "s"),
    (4, "F"): ("#0b6b6b", "o"),
}
LABEL = {(1, "F"): "Gen1 flexible", (1, "R"): "Gen1 rigid",
         (2, "F"): "Gen2 flexible", (2, "R"): "Gen2 rigid",
         (3, "F"): "Gen3 flexible", (3, "R"): "Gen3 rigid",
         (4, "F"): "Gen4 flexible"}

fig, ax = plt.subplots(figsize=(9, 7), dpi=160)
ax.set_facecolor("white")

# every other nozzle: faded, no error bars, no label — context only
for key, (color, marker) in STYLE.items():
    rest = [r for r in allrows if (int(r["Generation"]), r["Type"]) == key and not r["Representative"]]
    if rest:
        ax.plot([float(r["P_star"]) for r in rest], [float(r["T_star"]) for r in rest],
                marker, color=color, markersize=6, linestyle="none", alpha=0.25, zorder=1)

for key, (color, marker) in STYLE.items():
    grp = [r for r in rows if (int(r["Generation"]), r["Type"]) == key]
    if not grp:                                   # legend entry only, no points
        if any((int(r["Generation"]), r["Type"]) == key for r in allrows):
            ax.plot([], [], marker, color=color, markersize=6, alpha=0.4, linestyle="none",
                    label=LABEL[key])
        continue
    ax.errorbar([float(r["P_star"]) for r in grp], [float(r["T_star"]) for r in grp],
                xerr=[float(r["P_star_std"]) for r in grp],
                yerr=[float(r["T_star_std"]) for r in grp],
                fmt=marker, color=color, markersize=7, linestyle="none",
                elinewidth=0.8, capsize=2, alpha=0.95, zorder=3, label=LABEL[key])

ax.axvline(1.0, color="0.6", linestyle="--", linewidth=0.8, zorder=0)
ax.axhline(1.0, color="0.6", linestyle="--", linewidth=0.8, zorder=0)
ax.invert_xaxis()                                 # less power -> right
ax.set_xlabel("P* = power / no-nozzle power   (decreasing $\\rightarrow$ better)")
ax.set_ylabel("T* = thrust / no-nozzle thrust   (increasing $\\rightarrow$ better)")
ax.set_title("Nozzle performance map — no-nozzle rig = (1, 1)", fontweight="bold")
ax.grid(True, color="0.9", linewidth=0.6)
ax.set_axisbelow(True)
h, l = ax.get_legend_handles_labels()          # keep the legend in generation order
order = sorted(range(len(l)), key=lambda i: list(LABEL.values()).index(l[i]))
ax.legend([h[i] for i in order], [l[i] for i in order],
          loc="upper left", fontsize=9, framealpha=1)

OFF = {}
for r in rows:
    ax.annotate(f"{r['Index']}\n{r['Representative']}", (float(r["P_star"]), float(r["T_star"])),
                xytext=OFF.get(r["Index"], (-6, 9)), textcoords="offset points", fontsize=9, fontweight="bold",
                color="#333333")

fig.tight_layout()
fig.savefig(f"{S}/performance_map.png", facecolor="white")
print("saved", f"{S}/performance_map.png")
