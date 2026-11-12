# Guion de la final, opción A

24 láminas principales, 8 de consulta. Asignación de preparación: **30 minutos**, más 15 de discusión. No es un ensayo observado. Fuente económica: `code/verify.py`; resultados parciales y GE se explican por separado.

| Lámina | Min | Qué decir y qué poder defender |
|---|---:|---|
| 1 | 0,5 | «Comparo hogares con igual productividad y distintos activos. Quiero saber cuándo cambia su reparto de horas». La decisión es de horas, no de aceptar una vacante. |
| 2 | 1 | «La informalidad es más frecuente en hogares de menor gasto». Definir ocupados, quintiles y año. El gasto motiva, pero no mide activos ni identifica causalidad. |
| 3 | 1 | Dar la respuesta antes de desarrollar el modelo. Definir elasticidad como cuánto cambian las horas ante un cambio proporcional en su beneficio marginal. |
| 4 | 1 | Aiyagari conserva el ahorro bajo riesgo. La extensión agrega sectores y horas. La desigualdad de elasticidades es sensibilidad del modelo de dos sectores. |
| 5 | 1,5 | Recorrer las flechas: trabajo y ahorro hacia firmas; bienes e ingresos hacia hogares; impuesto y transferencia con gobierno. Distinguir capital agregado de la posición individual de activos. |
| 6 | 1 | Estado conocido, decisiones y evolución. Los precios se toman dados en el hogar y se determinan por mercados en equilibrio. Es tiempo continuo. |
| 7 | 1,5 | Explicar consumo, desutilidad y restricción de recursos. Psi cambia el nivel del costo de horas; phi cambia su curvatura. La prima solo se paga con activos negativos. |
| 8 | 1 | Comparar las dos tecnologías: ambas demandan factores; la informal deja beneficios que se reparten por trabajo efectivo. Conectar salarios y demanda de capital con precios. |
| 9 | 1 | «La distribución transforma decisiones individuales en ahorro y horas agregadas». Leer la acumulada de activos y explicar la ponderación por mu. No promediar fracciones de horas sin ponderar. |
| 10 | 1,5 | Recorrer el circuito precios → HJB → KFE → agregados → firmas/mercados → precios. Mostrar qué cierra r y qué cierra pI. Ese circuito es lo que se vuelve a resolver en GE. |
| 11 | 1 | Barrera por hora frente a prima de deuda. Ninguna es por sí sola un modelo de ofertas de empleo o default. |
| 12 | 1,5 | Va es cuánto aumenta el valor del hogar con una unidad más de activos. Derivar la desutilidad: el denominador cancela el exponente. Explicar por qué falta el multiplicador solo con tiempo holgado. |
| 13 | 2 | Leer las condiciones en lenguaje natural. La identidad es del bloque laboral; el signo por riqueza necesita Vaa negativo. No afirmar concavidad global demostrada. |
| 14 | 1,5 | Dividir horas, tomar logaritmos y aplicar la regla de la cadena. Demostrarlo sin leer. El paso difícil pendiente es la concavidad de la solución completa. |
| 15 | 1 | «La diagonal cancela el canal; por encima, más activos reducen la fracción informal, bajo las condiciones». Los ejes son elasticidades, no datos estimados ni fechas. |
| 16 | 1,5 | Explicar que todas las curvas comparan activos a un mismo z. El ejercicio deja Va, distribución y precios fijos y reajusta dos niveles. No es un GE nuevo. |
| 17 | 1 | «El cambio de elasticidad aumenta esta brecha dentro del ejercicio parcial». Convención D17: 4,31 a 10,43 pp. No calcular distancia contra la informalidad de personas por gasto. |
| 18 | 1,5 | «Ahora vuelvo a resolver GE para contrastar cuñas, con elasticidad común». Solo cambia la forma indicada. Constantes iniciales igualan pagos del caso de referencia, no los pagos finales del nuevo GE. |
| 19 | 1,5 | Separar contraste a parámetros fijos de reajuste a M1/M3 internos. La pequeña diferencia de V3 no identifica la forma; la razón de gasto no mejora contra su meta registrada. |
| 20 | 1,5 | Leer los cambios de r en puntos básicos y de K en porcentaje. Son diferencias estacionarias entre especificaciones. Explicar que mu y los precios se ajustan, no solo las horas. El control de precisión sigue abierto en A5. |
| 21 | 1 | Mostrar la declaración propia compilada: V es Va como función de activos y d es su derivada. `.comp` aplica la regla de la cadena y `ring` normaliza el álgebra. Lean comprueba políticas explícitas; no demuestra concavidad de la HJB ni GE. El flujo oficial sobre commit sigue pendiente. |
| 22 | 1,5 | Explicar el veredicto sobre el tope de tiempo: un mecanismo puede ser algebraicamente válido y no operar en la calibración. Falta insertar la foto manuscrita personal para cumplir la consigna. |
| 23 | 1 | Volver a la respuesta y a los límites. No abrir una nueva arquitectura F/I/N o una promesa de respuesta agregada que no se mostró. |
| 24 | 1,5 | Formular las tres preguntas y dejar espacio para respuestas. Usar los anexos enlazados cuando la pregunta requiera ecuaciones o precisión. |

Respuestas que conviene preparar:

- **¿Por qué no baja la fracción con riqueza si ambas horas bajan?** Con phi común, Va multiplica ambos niveles con el mismo exponente y se cancela en el cociente. Las horas totales pueden cambiar.
- **¿De dónde viene Vaa < 0?** Es condición de la proposición. La exportación histórica la cumple en la grilla; no se ha demostrado globalmente para esta HJB.
- **¿PhiI > phiF está estimado?** No. Es un rango ilustrativo de sensibilidad. La literatura revisada no identifica automáticamente estas dos elasticidades estructurales.
- **¿La barrera constante mejora el modelo?** Cambia M3 y permite diagnosticar dependencia de la forma. Recuperar M1/M3 mediante reajuste no garantiza mejora externa ni identifica una forma única.
- **¿Son comparables 4,31 del PE y 4,399 de D73?** No como contraste limpio. Corresponden a exportaciones, soluciones y reglas de corte distintas. Se comparan variantes dentro de cada bloque.
- **¿Por qué es un trabajo macro si la proposición es del hogar?** El hogar es una parte de una economía con distribución de estados, dos firmas y precios endógenos. Sus políticas se agregan y se resuelve un cierre de mercados. Los resultados condicionales y los GE cumplen papeles distintos en ese sistema.
- **¿Qué falta para entregar?** La prueba local propia ya compila. Faltan el flujo oficial sobre un paper publicado en commit y el manuscrito real que John hará después, además del ensayo y de los pendientes de precisión que se afirmen cerrados.
