import streamlit as st

st.set_page_config(page_title="Home", layout="wide")

st.title("Vaccine Uptake Simulation")

st.markdown("""
This app is a small policy laboratory for exploring how a finite communication budget can be optimally allocated over time to increase vaccine uptake — including the effect of temporary disinformation shocks.

Use the sidebar to navigate:
- **Model** — run simulations and download results
- **Conceptual Framework / Methodology** — a plain-English explanation + PDF
- **Limitations** — why the results must be interpreted carefully
- **About the model** — what the model is for and how to interpret it
""")

st.divider()
st.header("About me")

st.markdown("""
I'm **Edward de Vries**, a **BA Economics with French** student at **Durham University**, currently on exchange at **Aix-Marseille University**.

I'm interested in a career in health economics, with a focus on applied modelling and cost-effectiveness analysis.
""")

st.subheader("Contact")
st.markdown("""
- **LinkedIn:** https://www.linkedin.com/in/e-devries  
- **Email:** edwarddevries@outlook.com
""")
