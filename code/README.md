# Chequeos y figuras

Desde la raíz del repositorio:

```powershell
python -m pip install -r code/requirements.txt
python code/verify.py
```

`verify.py` es el único punto de entrada. Usa solo `data/baseline.csv`, `data/parameters.json` y `data/moments.json`: no requiere MATLAB, la tesis local ni microdatos. Si una afirmación falla, termina con error y no genera figuras.

| Archivo | Qué hace |
|---|---|
| `export_baseline.py` | Exporta la corrida de cierre de la tesis (`.mat`) a `data/` y valida la exportación. Ya se corrió; no hace falta repetirlo |
| `model.py` | Bloque de horas del hogar con `V_a`, `g` y precios fijos; momentos; recalibración de `psi_I` y `kappa_z1`; forma de `kappa(z)` |
| `verify.py` | Todas las comprobaciones; escribe `output/` y llama a `figures.py` |
| `figures.py` | Las cinco figuras de las slides, con la letra de las slides (`fonts/`, Latin Modern, licencia GUST) |

## Qué comprueba

- **FOC con SymPy.** Deriva las dos FOC de horas con elasticidades distintas, la solución cerrada, las segundas derivadas negativas, `d ln(l_I/l_F)/d ln V_a = phi_I - phi_F`, la derivada de `s_I` y la cancelación de `V_a` con elasticidad común. Comprueba que el signo se invierte si `phi_I < phi_F`.
- **Firmas y cierre.** FOC de capital y trabajo de ambas firmas, condiciones de tiempo (KKT) y la identidad de recursos.
- **La corrida de la tesis.** Grilla 200 × 40, densidad, `V_a` reconstruida desde la FOC formal (nunca se deriva el `V` guardado), `V_a` decreciente en `a`, nadie en el tope de horas, fracción informal sin pendiente por riqueza a igual `z`.
- **Momentos.** Reproduce M1, M3 y V3 de la tesis (`data/moments.json`) y que el dato V3 sea Q1 − Q5 del INEI.
- **Recalibración.** Para cada `phi_I` en {0.38, 0.45, 0.50, 0.60, 0.70} ajusta `psi_I` (M1) y `kappa_z1` (M3). Comprueba que M1 y M3 quedan fijos, que la pendiente por riqueza aparece y que V3 sube. Contrasta la solución cerrada con 36 maximizaciones numéricas.
- **Forma de la barrera.** Repite la recalibración con `kappa(z)` cuadrática y raíz; con `phi` común sigue sin haber pendiente por riqueza.
- **Ejemplo de la FOC.** Hogar pobre (percentil 10 de riqueza) y rico (percentil 90) con el mismo `z`.

## Corte de quintiles

V3 es la diferencia entre la fracción de horas informales del quintil de riqueza más bajo y la del más alto, con la masa `g * da`. Las slides usan el corte de la tesis (`idx_q20` de `model_main.m`: Q1 termina en el último nodo con acumulada ≤ 20 %), que da **4.41 pp** en la tesis. `verification.json` guarda también el corte que incluye el nodo que cruza el 20 % (4.31 pp); no se mezclan.

## Salidas

- `output/topic_numbers.tex`: todos los números de las slides y la propuesta; no se editan a mano.
- `output/verification.json`: parámetros, hashes de los insumos, chequeos, momentos, escenarios, formas de `kappa` y límites.
- `output/calibration.csv`, `share_curves.csv`, `sensitivity_pp.csv`: tablas de los escenarios.
- `figures/motivation_quintiles`, `foc_hours`, `informal_share_by_assets`, `wealth_gap_by_phi`, `moment_sensitivity_map` (`.pdf` para LaTeX, `.png` de vista previa).

## Límites

Es equilibrio parcial: `V_a`, `g` y precios quedan en los de la tesis. No resuelve una HJB/KF modificada ni el vaciado de mercados con `phi_I ≠ phi_F`; eso se hará con el solver MATLAB de la tesis. El rango de `phi_I` es ilustrativo. `effort_check.pdf` es un resto de la plantilla que todavía usan `paper/` y `slides/final.tex`.
