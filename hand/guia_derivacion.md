# Guía para tu derivación manuscrita

Esta guía tipografiada prepara la defensa. **No es el apéndice manuscrito del estudiante ni una constancia de que ya lo escribió.** El profesor pide ver tu derivación real y que puedas explicar cada paso. Usa papel o tableta, escribe con tus palabras y conserva fotos/escaneos legibles en esta carpeta.

## Hoja 1: problema, condiciones y FOC

1. Define `a` (activos), `z` (productividad fija), `Va` (valor marginal de activos), `RF/RI` (retornos por hora), `psi` (nivel de costo) y `phi` (elasticidad).
2. Escribe el bloque laboral: `H = Va(RF*lF + RI*lI) − sum_s psi_s*l_s^(1+1/phi_s)/(1+1/phi_s)`.
3. Declara `Va > 0`, `Rs > 0`, `psi_s > 0`, `phi_s > 0`, `l_s > 0` y tiempo holgado. Explica por qué se puede derivar en ese régimen.
4. Deriva término a término. Para `p = 1+1/phi_s`, usa `d(l_s^p)/dl_s = p*l_s^(p−1)`. Multiplica por `psi_s/p` y cancela `p`.
5. Obtén `Va*Rs − psi_s*l_s^(1/phi_s) = 0`.
6. Divide por `psi_s > 0`. Eleva a `phi_s > 0` usando una base positiva. Resulta `l_s = (Va*Rs/psi_s)^phi_s`.
7. Deriva de nuevo: `−(psi_s/phi_s)*l_s^(1/phi_s−1) < 0`. Explica que es concavidad del bloque de horas, no una prueba de concavidad de toda la HJB.

## Hoja 2: cociente y regla de la cadena

1. Define `q = lI/lF > 0`. Divide las dos políticas sin saltar el denominador.
2. Separa `q = K*Va^(phiI−phiF)`, con `K = (RI/psiI)^phiI/(RF/psiF)^phiF > 0`.
3. Escribe qué mantienes fijo: `z`, precios, retornos efectivos y parámetros. Explica por qué `K` no depende de `a` en esta comparación.
4. Usa el logaritmo solo después de verificar positividad: `ln q = ln K + (phiI−phiF)*ln Va`.
5. Deriva respecto a `a`: `(q'/q) = (phiI−phiF)*(Vaa/Va)`.
6. Multiplica por `q`: `q' = q*(phiI−phiF)*Vaa/Va`.
7. Define `s = q/(1+q)`. Aplica cociente: `s' = [q'(1+q) − q*q']/(1+q)^2 = q'/(1+q)^2`.
8. Sustituye `q'`. Comprueba por separado `s*(1−s) = q/(1+q)^2`.
9. Obtén `s' = s*(1−s)*(phiI−phiF)*Vaa/Va`.
10. Escribe que `0 < s < 1` y `Va > 0`. Solo entonces aplica `Vaa < 0` para los tres signos. Si `phiI = phiF`, el canal se anula aunque las horas totales cambien.

## Hoja 3: dónde se revisó a la IA

1. Añade al objetivo `lambdaH*(Hbar−lF−lI)`.
2. Deriva ambas FOC: `Va*Rs = psi_s*l_s^(1/phi_s) + lambdaH`.
3. Escribe `lambdaH >= 0`, tiempo factible y complementariedad `lambdaH*(Hbar−lF−lI)=0`.
4. Si el tiempo está holgado, demuestra que `lambdaH=0`. Si está activo, explica por qué ya no puedes usar sin cambios el cociente interior anterior.
5. Anota el diagnóstico reproducido del caso histórico: masa en el tope = 0; máximo de horas ≈ 0,749 con `Hbar=1`. Fuente: `code/output/final_verification.json`.
6. Redacta tu propio veredicto: el mecanismo que requiere un tope activo no opera en esa calibración. No basta que una derivación sea algebraicamente válida para que explique las cifras.

Para la exposición se necesita al menos la foto de la hoja pertinente en pantalla. Para el paper se requieren **todas** las derivaciones, incluidas firmas, agregación y contabilidad que aparezcan en el manuscrito. Esta guía cubre el núcleo de la proposición y el caso de revisión de IA; no declara completo el apéndice final.

Nombres sugeridos, cuando existan archivos reales: `01-foc-hogar.jpg`, `02-composicion.jpg`, `03-veredicto-tiempo.jpg`. No hay fotos con esos nombres en la versión de preparación.
