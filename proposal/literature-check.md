# Registro de fuentes efectivamente revisadas

Revisión contextual solicitada por John durante el punto 3, 14 de octubre de 2026.
No completa el punto 4 ni demuestra novedad de A2.
Las conexiones entre ideas y ecuaciones del modelo son interpretaciones del autor del proyecto, no resultados atribuidos a esas fuentes.

| Fuente y versión | Sección / página realmente leída | Qué sostiene y para qué se usa | Límite |
|---|---|---|---|
| Aníbal Pinto, “Naturaleza e implicaciones de la heterogeneidad estructural de la América Latina”, artículo de 1970, reimpreso en la compilación de CEPAL | Inicio del texto, párrafos 1 a 5; páginas impresas 549 a 551, PDF 79 a 81 (contando desde uno). La portadilla, PDF 77, identifica publicación original en El Trimestre Económico 37(1), número 145 | Diferencias entre estratos de productividad; contexto cepalino de la tesis | No se revisó todo el artículo. No atribuirle una partición exacta formal/informal ni mayor elasticidad de horas |
| Hernando de Soto, The Other Path, transcripción institucional del capítulo introductorio en ILD | “A Hostile Reception” y “From Migrants to Informals”; HTML sin paginación y sin edición impresa identificable | Barreras legales y costos de cumplir la ley; motivación institucional de la barrera formal | No se consultó una edición completa de El otro sendero ni se verificaron sus estadísticas. No inventar número de página |
| Martha Alter Chen, The Informal Economy: Definitions, Theories and Policies, WIEGO Working Paper 1 | Portada PDF: agosto de 2012; sección I, páginas impresas 4 a 6 (PDF 7 a 9) | Distingue escuelas dualista, estructuralista, legalista y voluntarista; ubica a De Soto en la legalista. Ayuda a evitar equivalencias de etiquetas | Su uso de estructuralista enfatiza subordinación y subcontratación. No equivale automáticamente a CEPAL/Pinto. La ficha web indica 2002; se usa la fecha del PDF efectivamente leído |

Enlaces directos:
- [Pinto, reimpresión en CEPAL](https://repositorio.cepal.org/server/api/core/bitstreams/51ea6365-fbcb-4e50-95d2-fde032656901/content).
- [De Soto, capítulo introductorio en ILD](https://www.ild.org.pe/publications/books/the-other-path).
- [Chen, PDF WIEGO WP 1](https://www.wiego.org/wp-content/uploads/2019/09/Chen_WIEGO_WP1.pdf).


## Lecturas para el tema (15 de octubre de 2026)

| Fuente y versión | Qué se leyó realmente | Para qué se usa | Límite |
|---|---|---|---|
| Achdou, Han, Lasry, Lions y Moll (2022), *Review of Economic Studies* 89(1), 45–86. PDF publicado en benjaminmoll.com | Introducción (pp. 46–47) y sección 2.1 (pp. 50–51) | Formulación HJB–KF en tiempo continuo y cierre con una firma representativa | No se revisó el resto del paper ni si trata algo parecido a φ_I ≠ φ_F |
| Aiyagari (1994), *Quarterly Journal of Economics* 109(3), 659–684 | Ficha y resumen del working paper en el sitio del Fed de Minneapolis | Identificar el baseline y su año | No se obtuvo el PDF original; no citar páginas |
| Galindo, Ledesma, Yépez y Salinas (2024), BCRP DT 2024-005 | Documento completo (manuscrito en `modeling_jb/Paper5_HAInformality.pdf`, 40 pp.: secciones 1–3 y 6) y presentación del Encuentro de Economistas del BCRP, octubre de 2023 | Economía de dotación (Huggett en tiempo continuo, como Achdou et al.), bono en oferta neta cero. Formal e informal son dos tipos exógenos, un proceso de Poisson de dos estados: de formal a informal con intensidad 0.204 (sigue formal con 81.6 %) y de informal a formal con 0.115 cuando el tamaño informal es 0.64 (sigue informal con 89.2 %). Cada tipo tiene su ingreso (0.33 y 1), impuesto (0 y 0.18), prima de deuda (0.02 solo informales) y aversión al riesgo (0.3 y 0.15). Sin oferta laboral, firmas ni producción. Conclusiones (sección 6): dejan como extensión "endogenous shifts between states", límites de deuda distintos y fricciones financieras o nominales. Presentación 2023: "Informality is exogenously given" | Mi tesis vuelve endógeno el reparto formal/informal en el margen intensivo, con producción (dos firmas y capital), dos bienes y cuñas que dependen de z. Falta: los trabajos que lo citan |
| INEI (2018), *Perú: evolución de los indicadores de empleo e ingresos por departamento, 2007–2017*, PDF oficial (Lib1537) | Cuadro 7.5 y sección 7.4.1, «Según condición socioeconómica» (p. 122 del PDF); Cuadro 6.41 (p. 438) | Dato de motivación: 97.1 % en Q1 («quintil más pobre») y 44.1 % en Q5 en 2017 | El cuadro no nombra la variable de los quintiles. Con ENAHO 2021 reproduzco la edición 2022 del mismo cuadro con quintiles de **gasto per cápita** (error máximo 0.2 pp; con ingreso, hasta 3.6 pp). **No son de riqueza** |
| INEI (2022), *Perú: evolución de los indicadores de empleo e ingresos por departamento, 2007–2021* (Lib1870) | Cuadro 7.5 (p. 120 impresa, p. 131 del PDF): 2018–2021 por quintil | Barras de 2019 en la slide 4 | 2020–2021 con pandemia |
| ENAHO 2021–2023, microdatos (módulos 05 y 34) descargados con `inei-microdatos` | Cálculo propio, `code/data/build_enaho_quintiles.py` | Barras de 2023 en la slide 4 | `ocupinf` no se publica en 2024–2025 |
| Tesis propia, tabla de metas y validaciones | Valores dato/modelo de M1–M3 y V1–V3 | `code/data/moments.json` | M2, V1 y V2 no se recalculan en este repo |
| EPEN 2025 (INEI), agregados por 4 niveles educativos calculados en la tesis (`epen_kappa_moments_edu4_2025.csv`, solo agregados) | Horas del empleo principal, totales y formales, y ocupados por grupo | M3 (superior menos hasta secundaria, 38.6 pp) y V6 por grupos | La asignación de grupos a tramos de z supone que la educación ordena perfectamente a z |
| Céspedes y Rendón (2012), BCRP DT 2012-017; versión en inglés IZA DP 6991 (nov. 2012) | IZA: resumen, sección 5 y Tabla 3 (por quintil de ingreso: 0.41 el más pobre y 0.30 el más rico; por periodo: de 0.45 a 0.29). BCRP, Cuadro 2 (pp. 18–19): formal 0.39 (e.e. 0.02) e informal 0.37, con ingreso total por hora. **Este corte lo leyó John; el PDF del BCRP está bloqueado por anti-bot** | φ_F = 0.38 (promedio) y la evidencia sobre φ_I frente a φ_F | Falta copiar el error estándar y el intervalo del informal, y la definición de informal que usan |
| Banco Mundial, WDI, SI.POV.GINI (API consultada el 15 oct 2026) | Perú: 40.1 en 2024 (40.7 en 2023, 40.3 en 2022) | Dato de V5 (0.40) | Es Gini de ingreso o consumo per cápita, no de consumo del modelo |
| Gini de riqueza (V4 = 0.68 en la tesis) | Tabla secundaria (Wikipedia, "List of sovereign states by wealth inequality") que cita el Global Wealth Databook de Credit Suisse: Perú 0.795 (2018), 0.788 (2019), 0.800 (2021) | Contrastar el 0.68 de la tesis | **No se abrió el Databook.** El 0.68 no tiene fuente verificada; si se usa Credit Suisse, el dato sería cerca de 0.80 |
| Pijoan-Mas (2006, *RED* 9(2)); Perry et al. (2007, Banco Mundial); Loayza (2016, *The World Economy* 39(12)); Meghir, Narita y Robin (2015, *AER* 105(4)) | **No releídos para este proyecto.** Se citan con lo que de ellos dice la bibliografía y la revisión de la tesis | Filas de la tabla de la slide 25 ("qué hace / qué le falta") | Antes de la final: confirmar en cada paper la frase de la tabla (horas como seguro; exclusión o escape; búsqueda sin ahorro) |

## Por leer antes de la presentación final

- **Barrera a la formalidad en la literatura macro.** Varios trabajos la modelan como un costo fijo de entrada o como impuestos que dependen del tamaño de la firma. Candidatos: Ulyssea (2018, *AER*), D'Erasmo y Moscoso Boedo (2012, *JEDC*) y Leal Ordóñez (2014, *RED*). No se han leído; **no citarlos en las slides** hasta verificarlos.
- **Evidencia de elasticidades de horas** de cuenta propia frente a asalariadas (D15).
- **Trabajos que citan a Galindo et al. (2024)** y versiones de trabajo de Achdou et al.

No se usaron las estadísticas históricas de estas lecturas en slides.
La tesis local se consultó como contexto, sección 1, párrafos que distinguen ambos paradigmas. Esa consulta no verifica por sí sola las citas de terceros incluidas en la tesis.

## Pendientes del punto 4

| Tarea | Estado |
|---|---|
| D15: evidencia de elasticidad de horas informales o de cuenta propia frente a formales | Pendiente; no se infiere de los enfoques anteriores |
| Achdou et al. (2022), citas con versión, sección y página | Parcial: introducción y sección 2.1 |
| Galindo et al. (2024), citas con versión, sección y página | Hecho con el manuscrito (secciones 2 y 6); falta cotejar la paginación de la versión DT 2024-005 |
| Apéndices, working papers y citantes más cercanos al mecanismo A2 | Pendiente; no afirmar novedad |
| INEI, Cuadro 7.5: quintiles de ingreso o gasto | Resuelto: gasto per cápita (réplica con ENAHO 2021); no son de riqueza |
