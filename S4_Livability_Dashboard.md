# Scenario 4 — City Livability Dashboard
## National Public Health Board (NPHB) Quarterly Report

**Role:** Data Analyst, National Public Health Board
**Stakeholder:** Dr. Neha Kapoor (Director) — public-facing Livability Report
**Dataset:** 5,000 cities x 15 metrics

---

## Methodology Note

**Livability Score (equal-weighted):**

```
Livability Score = average of (Healthcare, Safety, Education, Air Quality, Employment Rate)
```

Equal weighting was chosen as the fair, defensible default for a public report. In Tableau, parameters allow Dr. Kapoor to adjust the five weights interactively.

**Critical-City Flagging:**
A city is flagged **CRITICAL (red)** if it scores **below the 20th percentile on 3 or more** of the 5 livability dimensions. This catches cities with broad, systemic disadvantage rather than a single weak metric — making the flag fair and rigorous enough to withstand public scrutiny.

**City Health Card:** A report-card-style view comparing one selected city against the national average across all 5 dimensions.

---

## Key Findings

1. **901 cities (18.0%)** are flagged CRITICAL — below the 20th percentile on 3+ livability dimensions.

2. **The most common weakness is Healthcare Index** — 773 critical cities fall below the 20th percentile on it. This is the clearest target for a national program.

3. **Medium-tier cities are the most at-risk** at 18.7% critical, so budget allocation should be weighted toward this group.

4. **Recommendation:** prioritise the 901 flagged cities for intervention, leading with Healthcare improvement programs where the need is most widespread.

---

## Self-Assessment

**1. What was the hardest part?**
Building the critical-city flagging logic. It required calculating the 20th percentile for each of 5 dimensions, then counting how many a city fell below — equivalent to nested IF / LOD logic in Tableau.

**2. What would you improve with more time?**
I would add parameter-driven weights to the Livability Score and a fully interactive City Health Card that updates when a user clicks any city on the main chart (a Tableau dashboard action).

**3. What did you learn?**
For a public, budget-influencing report, *fairness* matters as much as accuracy. Flagging on 3+ dimensions (not just 1) prevents penalising a city for a single bad metric, which makes the methodology defensible to journalists and the public.
