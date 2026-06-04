# Scenario 2 — Green City Index
## UNEP Sustainability Scorecard

**Role:** Junior Data Analyst, GreenFuture Analytics
**Stakeholder:** Arjun Mehta (Team Lead) — prototype for UN Environment Programme
**Dataset:** 5,000 cities x 15 metrics

---

## Methodology Note

**Green Score formula (weighted composite):**

```
Green Score = (Air Quality x 30%) + (Energy Efficiency x 30%)
            + (Waste Management x 20%) + (Public Transport x 20%)
```

**Steps:**
1. Normalised all four metrics to a 0-100 scale using min-max normalisation.
2. Energy Consumption was **inverted** (lower consumption = higher score) since less energy use is environmentally better.
3. Applied the weighting above and ranked all 5,000 cities.
4. Ran K-Means clustering (k=3) on the four normalised metrics to find environmental profiles.

**Weighting justification:** Air Quality and Energy Efficiency carry the highest weight (30% each) because they are the most direct drivers of environmental and carbon impact. Waste Management and Public Transport (20% each) matter but affect sustainability more indirectly.

---

## Key Findings

1. **City size does NOT determine sustainability.** The correlation between population and Green Score is just **+0.01** — effectively zero. Bigger cities are not inherently dirtier.

2. **Cities fall into 3 clear environmental clusters:**
   - Green Leaders: 1,205 cities
   - Mixed Performers: 2,131 cities
   - Environmental Laggards: 1,664 cities

3. **Wide performance gap:** top city City465 scores 88.7 vs bottom city City4730 at 7.8 — an 81-point spread.

4. **Recommendation:** target the Environmental Laggards cluster for intervention — these cities share both poor air quality and poor energy efficiency, so investment there yields the biggest sustainability gains.

---

## Self-Assessment

**1. What was the hardest part?**
Deciding the weighting for the composite score. Since there is no "correct" weighting, I had to choose defensible weights and be ready to justify them, rather than just averaging everything equally.

**2. What would you improve with more time?**
I would add a parameter control so UN officials could adjust the four weights themselves and watch the rankings update live, and I would validate the clusters with a silhouette score.

**3. What did you learn?**
Normalisation is essential before combining metrics on different scales (Energy is 100-1000, Air Quality is 10-100). Without it, the largest-scale metric would dominate the composite unfairly.
