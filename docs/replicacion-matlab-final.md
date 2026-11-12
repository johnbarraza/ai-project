# Repetición MATLAB para la entrega, 12nov2026

Se ejecutó MATLAB R2025b Update2 y se resolvieron de nuevo dos GE de la presentación: referencia y ambas cuñas constantes reajustadas a los momentos internos. Ambos usan400nodos de activos,40de productividad y dominio de activos−1a40, con una copia idéntica del motorD73 y los resultados anteriores como inicializadores. No se cambiaron las ecuaciones ni se adoptó una especificación nueva.

La auditoría independiente en Python pasó masa/positividad, generador, HJB, KFE, clase cerrada única, FOC interiores, tiempo, mercados, gobierno, beneficios y cierre de recursos con ambos pagos de cuñas. También verificó la integridad del motor y las fuentes protegidas. En referencia, precios y momentos coinciden hasta redondeo de máquina; en el reajuste las diferencias absolutas son1,36e−10 en r,6,51e−9 en pI,2,06e−8 en K y como máximo1,43e−8 en M1/M3/V3.

El [export público](../code/data/final_matlab_replication.json) conserva los hashes de los MAT nuevos y anteriores, diagnósticos, diferencias y límites de comparación fijados antes de leerlas. `code/verify.py` liga esa evidencia a los casosD73 graficados. Este script no ejecuta MATLAB enCI. Los MAT completos permanecen locales; la copia de trabajo y el script de auditoría están en `modeling_jb/flujo/reportes/matlab-final-2026-11-12`.

Las figuras conservan las cifrasD73 del9nov; las dos repeticiones respaldan su reproducción sobre la misma grilla. Esto no es un estudio nuevo de refinamiento o truncamiento de productividad. La certificación global de precisión sigue pendiente. La sesión MATLAB del usuario quedó abierta, en su carpeta original y sin candado activo.
