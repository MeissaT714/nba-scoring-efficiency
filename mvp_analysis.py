import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np

mvp = pd.read_csv('mvp_seasons.csv - Sheet1.csv')

mvp['TS%'] = pd.to_numeric(mvp['TS%'], errors='coerce')
mvp['USG%'] = pd.to_numeric(mvp['USG%'], errors='coerce')
mvp['PTS'] = pd.to_numeric(mvp['PTS'], errors='coerce')
mvp['Year'] = pd.to_numeric(mvp['Year'], errors='coerce')

mvp['Label'] = mvp['Player'].apply(lambda x: x.split()[0][0] + '. ' + ' '.join(x.split()[1:])) + ' \'' + mvp['Year'].astype(str).str[-2:]

norm = mcolors.Normalize(vmin=mvp['Year'].min(), vmax=mvp['Year'].max())
cmap = cm.Blues
colors = [cmap(norm(year)) for year in mvp['Year']]

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(22, 10))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

for i, (_, row) in enumerate(mvp.iterrows()):
    ax.scatter(row['USG%'], row['TS%'], s=((row['PTS'] - 10) ** 2) * 3,
               color=colors[i], edgecolors='white', linewidths=0.5, zorder=2)
    ax.annotate(row['Label'], (row['USG%'], row['TS%']),
                fontsize=7, ha='left', color='white',
                xytext=(8, 8), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.7, edgecolor='none'))

sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label('Year', fontsize=10, color='white')
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')

ax.set_xlabel('Usage Rate (USG%)', color='white')
ax.set_ylabel('True Shooting % (TS%)', color='white')
ax.set_title('NBA MVP Seasons — Scoring Volume vs Efficiency (2001–2025)', color='white')
ax.set_xlim(mvp['USG%'].min() - 2, mvp['USG%'].max() + 2)
ax.set_ylim(mvp['TS%'].min() - 0.02, mvp['TS%'].max() + 0.02)
ax.tick_params(colors='white')
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')

plt.tight_layout()
plt.savefig('mvp_volume_vs_efficiency.png', dpi=150, facecolor='black')
plt.show()
print("Chart saved!")