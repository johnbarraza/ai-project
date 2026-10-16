# Procedencia de las figuras del modelo base

**Origen:** paquete de replicación de la tesis, [`aiyagari-2firms-peru`](https://github.com/johnbarraza/aiyagari-2firms-peru), carpeta `docs/images/`. Las generó el solver MATLAB R2025b del modelo base (corrida de cierre `test_AI098_cierre`, equilibrio general estacionario, φ_F = φ_I = 0.38, solo margen intensivo). Se copiaron sin cambios en el contenido; solo se recortó el margen blanco para que se lean mejor en la slide.

| Archivo | Qué muestra | Dónde se usa |
|---|---|---|
| `moll_equilibrium_asset_market_matlab.png` | Oferta de activos de los hogares S(r) y demanda de capital de las dos firmas K^D(r) = K_F + K_I; se cortan en r* = 0.066 y K* = 5.14 (Figura 7 de la tesis) | Anexo A16, página PDF 40 |
| `moll_informality_by_z_matlab.png` | Fracción de horas informales y formales por nodo de productividad z, promediada sobre la distribución de riqueza: 0.82 informal en z_min y 0.44 en z_max (Figura 5 de la tesis) | Referencia histórica; la slide 12 usa ahora el perfil regenerado por verify.py |

Son resultados del **modelo base calibrado** (la tesis), no de la sensibilidad φ_I > φ_F; las figuras de este proyecto las genera `code/verify.py`.

Revisión del 15 de octubre: se inspeccionaron el ploteador original y los vectores r_grid/S/KD del MAT, en solo lectura con scipy.io.loadmat. La línea une puntos calculados con tasas distintas; no es una serie temporal. No se ejecutó MATLAB ni se reinterpretó la saturación numérica como una propiedad económica del ahorro.

**Límites que conviene saber:**
- **S(r) es plana en 20 para r ≥ 0.10:** es el borde de la grilla de activos (a_max = 20); queda lejos del equilibrio.
- **Con r bajo, S(r) es negativa:** los hogares se endeudan hasta el límite a ≥ −1.
