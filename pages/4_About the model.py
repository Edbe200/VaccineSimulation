import streamlit as st

st.set_page_config(page_title="About the Model", layout="wide")
st.title("About the model")

st.markdown("""
## Purpose of the project

This project was built to explore how **economic optimisation** can be used to reason about vaccine communication strategies under budget constraints.

Rather than attempting to predict real-world outcomes, the model is designed to clarify trade-offs:
- how timing matters,
- how diminishing returns shape optimal strategies,
- and how temporary disruptions to trust can alter optimal policy responses.

The emphasis is on **transparency and interpretability**, not realism for its own sake.

---

## What kind of model this is

This is a **stylised, exploratory model**.

It is best understood as:
- a policy laboratory,
- a teaching and intuition-building tool,
- or a prototype for thinking about communication strategy design.

It is not intended to be a decision-support system or forecasting tool for real-world campaigns.

---

## Design philosophy

Several design choices are intentional:
- simplicity over completeness,
- clear mechanisms over hidden complexity,
- and a tight link between economic behaviour and health-economic outcomes.

Complex features such as heterogeneity, network effects, endogenous trust formation, and epidemiological transmission are abstracted away to keep the optimisation problem legible end-to-end.

---

## Project status

The Streamlit interface represents a **working prototype**.

The structure is intentionally modular, allowing future extensions if the use case demands them. However, any extension would be evaluated against the core goal of maintaining clarity and economic intuition.
""")
