import streamlit as st
from vaccination_engine import ModelParams, ShockParams

def render_inputs() -> tuple[ModelParams, ShockParams, bool]:
    """
    Renders the input UI.
    Returns: (params, shock, run_button_clicked)
    """
    st.subheader("Inputs")

    shock_enabled = st.checkbox(
        "Enable disinformation shock",
        value=st.session_state["shock_enabled"],
        key="shock_enabled",
    )

    with st.form("inputs_form"):
        st.markdown("## Core parameters")

        N = st.number_input("Population (N)", min_value=1, max_value=5_000_000,
                            value=int(st.session_state["N"]), step=1, key="N")
        T = st.number_input("Time horizon (T, periods)", min_value=1, max_value=60,
                            value=int(st.session_state["T"]), step=1, key="T")

        beta = st.number_input("Responsiveness to Communication (0.0001 to 1)", min_value=0.0001, max_value=1.0,
                               value=float(st.session_state["beta"]), step=0.0001, format="%.4f", key="beta")
        B = st.number_input("Budget per capita (£)", min_value=0.0, max_value=100.0,
                            value=float(st.session_state["B"]), step=0.1, format="%.2f", key="B")
        vaccinated_pop_start = st.number_input("Initial # of people vaccinated (0 to N)",
                                               min_value=0.0, max_value=float(N),
                                               value=float(st.session_state["vaccinated_pop_start"]),
                                               step=1.0, format="%.0f", key="vaccinated_pop_start")
        x = st.number_input("QALY multiplier per period (0 to 0.01)", min_value=0.0, max_value=0.01,
                            value=float(st.session_state["x"]), step=0.00001, format="%.5f", key="x")
        rho = st.number_input("Returns to scale of communication (0 to 1)", min_value=0.01, max_value=1.0,
                              value=float(st.session_state["rho"]), step=0.01, format="%.2f", key="rho")

        st.markdown("## Shock parameters")

        if shock_enabled:
            shock_start_t = st.number_input("Shock start period (period t)",
                                            min_value=1, max_value=int(T),
                                            value=min(int(st.session_state["shock_start_t"]), int(T)),
                                            step=1, key="shock_start_t")
            shock_beta_reduction_pct = st.number_input("Shock Strength (0 to 1)",
                                                       min_value=0.0, max_value=1.0,
                                                       value=float(st.session_state["shock_beta_reduction_pct"]),
                                                       step=0.01, format="%.2f", key="shock_beta_reduction_pct")
            shock_duration = st.number_input("Shock duration (# of periods)",
                                             min_value=1, max_value=int(T),
                                             value=min(int(st.session_state["shock_duration"]), int(T)),
                                             step=1, key="shock_duration")
        else:
            shock_start_t = 1
            shock_beta_reduction_pct = 0.0
            shock_duration = 0
            st.info("Shock is disabled. Shock parameters will be ignored.")

        run_button = st.form_submit_button("🚀 Calculate results", use_container_width=True)

    params = ModelParams(
        N=int(N),
        T=int(T),
        beta=float(beta),
        B=float(B),
        vaccinated_pop_start=float(vaccinated_pop_start),
        x=float(x),
        rho=float(rho),
    )
    shock = ShockParams(
        enabled=bool(shock_enabled),
        start_t=int(shock_start_t),
        beta_reduction_pct=float(shock_beta_reduction_pct),
        duration=int(shock_duration),
    )

    return params, shock, run_button
