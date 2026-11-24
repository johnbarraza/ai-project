# Formalización del paper, 24 de noviembre de 2026

La carpeta [lean/](../lean/) copia íntegramente el directorio generado `papers/Barraza26LaborComposition/` de AppliedModelingLib. Se respetó su `.gitignore`, sin forzar fuentes PDF ni archivos ignorados. El prototipo anterior se conserva en [lean-prototype/](../lean-prototype/). El [manifiesto](lean-workflow.json) fija los hashes publicables y los comandos realmente ejecutados.

La fuente vigente es el [paper publicado en 6777134](https://github.com/johnbarraza/ai-project/blob/6777134ba22670ebd53b65d21a48d719c09b3fbd/paper/paper.pdf). El flujo se inició con GPT-5.6 Sol, esfuerzo `xhigh`, como pide el curso. La reparación de interfaz y el inventario independiente de esa fuente avanzaron; el autor y coordinador se detuvieron después por un límite de uso. No se sustituyó esa revisión por una aceptación inventada.

| Evidencia | Resultado y alcance |
|---|---|
| [Check del curso](../lean/contribution-check-fast.txt), `python3 scripts/paper_contribution.py check Barraza26LaborComposition --fast` | Salida 0 el 24 de noviembre. Compilación forzada de `PaperInterface` y control de espacios del diff. No es una credencial de aceptación semántica. |
| [Build adicional](../lean/proof-interface-build.txt), `lake build +Barraza26LaborComposition.ProofInterface` | Salida 0. Incluye el endpoint `Barraza26LaborComposition.compositionConditionalHours`, de tipo `compositionConditionalHoursSpec`, y sus dependencias. |
| [Interfaz](../lean/PaperInterface.lean) y [prueba](../lean/ProofInterface.lean) | Un solo Spec y un endpoint para la Proposición 1. Se parte de las FOC de una rama interior, se recuperan las políticas y se prueba la identidad y los signos. No se prueba existencia del GE ni concavidad global. |
| Inventario independiente del paper | Una Proposición y cuatro Supuestos. Los supuestos y la definición de la fracción son prerrequisitos; no añaden resultados numerados. |
| Revisión semántica y cierre | **Abiertos.** Falta completar la migración del mapa, revisar independientemente la expansión exacta del Spec y los prerrequisitos, y ejecutar el cierre del protocolo. No existe `FINAL_CLOSURE_RECEIPT.md`. |

Los archivos generados conservan su estado de borrador: el README dice `Not started`, `status.json` contiene campos de plantilla y algunas notas mantienen el pin del 12 de noviembre o localizadores anteriores. No se editó la copia para aparentar un cierre. Esta página y el manifiesto explican el progreso posterior y esas limitaciones. El estado de la Proposición 1 en el apéndice del paper es **abierto**, aunque su endpoint compile.

El preflight no certificante identificó primero dos referencias con el sufijo `Spec` duplicado; se corrigieron solo esas referencias del mapa. Después se detuvo con salida 2: `source anchor 0 quote does not equal the current declared source slice`. Este es el bloqueo técnico inmediato: materializar de nuevo las citas y anclas sobre la fuente del 24 de noviembre. No se emitió un juicio semántico sobre un paquete con citas desactualizadas.

Para continuar se usa el mismo clon de AppliedModelingLib que produjo la carpeta, con sus dependencias y el módulo raíz registrado. La copia en `lean/` no es un proyecto Lake independiente. El prototipo sí tiene instrucciones propias de compilación. `code/verify.py` comprueba la identidad de los archivos y los recibos retenidos; no ejecuta ni certifica una nueva revisión Lean.

El siguiente paso es terminar el mapa y el preflight no certificante, obtener la revisión con contexto aislado y seguir la acción que indique el planificador del protocolo. Después debe reemplazarse íntegramente la copia de `lean/` y actualizarse la única fila del apéndice. Una compilación aprobada no elimina estos pendientes.
