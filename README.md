# Ahorro, flexibilidad de horas e informalidad en el Perú

**John Svante Barraza Ratachi · AI and Economic Modeling · UP 2026-II · Track B**
Versión de trabajo del 12 de noviembre de 2026.

**Pregunta.** ¿Cuándo influye la riqueza en el reparto de horas entre formal e informal, a igual productividad?

**Modelo macroeconómico.** Hogares con activos y productividad heterogéneos eligen ahorro, consumo y horas. Dos firmas demandan capital y trabajo; la distribución estacionaria agrega esas decisiones. La tasa de interés y el precio informal deben cerrar activos y bienes. El baseline es Aiyagari; se estudia un modelo de dos sectores y su sensibilidad de elasticidades.

**Resultado condicional.** Con retornos y costos positivos, horas interiores, tiempo holgado y valor marginal de activos positivo y diferenciable, la derivada de la fracción informal es `sI(1−sI)(phiI−phiF)Vaa/Va`. Si `Vaa<0`, más activos reducen esa fracción cuando `phiI>phiF`; con elasticidad común el canal directo se cancela. No se prueba aquí concavidad global de la HJB ni existencia del GE. Una relación agregada también depende de la distribución de productividad.

| Material | Estado y enlace |
|---|---|
| Presentación final | [PDF](slides/final.pdf) · [LaTeX](slides/final.tex): 24 láminas principales y 8 de consulta, con distribución, circuito GE, precios y capital |
| Manuscrito | [PDF](paper/paper.pdf) · [LaTeX](paper/paper.tex) · [bibliografía](paper/references.bib): borrador propio, proposición y prueba completa |
| Simulaciones | [Verificador](code/verify.py): PE reproducido y diagnósticos GE D73; [repetición MATLAB del 12nov](docs/replicacion-matlab-final.md) de dos casos, auditada |
| Lean propio | [Código y alcance](lean/README.md): derivada y signos comprobados localmente, sin `sorry`; flujo oficial sobre paper publicado en commit pendiente |
| Manuscrito personal | [Guía](hand/guia_derivacion.md): fotos y revisión del estudiante pendientes; la guía no las sustituye |
| Preparación oral | [Guion de 30 minutos](slides/final-notes.md) · [cumplimiento](docs/final-cumplimiento.md) |
| Primera entrega | [Propuesta](proposal/proposal.pdf) · [tema](slides/topic.pdf), conservados |
| Colaboración con IA | [Registro crudo](prompts.md); veredictos y límites en el paper |

**Reproducir:** instalar `code/requirements.txt` y ejecutar `python code/verify.py`. Compilar desde `paper/` con `pdflatex paper.tex`, `bibtex paper`, dos pasadas de `pdflatex`; desde `slides/`, dos pasadas de `pdflatex final.tex`. Lean tiene instrucciones separadas en su README.

Los números por personas/gasto y por horas/activos no se tratan como medidas idénticas. Los contrastes D73 son estacionarios, no IRF ni efectos causales. La precisión global sigue pendiente.

Según el [issue #7](https://github.com/alexanderquispe/AI-Econ-Modeling/issues/7), las slides se entregan en main el **12nov, 22:00 Lima**; exposición **13nov, 07:30**; paper completo **26nov, 22:00**. La final se publicó mediante el [PR #5](https://github.com/johnbarraza/ai-project/pull/5), con checks aprobados. El [paper fuente en commit](https://github.com/johnbarraza/ai-project/blob/8e51a872c874f09079ce106068cc065b0a0efbee/paper/paper.pdf) queda fijado para el flujo oficial. Los pendientes científicos permanecen explícitos.
