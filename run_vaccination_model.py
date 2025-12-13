# run_vaccination_model.py
import matplotlib.pyplot as plt
import numpy as np

from vaccination_engine import (
    ModelParams, ShockParams,
    optimize_budget_allocation,
    simulate_trajectory,
    build_results_dataframe,
    export_results_to_excel,
)

# ---------------------------------------------------------
# User options
# ---------------------------------------------------------
EXPORT_TO_EXCEL = True
EXCEL_FILENAME = "vaccination_model_results.xlsx"

# ---------------------------------------------------------
# Parameters
# ---------------------------------------------------------
params = ModelParams(
    N=1000,
    T=12,
    beta=0.05,
    B=5,
    vaccinated_pop_start=0,
    x=0.0002,
    rho=0.2
)

shock = ShockParams(
    enabled=True,
    start_t=5,               # 1-indexed
    beta_reduction_pct=0.6,  # reduce beta by 60%
    duration=3               # lasts 3 periods
)

# ---------------------------------------------------------
# Run optimisation
# ---------------------------------------------------------
print(f"Starting optimization (N={params.N}, B={params.B}, x={params.x})...")
result = optimize_budget_allocation(params=params, shock=shock)

if result.success:
    print("Optimization successful!")
else:
    print("Optimization failed:", result.message)

optimal_f = result.x

# ---------------------------------------------------------
# Simulate optimal trajectory + build table
# ---------------------------------------------------------
omega, p_values, conversions, beta_path, shock_active = simulate_trajectory(optimal_f, params, shock)
max_qalys = -result.fun
print(f"\nTotal Objective Value: {max_qalys:,.6f} QALYs")

df = build_results_dataframe(
    optimal_f=optimal_f,
    omega=omega,
    p_values=p_values,
    conversions=conversions,
    beta_path=beta_path,
    shock_active=shock_active,
    params=params
)

# Print a clean console version (optional)
print("\n" + "=" * 140)
print(df.to_string(index=False))
print("=" * 140)

# Optional Excel export
if EXPORT_TO_EXCEL:
    export_results_to_excel(df, EXCEL_FILENAME)
    print(f"\nResults table exported to '{EXCEL_FILENAME}'")

# ---------------------------------------------------------
# Plotting
# ---------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.set_xlabel("Time Period (t)")
ax1.set_ylabel("Budget Share ($f_t$)", fontweight="bold")
ax1.bar(range(1, params.T + 1), optimal_f, alpha=0.6)
ax1.set_ylim(0, max(optimal_f) * 1.3 if max(optimal_f) > 0 else 1)
ax1.set_xticks(range(1, params.T + 1))
ax1.grid(True, axis="x", alpha=0.3)

ax2 = ax1.twinx()
ax2.set_ylabel("Total Vaccinated Population", fontweight="bold")
ax2.plot(range(1, params.T + 1), omega[0:params.T], marker="o", linewidth=2)

# shade shock periods
if shock.enabled:
    for t in range(params.T):
        if shock_active[t]:
            ax1.axvspan(t + 0.5, t + 1.5, alpha=0.12)

plt.title(f"Optimal Allocation with Known Disinformation Shock (N={params.N}, B={params.B}, x={params.x})")
fig.tight_layout()
plt.show()
