"""Export the saved baseline with SciPy; never run MATLAB or modify the source."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.io import loadmat


SCALARS = (
    "tau", "w_F_star", "w_I_household_star", "nu_I", "Frisch", "psi_F",
    "psi_I", "kappa_z1", "H_bar", "r_star", "p_I_star",
)
FIELDS = ("g", "ell_F", "ell_I", "kappa_F_aa")
HEADER = "a,z,g,ell_F,ell_I,kappa_F_aa"
HERE = Path(__file__).resolve().parent
SOURCE_RELATIVE = (
    "HA-IE2025/Code/CONTINUOUS_TIME/Aiyagari_firmas/try_endog_labor_2_firms/"
    "replication_package/outputs/stationary/test_AI098_cierre/"
    "results_test_AI098_cierre.mat"
)


def check_export(table, params):
    """Fail on a malformed grid, invalid density, or inconsistent labor FOCs."""
    if table.ndim != 2 or table.shape[1] != 6 or not np.isfinite(table).all():
        raise ValueError("FAIL: expected six finite columns")
    a, z = np.unique(table[:, 0]), np.unique(table[:, 1])
    if len(a) < 2 or len(z) < 2 or len(table) != len(a) * len(z):
        raise ValueError("FAIL: expected the full rectangular (a, z) grid")
    np.testing.assert_array_equal(table[:, 0], np.repeat(a, len(z)))
    np.testing.assert_array_equal(table[:, 1], np.tile(z, len(a)))
    da = a[1] - a[0]
    np.testing.assert_allclose(np.diff(a), da, rtol=1e-12, atol=1e-14)
    if not all(np.isfinite(value) for value in params.values()):
        raise ValueError("FAIL: non-finite scalar")
    if not 0 <= params["tau"] < 1 or any(
        params[key] <= 0 for key in SCALARS if key not in ("tau", "r_star", "kappa_z1")
    ) or params["kappa_z1"] < 0:
        raise ValueError("FAIL: invalid baseline parameter domain")
    _, productivity, g, ell_f, ell_i, kappa = table.T
    if np.any(productivity <= 0) or np.any(g < 0) or np.any(kappa < 0):
        raise ValueError("FAIL: invalid productivity, density, or formal barrier")
    np.testing.assert_allclose(g.sum() * da, 1.0, rtol=0, atol=1e-10)
    if np.any(ell_f <= 0) or np.any(ell_i <= 0):
        raise ValueError("FAIL: both labor FOCs require positive hours")
    if np.any(ell_f + ell_i >= params["H_bar"]):
        raise ValueError("FAIL: interior FOCs require a slack time constraint")
    wage_f = (1 - params["tau"]) * params["w_F_star"] * productivity - kappa
    wage_i = params["w_I_household_star"] * productivity ** params["nu_I"]
    if np.any(wage_f <= 0) or np.any(wage_i <= 0):
        raise ValueError("FAIL: net/effective wages must be positive")
    va_f = params["psi_F"] * ell_f ** (1 / params["Frisch"]) / wage_f
    va_i = params["psi_I"] * ell_i ** (1 / params["Frisch"]) / wage_i
    if not np.isfinite(va_f).all() or not np.isfinite(va_i).all() or np.any(va_f <= 0):
        raise ValueError("FAIL: reconstructed V_a must be finite and positive")
    relative_gap = float(np.max(np.abs(va_i - va_f) / va_f))
    if relative_gap >= 1e-3:
        raise ValueError(f"FAIL: sectoral V_a relative gap {relative_gap:.12g} >= 1e-3")
    return relative_gap, float(da)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Path to results_test_AI098_cierre.mat")
    args = parser.parse_args()
    source = args.source.resolve(strict=True)
    before = source.stat()
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    data = loadmat(source, simplify_cells=True)
    if data["run_config"]["run_tag"] != "test_AI098_cierre":
        raise ValueError("FAIL: unexpected source run")
    # These saved multipliers must equal one for the requested informal wage formula.
    if data["theta"] != 1 or not np.all(data["qq_informal"] == 1):
        raise ValueError("FAIL: informal wage has additional non-unit multipliers")
    a, z = np.asarray(data["a"]), np.asarray(data["z"])
    if a.ndim != 1 or z.ndim != 1 or np.any(np.diff(a) <= 0) or np.any(np.diff(z) <= 0):
        raise ValueError("FAIL: source grids must be increasing vectors")
    for key in FIELDS:
        if data[key].shape != (len(a), len(z)):
            raise ValueError(f"FAIL: {key} does not match the source grid")
    params = {key: float(data[key]) for key in SCALARS}
    table = np.column_stack((
        np.repeat(a, len(z)), np.tile(z, len(a)),
        *(data[key].ravel(order="C") for key in FIELDS),
    ))
    relative_gap, da = check_export(table, params)
    if hashlib.sha256(source.read_bytes()).hexdigest() != source_hash:
        raise ValueError("FAIL: source content changed during export")
    if source.stat().st_mtime_ns != before.st_mtime_ns:
        raise ValueError("FAIL: source modification time changed during export")

    out = HERE / "data"
    out.mkdir(exist_ok=True)
    csv_path = out / "baseline.csv"
    json_path = out / "parameters.json"
    np.savetxt(csv_path, table, delimiter=",", header=HEADER, comments="", fmt="%.17g")
    json_path.write_text(json.dumps(params, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    exported = np.loadtxt(csv_path, delimiter=",", skiprows=1)
    exported_params = json.loads(json_path.read_text(encoding="utf-8"))
    np.testing.assert_array_equal(exported, table)
    if exported_params != params:
        raise ValueError("FAIL: JSON round-trip changed a scalar")
    check_export(exported, exported_params)

    exported_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    modified_at = datetime.fromtimestamp(before.st_mtime, timezone.utc).isoformat(timespec="seconds")
    readme = f"""# Baseline exportado: test_AI098_cierre

## Procedencia

- Fuente original, abierta solo para lectura (ruta relativa): `{SOURCE_RELATIVE}`.
- Ese `.mat` no está publicado en `aiyagari-2firms-peru`; el SHA-256 permite comprobar
  la identidad del archivo local si se dispone de él. El hash no sustituye su disponibilidad.
  Los chequeos del proyecto usan el CSV y el JSON incluidos aquí y no necesitan ese `.mat`.
- Corrida: `{data['run_config']['run_tag']}`.
- Fecha de corrida guardada en `run_config.created_at`: `{data['run_config']['created_at']}` (sin zona horaria declarada).
- Cabecera del archivo: `{data['__header__'].decode('ascii')}`.
- Última modificación del archivo fuente (UTC): `{modified_at}`.
- Exportación (UTC): `{exported_at}`.
- SHA-256 del `.mat`: `{source_hash}`.
- Lectura con `scipy.io.loadmat(..., simplify_cells=True)`, sin ejecutar MATLAB.
- El hash y la fecha de modificación de la fuente se comprobaron antes de escribir la exportación.

## Archivos y convenciones

- `baseline.csv`: {len(table)} filas, grilla de {len(a)} activos por {len(z)} productividades.
  Columnas exactas: `{HEADER}`. Orden ascendente en `a` y luego en `z`;
  corresponde a aplanar las matrices fuente de forma `(n_a, n_z)` en orden C.
  Se escriben 17 cifras significativas; al releer se recuperan exactamente los valores fuente.
- `parameters.json`: los once escalares solicitados, con los mismos nombres del `.mat`.
- `g` conserva la densidad original respecto de activos, por nodo discreto de productividad.
  El paso uniforme es `da = {da:.17g}`. La masa por celda es `g * da`;
  `sum(g * da) = {table[:, 2].sum() * da:.17g}`. No multiplicar por un paso de `z`.
- El CSV contiene resultados del modelo (~1 MB), no microdatos. No se exporta el `.mat` completo.

## Reconstrucción de V_a y comprobaciones

`V_a` y `V` no se exportan. Para cada fila se reconstruye:

```text
w_F_net = (1 - tau) * w_F_star * z - kappa_F_aa
w_I_eff = w_I_household_star * z**nu_I
V_a_F = psi_F * ell_F**(1 / Frisch) / w_F_net
V_a_I = psi_I * ell_I**(1 / Frisch) / w_I_eff
error_relativo = max(abs(V_a_I - V_a_F) / V_a_F)
```

Se usa `V_a_F` como reconstrucción. Error relativo máximo observado:
**{relative_gap:.12g}**, estrictamente menor que **1e-3**.
La fórmula informal es válida aquí porque `theta = 1` y `qq_informal = 1`
en toda la grilla (verificado en la fuente).

El exportador falla ante grillas incompletas o desordenadas, datos no finitos,
densidad negativa o no normalizada, salarios no positivos, horas no interiores,
error entre las FOC mayor o igual que el umbral, o diferencias al releer CSV/JSON.
Estas comprobaciones se aplican también a los archivos exportados.
La reproducción de M1/M3/V3 y las figuras se ejecutan con `python code/verify.py`.

## Reproducir la exportación

Desde la raíz de `ai-project`, con Python y `code/requirements.txt` instalados:

```powershell
python code/export_baseline.py '<ruta-local>/{SOURCE_RELATIVE}'
```

Puede pasarse otra ubicación del mismo archivo como argumento. La fecha de exportación
cambia en cada ejecución; CSV y parámetros son deterministas para la misma fuente.
El punto de entrada de las verificaciones del proyecto seguirá siendo `code/verify.py`;
el exportador solo se necesita para reconstruir estos insumos desde la fuente local.
"""
    (out / "README.md").write_text(readme, encoding="utf-8")
    print(f"OK: {len(table)} rows ({len(a)} x {len(z)}), exact CSV/JSON round-trip")
    print(f"OK: max relative V_a gap = {relative_gap:.12g} < 1e-3")
    print(f"SHA-256: {source_hash}")


if __name__ == "__main__":
    main()
