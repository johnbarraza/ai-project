# Veredictos del autor sobre afirmaciones de IA

Registro de la revisión personal de John Barraza. Solo se anota lo que el autor declaró haber comprobado.

## Esquinas y tope de horas vinculante (hoja 10.4 de la guía y caja KKT de la hoja manuscrita a)

- **Qué afirmó la IA:** con `l_s = 0` se cumple `Va R_s - lambda_H <= 0`; y `l_F + l_I = H` implica `lambda_H` libre en signo.
- **Mi veredicto:** acepto la condición de esquina; rechazo la segunda línea tal como estaba escrita.
- **Por qué:** en `l_s = 0` el costo marginal de horas es cero, así que la derivada del lagrangiano es `Va R_s - lambda_H`; si fuera positiva convendría trabajar algo, por eso debe ser `<= 0` (no estricta). Bajo el tope `l_F + l_I <= H` del paper, `lambda_H >= 0` también cuando el tope se alcanza; `lambda_H` libre en signo solo corresponde a un modelo que impone la igualdad.
- **Cómo lo comprobé:** revisé la derivada en el extremo `l_s = 0` y las condiciones KKT (factibilidad, `lambda_H >= 0`, complementariedad) en el caso vinculante. Las correcciones están en [errata-02.md](../hand/errata-02.md), puntos 1 y 3; la hoja manuscrita aún no las incorpora.

## Calibración histórica y tope de horas

- **Qué afirmó la IA:** el tope no explica la calibración histórica, porque la masa en el tope fue cero y las horas máximas fueron 0,749 con H = 1.
- **Mi veredicto:** acepto.
- **Cómo lo comprobé:** vi en la tabla de calibración que la masa en el tope es 0 y el máximo de horas es 0,749.

## Correcciones de la hoja original y cociente con h

- **Qué afirmó la IA:** mi hoja original tenía dos errores: el subíndice del denominador y la potencia de Va contada dos veces sin los niveles psi.
- **Mi veredicto:** acepto.
- **Cómo lo comprobé:** rehice el cociente y me dio `h Va^(phi_I - phi_F)`.

## Signo estricto y alcance de Lean

- **Qué afirmó la IA:** el signo estricto necesita `Vaa < 0` y `phi_I != phi_F`; Lean prueba la proposición bajo esos supuestos, pero no prueba que `Vaa < 0` se cumpla en el modelo.
- **Mi veredicto:** acepto.
- **Cómo lo comprobé:** leí la tabla de Lean en el apéndice; `Vaa < 0` es un supuesto.

## Residuo, curvatura de grilla y existencia global

- **Qué afirmó la IA:** un residuo pequeño y la curvatura en la grilla no prueban existencia global.
- **Mi veredicto:** acepto.
- **Cómo lo comprobé:** la grilla solo revisa puntos discretos con precios dados.
