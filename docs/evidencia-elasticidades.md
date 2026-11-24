# Evidencia de elasticidades: cotejo del 23nov2026

La versión pertinente para las cifras sectoriales es Céspedes y Rendón, *La elasticidad de oferta laboral de Frisch en economías con alta movilidad laboral*, [BCRP DT2012-017](https://www.bcrp.gob.pe/docs/Publicaciones/Documentos-de-Trabajo/2012/documento-de-trabajo-17-2012.pdf), octubre2012. La ficha de la versión inglesa [IZA DP6991](https://www.iza.org/publications/dp/6991/the-frisch-elasticity-in-labor-markets-with-high-job-turnover), noviembre2012, confirma autores, objeto y estimación alrededor de0,38. Se citan estas versiones de trabajo; no se afirma una publicación arbitrada posterior.

La extracción actual del PDF oficial BCRP mediante Firecrawl contiene el Cuadro2, ingreso total por hora: formal0,39, error estándar0,02 e intervalo0,35–0,44; informal0,37, error estándar0,02 e intervalo0,33–0,41. En el Cuadro3, ingreso principal por hora, informal es0,36 y formal0,39. No intercambiar esos cuadros.

El PDF IZA local efectivamente leído tiene22páginas y SHA256 `1acad32640511a816d899f4ceae2f3d87871fcdf2437f01d5a4ce10d6123d7dd`. Su Tabla3 (PDF22) presenta heterogeneidad por ingreso y periodo, pero no esas filas formal/informal. El archivo local llamado `D52-Cespedes-Rendon-BCRP2012.pdf` contiene una página de bloqueo Incapsula; no se contó como lectura del paper ni se atribuyó paginación a ese archivo. La extracción oficial actual se conserva en el registro privado `.firecrawl/bcrp2012-017.md`. No se hizo una revisión visual de ese Cuadro2 en el PDF oficial durante esta sesión.

## Interpretación para el modelo

El orden de las estimaciones puntuales no respalda imponer `φI>φF`: es el contrario. Los intervalos se superponen; no se realizó aquí un test de diferencia entre estimaciones. Además, comparar grupos de trabajadores formales e informales no identifica automáticamente elasticidades de dos actividades realizadas simultáneamente por un hogar del modelo.

Por tanto, el rango `φI=0,38…0,70` permanece como sensibilidad ilustrativa. El valor común0,38 tiene un antecedente agregado, pero no identifica por sí solo dos parámetros sectoriales ni el mecanismo de riqueza. El cálculo histórico que aplica la diferencia−0,02 alrededor de la referencia0,38 es otro ejercicio parcial; no reproduce literalmente los dos niveles0,39/0,37 ni una nueva calibración peruana.

Las cifras0,39/0,37 ya estaban en `code/verify.py`; el cotejo confirma su versión y cuadro, pero no las convierte en estimaciones estructurales del modelo. Esta limitación debe figurar en la discusión del paper final.
