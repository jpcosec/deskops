REFORMULACION
Propósito: que `deskops closeout verify --task <id> --run-dir <dir>` anticipe el fallo de `closeout commit --run-dir` cuando falta evidencia en el run-dir. Resultado: `--run-dir` opcional en verify; si se entrega, `ok:false` y reporte de cada archivo de `REQUIRED_EVIDENCE` ausente, con el mismo texto que usa commit; sin `--run-dir`, comportamiento actual. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no cambiar la evidencia que exige commit ni el JSON fuera del nuevo hallazgo; tocar `closeout.py`, `closure.py`, el golden de ayuda y los tests indicados. Es una tarea ejecutable de código, no un agregado ni paquete.

AMBIGUEDADES
1. “reporta como falla (ok:false) cada archivo de REQUIRED_EVIDENCE que falte en el run-dir, con el mismo texto que usa commit” frente a “'Missing required evidence in <run_dir>: <archivos separados por coma>'”. ¿Un finding por archivo o uno solo con la lista? ¿Qué `code` y campos? Obliga a inventar el esquema del hallazgo.
2. “el mismo texto que usa commit” y “archivos separados por coma” no fijan separador exacto ni orden. Obliga a inventar `", "` frente a `","` y el criterio de orden.
3. “Sin --run-dir, verify se comporta igual que hoy” no aclara si con `--run-dir` sigue escribiendo receipts ni si el chequeo ocurre antes o después. Obliga a inventar orden y efectos.
4. “cada archivo de REQUIRED_EVIDENCE que falte en el run-dir” no aclara si un run-dir inexistente equivale a que faltan todos. Obliga a inventar el manejo del directorio ausente.

DRY-RUN
Lecturas previstas: `closure.py` (`REQUIRED_EVIDENCE`, chequeo de commit, `verify_task_closeout`), `closeout.py` (parser de verify), `tests/test_closeout_declared_evidence.py`, golden de ayuda y tests de goldens/help. Cambios previstos: extraer `missing_run_evidence(run_dir)`, usarlo en commit y verify; añadir `--run-dir` al parser de verify; actualizar golden; agregar casos incompleto, completo y sin flag. Dependencias: `ClosureService`, `DeskopsOperations`, pytest, venv y worktree de `origin/main`. Validaciones futuras: ejecutar los cinco comandos listados; repetir fallas en worktree limpio y registrar solo las preexistentes. No se ejecuta nada aquí.

FUTURO
Otro nodo implementa helper, parser, tests y golden, y entrega un commit descriptivo. Un humano valida el contrato observable del reporte y la aceptación de fallas preexistentes. `closeout commit`/verify producen la evidencia y el registro de cierre.
