# Encargo del tester deskops-t-16e62e0d9f56 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas código, tests ni .sldb, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-deskops-quita-el-enlace-federado-al-store-de-spec2viz-de-su-sldb-g5-opcion-b-de-jp` (contrato: `deskops show task <id> --root .`). Las precisiones del coordinador de los motivos de los recibos preflight-1 y bundle-1 (desk/reviews/task-deskops-quita-el-enlace-federado-al-store-de-spec2viz-de-su-sldb-g5-opcion-b-de-jp/) son parte del contrato.
Entrega del ejecutor: cambios sin commitear en .sldb/store.yaml y .sldb/core/store_index.yaml (hechos con sldb stores remove spec2viz y sldb stores declare --write), más su evidencia en runs/subagents/exec-deskops-e-e1719ad4ee0d/ (result-summary.md, validation.log, antes-*.txt y despues-*.txt). No confíes en ese resumen: compruébalo. Ojo: en el checkout hay otros cambios sin commitear de otras sesiones (RunDocs, ReviewDocs, notas de inbox y una TaskDoc); no son de esta tarea.

1. Lee `git diff -- .sldb/store.yaml .sldb/core/store_index.yaml`: el enlace spec2viz (../spec2viz/.sldb) desaparece de los dos, los enlaces sldb, pron y scion quedan iguales y lo demás del diff son solo líneas include de RunDoc o store_hash.
2. Comprueba: `sldb stores list --store .sldb` sin spec2viz; `grep -rn '../spec2viz' .sldb` sin coincidencias; `sldb stores check --store .sldb`, `deskops doctor --root .` y `deskops graph missing --root .` sin hallazgos nuevos frente a los antes-*.txt del ejecutor (compara por conjunto de líneas).
3. Que una sesión sldb que abre este store ya no lea el store real de spec2viz: carga el store (por ejemplo con la API de sldb o `sldb stores list`/`sldb query`) y verifica que ningún documento ni modelo venga de ../spec2viz/.sldb. Si puedes, mide los archivos abiertos bajo ../spec2viz durante esa carga (por ejemplo con strace -f -e trace=openat, si está disponible) y anota el conteo.
4. Corre tú, de a un archivo y sin lock (`cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`): test_migrate_desk_stores.py, test_doctor_model_registration.py, test_desk_sync.py, test_doctor_absolute_paths.py.
5. Juzga el hallazgo del ejecutor (stores remove no actualiza store.yaml; hizo falta stores declare --write): ¿queda el store coherente y estable?
6. NO corras la suite completa ni stores build --check (orden del integrador wA:p1).

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, `sldb stores remove|declare|add` y cualquier escritura en .sldb, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-16e62e0d9f56/ y /dev/shm, y limpia lo tuyo en /dev/shm.

## Evidencia (en runs/subagents/test-deskops-t-16e62e0d9f56/)

- `validation.log`: cada comando con su salida y rc.
- `verdict.md`: veredicto `APROBADO` o `RECHAZADO`, con hallazgos y riesgos.
- Tu última línea en la conversación: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
