# Errata de la hoja 01

Revisión visual del PDF original el 23nov2026. La hoja se conserva intacta, conforme a la decisión anterior del autor.

1. En la primera razón de horas aparece `ℓI/ℓH`; debe ser `ℓI/ℓF`.
2. Después de establecer tiempo holgado y `λH=0`, la razón debe ser

   `ℓI/ℓF = [(RI/ψI)^φI / (RF/ψF)^φF] · Va^(φI−φF)`.

   La línea original conserva `Va` dentro del cociente de retornos y vuelve a multiplicar por `Va^(φI−φF)`, además de omitir los niveles ψ. Así cuenta dos veces la potencia de Va y no es el paso válido. Se debe sustituir esa línea completa por la expresión anterior antes de definir la constante `h`.

La conclusión de cancelación cuando las elasticidades son iguales es válida bajo las condiciones interiores, usando el cociente corregido. La igualdad de tiempo es otro régimen: su multiplicador no tiene la restricción de signo de KKT ni se puede deducir `λH=0` por holgura.

Esta nota identifica el error; no sustituye la hoja corregida a mano ni atribuye al autor una revisión que aún no ha entregado.
