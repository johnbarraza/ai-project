# Observaciones de revisión a 02-derivaciones-continuacion.pdf

Revisión de la hoja manuscrita del autor. No se modifica el original.

1. a) CPO: el denominador del costo aparece como `1 - 1/phi_s`; debe ser `1 + 1/phi_s`, que se cancela. La línea siguiente ya está correcta.
2. a) Cociente: el lado izquierdo debe ser `l_I / l_F`; en el denominador `Va R_F`, no `Va - R_F`; los niveles llevan subíndice, `psi_F^{phi_F} / psi_I^{phi_I}`.
3. a) Esquina: `l_s = 0` implica `Va R_s - lambda_H <= 0`, es decir `lambda_H >= Va R_s` (no estricta). Bajo el tope `l_F + l_I <= H`, `lambda_H >= 0` aunque el tope se alcance; `lambda_H` libre en signo solo si el modelo impusiera la igualdad.
4. b) Definición de q: debe ser `q = h Va^{phi_I - phi_F}` con `h = (R_I/psi_I)^{phi_I} / (R_F/psi_F)^{phi_F}`. Escribir `(Va R_I)^{phi_I} / (Va R_F)^{phi_F}` y además multiplicar por `Va^{phi_I - phi_F}` cuenta dos veces la potencia de Va. El resultado final `h Va^{phi_I - phi_F}`, la derivada logarítmica y los tres signos son correctos.
5. b) El factor `g` del signo debe definirse: `g = s_I(1 - s_I)/Va > 0`.
6. f) Notación: `(-a)_+ = max{-a, 0}`.
7. g) Explicitar `0 = b int a_dot dmu` por estacionariedad antes de despejar; la última línea equivale a `Y_F = C_F + delta(K_F + K_I) + K + D`, con `C = C_F`.
