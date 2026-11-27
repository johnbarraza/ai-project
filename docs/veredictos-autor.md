# Veredictos del autor sobre afirmaciones de IA

Registro de la revisión personal de John Barraza. Solo se anota lo que el autor declaró haber comprobado.

## Esquinas y tope de horas vinculante (hoja 10.4 de la guía y caja KKT de la hoja manuscrita a)

- **Qué afirmó la IA:** con `l_s = 0` se cumple `Va R_s - lambda_H <= 0`; y `l_F + l_I = H` implica `lambda_H` libre en signo.
- **Mi veredicto:** acepto la condición de esquina; rechazo la segunda línea tal como estaba escrita.
- **Por qué:** en `l_s = 0` el costo marginal de horas es cero, así que la derivada del lagrangiano es `Va R_s - lambda_H`; si fuera positiva convendría trabajar algo, por eso debe ser `<= 0` (no estricta). Bajo el tope `l_F + l_I <= H` del paper, `lambda_H >= 0` también cuando el tope se alcanza; `lambda_H` libre en signo solo corresponde a un modelo que impone la igualdad.
- **Cómo lo comprobé:** revisé la derivada en el extremo `l_s = 0` y las condiciones KKT (factibilidad, `lambda_H >= 0`, complementariedad) en el caso vinculante. Corregí mi hoja en consecuencia ([observaciones](../hand/errata-02.md), puntos 3 y 1).

## Pendientes

Veredictos personales sobre: calibración histórica del tope, correcciones de la hoja original y cociente con h, alcance de Lean y del signo estricto, y evidencia numérica frente a existencia global.
