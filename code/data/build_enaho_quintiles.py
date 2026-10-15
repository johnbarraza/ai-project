"""Informal employment rate by expenditure quintile, ENAHO annual 2021-2023 (aggregates only).

Not run by verify.py. Needs `pip install inei-microdatos` and downloads ~200 MB of microdata to a folder
outside the repo (microdata are never committed):

    python code/data/build_enaho_quintiles.py <download_dir>

Definitions (they reproduce INEI 2022, Cuadro 7.5, year 2021, within 0.2 pp):
- employed: ocu500 == 1, weight fac500a; informal: ocupinf == 1 (INEI variable; it is absent after 2023);
- quintiles of household expenditure per capita, gashog2d / mieperho, cut on the population
  distribution (factor07 * mieperho).
The output goes to code/data/moments.json under "enaho_own_quintiles".
"""
import copy
import json
import sys
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pyreadstat
from inei_microdatos import download_modules, load_catalog
from inei_microdatos.catalog import filter_catalog

HERE = Path(__file__).resolve().parent
KEYS = ["conglome", "vivienda", "hogar"]
YEARS = ("2021", "2022", "2023")


def download(dest):
    subset = []
    for survey in filter_catalog(load_catalog(), survey="enaho", year_min=int(YEARS[0]), year_max=int(YEARS[-1])):
        if survey["category"] != "ENAHO Actualizada":
            continue
        entry = dict(copy.deepcopy(survey), years={})
        for year, periods in survey["years"].items():
            for period, info in periods.items():
                if period.startswith("Anual"):
                    modules = [m for m in info["modules"] if m["module_code"] in ("5", "34")]
                    entry["years"].setdefault(year, {})[period] = dict(info, modules=modules, docs=[])
        subset.append(entry)
    download_modules(subset, dest=dest, fmt="STATA", workers=4, progress=False)


def read(zip_path, stem, wanted):
    with zipfile.ZipFile(zip_path) as archive, tempfile.TemporaryDirectory() as tmp:
        name = next(n for n in archive.namelist() if stem in n.lower() and n.lower().endswith(".dta"))
        path = archive.extract(name, tmp)
        _, meta = pyreadstat.read_dta(path, metadataonly=True)
        lookup = {c.lower(): c for c in meta.column_names}
        frame, _ = pyreadstat.read_dta(path, usecols=[lookup[c] for c in wanted])
    frame.columns = [c.lower() for c in frame.columns]
    for key in KEYS:
        frame[key] = frame[key].astype(str).str.strip().str.lstrip("0")
    return frame


def weighted_cuts(values, weights):
    order = np.argsort(values)
    return np.interp([0.2, 0.4, 0.6, 0.8], np.cumsum(weights[order]) / weights.sum(), values[order])


def rates(period_dir):
    emp = read(next(period_dir.glob("*Modulo05.zip")), "500", KEYS + ["ocu500", "ocupinf", "fac500a"])
    summ = read(next(period_dir.glob("*Modulo34.zip")), "sumaria", KEYS + ["mieperho", "gashog2d", "factor07"])
    summ = summ[summ["mieperho"] > 0].copy()
    spending = (summ["gashog2d"] / summ["mieperho"]).to_numpy()
    cuts = weighted_cuts(spending, (summ["factor07"] * summ["mieperho"]).to_numpy())
    summ["quintile"] = np.searchsorted(cuts, spending, side="right") + 1
    workers = emp[emp["ocu500"] == 1].merge(summ[KEYS + ["quintile"]], on=KEYS).dropna(subset=["ocupinf"])
    informal = (workers["ocupinf"] == 1).astype(float)
    weight = workers["fac500a"]
    by_quintile = [np.average(informal[workers.quintile == q], weights=weight[workers.quintile == q]) for q in range(1, 6)]
    return dict(total=round(100 * float(np.average(informal, weights=weight)), 1),
                quintiles=[round(100 * float(v), 1) for v in by_quintile], n_workers=int(len(workers)))


def main():
    dest = Path(sys.argv[1])
    download(dest)
    root = dest / "Condiciones de Vida y Pobreza - ENAHO"
    years = {year: rates(next((root / year).iterdir())) for year in YEARS}
    path = HERE / "moments.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["enaho_own_quintiles"]["years"] = years
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(years, indent=2))


if __name__ == "__main__":
    main()
