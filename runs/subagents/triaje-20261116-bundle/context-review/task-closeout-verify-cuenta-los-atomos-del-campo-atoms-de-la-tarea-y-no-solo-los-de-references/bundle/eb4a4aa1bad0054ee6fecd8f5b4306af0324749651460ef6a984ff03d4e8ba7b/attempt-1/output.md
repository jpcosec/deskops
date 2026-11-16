REFORMULACION
Propósito: que la compuerta `atom|materialization` de closeout verify/commit considere como evidencia los ids del campo `atoms` del TaskDoc, además de los `atom-*` de `references`. Resultado: cambio en `/mnt/ssd/proyectos/SLDB_1/deskops` sobre `deskops/services/closeout_gates.py`, `deskops/services/closure.py` y `tests/test_closeout_gates.py`; una tarea con `atoms` y sin `atom-*` en references pasa, y sin evidencia de átomo/materialización sigue fallando. Límites: no cambiar otras compuertas ni el formato del reporte; la compuerta de materialization no cambia; no tocar el status `draft`; tests de Validation fuera de `files` solo si el cambio los rompe legítimamente.

AMBIGUEDADES
1. “closeout verify y de closeout commit” frente a “Unir task.atoms a los atom-* de references al armar la evidencia de atomo”: no fija si el punto de unión es `closeout_reference_evidence` o los consumidores de `reference_evidence['atom']` en `closure.py`; obligaría a inventar la ruta de llamada.
2. “tarea sin ninguno sigue fallando”: puede significar sin `atoms` y sin `atom-*`, o sin átomo ni materialización; obligaría a inventar si el test debe excluir materializations.
3. “solo si el cambio los rompe por una razon legitima”: no define “legítima”; obligaría a inventar el criterio de edición.
4. “falla igual ahí”: no fija cómo comparar la falla con el worktree limpio; obligaría a inventar el criterio de equivalencia.

DRY-RUN
Leería el TaskDoc, la pill, los átomos ligados, `closeout_gates.py`, `closure.py` y los tests nombrados. Cambiaría la construcción de evidencia para concatenar y deduplicar `payload["atoms"]` con los `atom-*` de `references`, y ajustaría `closure.py` para consumir esa evidencia sin alterar materialization. Añadiría los dos casos en `tests/test_closeout_gates.py`. Dependencias: forma real de `TaskDoc.atoms`, helpers actuales y llamadas de closure. Validaría con los tres pytest indicados y la suite completa `-n 4`; ante fallas, ejecutaría el mismo comando en worktree limpio de `origin/main`. Sin ejecutar nada.

FUTURO
Otro nodo implementa y ejecuta pruebas/commit; un humano o la compuerta de cierre decide si las fallas de baseline son aceptables y si el informe basta; el dueño del workflow decide el cambio de `draft`.
