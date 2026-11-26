# Revisión de las pruebas originales y aplicación al modelo

Revisión del 26 de noviembre de 2026. Se examinó el artículo publicado de [Achdou, Han, Lasry, Lions y Moll (2022)](https://doi.org/10.1093/restud/rdab002), especialmente las secciones 4.6 y 7, y el [suplemento de la editorial](https://academic.oup.com/restud/article/89/1/45/6149490#supplementary-data). Se leyeron los argumentos pertinentes de A.1, A.7, A.8, el planteamiento de G.1 y las extensiones G.2 y G.3. Este cotejo amplía la lectura parcial registrada antes; no es una revisión de todos los resultados del artículo.

La copia editorial del suplemento tiene 65 páginas y SHA256 `ee80c0124310dafbe004405a9a44ee0bd6b1ecedc920dc6c806ec363f45a10ef`. Se contrastó con la copia del autor, fechada en sus metadatos en octubre de 2020 y con numeración distinta. Los localizadores siguientes corresponden a páginas del PDF editorial, que también están numeradas del 1 al 65. El trabajo original de [Aiyagari (1994)](https://doi.org/10.2307/2118417), pp. 668–670, aporta el antecedente del argumento de ahorro agregado y demanda de capital.

## Qué establece la referencia y qué puede trasladarse

| Resultado de la referencia | Paso de la prueba relevante | Aplicación al modelo del curso |
|---|---|---|
| Concavidad débil del valor a precios dados, A.1, PDF p. 1 | Objetivo cóncavo y conjunto factible convexo; de ahí valor débilmente cóncavo y consumo no decreciente | Hay una adaptación condicional para nuestro hogar, desarrollada abajo. No prueba curvatura estrictamente negativa ni regularidad global. |
| Existencia estacionaria, Proposición 4; A.7, PDF pp. 13–16 | Continuidad del ahorro agregado y comportamiento en los extremos de la tasa permiten encontrar un cruce con la oferta de bonos | Nuestro cierre exige dos mercados y dos precios, con horas y remuneraciones endógenas. Falta justificar la correspondencia de agregados y un argumento de existencia para ese sistema. |
| Unicidad, Proposición 5; A.8, PDF pp. 16–20 | Con IES al menos uno y no endeudamiento, el ahorro responde positivamente a la tasa; las trayectorias se ordenan y también el ahorro agregado | La utilidad logarítmica satisface la condición de IES del bloque de consumo, pero el modelo permite activos negativos. Además, el ingreso laboral se elige. No se hereda el orden de trayectorias. |
| Producción tipo Aiyagari, G.2, PDF pp. 52–53 | Una firma CRS y homogeneidad salarial del ahorro; para unicidad se añade una restricción sobre tecnología | La firma formal es CRS, pero hay otra firma con rendimientos decrecientes, beneficios repartidos, dos bienes y trabajo sectorial endógeno. No se demostró una reducción al problema representativo de G.2. |
| Prima entre deuda y ahorro, G.3, PDF pp. 53–55 | La Proposición A.3 analiza el caso determinista con `r_+ < rho < r_-` y caracteriza el ahorro cerca de cero | Es un antecedente pertinente de la prima de deuda. La prima propia depende de productividad y la desigualdad no se cumple para todos los tipos; tampoco es un teorema de existencia de nuestro GE. |

La falta de una transferencia directa no demuestra inexistencia o multiplicidad en nuestro modelo. Identifica los pasos que todavía no están probados.

## El punto exacto en que importa permitir deuda

En A.8.2, PDF p. 19, el modelo de referencia escribe `s(a,y)=y+ra−c(a,y)` y obtiene

$$
\partial_rs(a,y)=a-\partial_rc(a,y).
$$

Una respuesta negativa del consumo a la tasa garantiza una respuesta positiva del ahorro si `a>0`. Cuando `a<0`, la expresión deja de tener signo asegurado. El propio suplemento señala este paso. En nuestro problema, además, al cambiar los precios pueden cambiar las horas, sus retornos y el reparto de beneficios; por ello la derivada del ahorro contiene otras respuestas.

En G.2, la homogeneidad `S(r,w)=wS(r,1)` reduce el cierre con producción a una comparación escalar. La nota 21 del suplemento añade que la demanda normalizada de capital debe decrecer; ofrece como condición que la participación del capital sea menor que la elasticidad de sustitución de la producción. Verificar esa desigualdad solo para nuestra firma formal no prueba la propiedad del sistema completo.

## Comprobación de los parámetros propios

Se cotejaron los mismos 23 MAT y sus bitácoras, verificando sus hashes contra la auditoría nativa. En todos se mantienen utilidad logarítmica, `rho=0,073`, límite de activos `−1`, costos laborales con parámetros positivos y prima de deuda no negativa. La CES usa elasticidad 5 y peso formal 0,56; su exponente es 0,8. Es un agregador creciente y cóncavo. Las cuñas observadas no varían entre nodos de activos a una misma productividad.

Las tasas de los casos van de 0,06563 a 0,06738, por debajo del descuento. Esto es consistente con una condición de referencia, pero no prueba por sí solo existencia. La prima va de cero a 0,02: la tasa de deuda queda por debajo del descuento para algunos tipos y por encima para otros. No se cumplen uniformemente las condiciones de la Proposición A.3 de G.3.

Estos valores caracterizan las soluciones calibradas. Los 23 experimentos varían elasticidades, restricciones de tiempo o niveles reajustados; no constituyen un barrido de la tasa de interés bajo un único conjunto de parámetros que demuestre monotonía del ahorro agregado.

## Adaptación propia: argumento de concavidad débil a precios dados

Este es un argumento analítico complementario, con condiciones explícitas. No es una nueva proposición del paper ni una prueba certificada por Lean. Permite precisar qué parte del argumento de A.1 resulta adaptable.

Se fijan los precios, los retornos por hora, el reparto por trabajo efectivo y la transferencia que toma como dados un hogar individual. El proceso de productividad es exógeno y se usa la misma realización para comparar dos trayectorias. Se consideran controles adaptados, prima de deuda acotada e integrabilidad de las trayectorias suficiente para las esperanzas siguientes, y se supone valor finito en el intervalo de activos. Si se añade una restricción de admisibilidad o transversalidad, debe comprobarse que la construcción la respeta. La finitud del valor y las condiciones del horizonte infinito no quedan demostradas por una auditoría de grilla.

Defina

$$
b_z(a)=ra-\chi(z)(-a)_+.
$$

Como `chi(z)>=0` y `(-a)_+` es convexa, `b_z` es cóncava en activos. Los ingresos por horas son lineales en las decisiones del hogar a precios dados. El conjunto `ell_F,ell_I>=0`, `ell_F+ell_I<=Hbar` es convexo, al igual que el límite de activos. Una igualdad de horas también es una restricción convexa, aunque queda fuera de la rama interior de la Proposición 1 del paper.

Tome dos trayectorias admisibles con el mismo riesgo y un peso `theta` entre cero y uno. En las fórmulas de construcción se omite el índice temporal de activos y controles: se aplican en cada instante. Construya

$$
a_\theta=\theta a_1+(1-\theta)a_2,
\qquad \ell_{s,\theta}=\theta\ell_{s,1}+(1-\theta)\ell_{s,2}.
$$

La mezcla respeta las restricciones de horas y activos. No basta mezclar los consumos sin más, porque la deriva por deuda no es lineal. La diferencia

$$
\Delta=b_z(a_\theta)-\theta b_z(a_1)-(1-\theta)b_z(a_2)
=\chi(z)\{\theta(-a_1)_++(1-\theta)(-a_2)_+-(-a_\theta)_+\}\geq0
$$

puede consumirse en bien formal. Con su precio normalizado a uno y sin impuesto al consumo, establezca

$$
c_{F,\theta}=\theta c_{F,1}+(1-\theta)c_{F,2}+\Delta,
\qquad c_{I,\theta}=\theta c_{I,1}+(1-\theta)c_{I,2}.
$$

Al sustituir en el presupuesto, la deriva resultante es exactamente `theta*dot a_1+(1−theta)*dot a_2`. Se obtiene una trayectoria factible cuya utilidad es al menos la utilidad de la mezcla de consumos: la utilidad aumenta al añadir consumo formal. Además, `ln C` es cóncava y el costo laboral es convexo. Por tanto, la utilidad esperada descontada de la trayectoria construida satisface

$$
J_\theta\geq\theta J_1+(1-\theta)J_2.
$$

Aplicando la construcción a controles arbitrariamente cercanos al valor supremo y haciendo tender su error a cero, se obtiene

$$
v(a_\theta,z)\geq\theta v(a_1,z)+(1-\theta)v(a_2,z).
$$

Es concavidad débil, condicional a la admisibilidad e integrabilidad descritas. La corrección `Delta` es lo que permite tratar la prima de deuda sin asumir que el presupuesto es afín en activos. Se verificaron simbólicamente sus identidades en los casos de activos con el mismo signo y con signos opuestos. Eso respalda la manipulación algebraica; no certifica por máquina todo el argumento de control estocástico.

## Por qué se mantiene el Supuesto 4 del paper

Donde exista la segunda derivada, la concavidad débil da `Vaa<=0`. No garantiza `Vaa<0` en cada punto. Incluso una función estrictamente cóncava y suave puede tener segunda derivada cero: `v(a)=a−a^4`, en `−1/2<a<1/2`, tiene `Va>0`, pero `Vaa(0)=0`. Las derivadas de este contraejemplo se comprobaron simbólicamente.

La Proposición 1 afirma signos estrictos cuando las elasticidades difieren y `Vaa<0`. Por eso se conserva esa condición local. La verificación de curvatura negativa en las 23 grillas la respalda numéricamente; ni ese chequeo ni el argumento débil prueban que exista una segunda derivada estrictamente negativa en todo el dominio continuo, incluidas las fronteras y el cambio de régimen de deuda.

## Qué queda pendiente para existencia y unicidad del GE propio

El argumento de A.7 necesita continuidad del ahorro agregado y un cruce. Para este modelo habría que justificar solución individual y distribución estacionaria para los precios relevantes, continuidad y control de los momentos al tomar el estado estacionario, y una región de precios donde el cierre conjunto de capital y bien informal tenga una solución. La reducción de G.2 y los argumentos de orden de A.8 no están establecidos para nuestras dos firmas y cuñas.

Los candidatos computados con residuos pequeños siguen siendo evidencia numérica. No demuestran unicidad ni que toda inicialización converja al mismo precio, ni sustituyen un teorema del modelo continuo.

El paper, sus cuatro supuestos, la Proposición 1, su prueba y la carpeta Lean aceptada permanecen intactos. Este informe aporta el cotejo de fuentes y un argumento complementario para revisión; no cambia el estado de la formalización ni acredita revisión personal del autor.
