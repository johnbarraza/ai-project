# Revisión de `aiyagari-2firms-peru` para la entrega del curso

Revisado el24nov2026 a pedido de John. Se consultaron README, historial, ramas, código principal, configuración, auditoría de calibración, nota de convergencia, revisión bibliográfica y reporte Lean. La versión pública predeterminada es `master`, commit `8d0b6c31404d27f3cd350bc0f9493d5125a3962e`, del6oct2026. También existe la rama histórica `verificacion-lean`. No se modificó ese repositorio ni HA-IE2025 y no se ejecutó de nuevo su solver o su Lean en esta revisión.

## Avances aprovechables y límites

| Bloque | Evidencia revisada | Aplicación al paper del curso |
|---|---|---|
| Modelo macro | Dos firmas, dos bienes, horas simultáneas, ahorro, HJB/KFE y precios endógenos | Conservar el marco y citar el trabajo coautorado con Enzo Nevado. La proposición de composición es una contribución delimitada dentro de él |
| Preferencias y configuración | Código: gamma1, rho0,073, Frisch0,38, psiF55/psiI34, omegaCES0,56, theta1, nuI0,60; `setup_calibration.m` fija el target de horas0,509 | No copiar parámetros de versiones anteriores ni tratar rho como estimación externa independiente |
| Calibración | Auditoría: cuatro parámetros internos frente a tres objetivos; recomienda normalización o un cuarto momento | Los reajustes nuevos fijan psiF y recuperan dos metas internas con dos instrumentos. Eso no identifica todas las preferencias ni selecciona una forma entre familias |
| Indicadores | La auditoría distingue personas/gasto de horas/activos y clasificación por jefe de hogar de sector dominante en horas | Mantener esas diferencias; no presentar53% frente a4,4% como error de predicción homogéneo |
| Grilla de productividad | Se documenta sd(logz) realizada0,5281 frente a0,5440 y una alternativa de ancho2,8268 | No cambiar el soporte y atribuir todo a resolución. La alternativa requiere revisión/reajuste; no certifica automáticamente los experimentos actuales |
| Formalización histórica | Reporte parcial de bloques estáticos y contabilidad, con revisión semántica/humana pendiente | Sirve como antecedente; sus16teoremas no sustituyen la formalización de la Proposición1 del nuevo paper |
| México | Ejercicio de transporte y recalibración con ENOE, documentado como rechazo provisional de la especificación | No incorporarlo como validación exitosa ni ampliar el paper a otro país sin una pregunta y prueba propias |

## Diferencias de versiones observadas

El README público dice en su sección de reproducción que ejecutar `model_main` directamente usa500nodos de activos. El código fijado tiene `MODO_RAPIDO=true` en la línea134 y asigna200nodos en ese modo en la línea612; el modo de precisión usa500. Se toma el código/configuración realmente ejecutados como evidencia de la grilla, conservando la discrepancia documental.

El README menciona la corrida `test_AI098_cierre`, pero la consulta a su ruta en el commit fijado devolvió404. No se da por publicado su MAT por una mención en el README. Los exports del curso conservan procedencia y hashes de la fuente local. El repo público sí contiene otras corridas históricas; no se usan como si fueran la corrida de cierre o los nuevos GE de noviembre.

Los experimentos del13nov no aparecen como una actualización pública de ese `master`; se incorporan desde los MAT locales auditados en `code/data/paper_ge_experiments.json`. La comparación del curso separa ese bloque, la referencia histórica y las sensibilidades D73.

## Fuentes fijadas

- [README del modelo coautorado](https://github.com/johnbarraza/aiyagari-2firms-peru/blob/8d0b6c31404d27f3cd350bc0f9493d5125a3962e/README.md).
- [Código principal](https://github.com/johnbarraza/aiyagari-2firms-peru/blob/8d0b6c31404d27f3cd350bc0f9493d5125a3962e/model_main.m) y [configuración](https://github.com/johnbarraza/aiyagari-2firms-peru/blob/8d0b6c31404d27f3cd350bc0f9493d5125a3962e/calibracion/setup_calibration.m).
- [Auditoría de calibración](https://github.com/johnbarraza/aiyagari-2firms-peru/blob/8d0b6c31404d27f3cd350bc0f9493d5125a3962e/docs/AUDITORIA_CALIBRACION_PERU_Y_PAISES.md).
- [Convergencia](https://github.com/johnbarraza/aiyagari-2firms-peru/blob/8d0b6c31404d27f3cd350bc0f9493d5125a3962e/docs/REVISION_CONVERGENCIA_NZ.md), [revisión de claims](https://github.com/johnbarraza/aiyagari-2firms-peru/blob/8d0b6c31404d27f3cd350bc0f9493d5125a3962e/docs/REVISION_BIBLIOGRAFIA_CLAIMS_REFEREE.md) y [reporte Lean](https://github.com/johnbarraza/aiyagari-2firms-peru/blob/8d0b6c31404d27f3cd350bc0f9493d5125a3962e/lean/FINAL_VALIDATION_REPORT.md).

Los documentos de revisión del propio repo son diagnósticos, no fuentes que por sí solas verifiquen cada cita de terceros. Se cotejan los datos usados en el paper con sus fuentes específicas. Tampoco se afirma que los problemas históricos sigan presentes en cada corrida: cada export identifica su versión y controles.
