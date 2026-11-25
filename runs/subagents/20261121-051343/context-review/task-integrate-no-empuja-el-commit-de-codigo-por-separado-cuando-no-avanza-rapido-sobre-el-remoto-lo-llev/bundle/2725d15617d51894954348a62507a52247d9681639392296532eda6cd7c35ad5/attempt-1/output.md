## REFORMULACION

**Propósito:** corregir el paso de push de `integrate` para que no empuje por separado un commit de código que no avanza rápido sobre el remoto cuando el tip sí lo hace. **Resultado:** en `deskops/integrate.py` (`_steps`, ~línea 347) la lista de pushes incluye `git push origin <code>:<branch>` solo si el commit no está en `remote_ref` y `remote_ref` es ancestro de `code`; en caso contrario se omite y se imprime `código va con el tip: <code corto>`, llevándolo el push del tip. **Repo:** deskops (`tests/test_integrate.py`, CHANGELOG). **Límites:** dentro solo `integrate.py`, tests y CHANGELOG; fuera el resto. Es un `task.code` hoja, no un agregado: no hay hijos que recorrer.

## AMBIGUEDADES

1. «el remoto queda en el tip y contiene el commit de código» — no fija cómo comprobarlo (¿`git merge-base --is-ancestor`, `git branch --contains`?); obligaría a inventar la aserción.
2. «reusando el escenario de test_tip_extends_over_a_merge_of_the_remote_branch» — no dice si extraer fixture/helper o duplicar; obligaría a inventar un refactor.
3. «'código va con el tip: <code corto>'» — no define longitud de «corto» ni canal (stdout/log); obligaría a inventar el formato.
4. «CHANGELOG» — no indica archivo ni formato de entrada; obligaría a inventar ambos.
5. «El caso normal (el código avanza rápido) no cambia» — no dice si añadir test de no regresión; obligaría a inventar cobertura.

## DRY-RUN

Sin ejecutar. **Lecturas:** `integrate.py` (`_steps`, `code_in_origin`, lista de pushes), `tests/test_integrate.py` (escenario citado) y CHANGELOG. **Cambios previstos:** p1 test nuevo que falla antes; p2 condición con `git merge-base --is-ancestor remote_ref code` en la copia y mensaje; p3 CHANGELOG y commit `git commit -- <rutas>` con trailer `Task-Id:`. **Dependencias:** remoto bare del fixture y worktree que entrega dispatch. **Validación futura:** `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py`.

## FUTURO

Dispatch entrega el worktree; el Board enruta rituales; un humano revisa/mergea; el commit incorpora `Task-Id`. No son ambigüedades.
