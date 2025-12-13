import streamlit as st
from vaccination_engine import (
    optimize_budget_allocation,
    simulate_trajectory,
    build_results_dataframe,
)
from ui.model_state import init_defaults_if_missing, reset_to_defaults
from ui.model_inputs import render_inputs
from ui.model_outputs import render_results

st.set_page_config(page_title="Model", layout="wide")
st.title("Model")

init_defaults_if_missing()

# Reset button
top_left, _ = st.columns([1, 3])
with top_left:
    if st.button("↩️ Reset parameters to default", use_container_width=True):
        reset_to_defaults(clear_results=True)

params, shock, run_button = render_inputs()

if run_button:
    with st.spinner("Optimising budget allocation..."):
        result = optimize_budget_allocation(params=params, shock=shock)

    if not result.success:
        st.error(f"Optimisation failed: {result.message}")
    else:
        optimal_f = result.x
        omega, p_values, conversions, beta_path, shock_active = simulate_trajectory(optimal_f, params, shock)
        total_qalys = -result.fun

        df = build_results_dataframe(
            optimal_f=optimal_f,
            omega=omega,
            p_values=p_values,
            conversions=conversions,
            beta_path=beta_path,
            shock_active=shock_active,
            params=params,
        )

        st.session_state["latest_df"] = df
        st.session_state["latest_params"] = params
        st.session_state["latest_optimal_f"] = optimal_f
        st.session_state["latest_omega"] = omega
        st.session_state["latest_shock_active"] = shock_active
        st.session_state["latest_total_qalys"] = total_qalys
        st.session_state["latest_shock_enabled"] = shock.enabled

render_results()
