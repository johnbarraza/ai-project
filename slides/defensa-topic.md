# Hoja de defensa · presentación de tema (16 oct)

`topic.pdf` tiene 38 páginas: 17 de contenido, 5 separadores, el índice de anexos y 15 anexos (variables, firmas, equilibrio, momentos y formas de κ pasaron a anexos el 15 oct). Para cada slide: qué decir en una oración, de dónde sale cada número y qué preguntará probablemente el profesor. Los números vienen de `code/output/topic_numbers.tex`.

**Ritmo.** Unos 15 minutos sin interrupciones. Si vas tarde:
- Salta la slide 15 (gráfico de la FOC) y la 17 (fracción informal por activos).
- Las formas de κ, las firmas y el equilibrio ya están en anexos (A12, A4 y A5): si preguntan, usa el enlace.

**En la slide va poco texto; el ejemplo lo dices tú.** Ejemplo para la slide 5: *"Dos trabajadores con la misma productividad, uno sin ahorros y otro con ahorros. En mi modelo actual los dos dedican el 52 % de sus horas a lo informal. Si las horas informales son más flexibles: 54 % el pobre y 47 % el rico."*

---

## 1. Pregunta y track

**Slide 4 · Dato.** *"En el Perú los más pobres son mucho más informales: en 2023, 94 % en el primer quintil y 49 % en el quinto. La brecha bajó de 53 a 45 pp desde 2017, sobre todo porque subió la informalidad del quintil rico tras la pandemia."* La brecha V3 del modelo está en el anexo A11; la tabla de qué replica está en el anexo A9.
- **Fuente:** 2017, INEI (2018), Cuadro 7.5; 2019, INEI (2022), Cuadro 7.5 (p. 120); 2023, cálculo propio con ENAHO (`code/data/build_enaho_quintiles.py`).
- **"¿Quintiles de qué?"** De **gasto per cápita del hogar**, cortados sobre la población. Lo comprobé: con esa definición reproduzco el Cuadro 7.5 de 2021 con error máximo de 0.2 pp (con ingreso per cápita el error llega a 3.6 pp). **No son de riqueza.**
- **"¿Por qué no 2024?"** El INEI dejó de publicar la variable de informalidad (`ocupinf`) en la base 2024–2025. Reconstruirla exige replicar su definición; queda pendiente.
- **"¿Entonces son comparables con el modelo?"** No del todo: personas según su empleo principal frente a horas, gasto frente a riqueza. El dato motiva; no se calibra con él.

**Slide 5 · Pregunta.**
- **Colchón:** ajustar horas hacia lo informal cuando cae tu productividad z. Es un shock individual, no una crisis.
- **"Una respuesta no obvia"** *(es un resultado del modelo, no un dato).* En el modelo, el pobre trabaja más horas en ambos sectores porque un sol extra le vale más. La pregunta es por el **reparto**.

## 2. Modelo base y supuesto que cambio

**Slide 7 · Baseline y supuesto que cambio.** Aiyagari (1994): ahorro precautorio con mercados incompletos, una firma y un bien. `A = K` determina `r`. El supuesto que cambio es el de mi tesis: dos sectores con horas endógenas, dos firmas y dos bienes (precios r y p_I).
- **"¿Por qué tiempo continuo?"** La FOC de horas sale cerrada en cada (a, z), y HJB y KF se resuelven juntas (Achdou et al., 2022).
- **"¿Tu modelo anida a Aiyagari?"** Sí: con un solo sector vuelve a Aiyagari con trabajo endógeno.

**Slide 8 · Agentes.** Hogares, firma informal arriba y formal abajo, gobierno.
- **"¿Quién fija los precios?"** Nadie: todos son tomadores de precios (anexo A1, enlace en la slide).

**Anexo A2 · Variables.**
- a es endógena y z exógena.
- Decisiones del hogar: c_F, c_I, ℓ_F, ℓ_I.
- r y p_I se ajustan; w_F y w_I salen de las FOC de las firmas.
- **"¿V_a es una decisión?"** No: es la derivada de la función de valor, el valor de un sol más.

**Slide 9 · Timing.**
- **"¿El hogar conoce su z futura?"** No conoce el valor, pero sí el proceso: sabe que ln z sigue un Ornstein-Uhlenbeck con persistencia anual de 0.861 y desviación estacionaria de 0.544 (Hong, 2022). Forma expectativas racionales sobre z, y el término de cambio esperado de la HJB (anexo A3) es justamente ese valor esperado. El riesgo es idiosincrático y no hay seguro que lo cubra (mercados incompletos), por eso ahorra por precaución. No hay incertidumbre agregada: en el estado estacionario los precios son constantes y conocidos.
- **"¿Es un periodo después?"** No hay periodos: el hogar reoptimiza en cada instante.
- **"¿Estacionario significa que nadie se mueve?"** No: g no cambia, pero cada hogar sí se mueve dentro de ella.

**Slide 10 · Hogar.**
- **ln C:** γ = 1, como en Achdou et al.
- **χ(z) máx(−a, 0):** prima sobre la deuda. Si a < 0, el hogar paga r + χ(z) por cada sol que debe; si a ≥ 0, máx(−a, 0) = 0 y el término desaparece. Es el costo extra de endeudarse en el sistema financiero, mayor para los menos productivos.
- **φ_s:** elasticidad de Frisch, cuánto suben (%) las horas si el beneficio de una hora sube 1 %.

**Slide 11 · Barrera y prima de deuda.** κ(z) = κ_z1 w(z), χ(z) = χ w(z)^η y w(z) = (z_max − z)/(z_max − z_min).
- **"¿Qué es esa fracción? ¿z es constante?"**
  - z varía entre hogares; z_min = 0.22 y z_max = 3.39 son los extremos de la grilla de productividad (40 nodos).
  - w(z) es un **índice** que vale 1 para el menos productivo y 0 para el más productivo.
  - κ_z1 = 0.40 es la barrera máxima y χ = 0.02 la prima máxima.
- **"¿Por qué esa forma?"** Es la más simple que decrece en z con un solo parámetro, identificado por M3.
- **"¿Cuál es su debilidad?"** Depende de los extremos de la grilla: si amplías la grilla, cambia w(z). La forma por percentil κ_0[1 − F(z)], con F la distribución ergódica de z, no tiene ese problema; recalibrada da la misma brecha (4.4 pp; anexo A12 y A13). *(Decirlo antes de que lo pregunten da puntos.)*
- **"¿Y una barrera discreta, un umbral?"** z es un AR(1) continuo discretizado en 40 nodos. Un umbral cae entre nodos: los momentos quedan constantes por tramos, la calibración no funciona y el resultado depende de la grilla. Además, la FOC interior exige R_F(z) > 0 en todo z.
- **"¿Y un costo fijo, como en la literatura de informalidad?"** Un costo fijo actúa sobre entrar o no a la formalidad (margen extensivo), no sobre la FOC de horas. Queda para la extensión.
- **De Soto:** motiva las barreras.
- **ν_I = 0.6:** la productividad rinde menos en lo informal.
  - **"¿Está calibrado a algún momento?"** No directamente: en la tesis es un valor de referencia fijo (`model_main.m`, línea 178: "ventaja comparativa formal: benchmark usa 0.60"), no se ajusta a una meta. M1 calibra ψ, M2 calibra A_I y M3 calibra κ_z1.
  - **"¿Qué hace?"** Es el canal "estructuralista" del sorting: con ν_I < 1, el atractivo relativo de lo formal, ((1 − τ)w_F z − κ(z))/z^ν_I, crece con z (es un teorema en el Lean de la tesis). Junto con κ_z1 genera el gradiente de formalidad por z y el cociente salarial formal/informal, V1 = 2.33 frente a 2.30.
  - **"¿Y si fuera 1?"** Anexo A13: con φ común y recalibrando M1 y M3, la brecha Q1−Q5 baja de 4.4 a 2.3 pp, porque se pierde parte del sorting por z.
- **"¿El impuesto lo paga la firma o el hogar?"** Legalmente, el hogar: τ = 0.18 se descuenta del ingreso laboral formal, R_F = (1 − τ) w_F z − κ(z). La firma formal paga el salario bruto w_F y su FOC no tiene impuesto. Lo recaudado vuelve a los hogares como transferencia T = τ w_F L_F. Quién lo soporta económicamente depende del equilibrio: si las horas formales caen, w_F sube y la firma también carga una parte. El IGV existe en el solver (τ_c), pero vale 0 en la calibración final. La firma informal y las horas informales no pagan impuesto.

**Anexo A12 · Formas alternativas.**
- **Barrera:** con forma raíz o cuadrática, recalibrada, κ_z1 queda en 0.400–0.403 y la brecha en 4.3–4.4 pp.
- **"¿Por qué casi no cambia κ_z1?"** M3 compara z_max con z_min, donde κ vale 0 y κ_z1 en **cualquier** forma.
- **"¿Por qué la forma no crea gradiente por riqueza?"** κ depende solo de z.
- **Prima de deuda:** no entra en la FOC de horas; actúa a través de V_a, así que su forma se evalúa en equilibrio general (anexo A13).

**Anexo A4 · Firmas.** Dos FOC por firma: capital (α Y/K = r + δ) y trabajo.
- α_I + β_I = 0.22 + 0.619 < 1, así que queda un beneficio Π_I que se reparte por hora efectiva.

**Anexo A5 · Equilibrio.** r cierra el mercado de activos y p_I el del bien informal; el bien formal cierra por Walras.
- **"¿r es endógeno?"** En la tesis sí (r* = 0.066). **En este proyecto, por ahora, lo fijo:** es equilibrio parcial y lo digo.

**Anexo A9 · Momentos replicados y no replicados.**
- **Metas (M):** M1 51.7 frente a 50.9; M2 18.8 frente a 19.0; M3 37.8 frente a 38.6.
- **Validaciones (V):** V1 2.33 frente a 2.30; V2 1.465 frente a 1.913 (subestima); V3 4.4 frente a 53 (**no**).
- **Gini:** de riqueza 0.52 frente a ~0.68 (subestima); de consumo 0.22 frente a 0.40 (no comparable: el dato es de ingreso o consumo).
- **V6 (nuevo):** formalidad de superior menos la de hasta secundaria, 38.6 pp en la EPEN 2025 y 6.2 pp en el modelo. Es el mismo dato de M3, pero M3 lo compara con los dos nodos extremos de z (0.3 % de la masa cada uno). Por grupos con el peso de la EPEN el gradiente es casi plano (A14).
- **Fuentes del Gini:** consumo/ingreso 0.40 = Banco Mundial, SI.POV.GINI, Perú 2024 (40.1). Riqueza 0.68: la tesis lo da como referencia aproximada; el Databook de Credit Suisse reporta cerca de 0.79–0.80 para Perú en 2018–2021 (visto en una tabla secundaria, sin abrir el Databook). Si preguntan: el modelo subestima en cualquier caso.
- **"¿Por qué falla V3?"** A igual z la riqueza no cambia el reparto, y los datos clasifican personas, no horas.
- **"¿Y V4?"** Los modelos tipo Aiyagari concentran menos la riqueza que los datos (falta, por ejemplo, la heterogeneidad de retornos).
- **"¿De dónde sale cada número del modelo?"** M1, M3, V3 y el Gini de riqueza los recalculé desde la solución exportada; M2, V1, V2 y el Gini de consumo los reporta la corrida de la tesis.

**Slide 12 · Sensibilidad.** φ_I ∈ [0.38, 0.70] con φ_F = 0.38; la condición de la conjetura es φ_I > φ_F. La definición de Frisch está en la nota al pie.
- **Guion (30 s, lo que ya no está escrito en la slide):** *"En mi tesis impuse que las horas de los dos sectores respondan igual, φ_F = φ_I = 0.38, por simplicidad. No es una normalización: es justo el supuesto que hace que la riqueza no mueva el reparto. Aquí lo relajo: las horas informales, de cuenta propia y sin jornada fija, se ajustan más. El 0.38 viene de Céspedes y Rendón (2012); ellos estiman 0.39 para trabajadores formales y 0.37 para informales en Lima, pero comparan personas distintas, no cómo un mismo hogar reparte sus horas. Por eso uso φ_I entre 0.38 y 0.70 como sensibilidad."*
- **"¿Por qué serían más flexibles las horas informales?"** Cuenta propia, sin contrato ni jornada. Es la conjetura, y la evidencia peruana no la respalda en promedio.
- **"¿Hay estimaciones?"** Céspedes y Rendón (2012, BCRP DT 2012-017), con el panel de la EPE de Lima 2002–2010 (MaCurdy con efectos fijos, VI con tamaño de firma y corrección de Heckman): 0.38 en promedio, que es el φ_F de la tesis. Su Cuadro 2 (pp. 18–19 de la versión del BCRP), con ingreso total por hora, da **0.39 formal (e.e. 0.02) y 0.37 informal**: no difieren. Es evidencia **indirecta**: clasifica a personas distintas por su empleo principal; no mide cómo un mismo hogar reparte sus horas entre sectores, que es lo que mide φ_s en el modelo, y la diferencia (−0.02) es del tamaño de un error estándar. Por eso el rango de φ_I es una sensibilidad. Si insisten: con φ_I = 0.36 la brecha baja a 4.0 pp, la dirección que predice la conjetura cuando φ_I < φ_F.
- **"¿φ_F = φ_I no era una normalización?"** No. Una normalización no cambia resultados (H̄ = 1, precio formal = 1, E[z] = 1). φ común es el supuesto que cancela V_a: lo impuse en la tesis por simplicidad, y relajarlo es el proyecto.
- **"¿Eso está en Aiyagari?"** No: en Aiyagari el trabajo es exógeno y en Pijoan-Mas hay una sola φ. El supuesto φ_F = φ_I aparece al pasar a dos sectores en mi tesis.
  - La versión en inglés (IZA DP 6991) no trae el corte formal/informal. Sí trae el corte por ingreso: 0.41 en el quintil más pobre y 0.30 en el más rico. La heterogeneidad que miden va por ingreso, no por sector.
- **"¿No crea tipos ex ante?"** No. Todos tienen los mismos φ: son propiedades de la actividad, como ψ_F = 55 ≠ ψ_I = 34. En Galindo et al. los tipos son exógenos: cambian al azar (un informal sigue informal al año siguiente con 89 %) y cada uno trae su aversión al riesgo (0.3 informal, 0.15 formal).

## 3. Resultado esperado

**Slide 14 · FOC en cuatro pasos.**
1. Parto de la HJB: ρv = máx{ln C − Σ ψ_s ℓ_s^(1+1/φ_s)/(1+1/φ_s) + V_a ȧ} + (término de z).
2. ȧ contiene R_F ℓ_F + R_I ℓ_I, así que las horas solo aparecen en la desutilidad y en V_a R_s ℓ_s. Como ln C no depende de las horas, ese bloque se separa del consumo.
3. Derivo.
4. Igualo a cero: la FOC recuadrada.
- **"¿De dónde sale V_a R_s ℓ_s?"** De multiplicar V_a (cuánto vale un sol más) por la parte de ȧ que traen las horas: cada hora en s agrega R_s(z) soles al ahorro. El resto de ȧ (ra, T, −c) no depende de ℓ_s y desaparece al derivar.
- **"¿Y si los mercados no absorben a todos? La firma informal tiene rendimientos decrecientes."** En el modelo no hay racionamiento: las dos firmas contratan cualquier cantidad a su salario, y lo que se ajusta son los precios.
  - **Firma formal:** tiene rendimientos constantes; dado r, la FOC de capital fija K_F/L_F y por lo tanto w_F. Absorbe cualquier L_F sin que cambie w_F.
  - **Firma informal:** tiene rendimientos decrecientes (α_I + β_I < 1). El hogar recibe w̃_I = w_I + Π_I/L_I = (1 − α_I) p_I Y_I/L_I, el producto medio, que **cae si L_I sube**. Además, p_I se ajusta para que C_I = Y_I.
  - **Consecuencia:** si los pobres pasan horas a lo informal, en equilibrio general w̃_I baja y frena el efecto. La lectura de la slide vale **a precios dados**, y por eso el riesgo principal es el equilibrio general. En el experimento parcial, L_F y L_I agregados cambian menos de 0.3 % porque ψ_I se recalibra para M1, así que la presión sobre precios sería pequeña. No está demostrado.
  - La barrera de acceso a lo formal es κ(z), una cuña por hora, no una cola ni un racionamiento.
- **"¿Es máximo?"** La segunda derivada es −(ψ_s/φ_s) ℓ^(1/φ_s − 1) < 0.
- **"¿Y con tope de tiempo?"** Entra λ_H (A7). Nadie llega al tope: el máximo es 0.75 frente a H̄ = 1.

**Slide 15 · Gráfico de la FOC.**
- **Guion (30 s):** *"El eje vertical está en utilidad por hora adicional; el beneficio y el costo marginal se miden igual, por eso van en el mismo eje. Las rectas naranjas son el beneficio de una hora más, V_a R_s: son planas porque no dependen de las horas, y la del pobre está más arriba porque su V_a es mayor. Las curvas son el costo marginal. Donde se cortan están las horas óptimas de cada hogar. A la izquierda, en lo formal, el pobre trabaja 40 % más. A la derecha, con φ_I = 0.70 la curva es más plana y la misma diferencia de V_a mueve 86 % las horas informales; con φ común (gris) serían también 40 %."*
- **Lo que ya no dice la nota:** el pobre tiene a = −0.2 y el rico a = 12.3. Con φ_I = 0.70, ψ_I baja a 6.67 para mantener M1, y por eso la curva teal y la gris se cruzan.
- **"¿Qué es el término con λ en la HJB?"** El cambio esperado del valor por el shock de productividad: con intensidad λ_zz', z salta al nodo z' y el valor pasa de v(a,z) a v(a,z'). Es la versión discreta del OU (40 nodos). No depende de c ni de ℓ, por eso desaparece al derivar la FOC. La misma diferencia de V_a sube las horas formales 40 %, las informales 40 % con φ común (gris) y **86 %** con φ_I = 0.70.
- Hogar pobre: a = −0.2 (percentil 10). Rico: a = 12.3 (percentil 90). Ambos con z = 0.84.

**Slide 16 · Conjetura.** ℓ_I/ℓ_F ∝ V_a^(φ_I − φ_F).
- Condiciones (i)–(iii); la (iii) se cumple en la grilla, **no está demostrada**.
- **"¿Por qué 'si y solo si'?"** El signo de ∂s_I/∂a es el de (φ_I − φ_F) por ∂V_a/∂a, y este último es negativo.

**Slide 17 · Por activos.** Gris plano en 52 %; con φ_I = 0.70 va de 56 % (a = −1) a 45 % (a = 20).
- **"¿Por qué se cruzan?"** La recalibración de ψ_I mantiene M1 en el agregado.

**Anexo A11 · V3** (salió del deck principal el 15 oct; la slide 16 enlaza ahí). 4.4 → 5.8 → 6.7 → 8.7 → 10.6 pp.
- **"¿Por qué no llega a 53?"** Solo hay margen intensivo; falta entrar o salir de la informalidad.

## 4. Brecha en la literatura

**Slide 19.** Tabla de 6 filas y un recuadro: Galindo et al. ya conectan informalidad y riqueza, pero con el sector exógeno; aquí el hogar elige el reparto.
- **Pijoan-Mas (2006):** sí tiene oferta laboral endógena (Aiyagari con horas: trabajar más también asegura), pero con un solo sector. Mi tesis también tiene oferta laboral endógena, en dos sectores.
- **Lecturas propias** (en la propuesta, no en la slide): Achdou (introducción, sección 2), Galindo (modelo, sección 2, y conclusiones, sección 6; presentación de 2023) y el INEI.
- **El resto viene de la bibliografía de la tesis:** Pijoan-Mas (2006), Perry et al. (2007), Loayza (2016) y Meghir, Narita y Robin (2015).
- **"¿Leíste a Galindo?"** Sí. Es Huggett en tiempo continuo con ingreso exógeno: formal e informal son dos tipos exógenos que cambian al azar, con su ingreso (0.33 frente a 1), impuesto (0 frente a 0.18), prima de deuda (0.02 solo informales) y aversión al riesgo (0.3 frente a 0.15). Nadie elige ni trabaja horas, y no hay firmas. En sus conclusiones dejan como extensión volver endógeno el cambio entre estados: mi tesis lo hace en el margen intensivo, con producción y dos bienes. No digas que el resultado es nuevo: di que no aparece en lo revisado.

## 5. Plan y riesgos

**Slide 21.** Demostrar, simular el equilibrio general en MATLAB (primer intento en la slide: con φ_I = 0.50 y 0.70 aún no converge), formalizar en Lean y estimar φ_I.
- **Estimar φ_I:** sd(ln ℓ_I | z)/sd(ln ℓ_F | z) = φ_I/φ_F, con ENAHO dentro de cada nivel educativo.
- **Riesgo:** en equilibrio general cambian r, p_I y g. **Plan B:** el resultado condicional y la cota parcial.

**Slide 22 · La respuesta que busco.** Lee la oración.

## Anexos (enlace "Anexos" en la barra superior)

- **A1:** quién elige qué.
- **A2:** variables (estado, decisiones, precios).
- **A3:** HJB y KF.
- **A4:** firmas y sus FOC.
- **A5:** equilibrio (cómo se cierran los mercados) y por qué este proyecto es de equilibrio parcial.
- **A6:** agregación y Walras.
- **A7:** tope de tiempo.
- **A8:** parámetros.
- **A9:** momentos: metas M1–M3 y validaciones V1–V6, qué replica y qué no.
- **A10:** recalibración (fijar solo M1 baja M3 a 36.3).
- **A11:** brecha Q1−Q5 según φ_I (sube de 4.4 a 10.6 pp; dato 53).
- **A12:** formas de κ y de χ, justificación de la forma lineal y su límite.
- **A13:** robustez.
  - κ: 4.3–4.4 pp.
  - **ν_I = 1** ("¿y si la productividad rinde igual en lo informal?"): con φ común la brecha **baja** a 2.3 pp, porque desaparece parte del sorting por z. Con φ_I = 0.70 se toca el tope de horas, así que lo resuelve el solver de equilibrio general.
- **A14: formalidad por educación.** La cuña por hora no alcanza el gradiente educativo.
  - Con φ común, ℓ_F/ℓ_I ∝ (R_F/R_I)^φ_F. De primaria a universitaria, los odds de horas formales suben 21 veces en el dato y 1.6 en el modelo; para lograrlo, R_F/R_I tendría que cambiar unas 2 926 veces (21^(1/0.38)).
  - Mejor ajuste a los 4 grupos (M1 fijo): con barrera decreciente, R_F(z_min) > 0 topa el nivel y la brecha queda en 6.6 pp. Con barrera proporcional al salario llega a 18.6 pp, pero cobra el 94 % del salario formal mediano y lleva ψ_I a 344: no es creíble.
  - Lectura: el gradiente educativo es de **margen extensivo** (acceso a un empleo formal, Meghir, Narita y Robin 2015), que el modelo no tiene.
  - La educación se asigna a tramos de z: supone que la educación ordena perfectamente a z, el mejor caso para el modelo.
- **A15:** referencias y fuentes de datos.

## Glosario: cada símbolo con su rol

| Símbolo | Rol | Qué es | Valor o ejemplo |
|---|---|---|---|
| $a$ | estado (endógeno) | activos del hogar | de −1 a 20 en la grilla |
| $z$ | estado (exógeno) | productividad laboral; $\ln z$ sigue un proceso OU | de 0.22 a 3.39; nodo central 0.84 |
| $t$ | tiempo | tiempo continuo | — |
| $c$, $C$ | decisión / agregado | consumo; $C$ es la canasta CES de $c_F$ y $c_I$ | — |
| $F$, $I$ | subíndices | sector formal e informal | — |
| $s$ | subíndice | sector genérico, $s\in\{F,I\}$; en $s_I$, fracción informal de horas | $s_I=52\,\%$ a $z=0.84$ en la tesis |
| $\ell$ | decisión | horas, $\ell_F$ y $\ell_I$ | máximo total 0.75 |
| $H$ | parámetro | $\bar H$: tiempo disponible | 1 (normalización) |
| $u$ | función | utilidad del consumo, $\ln C$ | $\gamma=1$ |
| $\rho$ | parámetro | tasa de descuento | 0.073 |
| $\psi$ | parámetro | desutilidad de las horas de cada sector | $\psi_F=55$, $\psi_I=34$ |
| $\phi$ | parámetro | elasticidad de Frisch de las horas | $\phi_F=0.38$; $\phi_I$ de 0.38 a 0.70 |
| $R$ | precio efectivo | ingreso por hora que recibe el hogar, $R_F(z)$ y $R_I(z)$ | — |
| $w$ | precio / función | salarios $w_F$, $w_I$ y $\widetilde w_I$; y el índice $w(z)$ de las cuñas | $w_F=2.25$ |
| $\tau$ | parámetro | impuesto formal | 0.18 |
| $\kappa$ | parámetro / función | barrera por hora formal $\kappa(z)=\kappa_{z1}w(z)$ | $\kappa_{z1}=0.40$ |
| $\chi$ | parámetro / función | prima de deuda $\chi(z)=\chi w(z)^\eta$ | $\chi=0.02$ |
| $\eta$ | parámetro | curvatura de $\chi(z)$; $\eta_z$ es la reversión del OU | $\eta=1$ |
| $\nu$ | parámetro | $\nu_I$: rendimiento de $z$ en lo informal | 0.60 |
| $F$ | función | $F(z)$: distribución ergódica de $z$; en la forma por percentil $\kappa_0[1-F(z)]$ | $\kappa_0=0.401$ |
| $r$ | precio endógeno | tasa de interés | 0.066 en la tesis |
| $p$ | precio endógeno | $p_I$: precio del bien informal | 0.928 en la tesis |
| $T$ | transferencia | $T=\tau w_FL_F$ | — |
| $v$, $V$ | objeto de solución | función de valor $v(a,z)$; $V_a=\partial v/\partial a$ | $V_a$ decrece en $a$ en toda la grilla |
| $g$ | objeto de solución | distribución de hogares $g(a,z)$ | suma 1 |
| $A$ | parámetro / agregado | productividad de las firmas $A_F$, $A_I$; en Aiyagari, activos agregados | $A_I=0.98$ |
| $K$ | decisión de firma | capital $K_F$, $K_I$ | — |
| $L$ | decisión de firma | trabajo efectivo $L_F$, $L_I$ | — |
| $Y$ | agregado | producción de cada sector | — |
| $\alpha$ | parámetro | participación del capital | $\alpha_I=0.22$ |
| $\beta$ | parámetro | $\beta_I$: participación del trabajo informal | 0.619 |
| $\delta$ | parámetro | depreciación | — |
| $\Pi$ | agregado | $\Pi_I$: beneficio de la firma informal | — |
| $S$ | agregado | ahorro total de los hogares | — |
| $D$ | agregado | $\mathcal D$: recursos que absorbe la prima de deuda | — |
| $\lambda$ | multiplicador | $\lambda_H$: multiplicador de la restricción de tiempo | 0 en toda la grilla |
| $\mu$, $\sigma$ | parámetros | media y volatilidad del OU de $\ln z$ | — |
| $N$ | grilla | $N_z$: nodos de productividad | 40 |
