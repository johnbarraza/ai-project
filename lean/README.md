# Comprobación local propia del bloque laboral

`LaborComposition.lean` contiene las políticas laborales explícitas y pruebas de su derivada, regla de la cadena y tres casos de signo de la Proposición 1 del manuscrito nuevo.

El check local pasó con **Lean 4.30.0-rc2**, sin `sorry`, `admit`, axiomas añadidos ni `sorryAx`. Los únicos axiomas reportados son `propext`, `Classical.choice` y `Quot.sound`. La fuente, versión, commit de Mathlib y salida están ligados por hash en `verification/local_check.json` y `local_check.txt`.

`V` representa `a ↦ Va(a,z)` y `d` su derivada. `HasDerivAt V d a` y, para los signos, `d < 0`, son las condiciones de regularidad y concavidad del paper. El archivo no prueba concavidad global de la HJB, existencia del GE ni la derivación del problema dinámico completo.

Reproducción con Lake y las dependencias ya disponibles:

```text
cd lean
lake update
lake build
cd ..
python code/verify_lean.py
```

En esta máquina se reutilizó una caché de Mathlib de WSL, sin modificar sus fuentes:

```text
python code/verify_lean.py --wsl-cache /home/johnb/EconCSLib
```

## Flujo oficial pendiente

Esta carpeta es un **prototipo local propio**, no la carpeta generada completa de una corrida de contribución. El issue #7 exige publicar el paper en un commit, ejecutar el workflow de AppliedModelingLib y conservar el check `paper_contribution.py`. Falta ese recibo. No se copió la formalización antigua del modelo base como si verificara el nuevo paper.

Antes de la entrega definitiva debe incorporarse la carpeta generada íntegra y reconciliarse cada resultado del paper con sus declaraciones y estado. El check local y la revisión semántica humana son evidencias distintas; aún no se ha registrado esta última.
