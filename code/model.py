"""A2 labor block at fixed baseline V_a, density and prices (partial equilibrium)."""

import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from export_baseline import check_export

HERE = Path(__file__).resolve().parent
PHI_I_GRID = (0.38, 0.45, 0.50, 0.60, 0.70)  # D14: illustrative, not estimated.
# Debt premium chi(z) = chi * w(z)**eta of the closing run (run_metadata.txt); not in the CSV.
DEBT_PREMIUM = dict(chi=0.02, eta=1.0)


def load_baseline(data_dir=HERE / "data"):
    """Load exported model outputs only; no MATLAB, local thesis or microdata needed."""
    params = json.loads((data_dir / "parameters.json").read_text(encoding="utf-8"))
    table = np.loadtxt(data_dir / "baseline.csv", delimiter=",", skiprows=1)
    gap, da = check_export(table, params)
    a, z = np.unique(table[:, 0]), np.unique(table[:, 1])
    shape = (len(a), len(z))
    g, ell_f, ell_i, kappa = (table[:, col].reshape(shape) for col in range(2, 6))
    wage_f = (1 - params["tau"]) * params["w_F_star"] * z - kappa
    va = params["psi_F"] * ell_f ** (1 / params["Frisch"]) / wage_f
    mass = g * da
    cdf = np.cumsum(mass.sum(axis=1))
    # D17 includes the node crossing 20%; MATLAB excludes that node from Q1.
    q1_last = int(np.searchsorted(cdf, 0.20, side="left"))
    q1_matlab_last = max(int(np.searchsorted(cdf, 0.20, side="right")) - 1, 0)
    q5_first = int(np.searchsorted(cdf, 0.80, side="left"))
    return dict(params=params, a=a, z=z, mass=mass, ell_f=ell_f, ell_i=ell_i,
                kappa=kappa, va=va, va_relative_gap=gap, da=da,
                q1_last=q1_last, q1_matlab_last=q1_matlab_last, q5_first=q5_first)


def wages(z, params, kappa_z1, shape=1.0, weight=None):
    """R_F(z) and R_I(z); kappa(z) = kappa_z1 * w(z)**shape, w = (zmax - z)/(zmax - zmin).

    shape=1 is the thesis (linear); model_main.m uses the same kappa_z_shape exponent.
    weight replaces the grid-based w(z), e.g. percentile_weight(); None keeps the thesis form.
    """
    if not np.isfinite(kappa_z1) or kappa_z1 < 0:
        raise ValueError("FAIL: kappa_z1 must be finite and nonnegative")
    base_weight = (z[-1] - z) / (z[-1] - z[0]) if weight is None else weight
    low_weight = base_weight ** shape
    wage_f = (1 - params["tau"]) * params["w_F_star"] * z - kappa_z1 * low_weight
    wage_i = params["w_I_household_star"] * z ** params["nu_I"]
    if np.any(wage_f <= 0) or np.any(wage_i <= 0):
        raise ValueError("FAIL: A2 interior formula needs positive wages")
    return wage_f, wage_i


def interior_hours(va, z, params, phi_i, psi_i, kappa_z1, shape=1.0, weight=None):
    if not np.isfinite(phi_i) or not np.isfinite(psi_i) or phi_i <= 0 or psi_i <= 0:
        raise ValueError("FAIL: phi_I and psi_I must be finite and positive")
    if not np.isfinite(va).all() or np.any(va <= 0):
        raise ValueError("FAIL: V_a must be finite and positive")
    wage_f, wage_i = wages(z, params, kappa_z1, shape, weight)
    ell_f = (va * wage_f / params["psi_F"]) ** params["Frisch"]
    ell_i = (va * wage_i / psi_i) ** phi_i
    if not np.isfinite(ell_f + ell_i).all() or np.any(ell_f + ell_i >= params["H_bar"]):
        raise ValueError("FAIL: time constraint binds; A2 interior formula is inapplicable")
    return ell_f, ell_i


def informal_share(ell_f, ell_i, mass):
    return float(np.sum(mass * ell_i) / np.sum(mass * (ell_f + ell_i)))


def moments(ell_f, ell_i, baseline):
    mass = baseline["mass"]
    q1 = slice(0, baseline["q1_last"] + 1)
    q1_matlab = slice(0, baseline["q1_matlab_last"] + 1)
    q5 = slice(baseline["q5_first"], None)
    q1_share = informal_share(ell_f[q1], ell_i[q1], mass[q1])
    q1_matlab_share = informal_share(ell_f[q1_matlab], ell_i[q1_matlab], mass[q1_matlab])
    q5_share = informal_share(ell_f[q5], ell_i[q5], mass[q5])
    # M3 is a difference of formal fractions, weighted by hours within each z.
    formal_low = 1 - informal_share(ell_f[:, 0], ell_i[:, 0], mass[:, 0])
    formal_high = 1 - informal_share(ell_f[:, -1], ell_i[:, -1], mass[:, -1])
    return dict(M1=informal_share(ell_f, ell_i, mass), M3=formal_high - formal_low,
                V3=q1_share - q5_share, V3_matlab=q1_matlab_share - q5_share,
                Q1=q1_share, Q1_matlab=q1_matlab_share, Q5=q5_share,
                formal_z_min=formal_low, formal_z_max=formal_high,
                mass_at_cap=float(mass[ell_f + ell_i >= baseline["params"]["H_bar"]].sum()),
                max_hours=float(np.max(ell_f + ell_i)))


def quintile_shares(ell_f, ell_i, baseline):
    """Informal hours share by wealth quintile; node j goes to quintile ceil(cdf_j / 0.2).

    Same convention as model_main.m idx_q20: Q1 ends at the last node with cdf <= 20%.
    """
    mass = baseline["mass"]
    cdf = np.cumsum(mass.sum(axis=1))
    group = np.minimum(np.ceil(cdf / 0.2 - 1e-12), 5).astype(int)
    return [informal_share(ell_f[group == q], ell_i[group == q], mass[group == q]) for q in range(1, 6)]


def recalibrated_hours(baseline, phi_i, kappa_z1, shape=1.0, weight=None):
    """Hours for a given barrier, with psi_I set analytically so that M1 stays at the thesis value."""
    p, z, va, mass = (baseline[key] for key in ("params", "z", "va", "mass"))
    target_m1 = informal_share(baseline["ell_f"], baseline["ell_i"], mass)
    wage_f, wage_i = wages(z, p, kappa_z1, shape, weight)
    total_formal = np.sum(mass * (va * wage_f / p["psi_F"]) ** p["Frisch"])
    informal_scale = np.sum(mass * (va * wage_i) ** phi_i)
    psi_i = ((1 - target_m1) * informal_scale / (target_m1 * total_formal)) ** (1 / phi_i)
    ell_f, ell_i = interior_hours(va, z, p, phi_i, psi_i, kappa_z1, shape, weight)
    return psi_i, ell_f, ell_i


def max_barrier(baseline, shape=1.0, weight=None):
    """Largest barrier level that keeps R_F(z) > 0 at every z node (interior FOC)."""
    p, z = baseline["params"], baseline["z"]
    base_weight = (z[-1] - z) / (z[-1] - z[0]) if weight is None else weight
    low_weight = base_weight ** shape
    positive = low_weight > 0
    return float(np.min((1 - p["tau"]) * p["w_F_star"] * z[positive] / low_weight[positive])) * (1 - 1e-10)


def calibrate(baseline, phi_i, shape=1.0, weight=None):
    """Set psi_I analytically for M1, then solve the single M3 equation for kappa."""
    if not np.isfinite(phi_i) or phi_i <= 0:
        raise ValueError("FAIL: phi_I must be finite and positive")
    target = moments(baseline["ell_f"], baseline["ell_i"], baseline)

    def evaluate(kappa_z1):
        psi_i, ell_f, ell_i = recalibrated_hours(baseline, phi_i, kappa_z1, shape, weight)
        return psi_i, ell_f, ell_i, moments(ell_f, ell_i, baseline)

    # Positivity of the formal wage at every node provides the feasible upper bracket.
    kappa = brentq(lambda value: evaluate(value)[3]["M3"] - target["M3"],
                   0.0, max_barrier(baseline, shape, weight), xtol=1e-14, rtol=1e-14)
    psi_i, ell_f, ell_i, result = evaluate(kappa)
    return dict(phi_I=float(phi_i), psi_I=float(psi_i), kappa_z1=float(kappa), shape=float(shape),
                ell_f=ell_f, ell_i=ell_i, **result)


def percentile_weight(baseline):
    """1 - F(z) at each node, F the ergodic cdf of z at the node midpoint: no dependence on z_min, z_max."""
    mass_z = baseline["mass"].sum(axis=0)
    return 1 - (np.cumsum(mass_z) - mass_z / 2)


def group_formality(ell_f, ell_i, baseline, population_shares):
    """Formal share of hours in groups that cover consecutive slices of the z distribution.

    Groups go from low to high z (education ranks z). A node that straddles a cut is split by mass,
    so the moment is continuous in the cuts and in the parameters.
    """
    mass = baseline["mass"]
    formal_z, total_z = (mass * ell_f).sum(axis=0), (mass * (ell_f + ell_i)).sum(axis=0)
    cdf_z = np.concatenate([[0], np.cumsum(mass.sum(axis=0))])
    cuts = np.concatenate([[0], np.cumsum(population_shares) / np.sum(population_shares)])
    shares = []
    for low, high in zip(cuts[:-1], cuts[1:]):
        inside = np.clip(np.minimum(cdf_z[1:], high) - np.maximum(cdf_z[:-1], low), 0, None) / np.diff(cdf_z)
        shares.append(float((inside * formal_z).sum() / (inside * total_z).sum()))
    return np.asarray(shares)


def fit_education_groups(baseline, phi_i, data_shares, population_shares, weight=None, ad_valorem=False,
                         shapes=None):
    """Barrier level and curvature that best fit formality by education group (least squares).

    kappa(z) = level * weight(z)**s, or level * weight(z)**s * (1 - tau) w_F z if ad_valorem (a rate on the
    formal wage). psi_I keeps M1; the level is searched up to max_barrier, so R_F(z) > 0 at every node.
    """
    from scipy.optimize import minimize_scalar
    p, z = baseline["params"], baseline["z"]
    base_weight = (z[-1] - z) / (z[-1] - z[0]) if weight is None else weight
    gross = (1 - p["tau"]) * p["w_F_star"] * z if ad_valorem else np.ones_like(z)
    shapes = np.geomspace(0.1, 8, 40) if shapes is None else shapes
    best = None
    for shape in shapes:
        effective = base_weight ** shape * gross
        upper = max_barrier(baseline, 1.0, effective)

        def loss(fraction):
            _, ell_f, ell_i = recalibrated_hours(baseline, phi_i, fraction * upper, 1.0, effective)
            return float(np.sum((group_formality(ell_f, ell_i, baseline, population_shares) - data_shares) ** 2))
        result = minimize_scalar(loss, bounds=(0, 1), method="bounded", options=dict(xatol=1e-9))
        if best is None or result.fun < best["loss"]:
            best = dict(loss=float(result.fun), shape=float(shape), kappa_level=float(result.x * upper),
                        level_fraction_of_max=float(result.x), effective=effective)
    effective = best.pop("effective")
    psi_i, ell_f, ell_i = recalibrated_hours(baseline, phi_i, best["kappa_level"], 1.0, effective)
    kappa = best["kappa_level"] * effective
    return dict(best, phi_I=float(phi_i), psi_I=float(psi_i), ell_f=ell_f, ell_i=ell_i, ad_valorem=ad_valorem,
                kappa_over_gross=kappa / ((1 - p["tau"]) * p["w_F_star"] * z),
                groups=group_formality(ell_f, ell_i, baseline, population_shares), **moments(ell_f, ell_i, baseline))


def local_sensitivities(baseline, calibrated_base, relative_step=0.01):
    """Changes in pp after separate +1% perturbations, with no recalibration."""
    p = baseline["params"]
    base = {key: calibrated_base[key] for key in ("M1", "M3", "V3")}
    values = []
    for parameter in ("psi_I", "kappa_z1", "phi_I"):
        controls = {key: calibrated_base[key] for key in ("psi_I", "kappa_z1", "phi_I")}
        controls[parameter] *= 1 + relative_step
        ell_f, ell_i = interior_hours(baseline["va"], baseline["z"], p,
                                     controls["phi_I"], controls["psi_I"], controls["kappa_z1"])
        changed = moments(ell_f, ell_i, baseline)
        values.append([100 * (changed[key] - base[key]) for key in base])
    return np.asarray(values).T
