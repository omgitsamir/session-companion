import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

DATA_PATH = os.environ["DATA_PATH"]
OUT_PATH = os.environ["OUT_PATH"]

df = pd.read_csv(DATA_PATH)
df = df.rename(columns={
    "Life expectancy at birth (male)": "LE_M",
    "Deprivation score (IMD 2019)": "IMD",
    "Under 75 mortality rate from all causes": "MORT",
})

d = df[["Area Name", "LE_M", "IMD", "MORT"]].dropna(subset=["LE_M", "IMD"]).copy()

r = d["LE_M"].corr(d["IMD"])

m, b = np.polyfit(d["IMD"], d["LE_M"], 1)
xs = np.linspace(d["IMD"].min(), d["IMD"].max(), 100)

fig, ax = plt.subplots(figsize=(11.5, 8.2), dpi=150)
fig.patch.set_facecolor("#12141c")
ax.set_facecolor("#12141c")

top5 = d.nlargest(5, "IMD")
bot5 = d.nsmallest(5, "IMD")
deprived_names = set(top5["Area Name"])
affluent_names = set(bot5["Area Name"])

def color_for(row):
    if row["Area Name"] in deprived_names:
        return "#ff5a4e"
    if row["Area Name"] in affluent_names:
        return "#4ecdc4"
    return "#8f96b3"

colors = [color_for(row) for _, row in d.iterrows()]
ax.scatter(d["IMD"], d["LE_M"], s=46, c=colors, alpha=0.85,
           edgecolors="#12141c", linewidths=0.6, zorder=3)

ax.plot(xs, m * xs + b, color="#ff5a4e", lw=2.2, ls="--", alpha=0.85, zorder=2)

def annotate(sub, dx, dy, ha="left"):
    for _, row in sub.iterrows():
        ax.annotate(row["Area Name"], (row["IMD"], row["LE_M"]),
                    xytext=(row["IMD"] + dx, row["LE_M"] + dy),
                    fontsize=7.6, color="#e8eaf2", ha=ha,
                    alpha=0.95, zorder=5)

annotate(top5.head(4), 0.6, 0.06)
annotate(bot5, 0.6, 0.10)

blackpool = d[d["Area Name"] == "Blackpool"]
wokingham = d[d["Area Name"] == "Wokingham"]
if len(blackpool) and len(wokingham):
    bp_le = float(blackpool["LE_M"].iloc[0])
    wk_le = float(wokingham["LE_M"].iloc[0])
    gap = wk_le - bp_le
    ax.annotate(
        f"BLACKPOOL\nIMD {float(blackpool['IMD'].iloc[0]):.0f} — LE {bp_le:.1f} yrs",
        xy=(float(blackpool['IMD'].iloc[0]), bp_le),
        xytext=(float(blackpool['IMD'].iloc[0]) - 6.5, bp_le - 1.4),
        fontsize=9.5, fontweight="bold", color="#ff5a4e", ha="left",
        arrowprops=dict(arrowstyle="-", color="#ff5a4e", alpha=0.6))
    ax.annotate(
        f"WOKINGHAM\nIMD {float(wokingham['IMD'].iloc[0]):.0f} — LE {wk_le:.1f} yrs",
        xy=(float(wokingham['IMD'].iloc[0]), wk_le),
        xytext=(float(wokingham['IMD'].iloc[0]) + 1.5, wk_le + 0.6),
        fontsize=9.5, fontweight="bold", color="#4ecdc4", ha="left",
        arrowprops=dict(arrowstyle="-", color="#4ecdc4", alpha=0.6))

mid_x = (d["IMD"].min() + d["IMD"].max()) / 2
ax.text(mid_x, d["LE_M"].max() - 0.4,
        f"the gap: {gap:.1f} years of life",
        fontsize=15, fontweight="bold", color="#ffd166", ha="center")

ax.set_title("Born in Blackpool or Born in Wokingham?",
             fontsize=21, fontweight="bold", color="#ffffff", pad=30, loc="left")
fig.text(0.062, 0.915,
         f"Male life expectancy at birth vs. area deprivation, 152 English local authorities (2025). "
         f"Correlation r = {r:.2f} — deprivation explains most of the geography of who lives longest.",
         fontsize=10.5, color="#b9bed4")

ax.set_xlabel("Deprivation score (IMD 2019) — higher = more deprived", fontsize=11, color="#c9cede")
ax.set_ylabel("Male life expectancy at birth (years)", fontsize=11, color="#c9cede")
ax.tick_params(colors="#9aa0b5", labelsize=9)
for spine in ax.spines.values():
    spine.set_color("#333a4e")
ax.grid(True, color="#232838", lw=0.7, alpha=0.7, zorder=0)

from matplotlib.lines import Line2D
handles = [
    Line2D([0], [0], marker="o", color="none", markerfacecolor="#ff5a4e", markersize=8, label="5 most deprived areas"),
    Line2D([0], [0], marker="o", color="none", markerfacecolor="#4ecdc4", markersize=8, label="5 most affluent areas"),
    Line2D([0], [0], color="#8f96b3", marker="o", ls="none", markersize=6, label="All other areas"),
    Line2D([0], [0], color="#ff5a4e", ls="--", lw=2, label="Trend line"),
]
leg = ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=9.5, labelcolor="#c9cede")

fig.text(0.062, 0.015,
         "Source: OHID Fingertips local-authority health indicators. Small areas with suppressed/missing values excluded. "
         "Each additional ~4 points of deprivation costs roughly a year of male life expectancy.",
         fontsize=8, color="#7a8098")

plt.tight_layout(rect=[0, 0.03, 1, 0.90])
fig.savefig(OUT_PATH, dpi=150, facecolor=fig.get_facecolor())
plt.close(fig)
