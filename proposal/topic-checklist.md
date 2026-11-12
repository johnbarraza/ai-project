# Checklist del tema

La propuesta tiene 4 páginas (11 pt, una columna, margen de una pulgada). El deck tiene 41 páginas: 17 slides de contenido (incluye portada y estructura), 5 separadores principales, un separador ANEXOS, un índice y 17 anexos.

## Los cinco puntos del issue, en orden

| Punto del issue | Propuesta | Slides | Estado |
|---|---|---|---|
| 1. Pregunta y track | §1 y figura 1 | 4–5 | Dato del INEI y la pregunta (el ejemplo se dice oralmente) |
| 2. Baseline y supuesto que cambio | §2 | 7–13 | Aiyagari; supuesto que cambio: dos sectores con horas endógenas (el modelo de dos sectores); agentes, timing, hogar, barrera y prima de deuda; perfil de informalidad por z regenerado en Python; sensibilidad de la igualdad de elasticidades. Variables, firmas, equilibrio, momentos y formas de κ en anexos A2, A4, A5, A9 y A12 |
| 3. Resultado esperado (FOC y conjetura) | §3 | 15–17 | FOC, conjetura en palabras y un gráfico; fórmula y condiciones completas en A17; la brecha V3, en el anexo A11 |
| 4. Brecha en la literatura (por qué no está resuelto) | §4 y `literature-check.md` | 19 | **Parcial:** faltan los trabajos que citan a Galindo y las elasticidades |
| 5. Plan y riesgos | §5 | 21–22 | Demostrar, simular en equilibrio general y Lean; riesgo y alternativa; identificación empírica pendiente |

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

| Slides | Contenido | Tiempo |
|---|---|---:|
| 1–2 | Portada y estructura | 0:20 |
| 3–5 | Dato y pregunta | 1:40 |
| 6–9 | Baseline, agentes y timing | 2:20 |
| 10–11 | Hogar, barrera y prima de deuda | 1:40 |
| 12–13 | Modelo de dos sectores y sensibilidad | 1:40 |
| 14–17 | FOC, conjetura y gráfico por activos | 3:10 |
| 18–19 | Literatura | 1:10 |
| 20–22 | Plan y cierre | 1:15 |
| | **Total sin interrupciones** | **13:15** |

Son unos 13 minutos para un bloque de 20 con preguntas. Si vas tarde:
- Salta la slide 17 (fracción informal por activos); conserva la FOC (15) y la conjetura (16).

Las preguntas sobre esas slides se responden con los anexos.

## Reproducción

```powershell
python code/verify.py
cd proposal; latexmk -pdf proposal.tex; cd ..
cd slides;   latexmk -pdf topic.tex;    cd ..
```

## Revisión elegida por John: una figura por mensaje

**Pregunta actualizada por elección A de John:** ¿cuándo influye la riqueza en el reparto de horas entre formal e informal, para una misma productividad? Sustituye el encuadre de amortiguación de choques. La slide 22 distingue elasticidades iguales y distintas, incluidos ambos signos. Se retiraron el bloque "Una respuesta no obvia" y la asociación con cuenta propia sin jornada fija. Modelo y resultados numéricos conservados.

- Slide 9: el hogar conoce el estado y la ley de productividad, no el choque futuro; ahorro y riesgo exógeno mueven estados distintos.
- Slide 12: perfil de informalidad por z grande, generado por verify.py; comparación estacionaria entre productividades.
- Slide 13: motivo de la sensibilidad, qué cambia y qué se mantiene fijo.
- Slide 22: resultado de composición de horas a z fijo; respuesta al choque como pregunta adicional.
- Anexo A16: figura histórica S(r) y demanda de capital, con acceso desde la slide 12 y el índice.
- Referencia de exposición leída: Galindo, PPT octubre de 2023, alcance/estrategia/modelo/solución; manuscrito pp. 4 a 9 y 30. No se le atribuye evidencia de phi_I mayor que phi_F.

## Última revisión de John: definición, puente y menor densidad

- z definido como productividad laboral individual en la pregunta y el guion, distinguiéndolo de ingreso en Achdou/Moll y Galindo.
- Puente explícito entre el dato por gasto y la comparación por activos, sin atribuir identificación causal al gráfico.
- Conjetura principal en palabras por elección A de D34; fórmula y condiciones conservadas en A17.
- Página 23: solo ANEXOS, sin cabecera ni pie. Índice en página 24, A16 en 40 y A17 en 41.

La explicación gráfica BMg/CMg se eliminó por pedido de John (D33); la FOC conecta directamente con la conjetura.

D34: plan breve sin promesa de estimación por educación ni cota del GE; título del gráfico por activos explícito sobre el sentido de la relación.
