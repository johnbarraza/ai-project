# Ahorro, flexibilidad de horas e informalidad en el Perú

**John Svante Barraza Ratachi, AI and Economic Modeling, UP 2026-II, Track B**
Revisión de cierre del paper final: 2026-11-26. [Estado de requisitos y pendientes](docs/entrega-paper.md).

**Pregunta.** ¿Cuándo influye la riqueza en el reparto de horas entre formal e informal, a igual productividad?

**Modelo macroeconómico.** Hogares con activos y productividad heterogéneos eligen ahorro, consumo y horas. Dos firmas demandan capital y trabajo; la distribución estacionaria agrega esas decisiones. La tasa de interés y el precio informal deben cerrar activos y bienes. El baseline es Aiyagari; se estudia un modelo de dos sectores y su sensibilidad de elasticidades.

**Resultado condicional.** Con retornos positivos, costos laborales separables y parámetros positivos, activos y horas interiores, tiempo holgado y valor marginal de activos positivo y diferenciable, la derivada de la fracción informal es `sI(1−sI)(phiI−phiF)Vaa/Va`. Si `Vaa<0`, más activos reducen esa fracción cuando `phiI>phiF`; con elasticidad común el canal directo se cancela. Una relación agregada también depende de la distribución de productividad.

| Material | Estado y enlace |
|---|---|
| Presentación final | [PDF](slides/final.pdf), [LaTeX](slides/final.tex): modelo, proposición, simulaciones, Lean e IA, con anexos de consulta |
| Manuscrito | [PDF](paper/paper.pdf), [LaTeX](paper/paper.tex), [bibliografía](paper/references.bib): 13 páginas de cuerpo; GE y contrastes de tiempo incorporados; derivaciones manuscritas completas pendientes |
| Simulaciones | [Verificador](code/verify.py): PE, D73 y 23 GE guardados. [Auditoría MATLAB del26nov](docs/concavidad-equilibrio.md): curvatura negativa y mercados verificados; figura adicional y límites teóricos |
| Lean propio | [Estado y recibos](docs/estado-lean.md): carpeta oficial íntegra, proposición probada y cierre validado; revisión humana pendiente. Prototipo preservado aparte |
| Derivación a mano | [Hoja original y guías](hand/README.md): una página original con errata; guías laboral y macro disponibles; faltan las demás derivaciones personales |
| Primera entrega | [Propuesta](proposal/proposal.pdf), [tema](slides/topic.pdf), conservados |
| Colaboración con IA | [Registro](prompts.md), con enlace a la versión cruda; veredictos y límites en el paper |

**Reproducir:** instalar `code/requirements.txt` y ejecutar `python code/verify.py`. Compilar desde `paper/` con `pdflatex paper.tex`, `bibtex paper`, dos pasadas de `pdflatex`; desde `slides/`, dos pasadas de `pdflatex final.tex`. Lean tiene instrucciones separadas en su README.

Personas/gasto y horas/activos son medidas distintas. Los GE son estacionarios, sin IRF ni interpretación causal. Las elasticidades son una sensibilidad ilustrativa; [evidencia](docs/evidencia-elasticidades.md). La precisión por refinamiento y los teoremas globales de concavidad/existencia siguen abiertos.

Entrega completa: **26nov, 22:00 Lima**, según el [issue #7](https://github.com/alexanderquispe/AI-Econ-Modeling/issues/7). [Revisión de todos los requisitos](docs/revision-requisitos-final.md). Lean cerró por [PR #17](https://github.com/johnbarraza/ai-project/pull/17), sobre la [fuente matemática 6777134](https://github.com/johnbarraza/ai-project/blob/6777134ba22670ebd53b65d21a48d719c09b3fbd/paper/paper.pdf). El fallo del wrapper adicional y los pendientes personales están documentados.
