# Entrega del paper: revisión del 24nov2026

La regla vigente es el [issue #7, secciones 5–7](https://github.com/alexanderquispe/AI-Econ-Modeling/issues/7), consultado nuevamente el 24 de noviembre: repositorio completo en `main` el **26 de noviembre a las 22:00, Lima**. El paper requiere entre 8 y 20 páginas de cuerpo, 11pt, una columna y márgenes de una pulgada. La presentación fue otra entrega y se conserva.

| Requisito | Situación observada | Trabajo de cierre |
|---|---|---|
| Paper `.tex`, `.bib`, `.pdf` | Versión24nov: 13 páginas de cuerpo, 15 totales; GE con/sin reajuste, contrastes de tiempo y bibliografía incorporados | Cerrar la tabla y evidencia Lean; completar y cotejar las hojas personales |
| Fuentes y literatura | Seis referencias, incluido el modelo coautorado y el cotejo BCRP de elasticidades | Conservar límites de acceso/paginación y evitar afirmar novedad o elasticidades identificadas para Perú |
| Código y figuras reproducibles | `code/verify.py` pasa; corregido el recibo Lean frente a LF/CRLF | Se integraron 23 GE auditados y cuatro figuras nuevas para el paper |
| Formalización propia | Carpeta oficial copiada íntegra en `lean/`, prototipo preservado en `lean-prototype/`; check rápido y prueba compilados | [Revisión semántica y cierre abiertos](estado-lean.md), con bloqueo por límite de uso; tabla de una fila actualizada |
| Hojas personales | Una hoja original disponible, con errores identificados | Corregir a mano y completar todas las derivaciones; ver `hand/README.md` |
| Colaboración con IA | Registro actualizado, veredictos en el paper y enlace a la versión cruda | Corrección ortográfica autorizada aplicada solo a erratas inequívocas del usuario; respuestas de IA y textos copiados preservados |
| README de una página | Actualizado al estado real del paper y de sus componentes | Mantener abiertos los requisitos que aún no están completos |
| Propuesta y ambos decks | Versionados en `main` | Conservar fuentes/PDF históricos |
| CI y publicación | [PR#14](https://github.com/johnbarraza/ai-project/pull/14) fusionado el24nov con código/LaTeX aprobados; fuente6777134 fijada | Incorporar el cierre Lean y los archivos personales faltantes por PR; workflow conservado |

## Nuevos resultados preparados

El export `code/data/paper_ge_experiments.json` contiene solo resultados del modelo: ocho GE a parámetros fijos, siete con reajuste a M1/M3, seis con un tope de horas menor y dos con igualdad de tiempo. Son corridas MATLAB del13nov, reanalizadas el23nov; esta revisión no se presenta como una nueva ejecución MATLAB. Se conservaron los hashes de cada MAT y motor.

Además de HJB/KFE, mercados, distribución y recursos, se verificaron las condiciones laborales por nodo, incluidas esquinas y multiplicadores. Para estas corridas logarítmicas sin impuesto al consumo formal se recuperó `Va=1/(cF+pI*cI)` de la FOC de consumo. Eso evita usar diferencias centrales de V como sustituto de la derivada que efectivamente utilizó el control laboral. Los errores de estacionariedad fueron menores a1,4e−15, frente al criterio1e−6; no se relajó el umbral anterior para hacer pasar un caso.

Las figuras nuevas comparan la brecha de horas y el nivel agregado de informalidad, la tasa de interés y el capital, el tope frente a igualdad y los perfiles a productividad fija. El ejercicio reajustado recupera los dos momentos internos, pero esa coincidencia no identifica empíricamente una forma ni las elasticidades. La certificación global frente a grillas y dominio sigue abierta.

## Decisiones pendientes del autor

John pidió continuar el24nov después de aclarar las reglas y solicitar revisión del repo de base. Se conservó la pregunta y proposición vigentes y se incorporaron los avances ya resueltos. No se adoptó la alternativa de centrar el paper en otra proposición de igualdad de tiempo. Los cuatro supuestos, la Proposición1 y su prueba se cotejaron por hash y permanecen idénticos. Falta conocer la devolución específica de la exposición del13nov; el enlace al repo proporcionado por John no se presenta como una transcripción de esa devolución.

No se declara revisión humana, autoría de hojas nuevas ni cierre científico por el solo hecho de pasar código o compilar un PDF.
