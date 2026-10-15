"""Slide figures from verified arrays; called only after verify.check succeeds.

Notes, parameters and sources are typeset in the slide (from topic_numbers.tex), not inside
the figure, so every figure uses the slide font (Latin Modern Sans, bundled in code/fonts).
"""

import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "figures"
# Same colors as slides/topic.tex: base model gray dashed, extension in solid color.
INK, BASE, BLUE, TEAL, ORANGE, GRID = "#172033", "#8A94A3", "#223F91", "#008A92", "#D45D00", "#E3E8F0"


def style():
    logging.getLogger("fontTools").setLevel(logging.ERROR)  # bundled OTF has old timestamps
    fonts = sorted((HERE / "fonts").glob("*.otf"))
    for font in fonts:
        font_manager.fontManager.addfont(str(font))
    plt.rcParams.update({
        "font.family": "Latin Modern Sans" if fonts else "DejaVu Sans",
        "mathtext.fontset": "cm", "font.size": 15, "axes.labelsize": 15,
        "xtick.labelsize": 14, "ytick.labelsize": 14, "legend.fontsize": 14,
        "axes.titlesize": 15, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.edgecolor": INK, "axes.labelcolor": INK, "text.color": INK,
        "xtick.color": INK, "ytick.color": INK, "axes.spines.top": False,
        "axes.spines.right": False, "pdf.fonttype": 3,  # Type 3: the bundled OTF (CFF) fonts embed cleanly
        "svg.fonttype": "path", "svg.hashsalt": "ai-project"})


def save(fig, name):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight", pad_inches=0.04,
                metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(OUT / f"{name}.png", dpi=170, bbox_inches="tight", pad_inches=0.04)
    # SVG for the README: text as paths, no date, fixed ids, so reruns give the same file.
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", pad_inches=0.04, metadata={"Date": None})
    plt.close(fig)


def bars(ax, values, color, title, ylabel=None):
    labels = ["Q1\nmás pobre", "Q2", "Q3", "Q4", "Q5\nmás rico"]
    ax.bar(range(5), values, color=color, width=0.62)
    for x, y in enumerate(values):
        ax.text(x, y + 2, f"{y:.1f}", ha="center", va="bottom", fontsize=14)
    ax.set_xticks(range(5), labels)
    ax.set_ylim(0, 112)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_title(title)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(axis="y", color=GRID)
    ax.set_axisbelow(True)


def build_figures(baseline, scenarios, sensitivity, summary, moments_data):
    style()
    p = baseline["params"]

    # 1. Motivation (data only): informal employment by quintile, 2017 vs. the latest INEI years.
    inei = moments_data["inei_2018_cuadro_7_5"]
    recent = moments_data["inei_2022_cuadro_7_5"]["years"]
    own = moments_data["enaho_own_quintiles"]["years"]
    series = [(str(inei["year"]), inei["quintiles"], "#F2B27F"), ("2019", recent["2019"]["quintiles"], ORANGE),
              ("2023", own["2023"]["quintiles"], "#8C3D00")]
    fig, ax = plt.subplots(figsize=(9.6, 3.6))
    width = 0.26
    for k, (year, values, color) in enumerate(series):
        offset = (k - 1) * width
        ax.bar(np.arange(5) + offset, values, width=width, color=color, label=year)
        for x, y in zip(np.arange(5) + offset, values):
            ax.text(x, y + 1.5, f"{y:.0f}", ha="center", va="bottom", fontsize=12)
    ax.set_xticks(range(5), ["Q1\nmás pobre", "Q2", "Q3", "Q4", "Q5\nmás rico"])
    ax.set_ylabel("Empleo informal (% de ocupados)", fontsize=14)
    ax.set_ylim(0, 112)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.grid(axis="y", color=GRID)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncol=3, loc="upper right", fontsize=13)
    save(fig, "motivation_quintiles")

    # 2. Household FOC as marginal benefit = marginal cost, poor vs. rich at the same z.
    # Kept sparse: flat BMg lines labeled once, cost curves labeled at their end, one arrow per curve.
    ex = summary["foc_example"]
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6), sharey=True)
    hours = np.linspace(1e-4, 0.62, 400)
    top = 1.6 * ex["va_poor"] * max(ex["R_F"], ex["R_I"])
    panels = ((axes[0], "Horas formales", ex["R_F"], [(p["psi_F"], p["Frisch"], BLUE, "-", "CMg")]),
              (axes[1], "Horas informales", ex["R_I"],
               [(ex["psi_I_base"], p["Frisch"], BASE, "--", rf"CMg, $\phi_I={p['Frisch']:.2f}$"),
                (ex["psi_I_high"], ex["phi_I_high"], TEAL, "-", rf"CMg, $\phi_I={ex['phi_I_high']:.2f}$")]))
    for ax, title, ret, curves in panels:
        for va, label, ls_b in ((ex["va_poor"], "BMg pobre", "-."), (ex["va_rich"], "BMg rico", ":")):
            ax.axhline(va * ret, color=ORANGE, lw=1.6, ls=ls_b)
            ax.text(0.615, va * ret, label, ha="right", va="bottom", fontsize=13, color=ORANGE)
        for psi, phi, color, ls, name in curves:
            cost = psi * hours ** (1 / phi)
            ax.plot(hours, cost, color=color, ls=ls, lw=2.2, label=name)
            points = [(va * ret / psi) ** phi for va in (ex["va_rich"], ex["va_poor"])]
            for va, ell in zip((ex["va_rich"], ex["va_poor"]), points):
                ax.plot(ell, va * ret, "o", color=color, ms=6, mfc="white" if ls == "--" else color, zorder=4)
            change = 100 * (points[1] / points[0] - 1)
            # Solid curve: arrow between the two BMg lines; dashed (thesis) curve: arrow near the axis.
            y_arrow = 0.5 * (ex["va_rich"] + ex["va_poor"]) * ret if ls == "-" else 0.08 * top
            ax.annotate("", xy=(points[1], y_arrow), xytext=(points[0], y_arrow),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.8))
            ax.text(max(points) + 0.012, y_arrow, f"+{change:.0f} %", color=color, ha="left", va="center", fontsize=14)
        ax.set_title(title)
        ax.set_xlabel(r"Horas $\ell$ (fracción del tiempo)")
        ax.set_xlim(0, 0.62)
        ax.set_xticks([0, 0.2, 0.4, 0.6])
        ax.set_yticks([0, 1, 2, 3])
        ax.grid(axis="y", color=GRID)
        ax.legend(loc="upper left", frameon=False, fontsize=13, handlelength=2.2)
    axes[0].set_ylabel("Utilidad por hora")
    axes[0].set_ylim(0, top)
    fig.subplots_adjust(wspace=0.08)
    save(fig, "foc_hours")

    # 3. Informal share by assets at a fixed productivity node: base vs. extension.
    iz = summary["figure_a"]["z_index_zero_based"]
    fig, ax = plt.subplots(figsize=(9.6, 3.7))
    for row in scenarios:
        if row["phi_I"] not in (p["Frisch"], 0.50, 0.70):
            continue
        share = 100 * row["ell_i"][:, iz] / (row["ell_f"][:, iz] + row["ell_i"][:, iz])
        is_base = row["phi_I"] == p["Frisch"]
        color = BASE if is_base else (BLUE if row["phi_I"] == 0.50 else TEAL)
        ax.plot(baseline["a"], share, color=color, ls="--" if is_base else "-", lw=2.4)
        label = rf"$\phi_I=\phi_F={p['Frisch']:.2f}$ (mi modelo)" if is_base else rf"$\phi_I={row['phi_I']:.2f}$"
        ax.text(baseline["a"][-1] + 0.3, share[-1], label, color=color, va="center", fontsize=14)
    ax.set_xlabel(r"Activos del hogar $a$ (unidades del modelo)")
    ax.set_ylabel(r"Horas informales $s_I$ (%)")
    ax.set_xlim(baseline["a"][0], baseline["a"][-1])
    ax.set_xticks([0, 5, 10, 15, 20])
    ax.grid(axis="y", color=GRID)
    save(fig, "informal_share_by_assets")

    # 4. Wealth-quintile gap V3 as phi_I rises, with M1 and M3 held fixed.
    fig, ax = plt.subplots(figsize=(9.6, 3.7))
    phi = [row["phi_I"] for row in scenarios]
    v3 = [100 * row["V3_matlab"] for row in scenarios]
    ax.axhline(v3[0], color=BASE, ls="--", lw=2)
    ax.text(phi[-1], v3[0] - 0.35, rf"mi modelo, $\phi_I=\phi_F$: {v3[0]:.1f} pp", color=BASE,
            ha="right", va="top", fontsize=14)
    ax.plot(phi, v3, "o-", color=TEAL, lw=2.4, ms=7, label="equilibrio parcial")
    for x, y in zip(phi, v3):
        ax.annotate(f"{y:.1f}", (x, y), xytext=(0, 9), textcoords="offset points", ha="center", fontsize=14)
    # GE points (patched thesis solver) for the linear-barrier runs that exist so far.
    ge = sorted((r["Frisch_I"], 100 * r["V3"]) for r in summary.get("ge_runs", [])
                if r["converged"] and r["Frisch_I"] > p["Frisch"] and r["kappa_shape"] == 1 and r["nu_I"] == p["nu_I"] and r["debt_eta"] == 1)
    if ge:
        ax.plot(*zip(*ge), "D", color=ORANGE, ms=8, label="equilibrio general")
        for x, y in ge:
            ax.annotate(f"{y:.1f}", (x, y), xytext=(0, -18), textcoords="offset points", ha="center",
                        fontsize=14, color=ORANGE)
        ax.legend(frameon=False, loc="center left", fontsize=14)
    ax.annotate(f"Dato INEI {moments_data['inei_2018_cuadro_7_5']['year']}: "
                f"{moments_data['moments'][5]['data']:.0f} pp (fuera de escala)",
                xy=(0.04, 0.97), xycoords="axes fraction", va="top", color=ORANGE, fontsize=14)
    ax.set_xlabel(r"Elasticidad de las horas informales $\phi_I$")
    ax.set_ylabel("Brecha Q1 − Q5 (pp)")
    ax.set_xticks(phi)
    ax.set_ylim(0, 13)
    ax.grid(axis="y", color=GRID)
    save(fig, "wealth_gap_by_phi")

    # 5. Appendix: each parameter moves several moments (local, no recalibration).
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    cmap = LinearSegmentedColormap.from_list("changes", [ORANGE, "#F5F5F5", BLUE])
    limit = float(np.max(np.abs(sensitivity)))
    heat = ax.imshow(sensitivity, cmap=cmap, norm=TwoSlopeNorm(vmin=-limit, vcenter=0, vmax=limit), aspect="auto")
    ax.set_xticks(range(3), [r"$\psi_I$", r"$\kappa_{z1}$", r"$\phi_I$"])
    ax.set_yticks(range(3), ["M1 · horas informales", "M3 · formalidad", "V3 · brecha Q1 − Q5"])
    ax.set_xlabel(f"Parámetro que sube {100 * summary['sensitivities']['relative_step']:g}%")
    for (i, j), value in np.ndenumerate(sensitivity):
        ax.text(j, i, f"{value:+.2f} pp", ha="center", va="center",
                color="white" if abs(value) > 0.6 * limit else INK, fontsize=14)
    fig.colorbar(heat, ax=ax, label="pp", fraction=0.046, pad=0.03)
    ax.spines[:].set_visible(False)
    save(fig, "moment_sensitivity_map")

    # 6. Barrier and debt premium: functional forms on the actual z grid.
    from model import DEBT_PREMIUM
    z = baseline["z"]
    weight = (z[-1] - z) / (z[-1] - z[0])
    fig, (left, right) = plt.subplots(1, 2, figsize=(9.6, 3.4))
    styles = {0.5: (BASE, ":", "raíz"), 1.0: (TEAL, "-", "lineal (tesis)"), 2.0: (BASE, "--", "cuadrática")}
    for row in summary["kappa_shapes"]:
        if row["phi_I"] != p["Frisch"]:
            continue
        color, ls, label = styles[row["shape"]]
        left.plot(z, row["kappa_z1"] * weight ** row["shape"], color=color, ls=ls, lw=2.4, label=label)
    from model import percentile_weight
    left.plot(z, summary["kappa_percentile"][0]["kappa_0"] * percentile_weight(baseline), color=BLUE, ls="-.",
              lw=2.4, label=r"percentil, $1-F(z)$")
    left.set_title(r"Barrera por hora $\kappa(z)$ (recalibrada a M3)")
    for eta, (color, ls, label) in {0.0: (BASE, ":", r"constante ($\eta=0$)"), 1.0: (ORANGE, "-", r"lineal ($\eta=1$, tesis)"),
                                    2.0: (BASE, "--", r"cuadrática ($\eta=2$)")}.items():
        right.plot(z, DEBT_PREMIUM["chi"] * weight ** eta, color=color, ls=ls, lw=2.4, label=label)
    right.set_title(r"Prima de deuda $\chi(z)$")
    for ax in (left, right):
        ax.set_xlabel(r"Productividad $z$")
        ax.set_xticks([z[0], 1, 2, z[-1]], [f"{z[0]:.2f}\n" + r"$z_{\min}$", "1", "2", f"{z[-1]:.2f}\n" + r"$z_{\max}$"])
        ax.grid(axis="y", color=GRID)
        # Legend below the axes so it never covers the curves.
        ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.36), ncol=2, fontsize=13,
                  handlelength=2.2, columnspacing=1.2)
        ax.set_ylim(bottom=0)
    fig.subplots_adjust(wspace=0.25)
    save(fig, "barrier_forms")

    # 7. Formality by education (EPEN 2025) vs. the model, groups mapped to slices of the z distribution.
    edu = summary["education"]
    fig, ax = plt.subplots(figsize=(12.5, 3.4))
    x = np.arange(len(edu["groups"]))
    series = [("Dato EPEN 2025", edu["data"], ORANGE, None),
              ("Mi modelo (tesis)", edu["model_base"], BASE, None),
              ("Barrera por percentil, mejor ajuste", edu["fits"]["percentile"]["groups"], TEAL, None),
              ("Barrera proporcional al salario, mejor ajuste", edu["fits"]["ad_valorem"]["groups"], BLUE, "//")]
    width = 0.2
    for k, (label, values, color, hatch) in enumerate(series):
        offset = (k - 1.5) * width
        ax.bar(x + offset, 100 * np.asarray(values), width=width, color=color if hatch is None else "white",
               edgecolor=color, hatch=hatch, lw=1.2, label=label)
        for xi, v in zip(x + offset, values):
            ax.text(xi, 100 * v + 1.5, f"{100 * v:.0f}", ha="center", va="bottom", fontsize=11)
    ax.set_xticks(x, [f"{name}\n({100 * share:.0f} % ocupados)" for name, share in
                      zip(edu["groups"], edu["workers_share"])], fontsize=12)
    ax.set_ylabel("Horas formales (% del total)", fontsize=14)
    ax.set_ylim(0, 80)
    ax.set_yticks([0, 20, 40, 60, 80])
    ax.grid(axis="y", color=GRID)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="lower left", bbox_to_anchor=(0, 1.0), fontsize=13, ncol=4,
              handlelength=1.4, columnspacing=1.2)
    save(fig, "education_formality")
