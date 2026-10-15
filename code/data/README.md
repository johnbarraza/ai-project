# Baseline exportado: test_AI098_cierre

## Procedencia

- Fuente original, abierta solo para lectura (ruta relativa): `HA-IE2025/Code/CONTINUOUS_TIME/Aiyagari_firmas/try_endog_labor_2_firms/replication_package/outputs/stationary/test_AI098_cierre/results_test_AI098_cierre.mat`.
- Ese `.mat` no está publicado en `aiyagari-2firms-peru`; el SHA-256 permite comprobar
  la identidad del archivo local si se dispone de él. El hash no sustituye su disponibilidad.
  Los chequeos del proyecto usan el CSV y el JSON incluidos aquí y no necesitan ese `.mat`.
- Corrida: `test_AI098_cierre`.
- Fecha de corrida guardada en `run_config.created_at`: `2026-06-26 13:46:03` (sin zona horaria declarada).
- Cabecera del archivo: `MATLAB 5.0 MAT-file, Platform: PCWIN64, Created on: Fri Jun 26 13:46:03 2026`.
- Última modificación del archivo fuente (UTC): `2026-06-26T18:46:03+00:00`.
- Exportación (UTC): `2026-10-15T03:14:09+00:00`.
- SHA-256 del `.mat`: `71693044eeaee8b64b1446daf68b0c6af8784a9fb84af332858b001e8c0ecece`.
- Lectura con `scipy.io.loadmat(..., simplify_cells=True)`, sin ejecutar MATLAB.
- El hash y la fecha de modificación de la fuente se comprobaron antes de escribir la exportación.

## Archivos y convenciones

- `baseline.csv`: 8000 filas, grilla de 200 activos por 40 productividades.
  Columnas exactas: `a,z,g,ell_F,ell_I,kappa_F_aa`. Orden ascendente en `a` y luego en `z`;
  corresponde a aplanar las matrices fuente de forma `(n_a, n_z)` en orden C.
  Se escriben 17 cifras significativas; al releer se recuperan exactamente los valores fuente.
- `parameters.json`: los once escalares solicitados, con los mismos nombres del `.mat`.
- `g` conserva la densidad original respecto de activos, por nodo discreto de productividad.
  El paso uniforme es `da = 0.10552763819095479`. La masa por celda es `g * da`;
  `sum(g * da) = 1.0000000000000009`. No multiplicar por un paso de `z`.
- El CSV contiene resultados del modelo (~1 MB), no microdatos. No se exporta el `.mat` completo.
- `moments.json`, bloque `epen_2025_edu4`: ocupados, horas del empleo principal y horas formales por 4 niveles
  educativos (EPEN 2025, totales ponderados). Son los agregados que la tesis calcula en
  `data/enaho/output/epen_kappa_moments_edu4_2025.csv`; no hay microdatos. `verify.py` comprueba que reproducen
  el dato de M3 (38.6 pp) y los usa para V6 y el ajuste de la barrera por grupos.

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
**8.77068841111e-05**, estrictamente menor que **1e-3**.
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
python code/export_baseline.py '<ruta-local>/HA-IE2025/Code/CONTINUOUS_TIME/Aiyagari_firmas/try_endog_labor_2_firms/replication_package/outputs/stationary/test_AI098_cierre/results_test_AI098_cierre.mat'
```

Puede pasarse otra ubicación del mismo archivo como argumento. La fecha de exportación
cambia en cada ejecución; CSV y parámetros son deterministas para la misma fuente.
El punto de entrada de las verificaciones del proyecto seguirá siendo `code/verify.py`;
el exportador solo se necesita para reconstruir estos insumos desde la fuente local.

## `ge_runs.csv`: corridas de equilibrio general con `phi_I` distinto de `phi_F`

- **Origen:** copia local del solver MATLAB de la tesis (`model_main.m` del paquete de replicación). El único cambio es que acepta una elasticidad propia para las horas informales (`HA_IE_FRISCH_I`). El solver original no se modificó.
- **Corridas:** grilla rápida (I = 200, N_z = 40), con el mismo entorno que `test_AI098_cierre`. Cada fila es una corrida. `psi_I` y `kappa_z1` vienen de la recalibración en equilibrio parcial de `model.py`; en equilibrio general no se recalibran, así que M1 y M3 pueden moverse.
- **Regresión:** `ge_reg_phi038` (phi_I = phi_F = 0.38) reproduce la corrida de la tesis. `verify.py` lo exige con una tolerancia de 5e-4 en M1, M3, V3, Gini y r*.
- **Columnas:** las definiciones son las de `model.py`. La masa es `g * da`; V3 usa el corte de quintiles de la tesis. `z_nodes_with_negative_slope` es la fracción de nodos de z en que s_I cae con a.
- **Contenido:** son resultados del modelo, no microdatos.
