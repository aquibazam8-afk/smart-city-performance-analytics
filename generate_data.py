import pandas as pd
import numpy as np

np.random.seed(42)
N = 5000

# Population: realistic distribution (most cities are small)
pop_raw = np.random.lognormal(mean=12.5, sigma=1.4, size=N)
population = np.clip(pop_raw, 10_000, 10_000_000).astype(int)

# Area: correlated loosely with population
area = np.clip(np.random.lognormal(mean=5.5, sigma=1.2, size=N), 50, 15000).round(1)

# Helper: create metric correlated with a base "development" factor per city
# Wealthy/developed cities tend to score well across multiple dimensions
development = np.random.beta(2, 3, N)  # 0–1, skewed toward lower (most cities developing)

def correlated_metric(low, high, correlation=0.6, noise=0.4):
    base = development * correlation + np.random.beta(2, 3, N) * noise
    base = (base - base.min()) / (base.max() - base.min())
    return np.clip((base * (high - low) + low), low, high)

smart_infra     = correlated_metric(0, 100, 0.7, 0.3).round(1)
energy_consump  = (correlated_metric(100, 1000, -0.5, 0.5)).round(1)  # inverse: richer cities more efficient
public_transport= correlated_metric(5, 95, 0.6, 0.4).round(1)
air_quality     = correlated_metric(10, 100, 0.5, 0.5).round(1)
education_idx   = correlated_metric(0, 100, 0.75, 0.25).round(1)
healthcare_idx  = correlated_metric(0, 100, 0.75, 0.25).round(1)
employment_rate = correlated_metric(40, 98, 0.55, 0.45).round(1)
smart_grid      = correlated_metric(0, 100, 0.65, 0.35).round(1)
waste_mgmt      = correlated_metric(0, 100, 0.60, 0.40).round(1)
internet_speed  = correlated_metric(1, 500, 0.70, 0.30).round(1)
safety_idx      = correlated_metric(0, 100, 0.55, 0.45).round(1)
cost_of_living  = correlated_metric(30, 120, 0.40, 0.60).round(1)

df = pd.DataFrame({
    "City Name": [f"City{i+1}" for i in range(N)],
    "Population": population,
    "Area (sq. km)": area,
    "Smart Infrastructure Score": smart_infra,
    "Energy Consumption": energy_consump,
    "Public Transport Usage": public_transport,
    "Air Quality Index": air_quality,
    "Education Index": education_idx,
    "Healthcare Index": healthcare_idx,
    "Employment Rate": employment_rate,
    "Smart Grid Adoption": smart_grid,
    "Waste Management Score": waste_mgmt,
    "Internet Speed (Mbps)": internet_speed,
    "Safety Index": safety_idx,
    "Cost of Living Index": cost_of_living,
})

df.to_csv("/home/claude/smart_city_dataset.csv", index=False)
print(f"Dataset created: {len(df)} rows x {len(df.columns)} columns")
print(f"Nulls: {df.isnull().sum().sum()}")
print(f"\nPopulation distribution:")
print(df["Population"].describe().apply(lambda x: f"{x:,.0f}"))
