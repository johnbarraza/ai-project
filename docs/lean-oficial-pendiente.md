# Paso oficial pendiente para la formalización

La comprobación local propia ya existe y pasó. El [issue #7](https://github.com/alexanderquispe/AI-Econ-Modeling/issues/7), sección 6, prescribe además esta secuencia:

1. Revisar y publicar por rama → PR → merge el paper que será fuente. Registrar el hash real de ese commit. Hoy no existe ese commit publicado para el manuscrito nuevo.
2. Desde AppliedModelingLib actualizado, usar la configuración del curso: `gpt-5.6-sol`, razonamiento `xhigh`, y el workflow `paper-formalization` sobre el PDF en ese commit. Carpeta propuesta: `Barraza26LaborComposition`.
3. Conservar la salida de `python3 scripts/paper_contribution.py check Barraza26LaborComposition --fast`.
4. Copiar íntegra la carpeta generada como `lean/`, respetando sus archivos ignorados; conservar el prototipo local como antecedente si procede, sin confundirlo con esa generación.
5. Reconciliar Proposición 1, declaraciones y alcance. El paper asume regularidad y concavidad donde las usa; no debe añadirse la conclusión como hipótesis.

El prompt se completa con el hash real después de publicar:

```text
Please formalize my own paper, an unpublished manuscript with no arXiv
record: https://github.com/johnbarraza/ai-project/blob/<commit>/paper/paper.pdf
(pinned at commit <commit>), using the paper-formalization skill and
workflow in this repository.
Use Barraza26LaborComposition as the paper folder.
```

No se inventa el hash ni se declara ejecutada esa corrida. Antes de commit/push debe cumplirse la autorización expresa pedida por AGENTS.md. La derivación manuscrita y la revisión semántica personal son evidencias separadas.
