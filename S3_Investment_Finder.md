# Scenario 3 — City Opportunity Finder
## Smart Infrastructure Investment Screening Tool

**Role:** Data Analyst, NexaVenture Capital (private equity)
**Stakeholder:** David Chen (Managing Partner) — investment screening tool
**Dataset:** 5,000 cities x 15 metrics

---

## Methodology Note

**Two composite indices define the quadrant map:**

```
Economic Potential = (Employment Rate x 45%) + (Population x 35%) + (Affordability x 20%)
Infrastructure Gap = ((100 - Smart Infra) x 60%) + ((100 - Internet Speed) x 40%)
```

**Logic:**
- *Economic Potential:* Employment Rate is the strongest single signal of economic health (45%); Population captures market size (35%); lower Cost of Living (Affordability) improves investment margins (20%).
- *Infrastructure Gap:* Low Smart Infrastructure is the core investment thesis (60%); poor Internet Speed is the secondary signal of an underdeveloped digital base (40%).

**Quadrants:** Median reference lines on both axes split cities into four groups. The **PRIME TARGET** quadrant (high economic potential + large infrastructure gap) is the investment sweet spot.

---

## Key Findings

1. **825 cities** fall in the PRIME TARGET quadrant — strong economies currently held back by weak smart infrastructure.

2. **Top pick: City4856** — population 7,139,231, employment 63.6%, but Smart Infrastructure only 21.5 and internet 45.7 Mbps. A large, fixable gap in an economically strong city.

3. **1,702 cities are "Already Developed"** — economically strong but with little infrastructure gap, meaning low ROI potential. These should be avoided.

4. **Recommended shortlist:** City4856, City1650, City479, City562, City210 — all combine high economic potential with the widest infrastructure gaps.

---

## Self-Assessment

**1. What was the hardest part?**
Defining "Economic Potential" and "Infrastructure Gap" in a way that was defensible. The partners will ask "why these weights?", so each component needed a clear business rationale, not just intuition.

**2. What would you improve with more time?**
I would add interactive filters for population range, employment threshold, and cost of living so partners could refine the shortlist live, plus a click-to-drill city detail panel showing all 15 metrics.

**3. What did you learn?**
A good analytics tool is a *product*, not a report. The quadrant framing turns a 15-column dataset into a single decision ("is this city top-right?"), which is far more useful to a busy partner than raw numbers.
