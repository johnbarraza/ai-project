# Checklist del tema

La propuesta tiene 4 páginas (11 pt, una columna, margen de una pulgada). El deck tiene 42 páginas: 18 slides de contenido (incluye portada y estructura), 5 separadores principales, un separador ANEXOS, un índice y 17 anexos.

## Los cinco puntos del issue, en orden

| Punto del issue | Propuesta | Slides | Estado |
|---|---|---|---|
| 1. Pregunta y track | §1 y figura 1 | 4–5 | Dato del INEI y la pregunta (el ejemplo se dice oralmente) |
| 2. Baseline y supuesto que cambio | §2 | 7–13 | Aiyagari; supuesto que cambio: dos sectores con horas endógenas (el modelo de dos sectores); agentes, timing, hogar, barrera y prima de deuda; perfil de informalidad por z regenerado en Python; sensibilidad de la igualdad de elasticidades. Variables, firmas, equilibrio, momentos y formas de κ en anexos A2, A4, A5, A9 y A12 |
| 3. Resultado esperado (FOC y conjetura) | §3 | 15–18 | FOC, conjetura con condiciones y dos gráficos; la brecha V3, en el anexo A11 |
| 4. Brecha en la literatura (por qué no está resuelto) | §4 y `literature-check.md` | 20 | **Parcial:** faltan los trabajos que citan a Galindo y las elasticidades |
| 5. Plan y riesgos | §5 | 22–23 | Demostrar, simular en equilibrio general, Lean, estimar φ_I; plan B |

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
| 12–13 | Tesis en equilibrio y sensibilidad | 1.8 |
| 14–18 | FOC, conjetura y gráficos | 3.3 |
| 19–20 | Literatura | 1.0 |
| 21–23 | Plan y cierre | 1.0 |
| | **Total sin interrupciones** | **13.6** |

Son unos 13.6 minutos para un bloque de 20 con preguntas, y el profe interrumpe. Si vas tarde:
- Salta las slides 16 (gráfico de la FOC) y 18 (fracción informal por activos).

Las preguntas sobre esas slides se responden con los anexos.

## Reproducción

```powershell
python code/verify.py
cd proposal; latexmk -pdf proposal.tex; cd ..
cd slides;   latexmk -pdf topic.tex;    cd ..
```

## Revisión elegida por John: una figura por mensaje

**Pregunta actualizada por elección A de John:** ¿cuándo influye la riqueza en el reparto de horas entre formal e informal, para una misma productividad? Sustituye el encuadre de amortiguación de choques. La slide 23 distingue elasticidades iguales y distintas, incluidos ambos signos. Se retiraron el bloque "Una respuesta no obvia" y la asociación con cuenta propia sin jornada fija. Modelo y resultados numéricos conservados.

- Slide 9: el hogar conoce el estado y la ley de productividad, no el choque futuro; ahorro y riesgo exógeno mueven estados distintos.
- Slide 12: perfil de informalidad por z grande, generado por verify.py; comparación estacionaria entre productividades.
- Slide 13: motivo de la sensibilidad, qué cambia y qué se mantiene fijo.
- Slide 23: resultado de composición de horas a z fijo; respuesta al choque como pregunta adicional.
- Anexo A16: figura histórica S(r) y demanda de capital, con acceso desde la slide 12 y el índice.
- Referencia de exposición leída: Galindo, PPT octubre de 2023, alcance/estrategia/modelo/solución; manuscrito pp. 4 a 9 y 30. No se le atribuye evidencia de phi_I mayor que phi_F.

## Última revisión de John: definición, puente y menor densidad

- z definido como productividad laboral individual en la pregunta y el guion, distinguiéndolo de ingreso en Achdou/Moll y Galindo.
- Puente explícito entre el dato por gasto y la comparación por activos, sin atribuir identificación causal al gráfico.
- Conjetura principal reducida por elección A a una ecuación y una frase; detalle conservado en A17.
- Página 24: solo ANEXOS, sin cabecera ni pie. Índice en página 25, A16 en 41 y A17 en 42.
