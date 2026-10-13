import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch

path = os.environ["DATA_PATH"]
out = os.environ["OUT_PATH"]

df = pd.read_csv(path)
df.columns = [str(c).strip() for c in df.columns]

value_col = "Billion vehicle miles"
df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
df["Quarter"] = df["Quarter"].astype(str).str.strip()
df = df.dropna(subset=[value_col, "Quarter"])

road = "All Roads"
if road not in df["Road class"].unique():
    road = df["Road class"].dropna().iloc[0]

wanted = ["Cars and taxis", "Heavy goods vehicles"]
d = df[
    (df["Road class"] == road) &
    (df["Vehicle Type"].isin(wanted))
].copy()

d["year"] = d["Quarter"].str.extract(r"(\d{4})").astype(float)
d["q"] = d["Quarter"].str.extract(r"Q([1-4])").astype(float)
d = d.sort_values(["year", "q", "Vehicle Type"])

d["rolling_4q"] = (
    d.groupby("Vehicle Type")[value_col]
     .transform(lambda s: s.rolling(4, min_periods=2).mean())
)

wide = d.pivot_table(
    index=["year", "q", "Quarter"],
    columns="Vehicle Type",
    values="rolling_4q",
    aggfunc="mean"
).reset_index().sort_values(["year", "q"])

x = np.arange(len(wide))
cars = wide["Cars and taxis"].to_numpy(dtype=float)
hgv = wide["Heavy goods vehicles"].to_numpy(dtype=float)
quarters = wide["Quarter"].tolist()

navy = "#12304A"
blue = "#4D7895"
pale_blue = "#AFC5D2"
ink = "#10202E"
muted = "#627482"
orange = "#E06B45"
cream = "#F7F4EE"
grid = "#DCE4E8"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "xtick.color": muted,
    "ytick.color": muted,
})

fig, ax = plt.subplots(figsize=(15, 8.7), facecolor=cream)
fig.subplots_adjust(left=0.085, right=0.88, top=0.79, bottom=0.16)
ax.set_facecolor(cream)

for series, colour in [(cars, navy), (hgv, blue)]:
    ax.plot(
        x + 0.9, series, color=colour, lw=8, alpha=0.10,
        solid_capstyle="round", zorder=2
    )

line1, = ax.plot(
    x, cars, color=navy, lw=3.2, solid_capstyle="round",
    label="Cars & taxis", zorder=5,
    path_effects=[pe.SimpleLineShadow(offset=(1.8, -1.8), alpha=0.18),
                  pe.Normal()]
)
ax.fill_between(x, cars, 0, color=pale_blue, alpha=0.08, zorder=1)

ax2 = ax.twinx()
ax2.set_facecolor("none")
line2, = ax2.plot(
    x, hgv, color=blue, lw=3.0, solid_capstyle="round",
    label="Health score", zorder=6,
    path_effects=[pe.SimpleLineShadow(offset=(1.8, -1.8), alpha=0.18),
                  pe.Normal()]
)

if "2020Q1" in quarters and "2021Q2" in quarters:
    start = quarters.index("2020Q1")
    end = quarters.index("2021Q2")
    ax.axvspan(start, end, color=orange, alpha=0.075, zorder=0)
    ax.text(
        (start + end) / 2, max(np.nanmax(cars), 1) * 0.99,
        "COVID disruption", ha="center", va="top",
        fontsize=9, color=orange, fontweight="bold"
    )

ax.set_xlim(-2, len(x) + 3)
ax.set_ylim(0, max(np.nanmax(cars) * 1.18, 1))
ax2.set_ylim(0, max(np.nanmax(hgv) * 1.32, 1))

ax.set_ylabel("Cars & taxis — billion vehicle miles", color=navy, fontweight="bold")
ax2.set_ylabel("Health score", color=blue, fontweight="bold", labelpad=12)

ax.grid(axis="y", color=grid, lw=0.9)
ax.grid(axis="x", visible=False)
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_color(pale_blue)
ax2.spines["right"].set_linewidth(1.5)

tick_idx = [i for i, q in enumerate(quarters) if q.endswith("Q1")]
ax.set_xticks(tick_idx)
ax.set_xticklabels([quarters[i][:4] for i in tick_idx])
ax.tick_params(axis="x", length=0, pad=9)
ax.tick_params(axis="y", length=0)
ax2.tick_params(axis="y", length=0)

last_valid_c = np.where(np.isfinite(cars))[0][-1]
last_valid_h = np.where(np.isfinite(hgv))[0][-1]
ax.annotate(
    f"Latest 4Q avg\n{cars[last_valid_c]:.1f} bn",
    xy=(last_valid_c, cars[last_valid_c]),
    xytext=(last_valid_c + 1.0, cars[last_valid_c] + 1.7),
    color=navy, fontsize=10, fontweight="bold",
    arrowprops=dict(arrowstyle="-", color=navy, lw=1.1),
)
ax2.annotate(
    f"Latest 4Q avg\n{hgv[last_valid_h]:.1f} bn",
    xy=(last_valid_h, hgv[last_valid_h]),
    xytext=(last_valid_h + 1.0, hgv[last_valid_h] - 1.2),
    color=blue, fontsize=10, fontweight="bold",
    arrowprops=dict(arrowstyle="-", color=blue, lw=1.1),
)

ax.text(
    0.01, 1.055, "PAST", transform=ax.transAxes,
    color=muted, fontsize=10, fontweight="bold"
)
ax.text(
    0.99, 1.055, "FUTURE →  the road ahead",
    transform=ax.transAxes, ha="right",
    color=orange, fontsize=10, fontweight="bold"
)

if len(x) > 20:
    mid = len(x) // 2
    ax.annotate(
        "Like a tide that never quite returns,\n"
        "car traffic rose for decades — then reset.",
        xy=(mid, cars[mid]), xycoords="data",
        xytext=(mid - 18, ax.get_ylim()[1] * 0.70),
        fontsize=10.5, color=ink, linespacing=1.35,
        arrowprops=dict(arrowstyle="->", color=muted, lw=1.1,
                        connectionstyle="arc3,rad=-0.18"),
        bbox=dict(boxstyle="round,pad=0.45", fc="#EEF3F5",
                  ec="#C7D5DC", alpha=0.95),
    )

fig.text(
    0.085, 0.925,
    "The road came back — but not all the way",
    fontsize=25, color=ink, fontweight="bold"
)
fig.text(
    0.085, 0.887,
    "Great Britain’s traffic story is a long climb, a sudden brake, and a still-visible gap",
    fontsize=13.5, color=muted
)

leg = ax.legend(
    handles=[line1, line2], loc="upper left", bbox_to_anchor=(0.0, 1.015),
    ncol=2, frameon=False, fontsize=10.5, handlelength=2.8,
    columnspacing=1.8
)
for text in leg.get_texts():
    text.set_color(ink)

valid_cars = cars[np.isfinite(cars)]
valid_hgv = hgv[np.isfinite(hgv)]
latest_label = quarters[last_valid_c]
covid_pre = np.nan
if "2019Q4" in quarters:
    pre_i = quarters.index("2019Q4")
    covid_pre = cars[pre_i]

fact_text = (
    "CONTEXT  |  WHAT YOU’RE SEEING\n"
    f"129 quarterly observations • {road} • 4-quarter averages\n"
    f"{latest_label} is provisional. The chart keeps vehicle types separate:\n"
    "these categories are not an all-traffic total.\n"
    f"Cars now sit at {cars[last_valid_c]:.1f} bn miles"
)
if np.isfinite(covid_pre):
    fact_text += f", versus {covid_pre:.1f} bn just before the shock."

box = FancyBboxPatch(
    (0.61, 0.815), 0.30, 0.105, transform=fig.transFigure,
    boxstyle="round,pad=0.012,rounding_size=0.012",
    facecolor="#EAF0F2", edgecolor="#C8D5DA", linewidth=1.0
)
fig.add_artist(box)
fig.text(
    0.625, 0.902, fact_text, transform=fig.transFigure,
    fontsize=9.3, color=ink, va="top", linespacing=1.45
)

fig.text(
    0.085, 0.075,
    "Caption: A modest long-run reset after 2020 — with the distance between the lines doing most of the talking.",
    fontsize=10.5, color=muted, style="italic"
)
fig.text(
    0.085, 0.043,
    'Source: DfT TRA2503b. “Health score” is a deliberately broad label for the heavy-goods-vehicle series; '
    'recent quarters may be revised. Seasonal calendar-quarter data shown as 4-quarter averages.',
    fontsize=8.7, color=muted
)

plt.savefig(out, dpi=150, facecolor=fig.get_facecolor(), bbox_inches="tight")
plt.close(fig)
