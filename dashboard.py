import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import json, warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("/home/claude/smart_city_dataset.csv")
def pop_tier(p):
    if p < 100_000:    return "Small"
    if p < 1_000_000:  return "Medium"
    if p < 5_000_000:  return "Large"
    return "Mega"
df["Population Tier"] = df["Population"].apply(pop_tier)

with open("/home/claude/summary.json") as f:
    S = json.load(f)

OUR_CITY = S["our_city"]
peers = df[df["Population Tier"] == "Medium"].copy()
our = df[df["City Name"] == OUR_CITY].iloc[0]

# ── COLORS ──
C_DARK   = "#0D1B2A"
C_BLUE   = "#1A5276"
C_ACCENT = "#2E86AB"
C_ORANGE = "#E8871E"
C_GREEN  = "#27AE60"
C_RED    = "#C0392B"
C_LIGHT  = "#ECF0F1"
C_GRAY   = "#95A5A6"
C_WHITE  = "#FFFFFF"
C_GOLD   = "#F0B429"

fig = plt.figure(figsize=(18, 24), facecolor=C_DARK)

# ── Layout grid ──
gs = fig.add_gridspec(
    7, 4,
    hspace=0.45, wspace=0.35,
    top=0.96, bottom=0.03,
    left=0.04, right=0.97
)

# ── HEADER ────────────────────────────────────────────────────────────────────
ax_header = fig.add_subplot(gs[0, :])
ax_header.set_facecolor(C_BLUE)
ax_header.set_xlim(0, 1); ax_header.set_ylim(0, 1)
ax_header.axis('off')
ax_header.text(0.5, 0.72, "SMART CITY PERFORMANCE ANALYTICS",
               ha='center', va='center', fontsize=22, fontweight='bold',
               color=C_WHITE, fontfamily='DejaVu Sans')
ax_header.text(0.5, 0.28,
               f"Mayor's Benchmarking Report  |  {OUR_CITY}  vs  {S['total_peers']:,} Medium-Tier Peer Cities  |  5,000 Cities Dataset",
               ha='center', va='center', fontsize=11, color=C_LIGHT, alpha=0.9)

# ── KPI CARDS (row 1) ──────────────────────────────────────────────────────────
def kpi_card(ax, title, our_val, peer_val, rank, total, unit="", lower_better=False):
    ax.set_facecolor(C_DARK); ax.axis('off')
    ax.set_xlim(0,1); ax.set_ylim(0,1)
    # card background
    rect = FancyBboxPatch((0.02,0.04), 0.96, 0.92,
                          boxstyle="round,pad=0.02", linewidth=1.5,
                          edgecolor=C_ACCENT, facecolor="#112233")
    ax.add_patch(rect)
    # Title
    ax.text(0.5, 0.88, title, ha='center', va='top', fontsize=9.5,
            color=C_GRAY, fontweight='bold')
    # Main value
    ax.text(0.5, 0.66, f"{our_val}{unit}", ha='center', va='center',
            fontsize=24, fontweight='bold', color=C_WHITE)
    # Peer avg
    ax.text(0.5, 0.47, f"Peer Avg: {peer_val}{unit}", ha='center', va='center',
            fontsize=9, color=C_GRAY)
    # Gap
    gap = our_val - peer_val
    if lower_better:
        gap_good = gap < 0
        gap_str  = f"{'↓' if gap<0 else '↑'} {abs(gap):.1f} vs avg"
    else:
        gap_good = gap > 0
        gap_str  = f"{'↑' if gap>0 else '↓'} {abs(gap):.1f} vs avg"
    col = C_GREEN if gap_good else C_RED
    ax.text(0.5, 0.34, gap_str, ha='center', va='center', fontsize=9,
            color=col, fontweight='bold')
    # Rank badge
    rank_pct = 1 - (rank/total)
    badge_col = C_GREEN if rank_pct >= 0.6 else (C_GOLD if rank_pct >= 0.35 else C_RED)
    ax.text(0.5, 0.18, f"Rank  {rank:,} / {total:,}", ha='center', va='center',
            fontsize=8.5, color=badge_col, fontweight='bold')

ax_k1 = fig.add_subplot(gs[1, 0])
ax_k2 = fig.add_subplot(gs[1, 1])
ax_k3 = fig.add_subplot(gs[1, 2])
ax_k4 = fig.add_subplot(gs[1, 3])

kpi_card(ax_k1, "SMART INFRASTRUCTURE SCORE",
         S["smart_infra"], S["smart_infra_peer_avg"],
         S["smart_infra_rank"], S["total_peers"])

kpi_card(ax_k2, "ENERGY CONSUMPTION (lower=better)",
         S["energy"], S["energy_peer_avg"],
         S["energy_rank"], S["total_peers"], lower_better=True)

kpi_card(ax_k3, "PUBLIC TRANSPORT USAGE (%)",
         S["transport"], S["transport_peer_avg"],
         S["transport_rank"], S["total_peers"], unit="%")

# 4th KPI: Overall City Profile snapshot
ax_k4.set_facecolor(C_DARK); ax_k4.axis('off')
ax_k4.set_xlim(0,1); ax_k4.set_ylim(0,1)
rect = FancyBboxPatch((0.02,0.04), 0.96, 0.92,
                      boxstyle="round,pad=0.02", linewidth=1.5,
                      edgecolor=C_ACCENT, facecolor="#112233")
ax_k4.add_patch(rect)
ax_k4.text(0.5, 0.88, "CITY PROFILE SNAPSHOT", ha='center', va='top',
           fontsize=9.5, color=C_GRAY, fontweight='bold')
ax_k4.text(0.12, 0.72, f"Population:", fontsize=8.5, color=C_GRAY, va='center')
ax_k4.text(0.88, 0.72, f"{S['population']:,}", fontsize=8.5, color=C_WHITE,
           va='center', ha='right', fontweight='bold')
ax_k4.text(0.12, 0.58, f"Education:", fontsize=8.5, color=C_GRAY, va='center')
ax_k4.text(0.88, 0.58, f"{S['education']}", fontsize=8.5, color=C_WHITE,
           va='center', ha='right', fontweight='bold')
ax_k4.text(0.12, 0.44, f"Healthcare:", fontsize=8.5, color=C_GRAY, va='center')
ax_k4.text(0.88, 0.44, f"{S['healthcare']}", fontsize=8.5, color=C_WHITE,
           va='center', ha='right', fontweight='bold')
ax_k4.text(0.12, 0.30, f"Employment:", fontsize=8.5, color=C_GRAY, va='center')
ax_k4.text(0.88, 0.30, f"{S['employment']}%", fontsize=8.5, color=C_WHITE,
           va='center', ha='right', fontweight='bold')
ax_k4.text(0.12, 0.16, f"Tier:", fontsize=8.5, color=C_GRAY, va='center')
ax_k4.text(0.88, 0.16, f"Medium", fontsize=8.5, color=C_GOLD,
           va='center', ha='right', fontweight='bold')

# ── BAR CHART: City vs Peer Average ───────────────────────────────────────────
ax_bar = fig.add_subplot(gs[2, :2])
ax_bar.set_facecolor("#0a1520")
ax_bar.tick_params(colors=C_LIGHT)
for spine in ax_bar.spines.values(): spine.set_edgecolor("#1a3045")

metrics_display = ["Smart Infrastructure\nScore", "Public Transport\nUsage (%)"]
our_vals        = [S["smart_infra"],  S["transport"]]
peer_vals       = [S["smart_infra_peer_avg"], S["transport_peer_avg"]]
colors_our      = [C_RED, C_ORANGE]  # city is above/below avg

x = np.arange(len(metrics_display))
w = 0.35
bars1 = ax_bar.bar(x - w/2, peer_vals, w, label=f'Peer Average ({S["total_peers"]:,} cities)',
                   color=C_GRAY, alpha=0.6, zorder=3)
bars2 = ax_bar.bar(x + w/2, our_vals, w, label=f'{OUR_CITY}',
                   color=[C_ACCENT, C_ORANGE], alpha=0.9, zorder=3)

for bar in bars1:
    ax_bar.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.8,
                f"{bar.get_height():.1f}", ha='center', va='bottom',
                fontsize=9, color=C_GRAY)
for bar in bars2:
    ax_bar.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.8,
                f"{bar.get_height():.1f}", ha='center', va='bottom',
                fontsize=9, color=C_WHITE, fontweight='bold')

ax_bar.set_xticks(x)
ax_bar.set_xticklabels(metrics_display, color=C_LIGHT, fontsize=9)
ax_bar.set_ylabel("Score / %", color=C_GRAY, fontsize=9)
ax_bar.set_ylim(0, 100)
ax_bar.set_title("City vs Peer Average: Smart Infrastructure & Transport",
                 color=C_WHITE, fontsize=11, fontweight='bold', pad=8)
ax_bar.legend(fontsize=8, facecolor="#0a1520", edgecolor=C_ACCENT,
              labelcolor=C_LIGHT, loc='upper right')
ax_bar.yaxis.label.set_color(C_GRAY)
ax_bar.tick_params(axis='y', colors=C_GRAY)
ax_bar.grid(axis='y', color='#1a3045', linestyle='--', alpha=0.5, zorder=0)

# ── ENERGY CONSUMPTION CHART ──────────────────────────────────────────────────
ax_energy = fig.add_subplot(gs[2, 2:])
ax_energy.set_facecolor("#0a1520")
for spine in ax_energy.spines.values(): spine.set_edgecolor("#1a3045")

cats  = [f"Peer Average\n({S['total_peers']:,} cities)", f"{OUR_CITY}\n(Our City)",
         "Top 5 Best\nPeer Average"]
top5_energy_avg = peers.nsmallest(5,"Energy Consumption")["Energy Consumption"].mean()
vals  = [S["energy_peer_avg"], S["energy"], round(top5_energy_avg,1)]
cols  = [C_GRAY, C_RED, C_GREEN]

bars = ax_energy.bar(cats, vals, color=cols, alpha=0.85, zorder=3, width=0.5)
for bar, val in zip(bars, vals):
    ax_energy.text(bar.get_x()+bar.get_width()/2, bar.get_height()+5,
                   f"{val:.0f}", ha='center', va='bottom',
                   fontsize=11, color=C_WHITE, fontweight='bold')

ax_energy.set_ylabel("Energy Consumption (lower = better)", color=C_GRAY, fontsize=9)
ax_energy.set_ylim(0, max(vals)*1.22)
ax_energy.set_title("Energy Consumption: Our City vs Benchmark",
                    color=C_WHITE, fontsize=11, fontweight='bold', pad=8)
ax_energy.tick_params(colors=C_LIGHT, labelsize=9)
ax_energy.tick_params(axis='y', colors=C_GRAY)
ax_energy.grid(axis='y', color='#1a3045', linestyle='--', alpha=0.5, zorder=0)

note_y = max(vals)*1.10
ax_energy.text(1, note_y, "↑ 38% above\npeer average", ha='center', va='bottom',
               fontsize=8, color=C_RED, fontweight='bold')

# ── PEER DISTRIBUTION: Smart Infra ────────────────────────────────────────────
ax_dist = fig.add_subplot(gs[3, :2])
ax_dist.set_facecolor("#0a1520")
for spine in ax_dist.spines.values(): spine.set_edgecolor("#1a3045")

peer_infra = peers["Smart Infrastructure Score"]
ax_dist.hist(peer_infra, bins=40, color=C_ACCENT, alpha=0.5, edgecolor='none', zorder=2)
ax_dist.axvline(S["smart_infra"], color=C_RED, linewidth=2.5, zorder=5,
                label=f'{OUR_CITY}: {S["smart_infra"]}')
ax_dist.axvline(S["smart_infra_peer_avg"], color=C_GOLD, linewidth=2, linestyle='--', zorder=4,
                label=f'Peer Avg: {S["smart_infra_peer_avg"]}')
ax_dist.set_xlabel("Smart Infrastructure Score", color=C_GRAY, fontsize=9)
ax_dist.set_ylabel("Number of Cities", color=C_GRAY, fontsize=9)
ax_dist.set_title(f"Distribution: Smart Infrastructure (Medium-Tier Peers)",
                  color=C_WHITE, fontsize=11, fontweight='bold', pad=8)
ax_dist.legend(fontsize=8.5, facecolor="#0a1520", edgecolor=C_ACCENT, labelcolor=C_LIGHT)
ax_dist.tick_params(colors=C_GRAY, labelsize=8)
ax_dist.grid(axis='y', color='#1a3045', linestyle='--', alpha=0.4, zorder=0)

# ── TOP 10 PEERS: Smart Infrastructure ────────────────────────────────────────
ax_top = fig.add_subplot(gs[3, 2:])
ax_top.set_facecolor("#0a1520")
for spine in ax_top.spines.values(): spine.set_edgecolor("#1a3045")

top10 = peers.nlargest(10,"Smart Infrastructure Score")[["City Name","Smart Infrastructure Score"]].copy()
top10_cities = list(top10["City Name"]) + [OUR_CITY]
top10_scores = list(top10["Smart Infrastructure Score"]) + [S["smart_infra"]]
top10_labels = [f"★ {OUR_CITY}" if c==OUR_CITY else c for c in top10_cities]
top10_colors = [C_RED if c==OUR_CITY else C_ACCENT for c in top10_cities]

y_pos = np.arange(len(top10_cities))
ax_top.barh(y_pos, top10_scores, color=top10_colors, alpha=0.85, zorder=3)
ax_top.set_yticks(y_pos)
ax_top.set_yticklabels(top10_labels, color=C_LIGHT, fontsize=8.5)
ax_top.set_xlabel("Smart Infrastructure Score", color=C_GRAY, fontsize=9)
ax_top.set_title("Top 10 Peers + Our City: Smart Infrastructure",
                 color=C_WHITE, fontsize=11, fontweight='bold', pad=8)
for i, (score, city) in enumerate(zip(top10_scores, top10_cities)):
    ax_top.text(score+0.5, i, f"{score}", va='center', fontsize=8,
                color=C_WHITE if city!=OUR_CITY else C_RED, fontweight='bold')
ax_top.set_xlim(0, max(top10_scores)*1.12)
ax_top.tick_params(axis='x', colors=C_GRAY, labelsize=8)
ax_top.grid(axis='x', color='#1a3045', linestyle='--', alpha=0.4, zorder=0)
ax_top.invert_yaxis()

# ── SCATTER: Smart Infra vs Energy ────────────────────────────────────────────
ax_sc = fig.add_subplot(gs[4, :2])
ax_sc.set_facecolor("#0a1520")
for spine in ax_sc.spines.values(): spine.set_edgecolor("#1a3045")

sample = peers.sample(600, random_state=7)
ax_sc.scatter(sample["Smart Infrastructure Score"], sample["Energy Consumption"],
              alpha=0.25, s=12, color=C_ACCENT, zorder=2)
ax_sc.scatter(our["Smart Infrastructure Score"], our["Energy Consumption"],
              s=160, color=C_RED, zorder=6, marker='*',
              label=f'{OUR_CITY}')
ax_sc.axvline(S["smart_infra_peer_avg"], color=C_GOLD, linewidth=1.2,
              linestyle='--', alpha=0.6, label='Peer avg')
ax_sc.axhline(S["energy_peer_avg"], color=C_GOLD, linewidth=1.2,
              linestyle='--', alpha=0.6)

ax_sc.set_xlabel("Smart Infrastructure Score", color=C_GRAY, fontsize=9)
ax_sc.set_ylabel("Energy Consumption (lower=better)", color=C_GRAY, fontsize=9)
ax_sc.set_title("Smart Infrastructure vs Energy Consumption",
                color=C_WHITE, fontsize=11, fontweight='bold', pad=8)
ax_sc.legend(fontsize=8.5, facecolor="#0a1520", edgecolor=C_ACCENT, labelcolor=C_LIGHT)
ax_sc.tick_params(colors=C_GRAY, labelsize=8)
ax_sc.grid(color='#1a3045', linestyle='--', alpha=0.3, zorder=0)

# Add quadrant labels
ax_sc.text(85, 900, "High Infra\nHigh Energy", fontsize=7.5, color=C_GRAY, ha='center', alpha=0.7)
ax_sc.text(10, 900, "Low Infra\nHigh Energy", fontsize=7.5, color=C_RED, ha='center', alpha=0.8, fontweight='bold')
ax_sc.text(85, 150, "High Infra\nLow Energy\n(TARGET)", fontsize=7.5, color=C_GREEN, ha='center', alpha=0.8, fontweight='bold')
ax_sc.text(10, 150, "Low Infra\nLow Energy", fontsize=7.5, color=C_GRAY, ha='center', alpha=0.7)

# ── RADAR-STYLE MULTI-METRIC COMPARISON ───────────────────────────────────────
ax_radar = fig.add_subplot(gs[4, 2:], polar=True)
ax_radar.set_facecolor("#0a1520")

radar_metrics = ["Smart\nInfra","Energy\nEfficiency","Public\nTransport",
                 "Education","Healthcare","Employment"]
peer_avgs_radar = [
    S["smart_infra_peer_avg"],
    100 - (S["energy_peer_avg"]/10),   # invert energy (normalize to 0-100)
    S["transport_peer_avg"],
    peers["Education Index"].mean(),
    peers["Healthcare Index"].mean(),
    peers["Employment Rate"].mean(),
]
our_vals_radar = [
    S["smart_infra"],
    100 - (S["energy"]/10),
    S["transport"],
    S["education"],
    S["healthcare"],
    S["employment"],
]

N_r = len(radar_metrics)
angles = np.linspace(0, 2*np.pi, N_r, endpoint=False).tolist()
angles += angles[:1]
peer_avgs_radar += peer_avgs_radar[:1]
our_vals_radar  += our_vals_radar[:1]

ax_radar.plot(angles, peer_avgs_radar, color=C_GRAY, linewidth=1.5, linestyle='--', alpha=0.7)
ax_radar.fill(angles, peer_avgs_radar, color=C_GRAY, alpha=0.1)
ax_radar.plot(angles, our_vals_radar, color=C_ACCENT, linewidth=2.2)
ax_radar.fill(angles, our_vals_radar, color=C_ACCENT, alpha=0.2)

ax_radar.set_xticks(angles[:-1])
ax_radar.set_xticklabels(radar_metrics, color=C_LIGHT, fontsize=8.5)
ax_radar.set_ylim(0, 100)
ax_radar.set_yticks([20,40,60,80,100])
ax_radar.set_yticklabels(["20","40","60","80","100"], color=C_GRAY, fontsize=6.5)
ax_radar.grid(color='#1a3045', linestyle='--', alpha=0.5)
ax_radar.set_facecolor("#0a1520")
ax_radar.spines['polar'].set_edgecolor("#1a3045")

# Manual legend
ax_radar.plot([], [], color=C_ACCENT, linewidth=2.2, label=OUR_CITY)
ax_radar.plot([], [], color=C_GRAY, linewidth=1.5, linestyle='--', label='Peer Avg')
ax_radar.legend(loc='upper right', bbox_to_anchor=(1.35, 1.15),
                fontsize=8.5, facecolor="#0a1520", edgecolor=C_ACCENT, labelcolor=C_LIGHT)
ax_radar.set_title("City vs Peer: 6-Metric Profile",
                   color=C_WHITE, fontsize=11, fontweight='bold', pad=18)

# ── INVESTMENT RECOMMENDATIONS ─────────────────────────────────────────────────
ax_rec = fig.add_subplot(gs[5, :])
ax_rec.set_facecolor("#0a1520")
ax_rec.axis('off')
ax_rec.set_xlim(0,1); ax_rec.set_ylim(0,1)

rect = FancyBboxPatch((0.005,0.05), 0.99, 0.90,
                      boxstyle="round,pad=0.015", linewidth=1.5,
                      edgecolor=C_GOLD, facecolor="#0D1F1F")
ax_rec.add_patch(rect)
ax_rec.text(0.5, 0.88, "🏛  INVESTMENT RECOMMENDATIONS FOR MAYOR SHARMA",
            ha='center', va='center', fontsize=13, fontweight='bold', color=C_GOLD)

recs = [
    ("PRIORITY 1 — Energy Modernisation",
     C_RED,
     f"{OUR_CITY} consumes {S['energy']:.0f} units vs peer avg of {S['energy_peer_avg']:.0f} — 38% higher. "
     f"Rank {S['energy_rank']:,}/{S['total_peers']:,} in peer group. "
     f"Investing in smart grid technology and renewable energy can cut consumption by ~30% within 3 years, "
     f"reducing operational costs and carbon footprint. Top performers average just 130–160 units."),
    ("PRIORITY 2 — Smart Infrastructure Upgrade",
     C_ORANGE,
     f"Smart Infrastructure Score of {S['smart_infra']} puts the city at the 26th percentile (rank {S['smart_infra_rank']:,}/{S['total_peers']:,}). "
     f"Peer average is {S['smart_infra_peer_avg']}; top performers exceed 90+. "
     f"Focus investment on IoT sensor networks, open data platforms, and smart traffic management — "
     f"these deliver measurable ROI and raise the city's competitiveness for business attraction."),
    ("PRIORITY 3 — Public Transport Expansion",
     C_GOLD,
     f"Public transport usage at {S['transport']}% (peer avg: {S['transport_peer_avg']}%) — city is near the median. "
     f"However, top-performing peers exceed 87%. "
     f"Modest investment in bus rapid transit (BRT) and last-mile connectivity can lift adoption, "
     f"reduce road congestion, and support energy reduction goals simultaneously."),
]

y_positions = [0.70, 0.48, 0.26]
for (title, color, text), y in zip(recs, y_positions):
    # Priority label
    ax_rec.text(0.01, y+0.04, title, ha='left', va='center',
                fontsize=9.5, fontweight='bold', color=color)
    ax_rec.text(0.01, y-0.04, text, ha='left', va='center',
                fontsize=8.2, color=C_LIGHT, wrap=True,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#112233',
                          edgecolor=color, alpha=0.7, linewidth=0.8))

# ── FOOTER ─────────────────────────────────────────────────────────────────────
ax_footer = fig.add_subplot(gs[6, :])
ax_footer.set_facecolor(C_DARK); ax_footer.axis('off')
ax_footer.set_xlim(0,1); ax_footer.set_ylim(0,1)
ax_footer.text(0.5, 0.65, "Data Source: smart_city_dataset.csv  |  5,000 Cities  |  15 Performance Metrics",
               ha='center', fontsize=8, color=C_GRAY)
ax_footer.text(0.5, 0.25, "Analyst: Aquib Azam Ansari  |  Tools: Python (Pandas, NumPy, Matplotlib)  |  Scenario 1 — Mayor's Smart City Readiness Report",
               ha='center', fontsize=8, color=C_GRAY)

plt.savefig("/home/claude/smart_city_dashboard.png", dpi=150, bbox_inches='tight',
            facecolor=C_DARK, edgecolor='none')
print("Dashboard saved!")
