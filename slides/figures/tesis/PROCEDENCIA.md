# Procedencia

Figuras extraídas sin cambios (pdfimages) de `INFORMALIDAD_RIQUEZA_HA_PERU.pdf`, paquete `aiyagari-2firms-peru`:

- `ingreso_quintil.png`: Figura 4, p. 27.
- `lorenz.png`: Figura 3c, p. 25.

Misma calibración que las slides: M1 = 51,7 % y p_I = 0,928 en ambos documentos. Las genera MATLAB en ese paquete; `code/verify.py` no las regenera.
- `gasto_dominio.png`: Figura 6a, p. 29.
- `gasto_superpuesto.png`: las tres curvas de la figura 6a en un solo lienzo, generada con `gasto_superpuesto.py` desde `results_test_AI098_cierre.mat` (mismas reglas que `plot_moll_matlab_all.m`; reproduce medias 1,388/0,947/1,100 y masa formal 34,7 %).
