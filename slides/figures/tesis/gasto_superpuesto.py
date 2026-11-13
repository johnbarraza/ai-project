"""Gasto por sector dominante en un solo lienzo, con el formato de la figura 6a de la tesis.

Replica plot_moll_matlab_all.m (fig_gasto_distribution_by_formality): mismo .mat, mismo
reparto CES del gasto, mismas reglas de histograma y suavizado, colores y fuente.
Uso: python gasto_superpuesto.py <results_test_AI098_cierre.mat>
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat


def scalar(m, keys, default):
    for k in keys:
        if k in m:
            return float(np.asarray(m[k]).ravel()[0])
    return default


def wquantile(x, w, q):
    o = np.argsort(x)
    c = np.cumsum(w[o]) / w.sum()
    return float(x[o][np.searchsorted(c, q)])


def wstats(x, w):
    w = w / w.sum()
    mu = float(np.sum(w * x))
    return mu, wquantile(x, w, .5), float(np.sqrt(np.sum(w * (x - mu) ** 2)))


def wpdf(x0, w0, bins=70):
    lo, hi = wquantile(x0, w0, .005), wquantile(x0, w0, .995)
    x = np.linspace(lo, hi, max(160, 3 * bins))
    w0 = w0 / w0.sum()
    mu = np.sum(w0 * x0)
    sd = np.sqrt(np.sum(w0 * (x0 - mu) ** 2))
    bw = 1.06 * sd * (1 / np.sum(w0 ** 2)) ** (-1 / 5)
    pdf = (w0[None, :] * np.exp(-.5 * ((x[:, None] - x0[None, :]) / bw) ** 2)).sum(1) / (bw * np.sqrt(2 * np.pi))
    return x, pdf


m = loadmat(sys.argv[1], squeeze_me=True)
g, c = np.asarray(m["g"], float), np.asarray(m["c"], float)
da = np.asarray(m["da"], float)
p_i = scalar(m, ["p_I_star", "p_I"], 1.0)
om, eta, sig = scalar(m, ["omega_C"], .5), scalar(m, ["eta_C"], .5), scalar(m, ["sigma_C"], 1.0)
xi = (om * p_i / (1 - om)) ** sig
kap = (om * xi ** eta + (1 - om)) ** (1 / eta)
c_i = np.maximum(c, 1e-12) / kap
x = (xi * c_i + p_i * c_i).ravel(order="F")
w = np.maximum((g * (da[:, None] if da.ndim == 1 else da)).ravel(order="F"), 0)
w = w / w.sum()
formal = (np.asarray(m["ell_F"]) >= np.asarray(m["ell_I"])).ravel(order="F")

plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman"], "font.size": 13,
                     "mathtext.fontset": "stix", "axes.linewidth": .8})
lo, hi = max(0, wquantile(x, w, .001)), wquantile(x, w, .995)
fig, ax = plt.subplots(figsize=(11, 5.2))
groups = [(formal, (0, 0, 1), "Dominio formal"), (~formal, (1, 0, 0), "Dominio informal"),
          (np.ones_like(formal), (.45, .45, .45), "Total")]
lines = []
for k, (mask, col, name) in enumerate(groups):
    xg, wg = x[mask], w[mask]
    xp, yp = wpdf(xg, wg)
    mu, med, sd = wstats(xg, wg)
    ax.plot(xp, yp, color=col, lw=2.2, ls="--" if k == 2 else "-",
            label=f"{name}: media {mu:.2f}; desv. est. {sd:.2f}; masa {100*wg.sum():.0f}%".replace("0.", "0,").replace("1.", "1,"))
    ax.axvline(mu, color=col, ls=":", lw=1.2)
ax.set(xlim=(lo, hi), ylim=(0, None), xlabel="Gasto del modelo", ylabel="Densidad")
ax.tick_params(direction="in", top=True, right=True)
ax.legend(loc="upper right", frameon=True, edgecolor="black", fancybox=False, fontsize=15)
fig.tight_layout()
out = Path(__file__).with_name("gasto_superpuesto.png")
fig.savefig(out, dpi=300)
print("ok", out)
