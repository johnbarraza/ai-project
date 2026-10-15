# Procedencia de las figuras del modelo base

Son **candidatas**: se elige cuáles van a los slides durante la fase 7. Las que no se usen se borran antes del merge.

**Origen:** paquete de replicación `aiyagari-2firms-peru`, en `docs/images/` (<https://github.com/johnbarraza/aiyagari-2firms-peru>). Se generaron con el solver MATLAB R2025b del modelo base (corrida `test_AI098_cierre`), que solo tiene margen intensivo. Se copiaron sin cambios el 14 de octubre de 2026.

| Archivo | Qué muestra | Uso posible |
|---|---|---|
| `informalidad_peru_2023_nivel_educativo.png` | Informalidad por nivel educativo, Perú 2023 (INEI/ENAHO) | Motivación empírica (slide 2) |
| `moll_informality_by_z_matlab.png` | Fracción de horas informales por productividad $z$ | Resultado del baseline |
| `moll_time_use_by_z_excluding_leisure_matlab.png` | Horas formales e informales por $z$ | Margen intensivo del baseline |
| `moll_wealth_distribution_by_z_matlab.png` | Distribución de riqueza por $z$ | Mecanismo de acumulación |
| `moll_wealth_density_by_z_low_median_high_matlab.png` | Densidad de riqueza en $z$ bajo, mediano y alto | Mecanismo de acumulación |
| `moll_lorenz_curves_matlab.png` | Curvas de Lorenz | Desigualdad del baseline |
| `moll_savings_policy_matlab.png` | Política de ahorro $s(a,z)$ | Dinámica del hogar |
| `moll_equilibrium_asset_market_matlab.png` | Oferta y demanda de activos y la $r$ de equilibrio | Cierre GE (qué precio se ajusta) |

**Antes de poner cualquiera en un slide**, su nota al pie tiene que decir:
- qué ecuación o qué objeto del modelo grafica;
- ejes y unidades;
- que son resultados del **baseline** calibrado (no de la extensión);
- en el caso INEI, el año y la fuente.

Las figuras de la extensión (tres estados) las generará `code/verify.py` en este repo.
