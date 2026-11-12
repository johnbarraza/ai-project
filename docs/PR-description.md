# Preparar la final macro con paper propio y prueba Lean local

La final anterior conservaba el ejemplo de la plantilla y el paper no contenía el argumento del proyecto. Esta versión presenta la economía de agentes heterogéneos, su distribución, el circuito de mercados y el mecanismo laboral condicional, con figuras reproducibles y límites explícitos.

Incluye 24 láminas principales y 8 de consulta; un borrador de paper de 9 páginas de cuerpo; prueba propia de la derivada y sus signos comprobada localmente en Lean; guion de 30 minutos, matriz de cumplimiento y guía para las hojas personales. Se conservan propuesta, tema y workflow original.

Validación local: `python code/verify.py`; `python code/verify_lean.py --wsl-cache /home/johnb/EconCSLib`; compilación LaTeX/BibTeX de paper y final; 242 enlaces del deck sin destinos inválidos ni desbordamientos; `git diff --check` aprobado. Los diagnósticos GE se releen de exportaciones, sin nueva simulación MATLAB. El ensayo oral no se ha observado.

Pendientes declarados: flujo oficial AppliedModelingLib sobre el paper publicado en commit, revisión semántica del autor y fotos manuscritas que el estudiante indicó que hará después. La precisión numérica global continúa abierta. Esta publicación fija una versión de trabajo; no declara terminado el paper ni la formalización oficial.
