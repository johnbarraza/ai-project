# Formalización del paper, 2026-11-26

**Cierre aceptado:** el validador canónico terminó con salida 0.

La fuente matemática es el [paper publicado en 6777134](https://github.com/johnbarraza/ai-project/blob/6777134ba22670ebd53b65d21a48d719c09b3fbd/paper/paper.pdf). Los cuatro supuestos, la Proposición 1 y su prueba ordinaria se conservan por hash. Las aclaraciones editoriales y la tabla de evidencia se actualizaron después.

La carpeta `lean/` es una copia completa y exacta del directorio generado, con su `.gitignore` respetado. Los archivos ignorados se mantienen fuera del índice de Git, sin force-add. El prototipo histórico está en `lean-prototype/`. El [manifiesto](lean-workflow.json) vincula los archivos de texto mediante LF y los binarios mediante sus bytes exactos.

| Componente | Evidencia y alcance |
|---|---|
| Enunciados | Un resultado y sus prerrequisitos, con los juicios independientes retenidos en la carpeta. El cierre valida su vigencia. |
| Prueba | FOC a políticas explícitas, derivada, regla de la cadena y tres signos. Endpoint `compositionConditionalHours`, tipo `compositionConditionalHoursSpec`. |
| Fidelidad a la prueba ordinaria | Revisión independiente y sus registros en la carpeta generada. |
| Check del curso | [Salida real](lean-course-check.txt), exit 0. La compilación por sí sola no establece aceptación semántica. |
| Cierre canónico | [Salida real del validador](lean-closure-validation.txt). El manifiesto registra su código de salida efectivo. |
| Revisión humana | Pendiente. No se inventa aprobación ni comprensión personal. |

Las diez etapas del cierre estricto terminaron sin errores. El wrapper adicional `paper_contribution.py check Barraza26LaborComposition` terminó con exit 1: después del cierre y de sincronizar el README mediante la herramienta oficial, exige una acción ejecutable, pero el planificador devuelve `closeout_complete: true` y `next_action: null`. Se conserva la [salida completa](../lean/docs/generated/checks/paper-contribution-check-full.txt). Este wrapper no se presenta como aprobado; el check `--fast` exigido por el curso y el validador canónico sí pasaron.

El flujo utilizó GPT-5.6 Sol, esfuerzo `xhigh`. Las interrupciones por cuota y los arreglos previos de anclas/esquemas son historia del proceso. Los juicios válidos se conservaron durante las continuaciones.

El primer adversario final emitió FAIL F-01: la interfaz no representaba el costo laboral separable exacto del Supuesto 2. Se corrigió la premisa en Lean, sin cambiar el paper fuente, y se repitieron las dos revisiones afectadas sobre la superficie sucesora. La carpeta conserva el hallazgo y sus registros; la aceptación indicada arriba requiere además la nueva auditoría final y el validador canónico, no solo esas dos revisiones.

El alcance es la proposición condicional local del paper. Regularidad y concavidad de toda la HJB, existencia del GE y precisión global de las simulaciones quedan fuera de esa prueba. Los supuestos sobre el valor marginal y el tiempo holgado se declaran donde se usan.

Para reproducir Lean se necesita el proyecto AppliedModelingLib y sus dependencias, con el paper registrado. `lean/` conserva los nombres internos y rutas de esa contribución; no es un proyecto Lake independiente. `code/verify.py` comprueba la identidad de los archivos y recibos retenidos, no ejecuta una nueva auditoría Lean.

Los campos de resumen humano en el estado generado pueden conservar instrucciones de borrador. No se editó esa copia para simular una aprobación: la credencial técnica es el grafo aceptado señalado por el recibo, y la revisión humana permanece pendiente.
