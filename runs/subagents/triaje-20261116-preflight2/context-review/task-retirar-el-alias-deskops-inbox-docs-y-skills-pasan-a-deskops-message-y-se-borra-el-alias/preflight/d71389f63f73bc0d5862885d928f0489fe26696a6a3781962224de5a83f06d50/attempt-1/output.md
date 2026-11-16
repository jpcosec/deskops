## REFORMULACION

Encargo: eliminar por completo el alias CLI `deskops inbox` del repo deskops (`/mnt/ssd/proyectos/SLDB_1/deskops`). Resultado: ningún doc/skill versionado lo menciona; el alias, sus goldens de ayuda y sus tests desaparecen. Superficie: `deskops/cli/registry.py`, `docs/operator-manual.md`, `docs/faq.md`, `deskops/data/faq.md`, `.claude/skills/deskops-workflow/` (SKILL.md y references), goldens de ayuda, `tests/test_message_cli.py`, `tests/test_message_delivery.py`; condicionalmente `.opencode/` y `README.md`. Reemplazo indicado: `deskops inbox "<texto>" --kind K --root .` → `deskops message send "<texto>" --kind K --root .`. Fuera: `.pi/skills`. Límite: no hay más contexto; las condiciones del input se resuelven con grep.

## AMBIGUEDADES

1. «El patron de busqueda es grep -rnw 'deskops inbox'» frente a «grep -rn 'deskops inbox' docs .claude…»: distinto alcance/opción; obliga a inventar cuál grep define el cierre.
2. «deskops/data/faq.md si lo nombra» y «.opencode/ y README.md si el grep los muestra»: el ejecutor debe inventar si son versionados/editables o generados.
3. «los que lo listen como comando»: no se enumeran los goldens; obliga a inventar el conjunto exacto.
4. «regenerados con pytest --update-golden»: no consta que ese flag exista; obliga a inventar el mecanismo.
5. «Sin fallas nuevas… solo se acepta si falla igual ahí»: no define umbral ni qué informe; obliga a inventar formato y criterio de comparación.
6. «casos de alias»: no delimita si se borran tests completos o casos; obliga a inventar.

## DRY-RUN

Lecturas: los ocho ficheros listados y goldens bajo `tests/fixtures/golden/help`. Cambios: reescribir menciones a `message send`; borrar entrada del alias en `registry.py`; borrar casos de alias; regenerar goldens. Dependencias: venv `../.venv`, pytest, worktree base `origin/main`, mecanismo golden. Validaciones futuras: grep vacío, cinco suites dirigidas, suite completa y comparación de fallas en worktree limpio; informe final.

## FUTURO

El ejecutor entrega informe de fallas preexistentes y commit; un humano revisa el diff y aprueba; el agregado del drawer comprueba que no quedan caminos legacy.
