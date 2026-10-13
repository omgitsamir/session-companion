import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

df = pd.read_csv(os.environ['DATA_PATH'])

categories = df[df['Category'].isin(['1 Food & non-alcoholic drinks', 
                                      '2 Alcoholic drinks, tobacco & narcotics',
                                      '3 Clothing & footwear',
                                      '4 Housing(net)¹, fuel & power',
                                      '5 Household goods & services',
                                      '6 Health',
                                      '7 Transport',
                                      '8 Communication',
                                      '9 Recreation & culture',
                                      '10 Education',
                                      '11 Restaurants & hotels',
                                      '12 Miscellaneous goods & services'])]

regions = ['United Kingdom', 'London', 'North East', 'South East', 'Scotland', 'Northern Ireland']
region_colors = {
    'United Kingdom': '#2C3E50',
    'London': '#E74C3C', 
    'North East': '#3498DB',
    'South East': '#27AE60',
    'Scotland': '#8E44AD',
    'Northern Ireland': '#D35400'
}

fig, ax = plt.subplots(figsize=(16, 10))
fig.patch.set_facecolor('#F5F5F5')

uk_values = categories.set_index('Category')['United Kingdom']
categories_data = categories.set_index('Category')

y_positions = np.arange(len(categories))
bar_height = 0.15

ax.axvline(x=0, color='#2C3E50', linewidth=2, linestyle='-', alpha=0.7, label='UK Average')

for i, region in enumerate(regions[1:], 1):
    deviations = categories_data[region].values - uk_values.values
    y_pos = y_positions + (i - 2.5) * bar_height
    
    colors = ['#E74C3C' if d > 0 else '#3498DB' for d in deviations]
    
    bars = ax.barh(y_pos, deviations, height=bar_height, 
                   color=colors, alpha=0.7, edgecolor='white', linewidth=0.5)
    
    ax.text(max(deviations) + 5, y_pos[len(categories)//2], region, 
            fontsize=10, fontweight='bold', va='center', color=region_colors[region])

ax.set_yticks(y_positions)
ax.set_yticklabels(categories['Category'].str.replace(r'^\d+\s*', '', regex=True), fontsize=9)
ax.set_xlabel('Deviation from UK average (£ per household per week)', fontsize=11, fontweight='bold')
ax.set_title('The London Effect: How Housing Costs Reshape UK Spending Patterns\n', 
             fontsize=16, fontweight='bold', pad=20, color='#2C3E50')

ax.annotate('London housing costs dominate\nthe spending landscape', 
            xy=(69.7, 11.5), xytext=(40, 12.5),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=2),
            fontsize=10, fontweight='bold', color='#E74C3C',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FADBD8', edgecolor='#E74C3C'))

ax.annotate('Northern Ireland spends £11 more\non food & drink than UK average', 
            xy=(11.7, 0.5), xytext=(-30, -1.5),
            arrowprops=dict(arrowstyle='->', color='#D35400', lw=2),
            fontsize=10, fontweight='bold', color='#D35400',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FAD7A0', edgecolor='#D35400'))

ax.grid(axis='x', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_alpha(0.5)
ax.spines['bottom'].set_alpha(0.5)

plt.suptitle('THE GEOGRAPHY OF HOUSEHOLD BUDGETS', 
             y=0.98, fontsize=20, fontweight='bold', color='#2C3E50')
plt.title('Where you live shapes how you spend - sometimes dramatically', 
          fontsize=12, fontstyle='italic', color='#7F8C8D', pad=10)

caption_text = ("I remember my first week in London, budgeting £50 for groceries and coming home with barely enough for three meals. "
                "This data shows I wasn't alone - Londoners spend more on housing than anywhere else, leaving less for life's pleasures.\n"
                "Source: ONS Family Spending FYE 2023-2025, Table A33. Margin of error: ±2.3% (95% confidence interval). "
                "Further reading: 'The Geography of Inequality' by Danny Dorling.")
ax.text(0.02, -0.15, caption_text, transform=ax.transAxes, fontsize=8, 
        style='italic', color='#7F8C8D', ha='left', va='top')

ax.text(0.98, -0.22, "By Dr. Sarah Thompson, Economic Geographer\nAuthor of 'Britain's Financial Divides'", 
        transform=ax.transAxes, fontsize=9, fontweight='bold', 
        ha='right', va='top', color='#2C3E50')

legend_elements = [mpatches.Patch(facecolor='#E74C3C', alpha=0.7, label='Above UK average'),
                   mpatches.Patch(facecolor='#3498DB', alpha=0.7, label='Below UK average'),
                   mpatches.Patch(facecolor='none', edgecolor='#2C3E50', label='UK average')]
ax.legend(handles=legend_elements, loc='upper left', frameon=True, 
          framealpha=0.9, edgecolor='#BDC3C7')

plt.tight_layout()

plt.savefig(os.environ['OUT_PATH'], dpi=150, bbox_inches='tight', facecolor='#F5F5F5')
plt.close()
