# vaccination_engine.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from scipy.optimize import minimize


@dataclass(frozen=True)
class ModelParams:
    N: int = 1000
    T: int = 12
    beta: float = 0.05
    B: float = 5.0
    vaccinated_pop_start: float = 0.0
    x: float = 0.0002
    rho: float = 0.2


@dataclass(frozen=True)
class ShockParams:
    enabled: bool = False
    start_t: int = 1                  # 1-indexed
    beta_reduction_pct: float = 0.0   # 0.6 means reduce beta by 60%
    duration: int = 0                 # number of periods


def build_beta_path(params: ModelParams, shock: ShockParams) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns:
        beta_path: length T array of effective beta_t
        shock_active: length T boolean array
    """
    T = params.T
    beta_path = np.full(T, params.beta, dtype=float)
    shock_active = np.zeros(T, dtype=bool)

    if not shock.enabled or shock.duration <= 0:
        return beta_path, shock_active

    start_idx = max(shock.start_t - 1, 0)
    end_idx = min(start_idx + shock.duration, T)

    if start_idx >= T:
        return beta_path, shock_active

    reduction = float(np.clip(shock.beta_reduction_pct, 0.0, 1.0))
    beta_path[start_idx:end_idx] = params.beta * (1.0 - reduction)
    shock_active[start_idx:end_idx] = True

    return beta_path, shock_active


def simulate_trajectory(
    f: np.ndarray,
    params: ModelParams,
    shock: Optional[ShockParams] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Simulates the system using the exponential saturation model.

    Returns:
        omega: vaccinated stock array of length T+1 (omega[t] = stock at start of period t+1 in 1-indexing)
        p_values: length T array
        conversions: length T array
        beta_path: length T array
        shock_active: length T boolean array
    """
    shock = shock or ShockParams(enabled=False)
    beta_path, shock_active = build_beta_path(params, shock)

    omega = np.zeros(params.T + 1)
    omega[0] = params.vaccinated_pop_start

    p_values = np.zeros(params.T)
    conversions = np.zeros(params.T)

    total_vaccinated = params.vaccinated_pop_start

    for t in range(params.T):
        spend_t = params.B * max(float(f[t]), 0.0)

        beta_t = beta_path[t]
        p_t = 1.0 - np.exp(-beta_t * (spend_t ** params.rho))
        p_values[t] = p_t

        flow = p_t * (params.N - total_vaccinated)
        conversions[t] = flow

        total_vaccinated = total_vaccinated + flow
        omega[t + 1] = total_vaccinated

    return omega, p_values, conversions, beta_path, shock_active


def objective(f: np.ndarray, params: ModelParams, shock: Optional[ShockParams] = None) -> float:
    """
    Objective for minimizer: negative total QALYs.
    Model assumes omega_t contributes to QALYs in period t (stock at start of t).
    """
    omega, *_ = simulate_trajectory(f, params, shock)
    total_qalys = np.sum(omega[0:params.T]) * params.x
    return -total_qalys


def optimize_budget_allocation(
    params: ModelParams,
    shock: Optional[ShockParams] = None,
    initial_guess: Optional[np.ndarray] = None
):
    """
    Solves for optimal f on simplex.

    Returns:
        result: scipy.optimize.OptimizeResult
    """
    T = params.T
    shock = shock or ShockParams(enabled=False)

    if initial_guess is None:
        initial_guess = np.ones(T) / T

    constraints = ({'type': 'eq', 'fun': lambda f: np.sum(f) - 1.0})
    bounds = [(0.0, 1.0) for _ in range(T)]

    result = minimize(
        fun=lambda f: objective(f, params, shock),
        x0=initial_guess,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints
    )
    return result


def build_results_dataframe(
    optimal_f: np.ndarray,
    omega: np.ndarray,
    p_values: np.ndarray,
    conversions: np.ndarray,
    beta_path: np.ndarray,
    shock_active: np.ndarray,
    params: ModelParams
) -> pd.DataFrame:
    """
    Builds the period-by-period results table as a DataFrame.
    """
    rows = []
    cum_qalys = 0.0

    for t in range(params.T):
        w_start = omega[t]
        qalys_t = w_start * params.x
        cum_qalys += qalys_t

        rows.append({
            "t": t + 1,
            "Budget share (f_t)": float(optimal_f[t]),
            "Effective beta": float(beta_path[t]),
            "Shock active": bool(shock_active[t]),
            "Vaccination probability (p_t)": float(p_values[t]),
            "New vaccinations": float(conversions[t]),
            "Total vaccinated (start of t)": float(w_start),
            "QALYs gained in t": float(qalys_t),
            "Cumulative QALYs": float(cum_qalys),
        })

    return pd.DataFrame(rows)


def export_results_to_excel(df: pd.DataFrame, filename: str) -> None:
    """
    Writes results DataFrame to an Excel file in the current working directory.
    """
    df.to_excel(filename, index=False)
