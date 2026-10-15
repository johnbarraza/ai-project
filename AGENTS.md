# Instrucciones para agentes (Codex / Claude) — `ai-project` de John Barraza

Curso **AI and Economic Modeling** (UP 2026-II, prof. Alexander Quispe). Responde en español.
Reglas oficiales: [issue #7](https://github.com/alexanderquispe/AI-Econ-Modeling/issues/7). Si algo de este archivo lo contradice, gana el issue.

> **Lee primero:**
> - `E:\github\modeling_jb\plan_ai_project.md`: estado, flujo, resultados verificados y la sección "▶ Dónde nos quedamos".
> - `E:\github\modeling_jb\decisiones_ai_project.md`: cada decisión con su razonamiento y evidencia.
> - La §12 del plan tiene **todas las rutas**, incluido `HA-IE2025`.

## Decisión de alcance (14 oct 2026, D5 y D6 cerradas)

**Track B: el modelo económico detrás de mi tesis**, *Informalidad y distribución de riqueza en Perú*. Solo se pone mi nombre y "Track B": no se mencionan coautores ni asesor.

- **Pregunta (base, a pulir):** ¿para quién funciona el sector informal como **colchón** cuando le va mal: para todos, o solo para los de baja productividad? Es un shock **idiosincrático** de $z$, no agregado: no usar "crisis" ni shock MIT.
- **Baseline:** Aiyagari/Huggett en tiempo continuo (Achdou et al., 2022) con trabajo endógeno y **un solo sector**. Está anidado en mi modelo (teorema `classical_aiyagari_nesting` del Lean viejo). Ahí el único colchón es trabajar más horas.
- **Lo que cambio:** mi modelo de tesis, **solo margen intensivo**. Hogares con riqueza $a$ y productividad $z$ (OU) reparten horas entre formal e informal con $\ell_F+\ell_I\lear H$. Hay barrera formal $\kappa(z)$, prima de deuda $\chi(z)$, dos firmas, dos bienes (CES) y $r$, $p_I$ endógenos. Calibración de la tesis **fija**, sin recalibrar.
- **Núcleo de la presentación:** el bloque laboral del hogar dado $\partial_a v$. Resultados R1–R3 (ver el plan): la informalidad no depende de la riqueza en el interior (R1); el colchón es trabajar más (R2); con horas al tope, el hogar se mueve hacia el sector que paga más en el margen, y **el informal es colchón solo si $w_I^{eff}(z)>w_F^{net}(z)$** (R3).
- **Supuesto a declarar:** "más pobre ⇔ $\partial_a v$ más alto" requiere $v$ cóncava en $a$. Se verifica numéricamente, no se demuestra.
- **Fuera del alcance (va en "plan"):** el margen extensivo (motivado por la brecha V3: 4.4 contra 53 pp), el shock MIT y los contrafactuales de GE ($\kappa=0$, $\chi=0$, horas fijas).

## Cómo presentarlo para que se defienda

- **Guía con reglas, críticas reales del profe y recetas:** `E:\github\modeling_jb\guia_presentacion.md`. Aplica la receta **macro (5.5)** y la **dinámica (5.7)**:
  - mapa de agentes y línea de tiempo antes de las ecuaciones;
  - la lista de variables endógenas y qué precio se ajusta ($r$, $p_I$);
  - las condiciones de agregación;
  - una tabla de parámetros con rol y fuente.
- **El profe premia lo simple.** El hogar y las transiciones laborales van al frente. La maquinaria HJB/KFE va en una línea más el apéndice.
- **Cada símbolo tiene que poder defenderse** con su rol (decisión, endógena, parámetro o shock) y un ejemplo numérico.
- **Habrá preguntas seguras sobre:** por qué $\kappa(z)$ y $\chi(z)$ decrecen en $z$, por qué costo de aceptación 0 (identificación), qué es una intensidad efectiva vs. una tasa de llegada, y equilibrio parcial vs. general.

## Material fuente (local, en `_contexto/`, NO se sube)

| Carpeta | Contenido |
|---|---|
| `01_modelo_base/` | Documento final (`.md` y `.pdf`), anexo matemático (`.tex` y `.pdf`) y README del paquete de replicación |
| `02_margen_extensivo/` | Diseño (HJB/KFE de tres estados), integración GE, validaciones Perú y México, decisión stock-flujo, HANDOFF |
| `03_lean_base/` | La formalización existente del modelo base: 16 teoremas, parcial, hecha con EconCSLib |
| `04_estilo_figuras/` | Gráficos de Moll que sirven de referencia de estilo |

**Origen:** `C:\Users\johnb\Documents\GitHub\HA-IE2025`, que contiene el paquete `aiyagari-2firms-peru`. **No modifiques ese árbol.** No copies microdatos de ENAHO/ENOE ni CSV de `data/`.

## Reglas de trabajo

1. **Rama → PR → merge.** Rama actual: `topic-colchon-informal`. **No hagas commit ni push sin que John lo pida.**
2. **`prompts.md` es crudo:** prompts y respuestas relevantes, pegados tal cual, con lo que John aceptó, corrigió o rechazó.
3. **Números reproducibles:**
   - Las figuras del modelo de este proyecto las genera `code/verify.py`, que falla si una afirmación no se cumple.
   - Las figuras MATLAB del modelo base (`slides/figures/base_model/`) se usan como resultados del baseline, con su procedencia en `PROCEDENCIA.md`.
4. **Lean (paper final):** el issue exige correr el flujo de AppliedModelingLib sobre `paper/paper.pdf` en un commit fijado (GPT-5.6 Sol, `xhigh`). La formalización vieja con EconCSLib es referencia, no entregable.
5. **Herramientas.** Desde `E:\github\modeling_jb` corre:
   - `/armar-ai-project ../ai-project --rapido`: el proceso por fases.
   - `/explicar-expresiones ../ai-project`: la hoja de defensa.
   - `/simular-profe ../ai-project`: la nota estimada.

## Fechas

| Entregable | Merge en `main` | Presentación |
|---|---|---|
| Tema: `proposal/` (2–4 pp.) + `slides/topic` | **jue 15 oct, 22:00** | vie 16 oct, 07:30 (primero; 20 min con preguntas) |
| Final: `slides/final` | jue 12 nov, 22:00 | vie 13 nov, 07:30 (45 min) |
| Paper completo | jue 26 nov, 22:00 | — |
