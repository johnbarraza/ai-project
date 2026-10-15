# Instrucciones para agentes (Codex / Claude): `ai-project` de John Barraza

Curso **AI and Economic Modeling** (UP 2026-II, prof. Alexander Quispe). Responde en español.
Estilo solicitado por John: no usar rayas largas para incisos. Usar comas, paréntesis o frases separadas.
Nombres elegidos por John (D29, actualizados en D30): en la presentación, propuesta, figuras y guion usar **Modelo de dos sectores** y **Sensibilidad**, evitando “mi tesis”. Mantener **Baseline: Aiyagari**. En la slide de barrera y prima de deuda, solo definiciones breves; valores y fuentes en A8. Conservar la procedencia original en registros y archivos de datos.
Reglas oficiales: [issue #7](https://github.com/alexanderquispe/AI-Econ-Modeling/issues/7). Si algo de este archivo lo contradice, gana el issue.

> **Lee primero:**
> - `E:\github\modeling_jb\plan_ai_project.md`: estado, flujo, resultados verificados y la sección "▶ Dónde nos quedamos".
> - `E:\github\modeling_jb\decisiones_ai_project.md`: cada decisión con su razonamiento y evidencia.
> - La §12 del plan tiene **todas las rutas**, incluido `HA-IE2025`.

## Decisión de alcance (A2, D14/D17; margen intensivo)

**Track B: el modelo económico detrás de mi tesis**, *Informalidad y distribución de riqueza en Perú*. Solo se pone mi nombre y "Track B": no se mencionan coautores ni asesor.

- **Pregunta elegida por John (D26):** ¿cuándo influye la riqueza en el reparto de horas entre formal e informal, para una misma productividad? Título: *Ahorro, flexibilidad de horas e informalidad en el Perú*. Es una comparación condicional por activos a $z$ fijo. El riesgo de productividad del modelo sigue siendo idiosincrático; no se presenta una respuesta a un choque ni una comparación de bienestar.
- **Genealogía:** Aiyagari/Huggett en tiempo continuo (Achdou et al., 2022), de un sector, está anidado en el modelo de tesis. Extenderlo a dos sectores no equivale a introducir estados laborales discretos.
- **Terminología corregida por John:** reservar **baseline** para Aiyagari, una firma y un bien; incluirlo al inicio del deck. A2 se compara con **mi modelo de dos sectores**, con elasticidad común $\phi_F=\phi_I=0.38$. Hogares con riqueza $a$ y productividad $z$ (OU exógena) reparten horas formales e informales, con $\ell_F+\ell_I\le\bar H$. Hay dos firmas y bienes (CES), barrera formal $\kappa(z)$ y prima de deuda $\chi(z)$. Los nombres históricos de archivos y variables de código pueden conservar `baseline` para mantener trazabilidad.
- **Supuesto que cambia (D14):** $\phi_I>\phi_F$: las horas informales responden más a $V_a\equiv\partial_a v$. El rango de $\phi_I$ es ilustrativo, no una estimación; su justificación en fuentes sigue pendiente (D15).
- **Encuadre en slides y propuesta (John, 15 oct):** el supuesto que cambia frente a Aiyagari es el modelo de la tesis (dos sectores con horas endógenas, dos firmas y dos bienes). $\phi_I>\phi_F$ se presenta como **sensibilidad** (slide 12, "Sensibilidad: horas informales más flexibles"); sigue siendo la condición de la conjetura.
- **Núcleo A2:** bloque laboral del hogar dado $V_a>0$, salarios netos/efectivos positivos, $\phi_s,\psi_s>0$ y restricción de tiempo no vinculante. Las FOC implican $\partial\ln(\ell_I/\ell_F)/\partial\ln V_a=\phi_I-\phi_F$ y $\partial s_I/\partial V_a=s_I(1-s_I)(\phi_I-\phi_F)/V_a$. Si $V_a$ decrece con $a$, $s_I$ decrece con la riqueza a productividad fija.
- **Simulación (D17):** equilibrio parcial con $V_a$, distribución $g$ y precios del baseline fijos; recalibración conjunta de $\psi_I$ para mantener M1 · Horas informales y $\kappa_{z1}$ para mantener M3 · Brecha de formalidad por productividad. El aumento de V3 · Brecha Q1−Q5 es una comprobación numérica en el rango estudiado, no un teorema de equilibrio general.
- **R1–R3:** antecedentes del diagnóstico, no el núcleo actual. Nadie alcanza el tope en el baseline; R3 no opera en esa calibración.
- **Supuesto a declarar:** "más pobre ⇔ $\partial_a v$ más alto" requiere $v$ cóncava en $a$. Se verifica numéricamente, no se demuestra.
- **No crea tipos ex ante:** todos los hogares tienen los mismos $\phi_F,\phi_I$ (propiedades de la actividad, como $\psi_F\neq\psi_I$); la heterogeneidad sigue viniendo solo de $(a,z)$. En Galindo et al. (2024) formal e informal son tipos exógenos que cambian al azar (Poisson de dos estados), cada uno con su aversión al riesgo; nadie elige.
- **En las slides no se usa la etiqueta "A2"** (choca con "Anexo A2" y el público no la entiende): se dice "horas informales más flexibles, $\phi_I>\phi_F$". En el código y en las decisiones se conserva A2.
- **Interpretación aclarada con John (15 oct):** el hogar conoce su $z$ actual y la ley de evolución, no la realización futura. La figura por $z$ compara productividades dentro de una misma solución estacionaria, no fechas. La conjetura a $z$ fijo describe composición de horas por riqueza; no demuestra una mayor respuesta amortiguadora a una caída de $z$. La sensibilidad pregunta cuánto depende el resultado de la igualdad de elasticidades, sin atribuir ese orden a Galindo ni a una estimación sectorial.
- **Forma de $\kappa(z)$:** lineal en la tesis; `verify.py` prueba cuadrática y raíz recalibradas (V3 casi igual; $\kappa$ depende solo de $z$, no crea pendiente por riqueza). Un costo fijo de entrada es margen extensivo: fuera del alcance.
- **GE con $\phi_I\neq\phi_F$ (en curso, 15 oct):** copia parcheada del solver en `_contexto/matlab_ge/` (local; `model_main.m` con `HA_IE_FRISCH_I`). Corridas en `_contexto/matlab_ge/outputs/stationary/ge_*`, logs en `logs/`. La primera (`ge_reg_phi038`) debe reproducir `test_AI098_cierre`. `HA-IE2025` no se toca.
- **Fuera del alcance actual:** margen extensivo F/I/N y shock MIT. Los quintiles del INEI (Cuadro 7.5) son probablemente de ingreso (el Cuadro 6.41 del mismo informe dice "Quintiles de ingreso"); no son de riqueza.

## Cómo presentarlo para que se defienda

- **Guía con reglas, críticas reales del profe y recetas:** `E:\github\modeling_jb\guia_presentacion.md`. Aplica la receta **macro (5.5)** y la **dinámica (5.7)**:
  - mapa de agentes y línea de tiempo antes de las ecuaciones;
  - la lista de variables endógenas y qué precio se ajusta ($r$, $p_I$);
  - las condiciones de agregación;
  - una tabla de parámetros con rol y fuente.
- **El profe premia lo simple.** El hogar y las transiciones laborales van al frente. La maquinaria HJB/KFE va en una línea más el apéndice.
- **Orden solicitado por John:** mostrar por separado el problema y las FOC del hogar y de las firmas, y después conectarlos con los mercados. Usar $R_F,R_I$ para los retornos del hogar, distintos de los salarios brutos $w_F,w_I$ de las firmas. La barrera total es $\kappa(z)\ell_F$, una cuña por hora, no un costo fijo de entrada.
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
   - Las figuras usan la letra de las slides (`code/fonts/`). Mi modelo va en gris discontinuo y la extensión en color sólido. Los diagramas se dibujan en TikZ dentro de `topic.tex`.
   - Para el tema solo se entrega el PDF de Beamer. El HTML (Quarto/Reveal) se descartó y queda para la final.
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
