# Ampliación del paper: texto de revisión

Texto preparado el23nov y utilizado como base para la integración del24nov, tras el pedido de continuar. Conserva la pregunta y la Proposición1 del manuscrito publicado; incorpora GE y contrastes de tiempo sin adoptar otra arquitectura. Las cifras proceden de `code/output/paper_results.json`, generado por `code/verify.py`. El PDF actual ya contiene esa integración; siguen pendientes el cierre Lean y el apéndice manuscrito completo.

## Resumen actualizado propuesto

Estudio cuándo la riqueza modifica el reparto de horas formales e informales a productividad fija, dentro de una economía de agentes heterogéneos con dos sectores y precios endógenos. En una rama laboral interior con tiempo holgado, la derivada de la fracción informal depende de la diferencia entre las elasticidades sectoriales y de la pendiente del valor marginal de los activos. Bajo concavidad local, una elasticidad informal mayor genera una fracción decreciente por activos; con elasticidad común se cancela ese canal directo. El ejercicio parcial y dos protocolos de equilibrio general reproducen el mecanismo, pero muestran que la brecha por activos y el nivel agregado de informalidad responden de manera distinta al reajuste de parámetros. Los contrastes de tiempo delimitan la validez del resultado interior. No se identifican efectos causales ni parámetros sectoriales para Perú, ni se prueba concavidad global o existencia del equilibrio general.

## Incorporación de los GE con elasticidades distintas

La extensión cuantitativa resuelve de nuevo la HJB, la distribución y los mercados. Mantiene una grilla de 400 nodos de activos y 40 de productividad, activos entre −1 y 40 y elasticidad formal de 0,38. La elasticidad informal recorre ocho valores entre 0,38 y 0,70. Cada equilibrio sirve como inicializador del siguiente. Este procedimiento es continuación numérica entre estados estacionarios; no representa una transición temporal de la economía.

Se comparan dos protocolos. En el primero se conservan los niveles de desutilidad y la barrera de referencia. En el segundo se reajustan la desutilidad informal y el nivel de la barrera lineal para recuperar M1 y M3 del equilibrio de referencia de igual grilla. Son objetivos internos: no se vuelven a estimar con microdatos ni se redefine una tasa de personas como una razón de horas. El segundo protocolo incluye los siete valores de elasticidad distintos de la referencia.

Sin reajuste, la brecha V3 pasa de 4,40 a 9,34 puntos porcentuales, mientras que la proporción agregada de horas informales baja de 51,68 % a 30,94 %. Una brecha por activos mayor puede coexistir con menor informalidad agregada. La elasticidad modifica la curvatura, pero sus efectos de nivel dependen de la valoración marginal, los retornos y los parámetros mantenidos.

Con reajuste, M1 y M3 permanecen en sus valores internos de referencia y V3 llega a 10,46 puntos. El nivel de desutilidad informal termina en 6,6438 y el nivel de la barrera en 0,40393. La similitud con la brecha del ejercicio parcial es un resultado de este contraste; no demuestra que un cálculo parcial reproduzca cualquier efecto de equilibrio general.

**Figura propuesta:** [brecha y nivel agregado de informalidad](../code/figures/final/paper_ge_sensitivity.pdf). Eje horizontal: elasticidad informal. Panel izquierdo: diferencia Q1−Q5 de razones de horas informales, en puntos porcentuales; panel derecho: razón agregada de horas informales, en porcentaje. Los quintiles son de activos y reparten fraccionalmente el nodo de corte. No se mezclan con la convención histórica D17 del ejercicio parcial.

## Ajustes macroeconómicos

La distribución estacionaria agrega el ahorro y las horas y, junto con las demandas de factores, determina los precios compatibles con los mercados. La comparación de elasticidades debe examinar ese cierre además del perfil individual. Con reajuste y elasticidad informal de 0,70, la tasa de interés cambia −1,34 puntos básicos y el capital aumenta 0,080 % respecto de la referencia de la misma grilla. Sin reajuste, el cambio de interés es pequeño y positivo, mientras que el capital disminuye aproximadamente 0,370 %.

**Figura propuesta:** [interés y capital](../code/figures/final/paper_ge_aggregates.pdf). Los cambios se calculan respecto del mismo equilibrio de referencia. Son diferencias estacionarias entre especificaciones y protocolos de reajuste. No son IRF, efectos causales de una reforma ni ganancias de bienestar.

## Tiempo holgado, tope e igualdad

La condición de tiempo holgado es sustantiva. En la referencia, la igualdad de elasticidades cancela el efecto directo de activos sobre la composición a un mismo z. Al reducir el tope, algunos hogares alcanzan la restricción. Con un tope de 0,55, la masa en él es 27,34 %. La brecha media entre quintiles condicionales de activos, ponderada por la masa de cada z, es −0,98 puntos porcentuales. Este indicador compara fracciones individuales dentro de cada productividad; no es V3 agregado y no comparte automáticamente su signo.

La igualdad de tiempo impone otro conjunto factible. Obliga a todos los hogares a trabajar una cantidad fija y elimina el ajuste de horas totales, incluso cuando preferirían trabajar menos. Los casos de 0,49 y 0,60 mantienen elasticidades comunes y muestran pendientes por activos cuyo signo varía con los retornos relativos. La brecha dentro de z es, respectivamente, −2,27 y −1,42 puntos. La brecha agregada V3 sigue siendo positiva: 2,47 y 1,05 puntos. Estos resultados ilustran por qué no debe confundirse una comparación a productividad fija con una comparación de quintiles de toda la población.

**Figuras propuestas:** [restricciones de tiempo](../code/figures/final/paper_time_constraints.pdf) y [perfiles a productividad fija](../code/figures/final/paper_equality_profiles.pdf). En los perfiles se muestra elasticidad común; la modificación es el régimen de tiempo. La igualdad no contradice la Proposición 1: incumple su condición de holgura. Tampoco se evalúa como una política deseable sin estudiar bienestar y plausibilidad económica.

## Evidencia empírica y alcance

La sensibilidad no identifica las elasticidades sectoriales para Perú. El Cuadro 2 del BCRP DT2012-017 presenta estimaciones puntuales de 0,39 para trabajadores formales y 0,37 para informales, usando ingreso total por hora. El orden es contrario al rango ilustrativo con elasticidad informal mayor. Además, esas categorías de trabajadores no equivalen sin más a dos actividades simultáneas elegidas por un mismo hogar. Los intervalos se superponen y aquí no se realiza una prueba de diferencia entre estimaciones. La versión inglesa IZA tiene otra tabla de heterogeneidad; se debe citar el cuadro y la versión correctos. Véase [el cotejo de fuentes](evidencia-elasticidades.md).

La contribución se presenta como un diagnóstico de mecanismo dentro del modelo. No se afirma prioridad en toda la literatura ni mejor ajuste empírico frente a Galindo y coautores. El antecedente cercano y el modelo de este trabajo comparten el análisis de riqueza y riesgo; la diferencia estudiada son las horas simultáneas en una economía con producción y los supuestos que gobiernan su composición.

## Comprobaciones y pendientes que deben aparecer en el cierre

Los 23 GE fueron resueltos en MATLAB el 13 de noviembre y reanalizados desde sus MAT el 23. Se comprueban masa, generador, HJB, KFE, unicidad de clase cerrada, mercados, recursos y condiciones laborales. Para la utilidad logarítmica y el impuesto al consumo nulo registrado, la FOC de consumo recupera el valor marginal como el inverso del gasto. Esto permite verificar estacionariedad y esquinas laborales por nodo, distinguiendo el signo del multiplicador del tope del multiplicador libre de la igualdad.

Pasar estos controles no certifica precisión frente a grilla, dominio o truncamiento de productividad. Tampoco prueba concavidad global de la HJB. El reporte debe separar esas cuestiones del cierre de cada corrida.

La tabla Lean debe sustituirse por las declaraciones y el estado de la carpeta oficial una vez finalice su revisión independiente, con el commit fuente y la salida real del check. La hoja manuscrita original existe y tiene una errata identificada; todavía faltan las demás derivaciones personales. Ninguna guía tipografiada ni revisión de IA sustituye la autoría y adjudicación del estudiante.
