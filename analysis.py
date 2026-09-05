import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

players = pd.read_csv('advancedstats_py.csv - Sheet1-2.csv')
teams = pd.read_csv('teamwins_py.csv - Sheet1.csv')
pergame = pd.read_csv('correctedpergamestats.csv - Sheet1.csv')

players['G'] = pd.to_numeric(players['G'], errors='coerce')
players['MP'] = pd.to_numeric(players['MP'], errors='coerce')
players['TS%'] = pd.to_numeric(players['TS%'], errors='coerce')
players['USG%'] = pd.to_numeric(players['USG%'], errors='coerce')
teams['W'] = pd.to_numeric(teams['W'], errors='coerce')
pergame['PTS'] = pd.to_numeric(pergame['PTS'], errors='coerce')

players = players[players['MP'] >= 1800]

name_to_abbrev = {
    'Atlanta Hawks': 'ATL', 'Boston Celtics': 'BOS', 'Brooklyn Nets': 'BRK',
    'Charlotte Hornets': 'CHO', 'Chicago Bulls': 'CHI', 'Cleveland Cavaliers': 'CLE',
    'Dallas Mavericks': 'DAL', 'Denver Nuggets': 'DEN', 'Detroit Pistons': 'DET',
    'Golden State Warriors': 'GSW', 'Houston Rockets': 'HOU', 'Indiana Pacers': 'IND',
    'Los Angeles Clippers': 'LAC', 'Los Angeles Lakers': 'LAL', 'Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA', 'Milwaukee Bucks': 'MIL', 'Minnesota Timberwolves': 'MIN',
    'New Orleans Pelicans': 'NOP', 'New York Knicks': 'NYK', 'Oklahoma City Thunder': 'OKC',
    'Orlando Magic': 'ORL', 'Philadelphia 76ers': 'PHI', 'Phoenix Suns': 'PHO',
    'Portland Trail Blazers': 'POR', 'Sacramento Kings': 'SAC', 'San Antonio Spurs': 'SAS',
    'Toronto Raptors': 'TOR', 'Utah Jazz': 'UTA', 'Washington Wizards': 'WAS'
}

teams['Team_abbrev'] = teams['Team'].map(name_to_abbrev)
merged = players.merge(teams[['Team_abbrev', 'W']], left_on='Team', right_on='Team_abbrev', how='left')

merged['Player'] = merged['Player'].astype(str)
pergame['Player'] = pergame['Player'].astype(str)
merged = merged.merge(pergame[['Player', 'PTS']], on='Player', how='left')

plot_data = merged[merged['USG%'] >= 22.0].copy()
plot_data['Label'] = plot_data['Player'].apply(lambda x: x.split()[0][0] + '. ' + ' '.join(x.split()[1:]))
plot_data = plot_data.drop_duplicates(subset='Player', keep='first')
print(f"After dedup: {len(plot_data)}")
print(plot_data[['Player', 'Team', 'PTS']].to_string())
print(f"Players in chart: {len(plot_data)}")
med_usg = plot_data['USG%'].median()
med_ts = plot_data['TS%'].median()

fig, ax = plt.subplots(figsize=(16, 10))

ax.axvline(x=med_usg, color='gray', linestyle='--', alpha=0.5)
ax.axhline(y=med_ts, color='gray', linestyle='--', alpha=0.5)

ax.text(plot_data['USG%'].max() - 0.5, plot_data['TS%'].max() - 0.005, 'Elite and Efficient Scorers',
        fontsize=9, color='green', ha='right', va='top', fontweight='bold')
ax.text(plot_data['USG%'].min() + 0.5, plot_data['TS%'].max() - 0.005, 'Efficient Low Volume Scorers',
        fontsize=9, color='blue', ha='left', va='top', fontweight='bold')
ax.text(plot_data['USG%'].max() - 0.5, plot_data['TS%'].min() + 0.005, 'Inefficient High-Volume Scorers',
        fontsize=9, color='red', ha='right', va='bottom', fontweight='bold')
ax.text(plot_data['USG%'].min() + 0.5, plot_data['TS%'].min() + 0.005, 'Inefficient Low Volume Scorers',
        fontsize=9, color='gray', ha='left', va='bottom', fontweight='bold')

for _, row in plot_data.iterrows():
    team = row['Team']
    pts = row['PTS'] if pd.notna(row['PTS']) else 15
    logo_size = max(0.04, min(0.1, pts / 350))
    logo_path = f'logos/{team}.png'
    try:
        img = mpimg.imread(logo_path)
        imagebox = OffsetImage(img, zoom=logo_size)
        ab = AnnotationBbox(imagebox, (row['USG%'], row['TS%']), frameon=False)
        ax.add_artist(ab)
    except FileNotFoundError:
        ax.scatter(row['USG%'], row['TS%'], s=100, color='gray', alpha=0.6)

    ax.annotate(row['Label'], (row['USG%'], row['TS%']),
            fontsize=8.5, ha='left',
            xytext=(12, 12), textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, edgecolor='none'))

ax.set_xlabel('Usage Rate (USG%)')
ax.set_ylabel('True Shooting % (TS%)')
ax.set_title('Scoring Volume vs Efficiency — NBA 2025-26')
plt.tight_layout()
ax.set_xlim(plot_data['USG%'].min() - 2, plot_data['USG%'].max() + 2)
ax.set_ylim(plot_data['TS%'].min() - 0.02, plot_data['TS%'].max() + 0.02)
plt.savefig('volume_vs_efficiency.png', dpi=150)
plt.show()
print("Chart saved!")