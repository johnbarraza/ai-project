# Checklist del tema

La propuesta tiene 4 páginas (11 pt, una columna, margen de una pulgada). El deck tiene 38 páginas: 17 slides de contenido (incluye portada y estructura), 5 separadores, un índice de anexos con enlaces y 15 anexos.

## Los cinco puntos del issue, en orden

| Punto del issue | Propuesta | Slides | Estado |
|---|---|---|---|
| 1. Pregunta y track | §1 y figura 1 | 4–5 | Dato del INEI y la pregunta (el ejemplo se dice oralmente) |
| 2. Baseline y supuesto que cambio | §2 | 7–12 | Aiyagari; supuesto que cambio: dos sectores con horas endógenas (mi tesis); agentes, timing, hogar, barrera y prima de deuda; sensibilidad φ_I > φ_F. Variables, firmas, equilibrio, momentos y formas de κ en anexos A2, A4, A5, A9 y A12 |
| 3. Resultado esperado (FOC y conjetura) | §3 | 14–17 | FOC, conjetura con condiciones y dos gráficos; la brecha V3, en el anexo A11 |
| 4. Brecha en la literatura (por qué no está resuelto) | §4 y `literature-check.md` | 19 | **Parcial:** faltan los trabajos que citan a Galindo y las elasticidades |
| 5. Plan y riesgos | §5 | 21–22 | Demostrar, simular en equilibrio general, Lean, estimar φ_I; plan B |

## Requisitos de forma

- [x] Link del repositorio en la portada de las slides y de la propuesta.
- [x] Sin animaciones ni capturas de papers; las ecuaciones están en LaTeX.
- [x] Sin recuadros "Replace" de la plantilla en `proposal/` ni en `slides/topic.*`.
- [x] Todo número del modelo sale de `code/output/topic_numbers.tex`, generado por `verify.py`.
- [x] Figuras con la letra de las slides; mi modelo en gris discontinuo y la extensión en color sólido.
- [x] Cada figura lleva una nota: qué grafica, si es calibrada o ilustrativa y si es equilibrio parcial.
- [x] Índice de anexos con enlaces, y enlaces a cada parte en la barra superior.
- [x] Separadores con banda de color; pie de página con color.
- [x] Las slides no mencionan archivos de código; la trazabilidad está en `code/`.
- [ ] Derivación a mano de la FOC y de ∂s_I/∂V_a (`hand/`). Le toca a John.
- [ ] Ensayo con cronómetro (unos 14 min).

## Minutos orientativos

| Slides | Contenido | Min |
|---|---|---:|
| 1–2 | Portada y estructura | 0.5 |
| 3–5 | Dato y pregunta | 2.0 |
| 6–9 | Baseline, agentes y timing | 2.0 |
| 10–11 | Hogar, barrera y prima de deuda | 2.0 |
| 12 | Sensibilidad | 1.0 |
| 13–17 | FOC, conjetura y gráficos | 3.3 |
| 18–19 | Literatura | 1.0 |
| 20–22 | Plan y cierre | 1.0 |
| | **Total sin interrupciones** | **12.8** |

Son unos 12.8 minutos para un bloque de 20 con preguntas, y el profe interrumpe. Si vas tarde:
- Salta las slides 15 (gráfico de la FOC) y 17 (fracción informal por activos).

Las preguntas sobre esas slides se responden con los anexos.

## Reproducción

```powershell
python code/verify.py
cd proposal; latexmk -pdf proposal.tex; cd ..
cd slides;   latexmk -pdf topic.tex;    cd ..
```
