import os
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data_path = os.environ.get("DATA_PATH", "spending.csv")
out_path = os.environ.get("OUT_PATH", "uk_regional_spending_squeeze.png")

raw_json = [
    {
        "Category": "1 Food & non-alcoholic drinks",
        "United Kingdom": 69.2,
        "England": 69.5,
        "North East": 60.5,
        "North West": 66.4,
        "Yorkshire and The Humber": 66.0,
        "East Midlands": 69.3,
        "West Midlands": 66.4,
        "East": 74.2,
        "London": 68.7,
        "South East": 74.4,
        "South West": 73.0,
        "Wales": 66.1,
        "Scotland": 64.8,
        "Northern Ireland": 80.9,
    },
    {
        "Category": "2 Alcoholic drinks, tobacco & narcotics",
        "United Kingdom": 11.1,
        "England": 10.8,
        "North East": 9.2,
        "North West": 10.5,
        "Yorkshire and The Humber": 11.1,
        "East Midlands": 11.1,
        "West Midlands": 10.6,
        "East": 11.8,
        "London": 8.4,
        "South East": 12.0,
        "South West": 12.6,
        "Wales": 13.5,
        "Scotland": 10.7,
        "Northern Ireland": 14.3,
    },
    {
        "Category": "3 Clothing & footwear",
        "United Kingdom": 17.4,
        "England": 17.6,
        "North East": 17.5,
        "North West": 17.3,
        "Yorkshire and The Humber": 16.3,
        "East Midlands": 17.0,
        "West Midlands": 15.5,
        "East": 20.5,
        "London": 20.1,
        "South East": 15.4,
        "South West": 18.7,
        "Wales": 16.1,
        "Scotland": 13.7,
        "Northern Ireland": 25.5,
    },
    {
        "Category": "4 Housing(net)¹, fuel & power",
        "United Kingdom": 112.5,
        "England": 117.1,
        "North East": 82.1,
        "North West": 95.0,
        "Yorkshire and The Humber": 97.4,
        "East Midlands": 103.0,
        "West Midlands": 98.5,
        "East": 112.5,
        "London": 182.2,
        "South East": 122.4,
        "South West": 111.9,
        "Wales": 94.3,
        "Scotland": 90.0,
        "Northern Ireland": 76.7,
    },
    {
        "Category": "5 Household goods & services",
        "United Kingdom": 38.3,
        "England": 39.4,
        "North East": 35.1,
        "North West": 38.7,
        "Yorkshire and The Humber": 40.5,
        "East Midlands": 34.9,
        "West Midlands": 31.5,
        "East": 46.2,
        "London": 37.8,
        "South East": 40.0,
        "South West": 46.4,
        "Wales": 34.3,
        "Scotland": 30.0,
        "Northern Ireland": 38.7,
    },
    {
        "Category": "6 Health",
        "United Kingdom": 9.4,
        "England": 9.7,
        "North East": 5.3,
        "North West": 7.5,
        "Yorkshire and The Humber": 8.6,
        "East Midlands": 7.7,
        "West Midlands": 9.3,
        "East": 10.5,
        "London": 10.6,
        "South East": 12.7,
        "South West": 11.3,
        "Wales": 9.3,
        "Scotland": 6.4,
        "Northern Ireland": 10.4,
    },
    {
        "Category": "7 Transport",
        "United Kingdom": 88.0,
        "England": 88.9,
        "North East": 69.0,
        "North West": 72.8,
        "Yorkshire and The Humber": 82.8,
        "East Midlands": 88.5,
        "West Midlands": 89.1,
        "East": 107.3,
        "London": 71.4,
        "South East": 110.3,
        "South West": 98.3,
        "Wales": 84.7,
        "Scotland": 78.7,
        "Northern Ireland": 94.0,
    },
    {
        "Category": "8 Communication",
        "United Kingdom": 21.6,
        "England": 21.8,
        "North East": 20.0,
        "North West": 21.5,
        "Yorkshire and The Humber": 21.0,
        "East Midlands": 21.1,
        "West Midlands": 21.4,
        "East": 23.6,
        "London": 21.2,
        "South East": 22.8,
        "South West": 22.0,
        "Wales": 20.7,
        "Scotland": 21.1,
        "Northern Ireland": 21.3,
    },
    {
        "Category": "9 Recreation & culture",
        "United Kingdom": 73.4,
        "England": 73.9,
        "North East": 64.0,
        "North West": 68.8,
        "Yorkshire and The Humber": 71.0,
        "East Midlands": 64.9,
        "West Midlands": 74.2,
        "East": 84.4,
        "London": 55.6,
        "South East": 93.3,
        "South West": 80.1,
        "Wales": 78.9,
        "Scotland": 70.2,
        "Northern Ireland": 60.6,
    },
    {
        "Category": "10 Education",
        "United Kingdom": 6.3,
        "England": 7.1,
        "North East": 3.9,
        "North West": 3.5,
        "Yorkshire and The Humber": 3.8,
        "East Midlands": 3.0,
        "West Midlands": 4.7,
        "East": 7.2,
        "London": 12.9,
        "South East": 11.0,
        "South West": 7.1,
        "Wales": 2.2,
        "Scotland": 2.5,
        "Northern Ireland": 3.1,
    },
    {
        "Category": "11 Restaurants & hotels",
        "United Kingdom": 44.7,
        "England": 46.1,
        "North East": 35.9,
        "North West": 39.9,
        "Yorkshire and The Humber": 44.2,
        "East Midlands": 36.8,
        "West Midlands": 38.3,
        "East": 48.0,
        "London": 54.0,
        "South East": 52.2,
        "South West": 52.7,
        "Wales": 42.1,
        "Scotland": 33.3,
        "Northern Ireland": 44.4,
    },
    {
        "Category": "12 Miscellaneous goods & services",
        "United Kingdom": 45.2,
        "England": 46.6,
        "North East": 36.6,
        "North West": 42.0,
        "Yorkshire and The Humber": 43.2,
        "East Midlands": 41.0,
        "West Midlands": 42.4,
        "East": 54.4,
        "London": 47.6,
        "South East": 51.9,
        "South West": 51.2,
        "Wales": 39.3,
        "Scotland": 35.3,
        "Northern Ireland": 47.8,
    },
    {
        "Category": "13 Other expenditure items",
        "United Kingdom": 85.4,
        "England": 88.3,
        "North East": 66.3,
        "North West": 70.6,
        "Yorkshire and The Humber": 74.2,
        "East Midlands": 74.6,
        "West Midlands": 79.6,
        "East": 97.7,
        "London": 105.3,
        "South East": 106.0,
        "South West": 92.6,
        "Wales": 72.6,
        "Scotland": 71.1,
        "Northern Ireland": 66.1,
    },
    {
        "Category": "Total expenditure",
        "United Kingdom": 622.6,
        "England": 636.7,
        "North East": 505.5,
        "North West": 554.7,
        "Yorkshire and The Humber": 580.1,
        "East Midlands": 572.9,
        "West Midlands": 581.5,
        "East": 698.4,
        "London": 695.9,
        "South East": 724.2,
        "South West": 677.9,
        "Wales": 574.0,
        "Scotland": 528.0,
        "Northern Ireland": 583.8,
    },
]

if os.path.exists(data_path):
    try:
        df = pd.read_csv(data_path)
    except Exception:
        df = pd.DataFrame(raw_json)
else:
    df = pd.DataFrame(raw_json)

df["Category_Clean"] = (
    df["Category"].astype(str).str.replace(r"[¹\*\"]", "", regex=True).str.strip()
)

def get_row(keyword):
    match = df[df["Category_Clean"].str.contains(keyword, case=False, na=False)]
    if not match.empty:
        return match.iloc[0]
    return None

housing_row = get_row("Housing")
rec_row = get_row("Recreation")
total_row = get_row("Total expenditure")

regions = [
    "London",
    "South East",
    "East",
    "South West",
    "East Midlands",
    "West Midlands",
    "Yorkshire and The Humber",
    "North West",
    "Wales",
    "Scotland",
    "North East",
    "Northern Ireland",
]

housing_vals = [float(housing_row[r]) for r in regions]
rec_vals = [float(rec_row[r]) for r in regions]
total_vals = [float(total_row[r]) for r in regions]
housing_shares = [
    (h / t) * 100 for h, t in zip(housing_vals, total_vals, strict=False)
]

uk_housing = float(housing_row["United Kingdom"])
uk_rec = float(rec_row["United Kingdom"])

coicop_categories = [
    ("4 Housing, fuel & power", "Housing"),
    ("13 Other expenditure", "Other expenditure"),
    ("11 Restaurants & hotels", "Restaurants"),
    ("10 Education", "Education"),
    ("3 Clothing & footwear", "Clothing"),
    ("12 Misc goods & services", "Misc"),
    ("6 Health", "Health"),
    ("8 Communication", "Communication"),
    ("1 Food & non-alc drinks", "Food"),
    ("5 Household goods", "Household goods"),
    ("2 Alcohol & tobacco", "Alcohol"),
    ("7 Transport", "Transport"),
    ("9 Recreation & culture", "Recreation"),
]

diff_labels = []
diff_vals = []
for label, kw in coicop_categories:
    r = get_row(kw)
    if r is not None:
        diff = float(r["London"]) - float(r["United Kingdom"])
        diff_labels.append(label)
        diff_vals.append(diff)

plt.rcParams["font.sans-serif"] = [
    "DejaVu Sans",
    "Arial",
    "Helvetica",
    "sans-serif",
]
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.edgecolor"] = "#D0D7DE"
plt.rcParams["axes.linewidth"] = 0.8

fig = plt.figure(figsize=(15.5, 12.0), facecolor="#F8FAFC")

gs = fig.add_gridspec(
    nrows=3,
    ncols=2,
    height_ratios=[0.11, 0.54, 0.35],
    hspace=0.38,
    wspace=0.18,
    left=0.07,
    right=0.94,
    top=0.90,
    bottom=0.06,
)

fig.text(
    0.07,
    0.965,
    "The London Rent Trap: How Housing Costs Choke Recreation in the Capital",
    fontsize=20,
    weight="bold",
    color="#0F172A",
)
fig.text(
    0.07,
    0.938,
    "Average weekly household expenditure across UK regions (ONS Family Spending, FYE 2023–2025). Londoners pay £182.20/week on shelter,\nforcing discretionary spending on culture, sports, and entertainment to fall below every other region in the United Kingdom.",
    fontsize=10.5,
    color="#475569",
    linespacing=1.35,
)

kpi_ax = fig.add_subplot(gs[0, :])
kpi_ax.axis("off")

def draw_card(ax, x, y, width, height, title, value, subtitle, highlight=False):
    bg_color = "#FFFFFF"
    border_color = "#E2E8F0" if not highlight else "#E02424"
    box = patches.FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.015,rounding_size=0.03",
        facecolor=bg_color,
        edgecolor=border_color,
        linewidth=1.8 if highlight else 1.0,
        transform=ax.transAxes,
        zorder=2,
    )
    ax.add_patch(box)
    ax.text(
        x + 0.025,
        y + height - 0.28,
        title,
        transform=ax.transAxes,
        fontsize=9.0,
        weight="bold",
        color="#64748B",
        zorder=3,
    )
    ax.text(
        x + 0.025,
        y + height - 0.65,
        value,
        transform=ax.transAxes,
        fontsize=18.0,
        weight="bold",
        color="#E02424" if highlight else "#0F172A",
        zorder=3,
    )
    ax.text(
        x + 0.025,
        y + 0.12,
        subtitle,
        transform=ax.transAxes,
        fontsize=8.5,
        color="#64748B",
        zorder=3,
    )

draw_card(
    kpi_ax,
    0.00,
    0.02,
    0.31,
    0.96,
    "LONDON HOUSING & ENERGY",
    "£182.20 / wk",
    "62% above the UK average (£112.50)",
    highlight=True,
)
draw_card(
    kpi_ax,
    0.345,
    0.02,
    0.31,
    0.96,
    "LONDON SHELTER SHARE",
    "26.2% of budget",
    "Highest in UK (vs 16.2% in North East)",
    highlight=False,
)
draw_card(
    kpi_ax,
    0.69,
    0.02,
    0.31,
    0.96,
    "LONDON RECREATION SPEND",
    "£55.60 / wk",
    "Lowest in the UK (vs £93.30 in South East)",
    highlight=True,
)

ax_h = fig.add_subplot(gs[1, 0])
ax_r = fig.add_subplot(gs[1, 1])

y_pos = np.arange(len(regions))[::-1]

h_colors = [
    "#E02424" if r == "London" else "#1E3A8A" if r == "South East" else "#94A3B8"
    for r in regions
]
r_colors = [
    "#E02424" if r == "London" else "#0D9488" if r == "South East" else "#94A3B8"
    for r in regions
]

bars_h = ax_h.barh(
    y_pos, housing_vals, color=h_colors, height=0.68, zorder=3, edgecolor="none"
)
ax_h.axvline(
    uk_housing,
    color="#0F172A",
    linestyle="--",
    linewidth=1.2,
    alpha=0.75,
    zorder=4,
)
ax_h.text(
    uk_housing + 2,
    -0.6,
    f"UK Avg: £{uk_housing:.2f}",
    fontsize=9.0,
    fontweight="bold",
    color="#0F172A",
    alpha=0.85,
)

ax_h.set_yticks(y_pos)
ax_h.set_yticklabels(regions, fontsize=10, weight="medium", color="#1E293B")
ax_h.set_xlim(0, 225)
ax_h.set_xlabel("Weekly Spend (£ per household)", fontsize=9.5, color="#475569")
ax_h.set_title(
    "A. Housing (net), Fuel & Power\nLondon costs outstrip all other regions",
    loc="left",
    fontsize=12,
    weight="bold",
    color="#0F172A",
    pad=10,
)
ax_h.grid(axis="x", linestyle=":", alpha=0.6, zorder=1)
ax_h.set_facecolor("#FFFFFF")

for idx, (bar, val, share) in enumerate(
    zip(bars_h, housing_vals, housing_shares, strict=False)
):
    w = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2
    if regions[idx] == "London":
        ax_h.text(
            w + 3.0,
            y,
            f"£{val:.1f} ({share:.1f}% of all spend)",
            va="center",
            ha="left",
            fontsize=9.2,
            weight="bold",
            color="#E02424",
        )
    else:
        ax_h.text(
            w + 2.5,
            y,
            f"£{val:.1f}",
            va="center",
            ha="left",
            fontsize=8.5,
            color="#475569",
        )

bars_r = ax_r.barh(
    y_pos, rec_vals, color=r_colors, height=0.68, zorder=3, edgecolor="none"
)
ax_r.axvline(
    uk_rec, color="#0F172A", linestyle="--", linewidth=1.2, alpha=0.75, zorder=4
)
ax_r.text(
    uk_rec + 1.5,
    -0.6,
    f"UK Avg: £{uk_rec:.2f}",
    fontsize=9.0,
    fontweight="bold",
    color="#0F172A",
    alpha=0.85,
)

ax_r.set_yticks(y_pos)
ax_r.set_yticklabels([])
ax_r.set_xlim(0, 115)
ax_r.set_xlabel("Weekly Spend (£ per household)", fontsize=9.5, color="#475569")
ax_r.set_title(
    "B. Recreation & Culture\nLondon sinks to bottom of the national table",
    loc="left",
    fontsize=12,
    weight="bold",
    color="#0F172A",
    pad=10,
)
ax_r.grid(axis="x", linestyle=":", alpha=0.6, zorder=1)
ax_r.set_facecolor("#FFFFFF")

for idx, (bar, val) in enumerate(zip(bars_r, rec_vals, strict=False)):
    w = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2
    if regions[idx] == "London":
        ax_r.text(
            w + 2.5,
            y,
            f"£{val:.1f}  (Lowest in UK)",
            va="center",
            ha="left",
            fontsize=9.2,
            weight="bold",
            color="#E02424",
        )
    elif regions[idx] == "South East":
        ax_r.text(
            w + 2.5,
            y,
            f"£{val:.1f} (Leader)",
            va="center",
            ha="left",
            fontsize=8.5,
            weight="bold",
            color="#0D9488",
        )
    else:
        ax_r.text(
            w + 2.5,
            y,
            f"£{val:.1f}",
            va="center",
            ha="left",
            fontsize=8.5,
            color="#475569",
        )

ax_div = fig.add_subplot(gs[2, :])
ax_div.set_facecolor("#FFFFFF")

sort_order = np.argsort(diff_vals)
sorted_labels = [diff_labels[i] for i in sort_order]
sorted_diffs = [diff_vals[i] for i in sort_order]
y_div = np.arange(len(sorted_labels))

div_colors = [
    "#E02424" if d > 15 else "#F97316" if d > 0 else "#0D9488"
    for d in sorted_diffs
]

bars_div = ax_div.barh(
    y_div, sorted_diffs, color=div_colors, height=0.68, zorder=3
)
ax_div.axvline(0, color="#64748B", linewidth=1.1, zorder=4)

ax_div.set_yticks(y_div)
ax_div.set_yticklabels(
    sorted_labels, fontsize=9.5, weight="medium", color="#1E293B"
)
ax_div.set_xlim(-28, 82)
ax_div.set_xlabel(
    "Weekly Difference vs UK National Average (£/week)",
    fontsize=9.5,
    color="#475569",
)
ax_div.set_title(
    "C. The Structural Trade-Off: Where London Households Spend More vs. Less (Relative to UK Average)\n"
    "To pay the £69.70 housing premium, Londoners sacrifice car transport (-£16.60) and recreation (-£17.80).",
    loc="left",
    fontsize=11.5,
    weight="bold",
    color="#0F172A",
    pad=8,
)
ax_div.grid(axis="x", linestyle=":", alpha=0.6, zorder=1)

for bar, val in zip(bars_div, sorted_diffs, strict=False):
    w = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2
    if w >= 0:
        ax_div.text(
            w + 1.2,
            y,
            f"+£{val:.2f}",
            va="center",
            ha="left",
            fontsize=8.8,
            weight="bold" if abs(val) > 10 else "normal",
            color="#E02424" if val > 15 else "#C2410C" if val > 0 else "#475569",
        )
    else:
        ax_div.text(
            w - 1.2,
            y,
            f"-£{abs(val):.2f}",
            va="center",
            ha="right",
            fontsize=8.8,
            weight="bold" if abs(val) > 10 else "normal",
            color="#0D9488",
        )

ax_div.text(
    58,
    y_div[-1] - 0.2,
    "Rent & Energy\nDevour +£69.70/wk",
    fontsize=8.5,
    weight="bold",
    color="#E02424",
    ha="center",
    va="center",
    bbox=dict(
        boxstyle="round,pad=0.3",
        facecolor="#FEF2F2",
        edgecolor="#FECACA",
        linewidth=0.8,
    ),
)
ax_div.text(
    -20,
    y_div[0] + 0.5,
    "Public transit & smaller homes\noffset costs by -£34.40/wk",
    fontsize=8.5,
    weight="bold",
    color="#0D9488",
    ha="center",
    va="center",
    bbox=dict(
        boxstyle="round,pad=0.3",
        facecolor="#F0FDFA",
        edgecolor="#99F6E4",
        linewidth=0.8,
    ),
)

fig.text(
    0.07,
    0.015,
    "Source: Office for National Statistics (ONS) Family Spending, Table A33 (3-year weighted average FYE 2023 to FYE 2025). Values represent mean expenditure per household per week.",
    fontsize=8.2,
    color="#94A3B8",
)

plt.savefig(
    out_path, dpi=150, facecolor=fig.get_facecolor(), bbox_inches="tight"
)
plt.close()
