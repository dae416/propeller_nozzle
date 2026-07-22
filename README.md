# Squid-Inspired Jet Nozzle Dataset

Thrust and power measurements for **32 propeller-driven jet nozzles** across three
design generations, together with the printable geometry of each one.

Generation 1 is a Latin-hypercube sweep of the design space. Generations 2 and 3
were proposed by a multi-objective Bayesian optimizer (ARD Matérn-5/2 GP + qEHVI)
trained on everything measured before them, maximizing thrust while minimizing
current draw.

Nozzles come in two materials, **rigid** and **flexible**. In Generation 1 each
shape was printed in both, so the same geometry appears twice. From Generation 2
on, rigid and flexible are optimized separately — each nozzle is one material
only, with its own geometry. All were measured on a dynamometer in a water tank.

![Nozzle performance map](performance_map.png)

The four representative shapes, with error bars over the three thrust pulses;
every other measured nozzle is behind them in faded form. Both axes are ratios
against the bare propeller, which sits at (1, 1). **Up and to the right is
better** — the power axis is reversed so that less power draw points right.
Indices for the faded points are in the results table below.

---

## Representative shapes

<table>
<tr>
<td width="25%" align="center"><img src="previews/G2F2.png" width="200"><br><b>G2F2</b><br>Flexible best 1</td>
<td width="25%" align="center"><img src="previews/G3F1.png" width="200"><br><b>G3F1</b><br>Flexible best 2</td>
<td width="25%" align="center"><img src="previews/G3R2.png" width="200"><br><b>G3R2</b><br>Rigid best</td>
<td width="25%" align="center"><img src="previews/G1F3.png" width="200"><br><b>G1F3</b><br>Flexible worst</td>
</tr>
</table>

| Index | Role | Generation | Material | Thrust vs no-nozzle | Power vs no-nozzle | STL |
|---|---|---|---|---|---|---|
| **`G2F2`** | Flexible best 1 | 2 | Flexible | **+10.5%** ± 4.4% | **+1.4%** ± 2.0% | [`G2_F_S2.stl`](STL/G2_F_S2.stl) |
| **`G3F1`** | Flexible best 2 | 3 | Flexible | **+1.7%** ± 3.8% | **-1.1%** ± 1.9% | [`G3_F_S1.stl`](STL/G3_F_S1.stl) |
| **`G3R2`** | Rigid best | 3 | Rigid | **-2.3%** ± 3.4% | **-4.2%** ± 2.9% | [`G3_R_S2.stl`](STL/G3_R_S2.stl) |
| **`G1F3`** | Flexible worst | 1 | Flexible | **-41.2%** ± 3.5% | **+18.4%** ± 3.5% | [`G1S3.stl`](STL/G1S3.stl) |

Their shape parameters:

| Index | bulge | neck | tip_expansion | R_tip (mm) | t_bottom (mm) | t_top (mm) | L (mm) |
|---|---|---|---|---|---|---|---|
| `G2F2` | 0.9743 | 0.936 | 0.9288 | 50.2222 | 0.9466 | 1.1814 | 139.7882 |
| `G3F1` | 1.1 | 1 | 0.9167 | 46.4392 | 2 | 2 | 42.5 |
| `G3R2` | 0.8463 | 0.9246 | 0.8258 | 55.25 | 0.7 | 2 | 42.5 |
| `G1F3` | 0.8455 | 0.9322 | 0.8378 | 33.9944 | 1.5733 | 1.8579 | 145.2361 |

---

## Reading the numbers

Both metrics are ratios against the **no-nozzle** rig running in the same session:

| | meaning | good direction | 1.0 means |
|---|---|---|---|
| **T\*** | thrust ÷ no-nozzle thrust | ↑ higher | same thrust as bare propeller |
| **I\*** | current ÷ no-nozzle current | ↓ lower | same current as bare propeller |
| **P\*** | power ÷ no-nozzle power | ↓ lower | supply voltage is fixed, so P\* = I\* exactly |

**The tables below report these as percent change from the bare propeller**,
because it reads more directly: `+10.5%` thrust is T\* = 1.105, `-4.2%` power is
P\* = 0.958. So **positive thrust is good, negative power is good**. The `±` is
the standard deviation over the three pulses, also in percent. The CSVs keep the
raw ratios.

**Why normalize at all?** The rig's absolute output drifts between test sessions
by up to 20% — two Gen2 Rigid sessions measured the bare propeller at 26.9 N and
32.2 N. Yet the nozzle-to-baseline ratios in those two sessions were 0.865 and
0.853: the drift is in the rig, not in the nozzles. Dividing it out is what makes
generations comparable. Which no-nozzle run backs each session was chosen per
session by the experimenter, from the recorded data.

The consequence is that **T\* and I\* compare across the whole table, but raw
newtons would not** — which is why raw values are not published here. The
`Session` column records which no-nozzle run each row was divided by.

---

## Results

⭐ marks a representative shape. Sorted by thrust within each group.

**Gen1 Flexible**

| Index | Thrust | Power | Session | STL |
|---|---|---|---|---|
| `G1FCylinder` | +12.8% ± 3.7% | +6.1% ± 6.8% | G1 | — |
| `G1F6` | -5.7% ± 1.5% | +1.1% ± 8.7% | G1 | [`G1S6.stl`](STL/G1S6.stl) |
| `G1F2` | -7.2% ± 3.4% | +6.7% ± 5.2% | G1 | [`G1S2.stl`](STL/G1S2.stl) |
| `G1F1` | -8.3% ± 8.9% | +15.9% ± 15.3% | G1 | [`G1S1.stl`](STL/G1S1.stl) |
| `G1F8` | -11.6% ± 4.1% | -0.2% ± 4.1% | G1 | [`G1S8.stl`](STL/G1S8.stl) |
| `G1F5` | -13.4% ± 2.2% | -1.6% ± 3.0% | G1 | [`G1S5.stl`](STL/G1S5.stl) |
| `G1F3` ⭐ | -41.2% ± 3.5% | +18.4% ± 3.5% | G1 | [`G1S3.stl`](STL/G1S3.stl) |
| `G1F4` | -46.0% ± 1.1% | +11.0% ± 5.2% | G1 | [`G1S4.stl`](STL/G1S4.stl) |

**Gen1 Rigid**

| Index | Thrust | Power | Session | STL |
|---|---|---|---|---|
| `G1RCylinder` | -5.0% ± 1.8% | +4.4% ± 4.7% | G1 | — |
| `G1R2` | -5.2% ± 3.0% | +2.4% ± 4.0% | G1 | [`G1S2.stl`](STL/G1S2.stl) |
| `G1R5` | -8.6% ± 2.7% | +1.3% ± 5.1% | G1 | [`G1S5.stl`](STL/G1S5.stl) |
| `G1R8` | -10.8% ± 2.2% | +4.0% ± 4.7% | G1 | [`G1S8.stl`](STL/G1S8.stl) |
| `G1R6` | -13.3% ± 3.5% | -4.6% ± 4.6% | G1 | [`G1S6.stl`](STL/G1S6.stl) |
| `G1R1` | -15.3% ± 5.0% | +5.2% ± 7.2% | G1 | [`G1S1.stl`](STL/G1S1.stl) |
| `G1R4` | -53.7% ± 1.5% | +11.5% ± 1.7% | G1 | [`G1S4.stl`](STL/G1S4.stl) |
| `G1R3` | -73.5% ± 0.8% | +21.9% ± 5.7% | G1 | [`G1S3.stl`](STL/G1S3.stl) |

**Gen2 Flexible**

| Index | Thrust | Power | Session | STL |
|---|---|---|---|---|
| `G2F2` ⭐ | +10.5% ± 4.4% | +1.4% ± 2.0% | G2F | [`G2_F_S2.stl`](STL/G2_F_S2.stl) |
| `G2F1` | +2.8% ± 3.4% | +2.8% ± 1.1% | G2F | [`G2_F_S1.stl`](STL/G2_F_S1.stl) |
| `G2F3` | +2.3% ± 0.4% | -0.0% ± 5.2% | G2F | [`G2_F_S3.stl`](STL/G2_F_S3.stl) |
| `G2F4` | -13.0% ± 3.7% | +3.8% ± 3.3% | G2F | [`G2_F_S4.stl`](STL/G2_F_S4.stl) |

**Gen2 Rigid**

| Index | Thrust | Power | Session | STL |
|---|---|---|---|---|
| `G2R3` | -8.3% ± 3.7% | -0.0% ± 3.6% | G2R_S34 | [`G2_R_S3.stl`](STL/G2_R_S3.stl) |
| `G2R2` | -8.9% ± 2.2% | +1.5% ± 3.8% | G2R_S12 | [`G2_R_S2.stl`](STL/G2_R_S2.stl) |
| `G2R1` | -18.1% ± 1.3% | +0.9% ± 2.5% | G2R_S12 | [`G2_R_S1.stl`](STL/G2_R_S1.stl) |
| `G2R4` | -21.0% ± 3.8% | +14.3% ± 2.1% | G2R_S34 | [`G2_R_S4.stl`](STL/G2_R_S4.stl) |

**Gen3 Flexible**

| Index | Thrust | Power | Session | STL |
|---|---|---|---|---|
| `G3F1` ⭐ | +1.7% ± 3.8% | -1.1% ± 1.9% | G3F | [`G3_F_S1.stl`](STL/G3_F_S1.stl) |
| `G3F2` | -6.7% ± 1.8% | -3.5% ± 4.1% | G3F | [`G3_F_S2.stl`](STL/G3_F_S2.stl) |
| `G3F4` | -6.9% ± 2.3% | +2.0% ± 1.0% | G3F | [`G3_F_S4.stl`](STL/G3_F_S4.stl) |
| `G3F3` | -16.3% ± 3.1% | +4.6% ± 4.1% | G3F | [`G3_F_S3.stl`](STL/G3_F_S3.stl) |

**Gen3 Rigid**

| Index | Thrust | Power | Session | STL |
|---|---|---|---|---|
| `G3R2` ⭐ | -2.3% ± 3.4% | -4.2% ± 2.9% | G3R | [`G3_R_S2.stl`](STL/G3_R_S2.stl) |
| `G3R1` | -8.9% ± 2.9% | -3.5% ± 2.2% | G3R | [`G3_R_S1.stl`](STL/G3_R_S1.stl) |
| `G3R3` | -10.2% ± 3.6% | -5.2% ± 2.2% | G3R | [`G3_R_S3.stl`](STL/G3_R_S3.stl) |
| `G3R4` | -11.2% ± 1.4% | -6.2% ± 1.5% | G3R | [`G3_R_S4.stl`](STL/G3_R_S4.stl) |

---

## Files

| File | Content |
|---|---|
| [`nozzle_performance.csv`](nozzle_performance.csv) | 32 rows — the table above, machine-readable |
| [`geometry_parameters.csv`](geometry_parameters.csv) | 7 shape parameters per nozzle, same 32 rows, same `Index` |
| [`STL/`](STL) | 23 printable geometries |
| [`previews/`](previews) | Renders of the representative shapes |
| [`performance_map.png`](performance_map.png) | The plot at the top of this page |
| [`make_plot.py`](make_plot.py) | Script that regenerates the plot from the CSV |

### Columns

| Column | Meaning |
|---|---|
| `Index` | `G<generation><material><shape>` — e.g. `G1F3` is Generation 1, Flexible, shape 3. Joins the two CSVs 1:1 |
| `Generation` | 1–3 |
| `Type` | `R` rigid, `F` flexible |
| `Session` | Which no-nozzle run this row was normalized against; rows sharing a session are the most directly comparable |
| `T_star`, `I_star`, `P_star` | Normalized thrust, current, power (see above) |
| `*_std` | Standard deviation over the three pulses, normalized |
| `STL_File` | Geometry in `STL/` |
| `Representative` | Set for the four shapes highlighted above |

### Geometry parameters

| Parameter | Unit | Meaning |
|---|---|---|
| `bulge` | – | Mid-body radial expansion factor |
| `neck` | – | Throat contraction factor |
| `tip_expansion` | – | Outlet flare factor |
| `R_tip_mean_mm` | mm | Mean outlet radius |
| `t_bottom_mm`, `t_top_mm` | mm | Wall thickness at inlet / outlet |
| `L_mm` | mm | Nozzle length |

All nozzles share a fixed mounting interface: 85 mm inner bore, 110 mm flange,
2 mm flange thickness, 8 × ⌀4 mm bolts on a 51 mm circle.

---

## Notes

- **Only Generation 1 shares geometry between materials.** `G1R3` and `G1F3` are
  the same printed shape in different material, so they carry identical parameter
  rows and point at the same STL. Generation 2 and 3 nozzles are each a single
  material with geometry of their own — `G2F1` and `G2R1` are unrelated shapes.
  The optimizer runs one GP per material, trained only on that material's data.
- **`Cylinder`** is a plain reference tube, not an optimizer output, and has no
  STL. In flexible material it out-thrusts every shaped Generation 1 nozzle
  (T\* = 1.127) — worth knowing before reading too much into the early sweep.
- **Shape 7** of the Generation 1 sweep was never tested, so the indices skip
  from 6 to 8.
- **32 rows are 32 physical nozzles but only 24 distinct geometries.** Each
  Generation 1 shape was printed in both materials, so its 8 shapes account for
  16 rows. Generation 2 and 3 contribute 8 rows and 8 geometries each.
- **Generation 3 Rigid** numbers come from a 2026-05-06 processing run whose raw
  dynamometer files are no longer in the source project, so they cannot currently
  be recomputed from scratch.

## License

Measurement data and geometry from a DARPA-funded study of squid-inspired
propulsion. Please contact the repository owner before reuse.
