import io
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def make_plot(params, optimal_f, omega, shock_active, shock_enabled):
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.set_xlabel("Time period (t)")
    ax1.set_ylabel("Budget share ($f_t$)")
    ax1.bar(range(1, params.T + 1), optimal_f, alpha=0.6)
    ax1.set_ylim(0, max(optimal_f) * 1.3 if max(optimal_f) > 0 else 1)
    ax1.set_xticks(range(1, params.T + 1))
    ax1.grid(True, axis="x", alpha=0.3)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Total vaccinated (stock at start of t)")
    ax2.plot(range(1, params.T + 1), omega[0:params.T], marker="o", linewidth=2)

    if shock_enabled:
        for t in range(params.T):
            if shock_active[t]:
                ax1.axvspan(t + 0.5, t + 1.5, alpha=0.12)

    ax1.set_title(f"Optimal allocation (N={params.N}, B={params.B}, x={params.x})")
    fig.tight_layout()
    return fig


def dataframe_to_excel_bytes(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="results")
    return output.getvalue()

def fig_to_png_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)
    return buf.getvalue()

def render_results():
    """Renders results section if results exist in session_state."""
    if "latest_df" not in st.session_state:
        return

    st.divider()
    st.subheader("Results")

    df = st.session_state["latest_df"]
    params = st.session_state["latest_params"]
    optimal_f = st.session_state["latest_optimal_f"]
    omega = st.session_state["latest_omega"]
    shock_active = st.session_state["latest_shock_active"]
    total_qalys = st.session_state["latest_total_qalys"]
    shock_enabled = st.session_state["latest_shock_enabled"]

    colA, colB = st.columns([1, 1])

    with colA:
        st.markdown("### Key outputs")
        st.metric("Total QALYs (over horizon)", f"{total_qalys:,.6f}")
        st.metric("Total spend (£)", f"{params.N * params.B:,.2f}")

        if total_qalys > 0:
            st.metric("Cost per QALY (£/QALY)", f"{(params.N * params.B) / total_qalys:,.0f}")
        else:
            st.warning("Total QALYs is zero; cost/QALY undefined.")

    with colB:
        st.markdown("### Plot")
        fig = make_plot(params, optimal_f, omega, shock_active, shock_enabled)

        # Generate PNG bytes BEFORE Streamlit clears anything
        png_bytes = fig_to_png_bytes(fig)

        st.pyplot(fig, clear_figure=True)

        st.download_button(
            label="⬇️ Download plot (PNG)",
            data=png_bytes,
            file_name="vaccination_model_plot.png",
            mime="image/png",
            use_container_width=True,
        )
        


    st.markdown("### Results table")
    st.dataframe(df, use_container_width=True)

    st.markdown("### Download")
    try:
        excel_bytes = dataframe_to_excel_bytes(df)
        st.download_button(
            label="⬇️ Download Excel (.xlsx)",
            data=excel_bytes,
            file_name="vaccination_model_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    except ModuleNotFoundError:
        st.error("Excel export requires 'openpyxl'. Install it with: pip install openpyxl")
