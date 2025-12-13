import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Conceptual Framework", layout="wide")
st.title("Conceptual Framework")

st.markdown("""
This page explains the **intuition behind the model**, without relying on formal mathematics.
Its purpose is to make clear how the different components fit together and what each parameter represents conceptually.

---

## Core idea

The model represents a vaccination campaign as a **dynamic decision problem**.

A policymaker has:
- a fixed communication budget,
- a finite time horizon,
- and a population in which some individuals are already vaccinated and others are not.

Communication spending increases the probability that unvaccinated individuals choose to vaccinate, but with **diminishing returns**. Vaccinations accumulate into a stock of protected individuals, which generates health benefits over time.

The model asks how the communication budget should be allocated across time to maximise cumulative health benefits.

---

## Population and time

- **Population (N)**  
  The total number of individuals. All spending is interpreted on a *per-capita* basis, so scaling the population up does not mechanically change behaviour.

- **Time horizon (T)**  
  The number of discrete time periods (e.g. months). Earlier vaccination is more valuable because it generates benefits in more future periods.

---

## Budget and persuasion

- **Budget per capita (B)**  
  The total communication budget available per person over the full horizon. The model chooses how to distribute this across time.

- **Beta (responsiveness)**  
  Captures how effective communication is at persuading unvaccinated individuals. Higher values mean spending translates more strongly into uptake.

- **Rho (returns exponent)**  
  Controls diminishing returns to spending within a period. Lower values imply that concentrating spending quickly becomes inefficient, encouraging smoother allocation across time.

Together, these determine how spending in a given period maps into a vaccination probability.

---

## Vaccination dynamics

At the start of each period:
- some individuals are already vaccinated,
- the rest are unvaccinated.

Unvaccinated individuals independently decide whether to vaccinate in that period based on the campaign’s intensity. Newly vaccinated individuals join the vaccinated stock and remain vaccinated for the rest of the horizon.

This creates a **stock–flow structure**:
- flows of new vaccinations each period,
- accumulating into a stock that generates future benefits.

---

## Health outcomes and QALYs

The direct output of the model is **vaccinated person-periods**: one vaccinated individual protected for one period.

These are converted into **QALYs** using a simple multiplier:
- higher values imply greater health benefit per vaccinated person-period,
- lower values imply milder disease risk or lower vaccine effectiveness.

This mapping allows the model to report cost-effectiveness metrics such as **cost per QALY**.

---

## Disinformation shock

The model optionally includes a **known disinformation shock**:
- during a specified window, communication becomes less effective,
- represented as a temporary reduction in responsiveness.

Because the shock is assumed to be known in advance, the policymaker can optimally reallocate spending around it. This allows the model to study how optimal timing responds to temporary disruptions in trust or information quality.

---

## What this framework provides

The conceptual framework highlights:
- the value of early versus late vaccination,
- the role of diminishing returns,
- and how intertemporal optimisation responds to shocks.

For the full mathematical specification and optimisation problem, see the methodology PDF below.
""")

pdf_path = Path("assets/Simulation_Methodology.pdf")

if pdf_path.exists():
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="⬇️ Download full methodology (PDF)",
            data=f,
            file_name="Simulation_Methodology.pdf",
            mime="application/pdf",
        )
else:
    st.error("Methodology PDF not found.")
