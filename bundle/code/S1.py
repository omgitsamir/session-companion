import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DATA_PATH = os.environ.get("DATA_PATH")
OUT_PATH = os.environ.get("OUT_PATH")

if not DATA_PATH or not OUT_PATH:
    raise RuntimeError("DATA_PATH and OUT_PATH environment variables must be set.")

df = pd.read_csv(DATA_PATH)

df.columns = df.columns.str.strip()
for col in ["Vehicle Type", "Road class", "Quarter"]:
    df[col] = df[col].astype(str).str.strip()

df["Billion vehicle miles"] = pd.to_numeric(df["Billion vehicle miles"], errors="coerce")

df = df.dropna(subset=["Quarter", "Vehicle Type", "Road class", "Billion vehicle miles"])

df["Period"] = pd.PeriodIndex(df["Quarter"], freq="Q")
df = df.sort_values("Period")

road_totals = df[df["Road class"] == "All Roads"].copy()

rename = {
    "Cars and taxis": "Cars & taxis",
    "Light commercial vehicles": "Light commercial vehicles",
    "Heavy goods vehicles": "Heavy goods vehicles",
}
road_totals["Vehicle Type"] = road_totals["Vehicle Type"].replace(rename)

road_totals = road_totals.set_index("Period")
annual = (
    road_totals.groupby("Vehicle Type")["Billion vehicle miles"]
    .rolling(window=4, min_periods=4)
    .sum()
    .reset_index()
    .rename(columns={"Billion vehicle miles": "Annual_bvm"})
)

pivot = annual.pivot(index="Period", columns="Vehicle Type", values="Annual_bvm")
pivot = pivot.dropna()

base = pivot.iloc[0]
indexed = (pivot / base) * 100

plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"]})

fig, ax = plt.subplots(figsize=(13, 7), dpi=150)
fig.patch.set_facecolor("#FAFAFA")
ax.set_facecolor("#FAFAFA")

colors = {
    "Cars & taxis": "#2E5F8E",
    "Heavy goods vehicles": "#A42424",
    "Light commercial vehicles": "#E67E00",
}

ts = indexed.index.to_timestamp(how="end")

for vtype in ["Cars & taxis", "Heavy goods vehicles", "Light commercial vehicles"]:
    y = indexed[vtype].values
    lw = 4.0 if vtype == "Light commercial vehicles" else 2.4
    z = 4 if vtype == "Light commercial vehicles" else 2
    ax.plot(ts, y, label=vtype, color=colors[vtype], linewidth=lw, zorder=z)
    ax.fill_between(
        ts, 100, y, where=(y >= 100),
        color=colors[vtype], alpha=0.10, interpolate=True, zorder=1
    )

ax.axhline(100, color="#333333", linewidth=1.0, linestyle="--", zorder=1)

covid_period = pd.Period("2020Q2", freq="Q")
if covid_period in indexed.index:
    y_covid = indexed.loc[covid_period, "Light commercial vehicles"]
    ax.axvspan(
        pd.Period("2020Q1", freq="Q").to_timestamp(how="end"),
        pd.Period("2021Q1", freq="Q").to_timestamp(how="end"),
        color="#A42424", alpha=0.06, zorder=0, label=None,
    )
    ax.annotate(
        "COVID-19 shock",
        xy=(covid_period.to_timestamp(how="end"), y_covid),
        xytext=(pd.Period("2011Q1", freq="Q").to_timestamp(how="end"), y_covid + 45),
        arrowprops=dict(arrowstyle="->", color="#444444", lw=1.3),
        fontsize=10, color="#444444", fontweight="bold",
    )

fin_period = pd.Period("2008Q4", freq="Q")
if fin_period in indexed.index:
    y_fin = indexed.loc[fin_period, "Cars & taxis"]
    ax.annotate(
        "2008 financial crisis",
        xy=(fin_period.to_timestamp(how="end"), y_fin),
        xytext=(pd.Period("2002Q1", freq="Q").to_timestamp(how="end"), y_fin + 40),
        arrowprops=dict(arrowstyle="->", color="#444444", lw=1.3),
        fontsize=10, color="#444444",
    )

latest_period = indexed.index[-1]
latest_ts = latest_period.to_timestamp(how="end")
latest_van = indexed["Light commercial vehicles"].iloc[-1]
van_change = latest_van - 100
ax.annotate(
    f"Vans more than doubled\n(+{van_change:.0f}%)",
    xy=(latest_ts, latest_van),
    xytext=(latest_ts - pd.DateOffset(years=6), latest_van + 30),
    arrowprops=dict(arrowstyle="->", color=colors["Light commercial vehicles"], lw=1.8),
    fontsize=11, fontweight="bold", color=colors["Light commercial vehicles"],
)

fig.suptitle(
    "The Great British Van Boom",
    fontsize=22, fontweight="bold", ha="left", x=0.125, y=0.96,
)
ax.set_title(
    "Light commercial vehicles have left cars and lorries in the dust since 1994",
    fontsize=13, loc="left", color="#444444", pad=15,
)

ymax = indexed.max().max()
ax.set_ylim(80, ymax * 1.22)
ax.set_xlim(
    indexed.index[0].to_timestamp(how="end") - pd.DateOffset(months=6),
    indexed.index[-1].to_timestamp(how="end") + pd.DateOffset(months=12),
)
ax.set_ylabel("Index (Q4 1994 = 100)", fontsize=11)
ax.set_xlabel("")

ax.xaxis.set_major_locator(mdates.YearLocator(5))
ax.xaxis.set_minor_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.tick_params(axis="x", which="major", rotation=0)

ax.grid(True, linestyle="-", alpha=0.25)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
ax.spines["left"].set_color("#BBBBBB")
ax.spines["bottom"].set_color("#BBBBBB")

ax.legend(
    loc="upper left",
    frameon=True,
    fancybox=False,
    edgecolor="#CCCCCC",
    facecolor="white",
    fontsize=10,
)

short = {
    "Cars & taxis": "Cars",
    "Light commercial vehicles": "Vans",
    "Heavy goods vehicles": "HGVs",
}
stat_lines = [f"Change since Q4 1994"]
for vtype in ["Light commercial vehicles", "Cars & taxis", "Heavy goods vehicles"]:
    ch = indexed[vtype].iloc[-1] - 100
    sign = "+" if ch > 0 else ""
    stat_lines.append(f"{short[vtype]}: {sign}{ch:.0f}%")

stats_text = "\n".join(stat_lines)
ax.text(
    0.98, 0.55, stats_text,
    transform=ax.transAxes,
    fontsize=11, verticalalignment="center", horizontalalignment="right",
    family="monospace",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#CCCCCC", alpha=0.95),
)

fig.text(
    0.125, 0.02,
    "Source: DfT TRA2503b. Three selected vehicle types on all roads; not an exhaustive total. "
    "Rolling four-quarter sums remove seasonality. Recent quarters provisional.",
    fontsize=9, color="#666666",
)

plt.tight_layout(rect=[0, 0.04, 1, 0.94])
plt.savefig(OUT_PATH, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
