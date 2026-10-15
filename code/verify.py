"""Verify A2 and D17 from exported model results; regenerate topic numbers/figures.

Run: python code/verify.py
Scope: conditional labor proposition and fixed-V_a/g/prices experiments, not a new GE.
"""

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import minimize_scalar

from model import (PHI_I_GRID, calibrate, fit_education_groups, group_formality, interior_hours, load_baseline,
                   local_sensitivities, moments, percentile_weight, quintile_shares, wages)

HERE = Path(__file__).resolve().parent
GE_WALRAS_TOL = 1e-3  # regression run reaches 8.6e-5
# Céspedes y Rendón (2012), BCRP DT 2012-017, Cuadro 2 (ingreso total por hora; EPE Lima 2002-2010),
# as read by John on p. 18-19 of the BCRP PDF: formal 0.39 (e.e. 0.02), informal 0.37. Mean 0.38 = thesis phi_F.
FRISCH_EVIDENCE = dict(formal=0.39, informal=0.37, formal_se=0.02)


def require(condition, message):
    if not condition:
        raise AssertionError("FAIL: " + message)


def check_symbolic():
    va, lf, li, wf, wi, pf, pi, sf, si = sp.symbols(
        "V_a ell_F ell_I w_F w_I phi_F phi_I psi_F psi_I", positive=True)
    objective = va * (wf * lf + wi * li) - sf * lf ** (1 + 1 / pf) / (1 + 1 / pf) - si * li ** (1 + 1 / pi) / (1 + 1 / pi)
    solutions = {lf: (va * wf / sf) ** pf, li: (va * wi / si) ** pi}
    for hours, wage, phi, psi in ((lf, wf, pf, sf), (li, wi, pi, si)):
        foc = sp.diff(objective, hours)
        require(sp.simplify(foc - (va * wage - psi * hours ** (1 / phi))) == 0, "FOC")
        require(sp.simplify(sp.powdenest(foc.subs(solutions), force=True)) == 0, "closed-form optimum")
        soc = sp.simplify(sp.diff(objective, hours, 2))
        require(sp.simplify(soc + psi / phi * hours ** (1 / phi - 1)) == 0, "second derivative")
        require(soc.is_negative is True, "strictly negative second derivative")
    require(sp.diff(objective, lf, li) == 0, "separable Hessian")
    ratio = solutions[li] / solutions[lf]
    log_ratio = sp.expand_log(sp.log(ratio), force=True)
    require(sp.simplify(va * sp.diff(log_ratio, va) - (pi - pf)) == 0, "log-ratio elasticity")
    share = solutions[li] / (solutions[lf] + solutions[li])
    derivative = sp.diff(share, va)
    require(sp.simplify(derivative - share * (1 - share) * (pi - pf) / va) == 0, "share derivative")
    require(sp.simplify(derivative.subs(pi, pf)) == 0, "common-phi cancellation")
    for delta, expected_sign in ((sp.Rational(1, 10), 1), (-sp.Rational(1, 10), -1)):
        value = derivative.subs({pi: sp.Rational(38, 100) + delta, pf: sp.Rational(38, 100), va: 1, wf: 1, wi: 1, sf: 1, si: 1})
        require(sp.sign(value) == expected_sign, "sign reversal when phi_I < phi_F")
    return dict(FOC=True, strict_concavity=True, log_ratio_elasticity=True,
                share_derivative=True, common_phi_cancellation=True, reversed_sign_case=True)


def check_structure():
    """Check the distinct firm/household blocks and aggregate accounting."""
    k, labor, a, b, prod, price, wage, rental = sp.symbols(
        "K L alpha beta A p w rental", positive=True)
    formal = prod * k**a * labor**(1-a)
    informal = prod * k**a * labor**b
    for output, capital_share, labor_share, good_price in (
        (formal, a, 1-a, 1), (informal, a, b, price)):
        profit = good_price * output - wage * labor - rental * k
        require(sp.simplify(sp.diff(profit, k) -
                            (capital_share*good_price*output/k-rental)) == 0, "firm capital FOC")
        require(sp.simplify(sp.diff(profit, labor) -
                            (labor_share*good_price*output/labor-wage)) == 0, "firm labor FOC")
        residual = good_price*output-capital_share*good_price*output-labor_share*good_price*output
        require(sp.simplify(residual-(1-capital_share-labor_share)*good_price*output) == 0,
                "factor-payment profit identity")
    va, rf, ri, lf, li, pf, pi, sf, si, time, multiplier = sp.symbols(
        "V_a R_F R_I ell_F ell_I phi_F phi_I psi_F psi_I H lambda", positive=True)
    objective = va*(rf*lf+ri*li)-sf*lf**(1+1/pf)/(1+1/pf)-si*li**(1+1/pi)/(1+1/pi)
    lagrangian = objective+multiplier*(time-lf-li)
    for hours, ret, phi, psi in ((lf,rf,pf,sf),(li,ri,pi,si)):
        require(sp.simplify(sp.diff(lagrangian,hours) -
                            (va*ret-psi*hours**(1/phi)-multiplier)) == 0, "time KKT with positive hours")
    z, zmin, span, level = sp.symbols("z z_min span kappa_level", positive=True)
    barrier = level*(zmin+span-z)/span
    require(sp.simplify(sp.diff(barrier,z)+level/span) == 0, "linear barrier slopes downward")
    require(barrier.subs(z,zmin)==level and barrier.subs(z,zmin+span)==0, "barrier endpoints")
    hours = sp.symbols("hours", positive=True)
    require(sp.diff(barrier*hours,hours)==barrier, "barrier is a marginal hours cost")
    require((barrier*hours).subs(hours,0)==0, "barrier is not a fixed entry payment")
    yf, yi, cf, ci, wf, wi, lf, li, kf, ki, r, dep, tau, cost, debt = sp.symbols(
        "Y_F Y_I C_F C_I w_F w_I L_F L_I K_F K_I r delta tau KappaCost DebtCost")
    pi_i = price*yi-wi*li-(r+dep)*ki
    income = (1-tau)*wf*lf-cost+wi*li+pi_i+r*(kf+ki)-debt+tau*wf*lf
    aggregate_saving = (income-cf-price*ci).subs(wf,(yf-(r+dep)*kf)/lf)
    formal_residual = yf-cf-dep*(kf+ki)-cost-debt
    require(sp.simplify(aggregate_saving.subs(ci,yi)-formal_residual)==0,
            "Walras accounting includes barrier and debt resource costs")
    return dict(firm_FOCs=True, time_KKT=True, linear_barrier=True,
                hours_cost_not_fixed_entry=True, formal_resource_accounting=True)


def check_numerical_optimum(baseline, scenarios):
    """Independent scalar maximization of the primitive objective, not its FOC."""
    p, z, va = (baseline[key] for key in ("params", "z", "va"))
    worst = 0.0
    checks = 0
    for scenario in (scenarios[0], scenarios[-1]):
        wf, wi = wages(z, p, scenario["kappa_z1"])
        for ia in (0, len(baseline["a"]) // 2, len(baseline["a"]) - 1):
            for iz in (0, len(z) // 2, len(z) - 1):
                for wage, phi, psi, expected in (
                    (wf[iz], p["Frisch"], p["psi_F"], scenario["ell_f"][ia, iz]),
                    (wi[iz], scenario["phi_I"], scenario["psi_I"], scenario["ell_i"][ia, iz]),
                ):
                    result = minimize_scalar(
                        lambda hours: -(va[ia, iz] * wage * hours - psi * hours ** (1 + 1 / phi) / (1 + 1 / phi)),
                        bounds=(0, p["H_bar"]), method="bounded", options={"xatol": 1e-13})
                    require(result.success, "independent maximization converged")
                    worst = max(worst, abs(result.x - expected))
                    checks += 1
    require(worst < 2e-7, "closed form agrees with primitive maximization")
    return dict(sectoral_optimizations=checks, max_hours_error=float(worst))


def check():
    symbolic = check_symbolic()
    structure = check_structure()
    baseline = load_baseline()
    p = baseline["params"]
    require((len(baseline["a"]), len(baseline["z"])) == (200, 40), "closing-run grid is 200 by 40")
    base = moments(baseline["ell_f"], baseline["ell_i"], baseline)
    np.testing.assert_allclose([base["M1"], base["M3"], base["V3"]],
                               [0.5171, 0.3775, 0.0431], atol=5e-5, rtol=0)
    # Saved MATLAB values, model_main.m idx_q20 convention, not the D17 cutoff.
    np.testing.assert_allclose([base["Q1_matlab"], base["Q5"], base["V3_matlab"]],
                               [0.5430113247673032, 0.4989318748130429, 0.044079449954260275], atol=1e-12, rtol=0)
    require(base["mass_at_cap"] == 0, "no baseline mass at time cap")
    require(base["max_hours"] < p["H_bar"], "time cap is slack at every two-sector model node")
    require(np.all(np.diff(baseline["va"], axis=0) < 0), "V_a strictly decreases with a at every z")
    share_base = baseline["ell_i"] / (baseline["ell_f"] + baseline["ell_i"])
    common_phi_range = float(np.ptp(share_base, axis=0).max())
    require(common_phi_range < 1e-12, "common-phi share is independent of a at fixed z")
    wf, _ = wages(baseline["z"], p, p["kappa_z1"])
    np.testing.assert_allclose((1 - p["tau"]) * p["w_F_star"] * baseline["z"] - baseline["kappa"],
                               np.broadcast_to(wf, baseline["va"].shape), atol=1e-14, rtol=0)
    scenarios = [calibrate(baseline, phi) for phi in PHI_I_GRID]
    expected_psi = (34.00, 19.50, 14.42, 9.19, 6.67)
    expected_kappa = (0.4000, 0.4008, 0.4013, 0.4022, 0.4029)
    expected_v3_pp = (4.31, 5.66, 6.62, 8.53, 10.43)
    for result, psi, kappa, v3 in zip(scenarios, expected_psi, expected_kappa, expected_v3_pp):
        np.testing.assert_allclose([result["M1"], result["M3"]], [base["M1"], base["M3"]], atol=1e-10, rtol=0)
        np.testing.assert_allclose(result["psi_I"], psi, atol=0.005, rtol=0)
        np.testing.assert_allclose(result["kappa_z1"], kappa, atol=5e-5, rtol=0)
        np.testing.assert_allclose(100 * result["V3"], v3, atol=0.005, rtol=0)
        require(result["mass_at_cap"] == 0, "all recalibrated scenarios remain interior")
        shares = result["ell_i"] / (result["ell_f"] + result["ell_i"])
        if result["phi_I"] > p["Frisch"]:
            require(np.all(np.diff(shares, axis=0) < 0), "informal share decreases with wealth at each z")
    require(round(scenarios[0]["psi_I"], 2) == 34.00, "recover baseline psi_I at stated two-decimal precision")
    require(np.all(np.diff([result["V3"] for result in scenarios]) > 0), "V3 rises on the five-point D17 grid")
    # B2: maintaining M1 alone must not be mistaken for maintaining M3.
    _, wage_i_base = wages(baseline["z"], p, p["kappa_z1"])
    phi_high = scenarios[-1]["phi_I"]
    informal_scale = np.sum(baseline["mass"] * (baseline["va"] * wage_i_base) ** phi_high)
    formal_total = np.sum(baseline["mass"] * baseline["ell_f"])
    psi_only = ((1 - base["M1"]) * informal_scale / (base["M1"] * formal_total)) ** (1 / phi_high)
    only_f, only_i = interior_hours(baseline["va"], baseline["z"], p, phi_high, psi_only, p["kappa_z1"])
    only_moments = moments(only_f, only_i, baseline)
    np.testing.assert_allclose(only_moments["M1"], base["M1"], atol=1e-10, rtol=0)
    np.testing.assert_allclose(only_moments["M3"], 0.3630, atol=5e-5, rtol=0)
    require(only_moments["M3"] < base["M3"], "B2: fixing M1 alone lowers M3 in this experiment")
    require(all(np.all(row["ell_f"] > 0) and np.all(row["ell_i"] > 0) for row in scenarios),
            "B3: both sectors retain positive hours at every node")
    reverse_f, reverse_i = interior_hours(baseline["va"], baseline["z"], p, 0.30, p["psi_I"], p["kappa_z1"])
    require(np.all(np.diff(reverse_i / (reverse_f + reverse_i), axis=0) > 0), "wealth sorting reverses when phi_I < phi_F")
    optimizer_check = check_numerical_optimum(baseline, scenarios)
    sensitivity = local_sensitivities(baseline, scenarios[0])
    require(sensitivity[0, 0] < 0, "psi_I lowers the informal hours share")
    require(sensitivity[1, 1] > 0, "kappa_z1 raises the productivity formality gap")
    require(sensitivity[2, 2] > 0, "phi_I raises V3 under the local fixed-control perturbation")
    labor_base = np.array([np.sum(baseline["mass"] * baseline["ell_f"] * baseline["z"]),
                           np.sum(baseline["mass"] * baseline["ell_i"] * baseline["z"] ** p["nu_I"])])
    effective_labor_changes = []
    for row in scenarios:
        labor = np.array([np.sum(baseline["mass"] * row["ell_f"] * baseline["z"]),
                          np.sum(baseline["mass"] * row["ell_i"] * baseline["z"] ** p["nu_I"])])
        effective_labor_changes.append((100 * (labor / labor_base - 1)).tolist())
    require(np.max(np.abs(effective_labor_changes)) < 0.3, "effective L_F/L_I change by less than 0.3 percent on this grid")
    z_index = (len(baseline["z"]) - 1) // 2
    # Slide figures and moment table: same quintile cut as the thesis (model_main.m idx_q20).
    quintiles_base = quintile_shares(baseline["ell_f"], baseline["ell_i"], baseline)
    np.testing.assert_allclose([quintiles_base[0], quintiles_base[4]], [base["Q1_matlab"], base["Q5"]],
                               atol=1e-12, rtol=0)
    require(np.all(np.diff([row["V3_matlab"] for row in scenarios]) > 0), "V3 (thesis cut) rises with phi_I")
    moments_data = json.loads((HERE / "data" / "moments.json").read_text(encoding="utf-8"))
    by_code = {row["code"]: row for row in moments_data["moments"]}
    for code, value in (("M1", base["M1"]), ("M3", base["M3"]), ("V3", base["V3_matlab"])):
        require(round(100 * value, 1) == by_code[code]["model_thesis"], f"{code} reproduces the thesis value")
    wealth_mass = baseline["mass"].sum(axis=1)
    mean_assets = float(np.sum(wealth_mass * baseline["a"]))
    gini_assets = float(np.sum(np.outer(wealth_mass, wealth_mass) * np.abs(np.subtract.outer(baseline["a"], baseline["a"]))) / (2 * mean_assets))
    require(round(gini_assets, 2) == by_code["V4"]["model_thesis"], "wealth Gini reproduces the thesis value")
    inei = moments_data["inei_2018_cuadro_7_5"]["quintiles"]
    require(round(inei[0] - inei[-1], 1) == by_code["V3"]["data"], "V3 data target equals INEI Q1 minus Q5")
    require(np.all(np.diff(inei) < 0), "INEI informality falls across quintiles")
    for year, row in moments_data["inei_2022_cuadro_7_5"]["years"].items():
        require(np.all(np.diff(row["quintiles"]) < 0), f"INEI {year}: informality falls across quintiles")
    own = moments_data["enaho_own_quintiles"]["years"]
    np.testing.assert_allclose(own["2021"]["quintiles"], moments_data["inei_2022_cuadro_7_5"]["years"]["2021"]["quintiles"],
                               atol=0.25, rtol=0)  # own ENAHO computation reproduces the published table
    require(own["2021"]["total"] == moments_data["inei_2022_cuadro_7_5"]["years"]["2021"]["total"],
            "own ENAHO 2021 total equals INEI")
    # FOC figure: same z, a poor (10th percentile of wealth) and a rich (90th) household.
    cdf = np.cumsum(baseline["mass"].sum(axis=1))
    ia_poor, ia_rich = (int(np.searchsorted(cdf, q)) for q in (0.10, 0.90))
    va_poor, va_rich = float(baseline["va"][ia_poor, z_index]), float(baseline["va"][ia_rich, z_index])
    require(va_poor > va_rich, "the poor household values one more unit of assets more")
    r_f, r_i = (float(w[z_index]) for w in wages(baseline["z"], p, p["kappa_z1"]))
    ratio = va_poor / va_rich
    foc_example = dict(z_index=z_index, a_poor=float(baseline["a"][ia_poor]), a_rich=float(baseline["a"][ia_rich]),
                       va_poor=va_poor, va_rich=va_rich, R_F=r_f, R_I=r_i,
                       psi_I_base=scenarios[0]["psi_I"], psi_I_high=scenarios[-1]["psi_I"],
                       phi_I_high=scenarios[-1]["phi_I"],
                       pct_formal=100 * (ratio ** p["Frisch"] - 1),
                       pct_informal_high=100 * (ratio ** scenarios[-1]["phi_I"] - 1))
    share_high = scenarios[-1]["ell_i"] / (scenarios[-1]["ell_f"] + scenarios[-1]["ell_i"])
    foc_example.update(share_base=float(share_base[0, z_index]),
                       share_high_poor=float(share_high[ia_poor, z_index]),
                       share_high_rich=float(share_high[ia_rich, z_index]))
    require(foc_example["share_high_poor"] > foc_example["share_base"] > foc_example["share_high_rich"],
            "example: with phi_I > phi_F the poor household is more informal than the rich one at the same z")
    require(foc_example["pct_informal_high"] > foc_example["pct_formal"] > 0,
            "the same V_a gap moves informal hours more when phi_I > phi_F")
    # Barrier shape kappa(z) = kappa_z1 * w(z)**shape, recalibrated to M1 and M3 (shape=1 is the thesis).
    kappa_shapes = []
    for shape in (0.5, 1.0, 2.0):
        for phi in (p["Frisch"], PHI_I_GRID[-1]):
            row = calibrate(baseline, phi, shape)
            np.testing.assert_allclose([row["M1"], row["M3"]], [base["M1"], base["M3"]], atol=1e-10, rtol=0)
            require(row["mass_at_cap"] == 0, "alternative kappa shapes remain interior")
            shares = row["ell_i"] / (row["ell_f"] + row["ell_i"])
            if phi == p["Frisch"]:
                require(float(np.ptp(shares, axis=0).max()) < 1e-12, "common phi: no wealth slope for any kappa shape")
            else:
                require(np.all(np.diff(shares, axis=0) < 0), "phi_I > phi_F: wealth slope for every kappa shape")
            kappa_shapes.append(dict(shape=shape, phi_I=phi, psi_I=row["psi_I"], kappa_z1=row["kappa_z1"],
                                     V3_matlab=row["V3_matlab"]))
    # The estimated sector gap (informal minus formal) applied around the thesis phi_F, recalibrated to M1 and M3.
    evidence_gap = FRISCH_EVIDENCE["informal"] - FRISCH_EVIDENCE["formal"]
    evidence_row = calibrate(baseline, p["Frisch"] + evidence_gap)
    require(evidence_gap < 0 and evidence_row["V3_matlab"] < base["V3_matlab"],
            "with the estimated phi_I < phi_F the wealth gap falls below the thesis value")
    frisch_evidence = dict(FRISCH_EVIDENCE, gap=evidence_gap, phi_I=p["Frisch"] + evidence_gap,
                           V3_matlab=evidence_row["V3_matlab"], psi_I=evidence_row["psi_I"])
    # Barrier by percentile of z, kappa(z) = kappa_0 * (1 - F(z)): does not depend on the grid ends.
    kappa_percentile = []
    for phi in (p["Frisch"], PHI_I_GRID[-1]):
        row = calibrate(baseline, phi, 1.0, percentile_weight(baseline))
        np.testing.assert_allclose([row["M1"], row["M3"]], [base["M1"], base["M3"]], atol=1e-10, rtol=0)
        require(row["mass_at_cap"] == 0, "percentile barrier remains interior")
        kappa_percentile.append(dict(phi_I=phi, psi_I=row["psi_I"], kappa_0=row["kappa_z1"], V3_matlab=row["V3_matlab"]))
    # Productivity rewarded equally in both sectors (nu_I = 1), common phi, recalibrated to M1 and M3.
    equal_returns = dict(baseline, params=dict(p, nu_I=1.0))
    nu_one = calibrate(equal_returns, p["Frisch"])
    np.testing.assert_allclose([nu_one["M1"], nu_one["M3"]], [base["M1"], base["M3"]], atol=1e-10, rtol=0)
    require(nu_one["V3_matlab"] < base["V3_matlab"], "nu_I = 1 lowers the composition gap V3")
    # V6: formality by education (EPEN 2025), groups mapped to consecutive slices of the z distribution.
    # M3 in the model compares the two extreme z nodes (0.3% of mass each); the data compare broad groups.
    edu = moments_data["epen_2025_edu4"]["groups"]
    workers, hours, formal_hours = (np.array([g[k] for g in edu]) for k in ("workers", "hours_main", "formal_hours_main"))
    edu_data = formal_hours / hours
    broad_data = float(formal_hours[2:].sum() / hours[2:].sum() - formal_hours[:2].sum() / hours[:2].sum())
    require(round(100 * broad_data, 1) == by_code["M3"]["data"], "M3 data equals the broad EPEN education gap")
    broad_workers = [workers[:2].sum(), workers[2:].sum()]

    def broad_gap(ell_f, ell_i):
        low, high = group_formality(ell_f, ell_i, baseline, broad_workers)
        return float(high - low)
    edu_base = group_formality(baseline["ell_f"], baseline["ell_i"], baseline, workers)
    require(np.all(np.diff(edu_base) > 0), "model formality rises across education groups")
    require(broad_gap(baseline["ell_f"], baseline["ell_i"]) < 0.5 * broad_data,
            "V6: the model education gradient is far below the data")
    odds_data, odds_model = edu_data / (1 - edu_data), edu_base / (1 - edu_base)
    education = dict(groups=[g["name"] for g in edu], workers_share=(workers / workers.sum()).tolist(),
                     data=edu_data.tolist(), model_base=edu_base.tolist(), broad_data=broad_data,
                     broad_model_base=broad_gap(baseline["ell_f"], baseline["ell_i"]),
                     model_M3_extreme_nodes=base["M3"],
                     extreme_node_mass=[float(baseline["mass"][:, 0].sum()), float(baseline["mass"][:, -1].sum())],
                     odds_ratio_data=float(odds_data[-1] / odds_data[0]),
                     odds_ratio_model=float(odds_model[-1] / odds_model[0]),
                     # Common phi: formal/informal hour odds scale as (R_F/R_I)**phi_F at a given V_a.
                     required_wage_ratio_change=float((odds_data[-1] / odds_data[0]) ** (1 / p["Frisch"])),
                     fits={})
    for name, options in (("grid", {}), ("percentile", dict(weight=percentile_weight(baseline))),
                          ("ad_valorem", dict(weight=percentile_weight(baseline), ad_valorem=True))):
        fit = fit_education_groups(baseline, p["Frisch"], edu_data, workers, **options)
        np.testing.assert_allclose(fit["M1"], base["M1"], atol=1e-10, rtol=0)
        require(fit["mass_at_cap"] == 0, f"{name} barrier fit remains interior")
        education["fits"][name] = dict(shape=fit["shape"], level=fit["kappa_level"],
                                       level_fraction_of_max=fit["level_fraction_of_max"],
                                       groups=fit["groups"].tolist(), broad_gap=broad_gap(fit["ell_f"], fit["ell_i"]),
                                       kappa_over_gross=[float(fit["kappa_over_gross"][i]) for i in (0, z_index, -1)],
                                       psi_I=fit["psi_I"], V3_matlab=fit["V3_matlab"], sse=fit["loss"])
    fits = education["fits"]
    require(max(fits["grid"]["broad_gap"], fits["percentile"]["broad_gap"]) < 0.5 * broad_data,
            "a per-hour barrier capped by R_F(z_min) > 0 cannot reach the education gradient")
    require(fits["ad_valorem"]["broad_gap"] < broad_data, "even a barrier proportional to the wage falls short")
    require(fits["ad_valorem"]["kappa_over_gross"][1] > 0.5, "the ad valorem fit needs a barrier above half the median wage")
    try:
        calibrate(equal_returns, PHI_I_GRID[-1])
        nu_one_high_interior = True
    except ValueError:
        nu_one_high_interior = False  # time cap binds: needs the KKT solution (GE solver)
    # General-equilibrium runs of the patched thesis solver (phi_I != phi_F), if exported.
    ge_runs = []
    ge_path = HERE / "data" / "ge_runs.csv"
    if ge_path.exists():
        with ge_path.open(encoding="utf-8") as stream:
            ge_runs = [{k: (val if k == "tag" else float(val)) for k, val in row.items()} for row in csv.DictReader(stream)]
        # A run counts only if markets clear; a bisection that ran out of iterations is reported, not used.
        for row in ge_runs:
            row["converged"] = bool(row["walras_err"] <= GE_WALRAS_TOL and np.isfinite(row["V3"]))
            row.update({k: None for k, v in row.items() if isinstance(v, float) and not np.isfinite(v)})
        reg = [row for row in ge_runs if row["tag"] == "ge_reg_phi038"]
        require(len(reg) == 1, "GE export contains the regression run")
        reg = reg[0]
        np.testing.assert_allclose([reg["M1"], reg["M3"], reg["V3"], reg["gini_assets"], reg["r_star"]],
                                   [base["M1"], base["M3"], base["V3_matlab"], gini_assets, p["r_star"]], atol=5e-4, rtol=0)
        require(reg["z_nodes_with_negative_slope"] == 0, "GE regression: no wealth slope with common phi")
    summary = dict(kappa_shapes=kappa_shapes, kappa_percentile=kappa_percentile, gini_assets=gini_assets,
                   ge_runs=ge_runs, education=education, frisch_evidence=frisch_evidence,
                   nu_one=dict(psi_I=nu_one["psi_I"], kappa_z1=nu_one["kappa_z1"], V3_matlab=nu_one["V3_matlab"],
                               high_phi_interior=nu_one_high_interior),
        scope="A2 conditional labor proposition; illustrative partial equilibrium, not a new GE",
        inputs_sha256={name: hashlib.sha256((HERE / "data" / name).read_bytes()).hexdigest()
                       for name in ("baseline.csv", "parameters.json")},
        parameters=p, symbolic=symbolic, structure=structure, baseline=base,
        va_relative_gap=baseline["va_relative_gap"], common_phi_share_range=common_phi_range,
        max_dVa_da_step=float(np.diff(baseline["va"], axis=0).max()), optimizer=optimizer_check,
        quintiles=dict(primary="D17: include first node reaching 20%", alternative="MATLAB: last node at or below 20%",
                       Q1_last_index_zero_based=baseline["q1_last"], Q1_matlab_last_index_zero_based=baseline["q1_matlab_last"],
                       Q5_first_index_zero_based=baseline["q5_first"],
                       Q1_mass=float(baseline["mass"][:baseline["q1_last"] + 1].sum()),
                       Q1_matlab_mass=float(baseline["mass"][:baseline["q1_matlab_last"] + 1].sum()),
                       Q5_mass=float(baseline["mass"][baseline["q5_first"]:].sum())),
        scenarios=[{key: value for key, value in row.items() if key not in ("ell_f", "ell_i")} for row in scenarios],
        psi_only_calibration=dict(phi_I=phi_high, psi_I=float(psi_only), kappa_z1=p["kappa_z1"], **only_moments),
        sensitivities=dict(relative_step=0.01, rows=["M1", "M3", "V3"], columns=["psi_I", "kappa_z1", "phi_I"], delta_pp=sensitivity.tolist()),
        effective_labor=dict(baseline_L_F=float(labor_base[0]), baseline_L_I=float(labor_base[1]),
                             columns=["L_F_change_percent", "L_I_change_percent"], changes_percent=effective_labor_changes,
                             interpretation="Small changes here do not bound GE price responses."),
        quintile_shares_base=quintiles_base, foc_example=foc_example,
        figure_a=dict(z_index_zero_based=z_index, z_node=float(baseline["z"][z_index]),
                      grid_median=float(np.median(baseline["z"])), convention="lower of the two central productivity nodes"),
        tolerances=dict(baseline_moments=5e-5, fixed_M1_M3=1e-10, rounded_psi_I=0.005,
                        rounded_kappa_z1=5e-5, rounded_V3_pp=0.005, va_relative_gap=1e-3),
        limitations=["V_a, g and prices are fixed; no modified HJB/KFE/market-clearing check or GE solution.",
                     "phi_I range is illustrative, not identified or supported by a literature search yet (D15).",
                     "Wealth quintiles of hours are not directly comparable with INEI worker classifications; source check pending.",
                     f"Stored baseline psi_I={p['psi_I']:g}; FOC reconstruction gives {scenarios[0]['psi_I']:.12g}, which rounds to {scenarios[0]['psi_I']:.2f}."])
    return baseline, scenarios, sensitivity, summary, moments_data


def ge_macros(runs):
    """Macros for the GE slide; GeAvailable=0 hides it until the runs exist."""
    lin = {round(r["Frisch_I"], 2): r for r in runs
           if r["converged"] and r["kappa_shape"] == 1 and r["nu_I"] == 0.6 and r["debt_eta"] == 1}
    out = {"GeAvailable": "1" if 0.38 in lin and 0.7 in lin else "0"}
    for phi, name in ((0.38, "Base"), (0.5, "Mid"), (0.7, "High")):
        r = lin.get(phi)
        out[f"GeVThree{name}PP"] = f"{100 * r['V3']:.1f}" if r else "--"
        out[f"GeMOne{name}"] = f"{100 * r['M1']:.1f}" if r else "--"
        out[f"GeMThree{name}"] = f"{100 * r['M3']:.1f}" if r else "--"
        out[f"GeR{name}"] = f"{100 * r['r_star']:.2f}" if r else "--"
        out[f"GePI{name}"] = f"{r['p_I_star']:.3f}" if r else "--"
        out[f"GeGini{name}"] = f"{r['gini_assets']:.3f}" if r else "--"
        out[f"GeSlope{name}"] = f"{100 * r['z_nodes_with_negative_slope']:.0f}" if r else "--"
    # Barrier shapes in GE with common phi (root and quadratic, recalibrated in partial equilibrium).
    shapes = [100 * r["V3"] for r in runs if r["converged"] and round(r["Frisch_I"], 2) == 0.38
              and r["kappa_shape"] != 1 and r["nu_I"] == 0.6 and r["debt_eta"] == 1]
    out["GeKappaAvailable"] = "1" if shapes else "0"
    out["GeKappaVThreeRange"] = f"{min(shapes):.2f}--{max(shapes):.2f}" if shapes else "--"
    base = lin.get(0.38)
    out["GeVThreeBaseTwoPP"] = f"{100 * base['V3']:.2f}" if base else "--"
    return out


def write_outputs(baseline, scenarios, sensitivity, summary, moments_data):
    out = HERE / "output"
    out.mkdir(exist_ok=True)
    (out / "verification.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    columns = ("phi_I", "psi_I", "kappa_z1", "M1", "M3", "V3", "V3_matlab", "Q1", "Q1_matlab", "Q5", "max_hours", "mass_at_cap")
    with (out / "calibration.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows({key: row[key] for key in columns} for row in scenarios)
    iz = summary["figure_a"]["z_index_zero_based"]
    selected = [row for row in scenarios if row["phi_I"] in (baseline["params"]["Frisch"], 0.5, 0.7)]
    curves = np.column_stack((baseline["a"], *(row["ell_i"][:, iz] / (row["ell_f"][:, iz] + row["ell_i"][:, iz]) for row in selected)))
    np.savetxt(out / "share_curves.csv", curves, delimiter=",", comments="", fmt="%.17g",
               header="a," + ",".join(f"s_I_phi_{row['phi_I']:g}" for row in selected))
    np.savetxt(out / "sensitivity_pp.csv", sensitivity, delimiter=",", comments="", fmt="%.17g", header="psi_I,kappa_z1,phi_I")
    # All reported model values in the proposal/deck are consumed through these macros.
    p, base, high = summary["parameters"], summary["baseline"], scenarios[-1]
    numbers = {
        "PhiBase": f"{p['Frisch']:.2f}", "PhiMid": f"{scenarios[2]['phi_I']:.2f}",
        "PhiHigh": f"{high['phi_I']:.2f}", "PsiFormal": f"{p['psi_F']:g}",
        "PsiInformalBase": f"{p['psi_I']:.2f}", "PsiRecovered": f"{scenarios[0]['psi_I']:.6f}",
        "PsiInformalHigh": f"{high['psi_I']:.2f}", "KappaBase": f"{p['kappa_z1']:.4f}",
        "KappaHigh": f"{high['kappa_z1']:.4f}", "TaxFormal": f"{p['tau']:.2f}",
        "NuInformal": f"{p['nu_I']:.2f}", "TimeCap": f"{p['H_bar']:g}",
        "MOnePercent": f"{100 * base['M1']:.2f}", "MThreePP": f"{100 * base['M3']:.2f}",
        "MThreePsiOnlyPP": f"{100 * summary['psi_only_calibration']['M3']:.2f}",
        "VThreeBasePP": f"{100 * base['V3']:.2f}", "VThreeHighPP": f"{100 * high['V3']:.2f}",
        "VThreeMatlabPP": f"{100 * base['V3_matlab']:.2f}",
        "CapMassPercent": f"{100 * base['mass_at_cap']:.0f}", "MaxHoursBase": f"{base['max_hours']:.2f}",
        "MaxHoursHigh": f"{high['max_hours']:.2f}", "CentralProductivity": f"{summary['figure_a']['z_node']:.4f}",
        "QOneMassPercent": f"{100 * summary['quintiles']['Q1_mass']:.2f}",
        "QOneMatlabMassPercent": f"{100 * summary['quintiles']['Q1_matlab_mass']:.2f}",
        "GridAssets": str(len(baseline['a'])), "GridProductivity": str(len(baseline['z'])),
        "VThreeThesisBasePP": f"{100 * base['V3_matlab']:.1f}",
        "VThreeThesisHighPP": f"{100 * high['V3_matlab']:.1f}",
        "QOneSharePercent": f"{100 * summary['quintile_shares_base'][0]:.1f}",
        "QFiveSharePercent": f"{100 * summary['quintile_shares_base'][4]:.1f}",
        "FocAPoor": f"{summary['foc_example']['a_poor']:.1f}", "FocARich": f"{summary['foc_example']['a_rich']:.1f}",
        "FocPctFormal": f"{summary['foc_example']['pct_formal']:.0f}",
        "ShareCentralBase": f"{100 * summary['foc_example']['share_base']:.0f}",
        "ShareHighPoor": f"{100 * summary['foc_example']['share_high_poor']:.0f}",
        "ShareHighRich": f"{100 * summary['foc_example']['share_high_rich']:.0f}",
        "FocPctInformalHigh": f"{summary['foc_example']['pct_informal_high']:.0f}",
        "IneiYear": str(moments_data['inei_2018_cuadro_7_5']['year']),
        **ge_macros(summary["ge_runs"]),
        "VThreeNuOnePP": f"{100 * summary['nu_one']['V3_matlab']:.1f}",
        "KappaNuOne": f"{summary['nu_one']['kappa_z1']:.3f}",
        "GiniAssets": f"{summary['gini_assets']:.2f}",
        "VThreeKappaRangeBase": "--".join(f"{100 * f(v):.1f}" for f in (min, max) for v in
                                          [[r['V3_matlab'] for r in summary['kappa_shapes'] if r['phi_I'] == p['Frisch']]]),
        "VThreeKappaRangeHigh": "--".join(f"{100 * f(v):.1f}" for f in (min, max) for v in
                                          [[r['V3_matlab'] for r in summary['kappa_shapes'] if r['phi_I'] != p['Frisch']]]),
        "KappaRangeShapes": "--".join(f"{f(v):.3f}" for f in (min, max) for v in
                                      [[r['kappa_z1'] for r in summary['kappa_shapes']]]),
        "FrischFormalCR": f"{summary['frisch_evidence']['formal']:.2f}",
        "FrischInformalCR": f"{summary['frisch_evidence']['informal']:.2f}",
        "FrischGapCR": f"{summary['frisch_evidence']['gap']:.2f}".replace("-", "$-$"),
        "PhiEvidence": f"{summary['frisch_evidence']['phi_I']:.2f}",
        "VThreeEvidencePP": f"{100 * summary['frisch_evidence']['V3_matlab']:.1f}",
        "KappaPercentile": f"{summary['kappa_percentile'][0]['kappa_0']:.3f}",
        "VThreePctBasePP": f"{100 * summary['kappa_percentile'][0]['V3_matlab']:.1f}",
        "VThreePctHighPP": f"{100 * summary['kappa_percentile'][1]['V3_matlab']:.1f}",
        "VSixData": f"{100 * summary['education']['broad_data']:.1f}",
        "VSixModel": f"{100 * summary['education']['broad_model_base']:.1f}",
        "VSixPercentile": f"{100 * summary['education']['fits']['percentile']['broad_gap']:.1f}",
        "VSixAdValorem": f"{100 * summary['education']['fits']['ad_valorem']['broad_gap']:.1f}",
        "AdValoremMedianPercent": f"{100 * summary['education']['fits']['ad_valorem']['kappa_over_gross'][1]:.0f}",
        "AdValoremPsiI": f"{summary['education']['fits']['ad_valorem']['psi_I']:.0f}",
        "VThreeAdValoremPP": f"{100 * summary['education']['fits']['ad_valorem']['V3_matlab']:.1f}",
        "VThreePercentilePP": f"{100 * summary['education']['fits']['percentile']['V3_matlab']:.1f}",
        "EduOddsData": f"{summary['education']['odds_ratio_data']:.0f}",
        "EduOddsModel": f"{summary['education']['odds_ratio_model']:.1f}",
        "EduRequiredRatio": f"{summary['education']['required_wage_ratio_change']:,.0f}".replace(",", "\\,"),
        "ExtremeNodeMassPercent": f"{100 * summary['education']['extreme_node_mass'][0]:.1f}",
        "IneiQOne": f"{moments_data['inei_2018_cuadro_7_5']['quintiles'][0]:.1f}",
        "IneiQFive": f"{moments_data['inei_2018_cuadro_7_5']['quintiles'][4]:.1f}",
        "IneiQOneLatest": f"{moments_data['enaho_own_quintiles']['years']['2023']['quintiles'][0]:.0f}",
        "IneiQFiveLatest": f"{moments_data['enaho_own_quintiles']['years']['2023']['quintiles'][4]:.0f}",
        "IneiGapLatest": f"{moments_data['enaho_own_quintiles']['years']['2023']['quintiles'][0] - moments_data['enaho_own_quintiles']['years']['2023']['quintiles'][4]:.1f}",
        "IneiGapPreCovid": f"{moments_data['inei_2022_cuadro_7_5']['years']['2019']['quintiles'][0] - moments_data['inei_2022_cuadro_7_5']['years']['2019']['quintiles'][4]:.1f}",
    }
    # Moment table: data targets and thesis values; M1, M3 and V3 are recomputed above.
    names = dict(M1="MOne", M2="MTwo", M3="MThree", V1="VOne", V2="VTwo", V3="VThree", V4="VFour", V5="VFive")
    for row in moments_data["moments"]:
        digits = 3 if row["code"] == "V2" else (2 if row["code"] in ("V1", "V4", "V5") else 1)
        numbers["Data" + names[row["code"]]] = f"{row['data']:.{digits}f}"
        numbers["Model" + names[row["code"]]] = f"{row['model_thesis']:.{digits}f}"
    tex = "% Generated by python code/verify.py; do not edit numerical values by hand.\n"
    tex += "".join("\\newcommand{\\" + name + "}{" + value + "}\n" for name, value in numbers.items())
    tex += "\\newcommand{\\CalibrationRows}{%\n"
    tex += "".join(f"{row['phi_I']:.2f} & {row['psi_I']:.2f} & {row['kappa_z1']:.4f} & {100 * row['V3_matlab']:.2f} \\\\\n" for row in scenarios)
    tex += "}\n"
    (out / "topic_numbers.tex").write_text(tex, encoding="utf-8")


def main():
    baseline, scenarios, sensitivity, summary, moments_data = check()
    write_outputs(baseline, scenarios, sensitivity, summary, moments_data)
    from figures import build_figures
    build_figures(baseline, scenarios, sensitivity, summary, moments_data)
    print("OK: SymPy, baseline, quintile conventions, joint calibration and independent maxima")
    print(f"V_a relative gap: {baseline['va_relative_gap']:.12g}")
    print("phi_I   psi_I       kappa_z1    V3 D17 (pp)   V3 MATLAB (pp)")
    for row in scenarios:
        print(f"{row['phi_I']:.2f}    {row['psi_I']:.6f}   {row['kappa_z1']:.7f}   {100*row['V3']:.6f}      {100*row['V3_matlab']:.6f}")
    print("OK: wrote code/output/verification.json, topic_numbers.tex and five figures (PDF/PNG)")


if __name__ == "__main__":
    main()
