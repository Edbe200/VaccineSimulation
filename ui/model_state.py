import streamlit as st

DEFAULTS = {
    "N": 1000,
    "T": 12,
    "beta": 0.05,
    "B": 5.0,
    "vaccinated_pop_start": 0.0,
    "x": 0.0002,
    "rho": 0.2,
    "shock_enabled": True,
    "shock_start_t": 5,
    "shock_beta_reduction_pct": 0.6,
    "shock_duration": 3,
}

LATEST_KEYS = [
    "latest_df",
    "latest_params",
    "latest_optimal_f",
    "latest_omega",
    "latest_shock_active",
    "latest_total_qalys",
    "latest_shock_enabled",
]

def init_defaults_if_missing():
    # Only fill in missing keys; never overwrite user-changed values
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_to_defaults(clear_results: bool = True):
    """Reset parameters (and optionally results) then rerun."""
    for k, v in DEFAULTS.items():
        st.session_state[k] = v
    if clear_results:
        for k in LATEST_KEYS:
            st.session_state.pop(k, None)
    st.rerun()
