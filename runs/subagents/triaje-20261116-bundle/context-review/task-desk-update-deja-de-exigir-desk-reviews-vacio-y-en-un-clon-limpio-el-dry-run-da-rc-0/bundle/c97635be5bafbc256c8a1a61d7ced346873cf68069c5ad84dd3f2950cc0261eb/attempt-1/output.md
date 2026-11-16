## REFORMULACION
Propósito: eliminar el falso positivo que hace que `deskops desk update` exija `desk/reviews/` aunque sea una carpeta vacía no versionada por git. Resultado: el dry-run deja de listar `desk/reviews/` como estructura faltante y, en un clon limpio tras `deskops init .`, commit y clone, devuelve rc 0; el primer recibo crea la carpeta. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: tocar `deskops/cli/commands/desk.py`, `tests/test_cli.py` y el golden `tests/fixtures/golden/scaffold/update.json` solo si nombra `desk/reviews/`; no añadir `.gitkeep`.

## AMBIGUEDADES
1. Cita: “Verificar que review.py crea desk/reviews al escribir el primer recibo.” Los `files` no incluyen `deskops/services/review.py`. Si la verificación falla, ¿se corrige ese archivo o solo se informa? Obligaría a inventar alcance y archivo modificable.
2. Cita: “la lista de esas fallas va en el informe de la tarea”. No se define formato, ruta ni nombre del informe. Obligaría a inventar el artefacto de cierre.
3. Cita: “test con git init, init, commit, clone”. No aclara si `.sldb` debe quedar versionado en el commit; sin store en el clon, el rc 0 podría depender de otro estado. Obligaría a inventar el setup del store.

## DRY-RUN
Lecturas: bloque `missing_desk_files` de `desk.py`, `review.py`, `tests/test_cli.py`, golden `update.json` y tests de goldens/review. Cambios previstos: quitar el `if` que añade `desk/reviews/`; actualizar el golden eliminando `desk/reviews/` de “Missing desk structure”; añadir test con `tmp_path`, `git init -b main`, `deskops init`, commit, clone y `deskops desk update --root <clon>` sin `--apply`, esperando rc 0; comprobar que el primer recibo crea la carpeta. Dependencias: git, pytest, venv y fixtures. Validaciones futuras: los cuatro comandos del TaskDoc, incluida la suite completa con `-n 4` y comparación de fallas en worktree de `origin/main`.

## FUTURO
Un nodo ejecutor implementará los cambios y correrá las validaciones; un humano decidirá si acepta fallas preexistentes y aprobará el cierre/commit. El informe de la tarea lo producirá el ejecutor.
