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
rows = list(csv.DictReader(open(f"{S}/nozzle_performance.csv")))

STYLE = {                       # (generation, type) -> color, marker
    (1, "F"): ("#ff8080", "o"), (1, "R"): ("#9a9a9a", "s"),
    (2, "F"): ("#8c0d0d", "o"), (2, "R"): ("#262626", "s"),
    (3, "F"): ("#5a005a", "o"), (3, "R"): ("#00264d", "s"),
}
LABEL = {(1, "F"): "Gen1 flexible", (1, "R"): "Gen1 rigid",
         (2, "F"): "Gen2 flexible", (2, "R"): "Gen2 rigid",
         (3, "F"): "Gen3 flexible", (3, "R"): "Gen3 rigid"}

fig, ax = plt.subplots(figsize=(9, 7), dpi=160)
ax.set_facecolor("white")

for key, (color, marker) in STYLE.items():
    grp = [r for r in rows if (int(r["Generation"]), r["Type"]) == key]
    ax.errorbar([float(r["P_star"]) for r in grp], [float(r["T_star"]) for r in grp],
                xerr=[float(r["P_star_std"]) for r in grp],
                yerr=[float(r["T_star_std"]) for r in grp],
                fmt=marker, color=color, markersize=7, linestyle="none",
                elinewidth=0.8, capsize=2, alpha=0.9, label=LABEL[key])

ax.axvline(1.0, color="0.6", linestyle="--", linewidth=0.8, zorder=0)
ax.axhline(1.0, color="0.6", linestyle="--", linewidth=0.8, zorder=0)
ax.invert_xaxis()                                 # less power -> right
ax.set_xlabel("P* = power / no-nozzle power   (decreasing $\\rightarrow$ better)")
ax.set_ylabel("T* = thrust / no-nozzle thrust   (increasing $\\rightarrow$ better)")
ax.set_title("Nozzle performance map — no-nozzle rig = (1, 1)", fontweight="bold")
ax.grid(True, color="0.9", linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(loc="upper left", fontsize=9, framealpha=1)

# Index labels: greedy placement — try offsets around the point, keep the first
# that clears every label already placed. The cluster near T*~0.9 is dense enough
# that fixed offsets become unreadable.
OFFSETS = [(-5, 6), (-5, -13), (7, -3), (-30, -3), (7, 8), (-32, 8), (7, -13), (-32, -13)]
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
placed = []
for r in sorted(rows, key=lambda r: -float(r["T_star"])):
    x, y = float(r["P_star"]), float(r["T_star"])
    ann = ax.annotate(r["Index"], (x, y), xytext=OFFSETS[0], textcoords="offset points",
                      fontsize=7, color="#333333",
                      fontweight="bold" if r["Representative"] else "normal")
    best, best_hits = OFFSETS[0], None
    for off in OFFSETS:
        ann.set_position(off)
        bb = ann.get_window_extent(renderer).expanded(1.05, 1.05)
        hits = sum(bb.overlaps(p) for p in placed)
        if hits == 0:
            best, best_hits = off, 0
            break
        if best_hits is None or hits < best_hits:
            best, best_hits = off, hits
    ann.set_position(best)
    placed.append(ann.get_window_extent(renderer).expanded(1.05, 1.05))
fig.tight_layout()
fig.savefig(f"{S}/performance_map.png", facecolor="white")
print("saved", f"{S}/performance_map.png")
