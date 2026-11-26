# Guía complementaria para las derivaciones macro

**Material tipografiado de preparación. No es evidencia manuscrita ni un veredicto personal de John.** Desarrolla y explica cada paso en tus propias hojas; verifica las condiciones antes de usar una regla. Conserva las fotos originales y cualquier corrección personal por separado.

Esta guía acompaña el modelo de [paper/paper.tex](../paper/paper.tex). Las hojas B y C de [la guía laboral](guia_derivacion.tex) ya desarrollan la Proposición 1. Aquí se conectan consumo, firmas, distribución y recursos, sin añadir otra proposición al paper.

Los activos y los gastos del presupuesto se miden en unidades del bien formal. `Va` valora una unidad adicional de activos en esas unidades.

Las identidades de firmas, homogeneidad y recursos se comprueban en [code/macro_checks.py](../code/macro_checks.py), llamado por `code/verify.py`. El reporte registra sus condiciones y límites.

## 1. Consumo y valor marginal de activos

Trabaja en la rama de consumo interior de las corridas analizadas: `cF>0`, `cI>0`, precio `pI>0`, utilidad `ln C` e impuesto al consumo cero. La canasta CES es diferenciable y homogénea de grado uno. Escribe `C_{cF}=∂C/∂cF` y `C_{cI}=∂C/∂cI` para las derivadas de la canasta. Los agregados de consumo se introducen en la sección 4.

1. El bloque de consumo de la HJB, dados los demás objetos, es

   $$\ln C(c_F,c_I)-V_a(c_F+p_Ic_I).$$

2. Regla de la cadena y FOC interiores:

   $$\frac{C_{c_F}}{C}-V_a=0,\qquad\frac{C_{c_I}}{C}-p_IV_a=0.$$

3. Multiplica la primera igualdad por `cF`, la segunda por `cI`, y suma:

   $$\frac{c_FC_{c_F}+c_IC_{c_I}}{C}=V_a(c_F+p_Ic_I).$$

4. Teorema de Euler para una función diferenciable homogénea de grado uno:

   $$c_FC_{c_F}+c_IC_{c_I}=C.$$

5. Sustituye, divide por el gasto positivo y obtén

   $$1=V_a(c_F+p_Ic_I),\qquad V_a=\frac1{c_F+p_Ic_I}.$$

Explica por qué esta identidad permite recuperar el `Va` usado por el control laboral en esas corridas. Si cambia la utilidad o aparece un impuesto al consumo, hay que volver a derivar las FOC correspondientes. La identidad no prueba concavidad de la función de valor.

## 2. Firma formal

Supón factores interiores positivos, `AF>0`, `0<α<1`, `wF>0` y `r+δ>0`. El precio del bien formal es uno; el costo del capital es `r+δ`.

1. Escribe producción y beneficio:

   $$Y_F=A_FK_F^\alpha L_F^{1-\alpha},\qquad
   \Pi_F=Y_F-w_FL_F-(r+\delta)K_F.$$

2. Regla de la potencia, primero respecto al capital y luego al trabajo:

   $$\alpha A_FK_F^{\alpha-1}L_F^{1-\alpha}=r+\delta,$$
   $$(1-\alpha)A_FK_F^\alpha L_F^{-\alpha}=w_F.$$

3. Multiplica por `KF` y `LF`, respectivamente:

   $$(r+\delta)K_F=\alpha Y_F,\qquad w_FL_F=(1-\alpha)Y_F.$$

4. Sustituye ambos pagos en el beneficio:

   $$\Pi_F=Y_F-(1-\alpha)Y_F-\alpha Y_F=0.$$

Estos pasos describen la rama interior compatible con los precios de factores. Con rendimientos constantes, las FOC por sí solas no fijan una escala única de la firma: las cantidades deben ser compatibles con los mercados del modelo.

## 3. Firma informal y retorno del hogar

Usa factores positivos, `AI>0`, `pI>0`, `αI>0`, `βI>0` y `αI+βI<1`.

1. Escribe el problema:

   $$Y_I=A_IK_I^{\alpha_I}L_I^{\beta_I},\qquad
   \Pi_I=p_IY_I-w_IL_I-(r+\delta)K_I.$$

2. Deriva respecto a cada factor y multiplica por ese factor:

   $$p_I\alpha_IA_IK_I^{\alpha_I-1}L_I^{\beta_I}=r+\delta
   \quad\Rightarrow\quad (r+\delta)K_I=\alpha_Ip_IY_I,$$
   $$p_I\beta_IA_IK_I^{\alpha_I}L_I^{\beta_I-1}=w_I
   \quad\Rightarrow\quad w_IL_I=\beta_Ip_IY_I.$$

3. Sustituye en el beneficio:

   $$\Pi_I=p_IY_I-\beta_Ip_IY_I-\alpha_Ip_IY_I
   =(1-\alpha_I-\beta_I)p_IY_I>0.$$

4. Declara la convención de reparto por trabajo efectivo del modelo y usa `LI>0`:

   $$\widetilde w_I=w_I+\frac{\Pi_I}{L_I},\qquad
   R_I(z)=\widetilde w_Iz^{\nu_I}.$$

5. Con `LI=∫z^νI ℓI dμ`, integrar el ingreso informal de los hogares da

   $$\int R_I(z)\ell_I\,d\mu
   =\widetilde w_IL_I=w_IL_I+\Pi_I.$$

Explica la diferencia entre `wI`, salario pagado por la firma, y el retorno efectivo que también incorpora el reparto de beneficios. El reparto es una convención del modelo; la FOC de la firma no lo deriva.

## 4. Del presupuesto individual al cierre de recursos

Condiciones usadas: distribución estacionaria normalizada `∫dμ=1`, integrales finitas y condiciones de frontera compatibles con ahorro agregado estacionario. Escribe `K=KF+KI`, `CF=∫cF dμ`, `CI=∫cI dμ`, `S=∫a dμ`.

1. Integra el presupuesto individual:

   $$\int\dot a\,d\mu
   =\int R_F\ell_F\,d\mu+\int R_I\ell_I\,d\mu
   +rS-\mathcal D+T-C_F-p_IC_I,$$

   donde `𝒟=∫χ(z)(−a)+ dμ` es el pago de prima sobre deuda y `𝒦=∫κ(z)ℓF dμ` es la barrera formal. El símbolo `(−a)+` representa `max(−a,0)`.

2. Usa los retornos por hora y los agregados de trabajo efectivo:

   $$\int R_F\ell_F\,d\mu=(1-\tau)w_FL_F-\mathcal K,$$
   $$\int R_I\ell_I\,d\mu=w_IL_I+\Pi_I.$$

3. Sustituye `T=τwFLF`; recaudación y devolución se cancelan:

   $$\int\dot a\,d\mu
   =w_FL_F+w_IL_I+\Pi_I+rS
   -\mathcal K-\mathcal D-C_F-p_IC_I.$$

4. Usa los beneficios y pagos de factores ya derivados:

   $$w_FL_F=Y_F-(r+\delta)K_F,$$
   $$w_IL_I+\Pi_I=p_IY_I-(r+\delta)K_I.$$

5. Impón el mercado de activos `S=K` y simplifica `(r+δ)K−rK=δK`:

   $$\int\dot a\,d\mu
   =Y_F+p_IY_I-\delta K-\mathcal K-\mathcal D-C_F-p_IC_I.$$

6. En el estado estacionario agregado, `∫dot a dμ=0`. Con el mercado informal `CI=YI`, cancela `pIYI−pICI` y despeja:

   $$Y_F=C_F+\delta(K_F+K_I)+\mathcal K+\mathcal D.$$

Para justificar la media de ahorro cero, toma un intervalo `h>0` y la trayectoria de activos dada por el presupuesto. Con integrabilidad para aplicar Fubini y distribución estacionaria:

$$\mathbb E[a_{t+h}]-\mathbb E[a_t]
=\mathbb E\!\left[\int_t^{t+h}\dot a_s\,ds\right]
=\int_t^{t+h}\mathbb E[\dot a_s]\,ds
=h\int\dot a\,d\mu.$$

La estacionariedad hace cero el lado izquierdo. Divide por `h>0` para obtener `∫dot a dμ=0`.

Justifica cada cancelación. Un hogar puede ahorrar o desahorrar aunque el ahorro medio sea cero. El cierre requiere las dos cuñas; omitir una cambia la comprobación de recursos. Los precios `r` y `pI` se ajustan para compatibilizar las decisiones y los mercados.

## 5. Tope de horas frente a igualdad

Con horas positivas, deriva el lagrangiano laboral usando `+λH(Hbar−ℓF−ℓI)`:

$$V_aR_s-\psi_s\ell_s^{1/\phi_s}-\lambda_H=0.$$

Para el tope `ℓF+ℓI≤Hbar`, añade factibilidad, `λH≥0` y complementariedad:

$$\lambda_H(\bar H-\ell_F-\ell_I)=0.$$

Escribe las implicaciones en su dirección correcta: holgura estricta implica `λH=0`; `λH>0` implica que el tope se alcanza. Alcanzar el tope también puede ocurrir con `λH=0`. Si un sector tiene cero horas, hay que tratar su condición de esquina y no dividir por esas horas.

Para la igualdad `ℓF+ℓI=Hbar`, el multiplicador es libre en signo. No se agrega la restricción dual `λH≥0`. Es otro conjunto factible y queda fuera del supuesto de tiempo holgado de la Proposición 1. Las pendientes de las simulaciones con igualdad no son una extensión demostrada de esa proposición.

## Revisión personal antes de fotografiar

Comprueba denominadores positivos, reglas de potencia, cadena y cociente, qué objetos se mantienen fijos y qué igualdades son condiciones de equilibrio. Explica el significado de cada variable y distingue un supuesto, una FOC y una identidad de agregación. Une estas hojas con la prueba laboral completa y la corrección personal de los dos errores de la hoja original. Esta guía impresa no completa el requisito manuscrito.
