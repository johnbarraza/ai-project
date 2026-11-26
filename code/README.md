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
| `figures.py` | Figuras de las slides, con la letra de las slides (`fonts/`, Latin Modern, licencia GUST) |

## Qué comprueba

- **FOC con SymPy.** Deriva las dos FOC de horas con elasticidades distintas, la solución cerrada, las segundas derivadas negativas, `d ln(l_I/l_F)/d ln V_a = phi_I - phi_F`, la derivada de `s_I` y la cancelación de `V_a` con elasticidad común. Comprueba que el signo se invierte si `phi_I < phi_F`.
- **Firmas y cierre.** FOC de capital y trabajo de ambas firmas, condiciones de tiempo (KKT) y la identidad de recursos.
- **La corrida de la tesis.** Grilla 200 × 40, densidad, `V_a` reconstruida desde la FOC formal (nunca se deriva el `V` guardado), `V_a` decreciente en `a`, nadie en el tope de horas, fracción informal sin pendiente por riqueza a igual `z`.
- **Perfil por productividad.** Calcula la razón de horas informales a totales dentro de cada nodo de `z`, ponderadas por `g * da`. Exige que disminuya entre nodos y que coincida con la fracción individual a ese `z` bajo elasticidad común. Es una comparación estacionaria entre estados, no una trayectoria temporal ni una respuesta a un choque.
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
- `output/share_by_productivity.csv`: `z,s_I,s_F`, el perfil de la tesis que se muestra en la slide 12.
- `figures/motivation_quintiles`, `foc_hours`, `informal_share_by_assets`, `wealth_gap_by_phi`, `moment_sensitivity_map` (`.pdf` para LaTeX, `.png` de vista previa).
- `figures/informal_share_by_productivity`: perfil estacionario de horas informales por `z`, en PDF/PNG/SVG, generado únicamente después de pasar las comprobaciones.

## Límites

El ejercicio histórico de elasticidades es equilibrio parcial: `V_a`, `g` y precios quedan fijos. Los GE posteriores se resolvieron en MATLAB y sus resultados guardados se auditan y grafican por separado; no se les atribuye una nueva resolución en CI. El rango de `phi_I` es ilustrativo. El ejemplo de esfuerzo de la plantilla no representa el modelo de este proyecto.

## Avances para el paper, 23nov2026

`macro_checks.py`, llamado por `verify.py`, comprueba simbólicamente pagos de factores y beneficios de ambas firmas, homogeneidad CES y cierre de recursos con las dos cuñas. Guarda condiciones y alcance en `output/macro_identities.json`. Es la comprobación reproducible que acompaña la guía macro; no demuestra existencia del GE ni reemplaza las hojas personales.

`paper_results.py`, llamado por `verify.py`, verifica el export `data/paper_ge_experiments.json` y genera cuatro figuras `figures/final/paper_*`: sensibilidad de elasticidades con y sin reajuste, interés/capital, tope frente a igualdad de tiempo y perfiles por activos a productividad fija. Son23GE resueltos en MATLAB el13nov, reanalizados desde sus MAT el23nov; no nuevas simulaciones de esta revisión.

El export conserva hashes de los MAT y motores, diagnósticos y perfiles de políticas. Los objetivos M1/M3 son los del GE de referencia de la misma grilla, no una nueva estimación con microdatos. La brecha dentro de z usa quintiles condicionales de activos con reparto fraccional del nodo de corte; se distingue de la convención histórica D17. No hay certificación global de precisión.

`python -m unittest discover -s code -p test_verify_lean.py` comprueba que los recibos toleren conversiones LF/CRLF de Git y rechacen cambios de contenido. `verify.py` también coteja los archivos oficiales con `docs/lean-workflow.json`; conserva la comprobación del prototipo, ahora en `lean-prototype/`. Estos controles de identidad no ejecutan Lean ni sustituyen la revisión semántica. El [estado oficial](../docs/estado-lean.md) distingue los builds aprobados del cierre todavía abierto.
