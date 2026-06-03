import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("/home/claude/smart_city_dataset.csv")

# ── 1. POPULATION TIERS ──────────────────────────────────────────────────────
def pop_tier(p):
    if p < 100_000:    return "Small"
    if p < 1_000_000:  return "Medium"
    if p < 5_000_000:  return "Large"
    return "Mega"

df["Population Tier"] = df["Population"].apply(pop_tier)

tier_counts = df["Population Tier"].value_counts()
print("=== POPULATION TIERS ===")
print(tier_counts)

# ── 2. PICK "OUR CITY" ────────────────────────────────────────────────────────
# We want a Medium-tier city with strong Education & Healthcare but weak Smart Infra
# — tells a clear story for the Mayor: "you're liveable, now modernise"
medium = df[df["Population Tier"] == "Medium"].copy()

# Score: high education + healthcare, low smart infra → biggest gap story
medium["story_score"] = (
    medium["Education Index"] * 0.35 +
    medium["Healthcare Index"] * 0.35 -
    medium["Smart Infrastructure Score"] * 0.30
)
our_city_row = medium.nlargest(1, "story_score").iloc[0]
OUR_CITY = our_city_row["City Name"]
print(f"\n=== OUR CITY: {OUR_CITY} ===")
print(our_city_row[["Population","Smart Infrastructure Score",
                     "Energy Consumption","Public Transport Usage",
                     "Education Index","Healthcare Index"]].to_string())

# ── 3. PEER GROUP ─────────────────────────────────────────────────────────────
peers = df[df["Population Tier"] == "Medium"].copy()
our  = df[df["City Name"] == OUR_CITY].iloc[0]

# Key metrics for Scenario 1
METRICS = ["Smart Infrastructure Score", "Energy Consumption", "Public Transport Usage"]

print(f"\n=== PEER GROUP SIZE: {len(peers)} cities ===")
print("\nPeer group averages:")
print(peers[METRICS].mean().round(1))

# ── 4. RANKINGS in peer group ─────────────────────────────────────────────────
# Energy Consumption: LOWER is better → rank ascending
peers_ranked = peers.copy()
peers_ranked["Rank_SmartInfra"]   = peers_ranked["Smart Infrastructure Score"].rank(ascending=False, method='min').astype(int)
peers_ranked["Rank_Energy"]       = peers_ranked["Energy Consumption"].rank(ascending=True,  method='min').astype(int)  # lower=better
peers_ranked["Rank_Transport"]    = peers_ranked["Public Transport Usage"].rank(ascending=False, method='min').astype(int)

our_ranks = peers_ranked[peers_ranked["City Name"] == OUR_CITY].iloc[0]
total_peers = len(peers_ranked)

print(f"\n=== {OUR_CITY} RANKINGS (out of {total_peers} Medium cities) ===")
print(f"Smart Infrastructure Score : {our['Smart Infrastructure Score']:.1f}  → Rank {our_ranks['Rank_SmartInfra']} / {total_peers}")
print(f"Energy Consumption         : {our['Energy Consumption']:.1f}  → Rank {our_ranks['Rank_Energy']} / {total_peers}  (lower=better)")
print(f"Public Transport Usage     : {our['Public Transport Usage']:.1f}% → Rank {our_ranks['Rank_Transport']} / {total_peers}")

# ── 5. TOP 5 PEER PERFORMERS ──────────────────────────────────────────────────
top5_infra     = peers.nlargest(5, "Smart Infrastructure Score")[["City Name","Smart Infrastructure Score","Population"]]
top5_energy    = peers.nsmallest(5, "Energy Consumption")[["City Name","Energy Consumption","Population"]]
top5_transport = peers.nlargest(5, "Public Transport Usage")[["City Name","Public Transport Usage","Population"]]
print("\n=== TOP 5 PEERS: Smart Infrastructure ===")
print(top5_infra.to_string(index=False))
print("\n=== TOP 5 PEERS: Energy Efficiency (lowest consumption) ===")
print(top5_energy.to_string(index=False))
print("\n=== TOP 5 PEERS: Public Transport ===")
print(top5_transport.to_string(index=False))

# ── 6. GAP FROM PEER AVERAGE ─────────────────────────────────────────────────
peer_avg = peers[METRICS].mean()
gaps = {m: our[m] - peer_avg[m] for m in METRICS}
# Energy: negative gap = good (below average consumption)
print(f"\n=== {OUR_CITY} vs Peer Average ===")
for m, g in gaps.items():
    direction = "ABOVE" if g > 0 else "BELOW"
    print(f"  {m}: {our[m]:.1f}  |  Peer avg: {peer_avg[m]:.1f}  |  Gap: {g:+.1f} ({direction} average)")

# ── 7. INVESTMENT RECOMMENDATIONS ────────────────────────────────────────────
print(f"\n=== INVESTMENT RECOMMENDATIONS FOR {OUR_CITY} ===")

# Priority areas = metrics where city is below peer average (or bottom 40th percentile)
infra_pct  = (peers["Smart Infrastructure Score"] <= our["Smart Infrastructure Score"]).mean() * 100
energy_pct = (peers["Energy Consumption"] >= our["Energy Consumption"]).mean() * 100  # lower is better
trans_pct  = (peers["Public Transport Usage"] <= our["Public Transport Usage"]).mean() * 100

print(f"Smart Infrastructure Score: city is at {infra_pct:.0f}th percentile in peer group")
print(f"Energy Efficiency         : city is at {energy_pct:.0f}th percentile (higher = more efficient)")
print(f"Public Transport Usage    : city is at {trans_pct:.0f}th percentile in peer group")

# ── 8. SAVE KEY NUMBERS for dashboard / resume ───────────────────────────────
summary = {
    "our_city": OUR_CITY,
    "our_population": int(our["Population"]),
    "tier": "Medium",
    "total_peers": total_peers,
    "smart_infra_score": round(our["Smart Infrastructure Score"], 1),
    "smart_infra_peer_avg": round(peer_avg["Smart Infrastructure Score"], 1),
    "smart_infra_rank": int(our_ranks["Rank_SmartInfra"]),
    "energy_score": round(our["Energy Consumption"], 1),
    "energy_peer_avg": round(peer_avg["Energy Consumption"], 1),
    "energy_rank": int(our_ranks["Rank_Energy"]),
    "transport_score": round(our["Public Transport Usage"], 1),
    "transport_peer_avg": round(peer_avg["Public Transport Usage"], 1),
    "transport_rank": int(our_ranks["Rank_Transport"]),
    "infra_percentile": round(infra_pct, 0),
    "energy_percentile": round(energy_pct, 0),
    "transport_percentile": round(trans_pct, 0),
}
import json
with open("/home/claude/summary.json","w") as f:
    json.dump(summary, f, indent=2)

print("\n=== SUMMARY SAVED ===")
print(json.dumps(summary, indent=2))
