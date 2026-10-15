# Ahorro, flexibilidad de horas e informalidad en el Perú

[![build](https://github.com/johnbarraza/ai-project/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/johnbarraza/ai-project/actions/workflows/build.yml)

**John Svante Barraza Ratachi** · Track B: el modelo detrás de mi tesis · AI and Economic Modeling, Universidad del Pacífico, 2026-II

[Propuesta (PDF)](proposal/proposal.pdf) · [Slides del tema (PDF)](slides/topic.pdf) · [Chequeos](code/README.md) · [Reglas del curso](https://github.com/alexanderquispe/AI-Econ-Modeling/issues/7)

## Pregunta

**¿Bajo qué condición la informalidad amortigua más a los hogares con menos ahorro, a igual productividad?**

En 2023 tiene empleo informal el 94 % de los ocupados del quintil de gasto más pobre y el 49 % del más rico (ENAHO). El modelo de mi tesis genera una brecha de solo 4.4 puntos entre el quintil de riqueza más bajo y el más alto.

<img src="code/figures/motivation_quintiles.svg" alt="Empleo informal por quintil de gasto per cápita del hogar, Perú 2017, 2019 y 2023: cae de 97 % en el quintil más pobre a 44 % en el más rico en 2017" width="640">

## Modelo

- **Baseline:** Aiyagari (1994) en tiempo continuo (Achdou et al., 2022). Hogares que ahorran por precaución, una firma y un bien; $r$ cierra el mercado de activos.
- **Supuesto que cambio (mi tesis):** dos sectores con horas endógenas. El hogar, con activos $a$ y productividad exógena $z$, elige consumo y horas formales $\ell_F$ e informales $\ell_I$. Hay dos firmas (la informal con rendimientos decrecientes) y dos bienes, con precios $r$ y $p_I$. La barrera por hora formal $\kappa(z)$ y la prima de deuda $\chi(z)$ caen con $z$.
- **Sensibilidad:** horas informales más flexibles, $\phi_I>\phi_F$. En la tesis, $\phi_F=\phi_I=0.38$.

$$\max\ \mathbb E_0\int_0^\infty e^{-\rho t}\Big[\ln C-\sum_{s\in\lbrace F,I\rbrace}\frac{\psi_s\ell_s^{1+1/\phi_s}}{1+1/\phi_s}\Big]dt
\quad\text{s.a.}\quad
\dot a=R_F(z)\ell_F+R_I(z)\ell_I+ra-\chi(z)\max(-a,0)+T-c_F-p_Ic_I,\quad a\ge\underline a,\quad \ell_F+\ell_I\le\bar H$$

<img src=".github/assets/mecanismo.svg" alt="Mecanismo: menos activos suben el valor de un sol más, V_a; eso sube las horas de ambos sectores, y la fracción informal cae con los activos solo si phi_I es mayor que phi_F" width="760">

## Resultado esperado (conjetura)

De la HJB, con solución interior, la FOC de cada sector es $V_aR_s(z)=\psi_s\ell_s^{1/\phi_s}$. Dividiendo las dos FOC:

$$\frac{\partial\ln(\ell_I/\ell_F)}{\partial\ln V_a}=\phi_I-\phi_F,\qquad
\frac{\partial s_I}{\partial V_a}=s_I(1-s_I)\,\frac{\phi_I-\phi_F}{V_a},\qquad s_I=\frac{\ell_I}{\ell_F+\ell_I}.$$

**Conjetura.** Si (i) la solución es interior, $\ell_F+\ell_I<\bar H$; (ii) $R_F(z),R_I(z)>0$; y (iii) $V_a$ decrece con $a$, entonces, a igual $z$, la fracción informal $s_I$ decrece con los activos **si y solo si** $\phi_I>\phi_F$. Con elasticidad común, $V_a$ se cancela y la riqueza no cambia el reparto. La condición (iii) se cumple en toda la grilla de la calibración, pero no está demostrada.

<img src="code/figures/informal_share_by_assets.svg" alt="Fracción informal de las horas según los activos del hogar, con productividad fija: plana en 52 % con elasticidad común y decreciente con phi_I igual a 0.50 y 0.70" width="700">

En equilibrio parcial, manteniendo las metas M1 y M3, la brecha entre el quintil de riqueza más bajo y el más alto sube de 4.4 a 10.6 puntos con $\phi_I=0.70$: sube, pero queda lejos de los 53 puntos del dato (anexo A11 de las slides).

## Estado

| Parte | Dónde | Estado |
|---|---|---|
| Tema: propuesta (4 pp.) y slides | [proposal/](proposal/proposal.pdf) · [slides/](slides/topic.pdf) | Listos para el 16 de octubre |
| Chequeos, números y figuras | [code/](code/README.md) | `python code/verify.py` pasa y regenera todo |
| Datos del modelo | [code/data/](code/data/README.md) | Resultados exportados de la corrida de la tesis; sin microdatos |
| Literatura | [literature-check.md](proposal/literature-check.md) | Galindo et al. (2024) leído; faltan los trabajos que lo citan |
| Equilibrio general con $\phi_I\neq\phi_F$ | solver MATLAB de la tesis | Reproduce el caso de $\phi$ común; con $\phi_I$ = 0.50 y 0.70 aún no converge |
| Derivaciones a mano | `hand/` | Pendiente |
| Paper, slides finales y Lean | `paper/`, `slides/final.tex`, `lean/` | Pendientes; aún con material de la plantilla |
| Colaboración con IA | [prompts.md](prompts.md) | Registro crudo en preparación; se sube antes de la presentación final |

## Reproducir

```bash
python -m pip install -r code/requirements.txt
python code/verify.py              # números, figuras y chequeos; falla si una afirmación no se cumple
cd proposal && latexmk -pdf proposal.tex && cd ..
cd slides && latexmk -pdf topic.tex && cd ..
```
