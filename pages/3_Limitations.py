import streamlit as st

st.set_page_config(page_title="Limitations", layout="wide")
st.title("Limitations")

st.markdown("""
This model is intentionally simplified. While this allows the optimisation problem to remain transparent and interpretable, it also imposes important limitations. Results should therefore be understood as **conceptual insights**, not literal policy prescriptions.

Below, we outline the main limitations of the framework and explain why they matter.

---

## 1. Narrow focus on information and advertising channels
The model considers only one policy lever: information and advertising-based communication designed to influence vaccination decisions. All changes in uptake arise through this channel alone.

In practice, vaccine uptake is shaped by a much wider set of factors, including:
- supply constraints and logistics,
- access costs (time, distance, administrative barriers),
- mandates or incentives,
- healthcare provider behaviour,
- institutional trust and prior experience,
- and broader social or political dynamics.

By abstracting from these mechanisms, the model isolates the role of communication in a clean way, but at the cost of ignoring interactions between advertising and other policy tools. As a result, the model should be interpreted as analysing one component of a broader vaccination strategy, rather than vaccine policy as a whole.

---

## 2. Homogeneous population and uniform behavioural response
The population is treated as fully homogeneous. All individuals share the same vaccination probability in a given period, and this probability depends only on aggregate spending and model parameters.

This abstracts away from substantial real-world heterogeneity, including:
- differences in risk perception,
- access constraints,
- trust in institutions,
- demographic and socioeconomic factors,
- and variation in responsiveness to different forms of messaging.
            
As a result, the model cannot capture subgroup-specific strategies, distributional effects, or differential uptake dynamics across populations.

---

## 3. Time-horizon effects and persistent vaccine effectiveness

Vaccination is assumed to generate health benefits indefinitely over the model’s time horizon. Extending the horizon therefore mechanically increases total vaccinated person-periods and improves implied cost-effectiveness.

In reality, vaccine-induced protection is rarely permanent. Booster requirements, waning immunity, pathogen evolution, and changes in disease prevalence all limit the duration over which vaccination confers health benefits. The model does not include revaccination, immunity decay, or epidemiological dynamics, and therefore overstates long-run benefits when the horizon is extended.

The time horizon should thus be interpreted as a modelling device rather than a literal representation of lifetime protection.

---

## 4. Simplified modelling of disinformation dynamics

Disinformation is modelled as a temporary reduction in a single parameter governing responsiveness to communication. This is a strong and simplifying assumption.

In reality, disinformation may:
- directly reduce willingness to vaccinate,
- affect trust asymmetrically across groups,
- interact with prior beliefs,
- or generate persistence effects that outlast the initial shock.

Moreover, even if persuasion were temporarily less effective, a real-world policymaker might choose to **increase** communication spending during such periods to counter false narratives, signal commitment, or maintain credibility. The model’s implication that optimal spending may fall during a disinformation shock reflects a narrow economic trade-off within the assumed structure, not a general policy recommendation.

Communication policies often carry signalling, political, and reputational meaning that extends beyond immediate behavioural response, and these channels are not fully captured here.

---

## 5. Constant advertising effectiveness and lack of adaptive targeting
The model assumes that the effectiveness of communication spending is independent of the composition of the remaining unvaccinated population. In each period, spending translates into vaccination probability through a fixed functional form, regardless of how small or concentrated the unvaccinated group has become.

In practice, communication strategies are often adaptive. As overall uptake rises and the remaining unvaccinated population becomes smaller or more clustered within particular communities, it may become optimal to shift from broad, generalised messaging (e.g. mass media campaigns) to highly targeted interventions.

In an extreme case, if only a single individual remained unvaccinated and a substantial budget were still available, the model would mechanically allocate spending to generalised persuasion. In reality, a policymaker might instead pursue direct engagement or targeted incentives. While stylised, this example illustrates a broader limitation: the model does not capture endogenous shifts from mass communication to targeted outreach as uptake increases.

---

## Summary

Taken together, these limitations highlight that the model is best viewed as a **conceptual and exploratory framework**. Its primary value lies in clarifying mechanisms and trade-offs, not in delivering precise or directly actionable policy guidance.

Any real-world application would require substantial extension, calibration, and institutional context.
""")
