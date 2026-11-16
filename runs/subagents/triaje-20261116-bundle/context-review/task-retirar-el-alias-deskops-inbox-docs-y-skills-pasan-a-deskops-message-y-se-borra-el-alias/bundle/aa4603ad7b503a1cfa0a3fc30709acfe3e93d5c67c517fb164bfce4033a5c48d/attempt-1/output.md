## REFORMULACION
El nodo es ejecutable, no agregado. Propósito: retirar el alias deprecado `deskops inbox` y dejar `deskops message` como única superficie documentada. Resultado: ningún documento o skill versionado usa el alias; el alias, su ayuda, goldens y tests desaparecen; las validaciones pasan. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: entran `deskops/cli/registry.py`, `docs/operator-manual.md`, `docs/faq.md`, la skill `.claude/skills/deskops-workflow` y tests/goldens; quedan fuera `.pi/skills` y cualquier cambio de datos reales del desk.

## AMBIGUEDADES
1. «El alias, sus goldens de ayuda y sus tests desaparecen» y «los que lo listen como comando»: el bundle no enumera todos los goldens ni casos exactos; obligaría a inventar el inventario.
2. Los docs describen la gramática del alias: «Its flag grammar (`--list`, `--show`, `--ack`) still works», pero el input solo da el reemplazo de `send`; obligaría a inventar si se borran esos párrafos o se traducen a `message list/read/ack`.
3. «deskops/data/faq.md si lo nombra» y «README.md si el grep los muestra»: no hay contenido ni listado de esos archivos; obligaría a inventar si existen y qué contienen.
4. «.opencode/» aparece en scope y validación, pero no en `files` ni en el bundle; obligaría a inventar qué archivo concreto editar.

## DRY-RUN
Lecturas: TaskDoc, `registry.py`, `docs/operator-manual.md`, `docs/faq.md`, `SKILL.md`, `references/deskops-cli.md`, `references/vocabulary.md`, tests de mensajes y goldens de ayuda. Ejecutaría `grep -rnw 'deskops inbox'` sobre el alcance indicado. Cambios previstos: reescribir menciones documentales a `deskops message send`; quitar el registro/alias y su aviso de deprecado; eliminar casos de test que invocan el alias; borrar o regenerar goldens que lo listan. Dependencias: conocer la definición exacta del alias, el harness de goldens y usar roots sandbox para mutaciones CLI. Validaciones futuras: los seis comandos del TaskDoc, regeneración de goldens, suite completa y comparación de fallas en worktree limpio de `origin/main`.

## FUTURO
Un ejecutor aplicará los cambios y correrá las validaciones; un humano decidirá los puntos ambiguos tras el grep (incluidos `.opencode`, `README.md` y `deskops/data/faq.md`). El cierre requiere tests, commit descriptivo e informe de fallas preexistentes.
