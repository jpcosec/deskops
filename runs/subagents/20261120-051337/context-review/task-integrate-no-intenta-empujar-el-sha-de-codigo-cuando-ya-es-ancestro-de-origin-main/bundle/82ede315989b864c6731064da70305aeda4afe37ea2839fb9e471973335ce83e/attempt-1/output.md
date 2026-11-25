## REFORMULACION

Encargo de planificación (no ejecución) de un cambio en el repo deskops, archivo `deskops/integrate.py`: que el integrate omita el push del SHA de código cuando ya es ancestro de `origin/main`, lo informe como `código ya en origin: <sha>` y continúe con suite, checks y push de la punta; si no es ancestro, todo sigue igual. Resultado: test que falla antes y pasa después, cambio en el paso de push, CHANGELOG y commit con rutas nombradas y Task-Id. Límites: solo integrate.py, su test y CHANGELOG; fuera el resto de integrate.

## AMBIGUEDADES

1. «`git merge-base --is-ancestor <sha> origin/<branch>` después del fetch» frente a «ancestro de origin/main»: no fija la rama base; obligaría a inventar `<branch>`.
2. «deskops/integrate.py (el paso de push) y su test»: hay dos pushes (sha y punta) y no precisa cuál paso se modifica ni cómo distinguirlo.
3. «lo informa ('código ya en origin: <sha>')»: no indica canal (print, log, retorno) ni formato exacto; obligaría a inventar la interfaz de salida.
4. «y su test»: no nombra archivo; la validación cita `tests/test_integrate.py`, pero no afirma que sea ese; obligaría a inventar la ruta.
5. «después del fetch»: no dice qué fetch ni si el chequeo precede al push del sha; obligaría a inventar orden y fuente remota.
6. «la suite completa la corre integrate»: no aparece en Validation (solo `tests/test_integrate.py`); obligaría a inventar quién ejecuta la suite.

## DRY-RUN

Lecturas: `integrate.py`, `tests/test_integrate.py`, CHANGELOG. Cambios previstos: test con repo temporal cuyo remoto ya contiene el commit; implementar check `merge-base --is-ancestor` tras fetch con rama de salto y mensaje; entrada de CHANGELOG; commit con rutas y Task-Id. Dependencias: git, pytest, remoto temporal. Validaciones futuras: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py`, luego suite completa; comprobar mensaje y push de punta.

## FUTURO

El nodo ejecutor implementa y corre los tests; CI o la suite completa valida; un humano revisa CHANGELOG y hace merge; el Board transiciona el nodo.
