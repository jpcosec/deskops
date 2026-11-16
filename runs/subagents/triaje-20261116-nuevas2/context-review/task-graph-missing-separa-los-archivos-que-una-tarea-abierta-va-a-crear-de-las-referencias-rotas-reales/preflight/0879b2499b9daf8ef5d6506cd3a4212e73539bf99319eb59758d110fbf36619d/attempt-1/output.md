## REFORMULACION
El nodo debe modificar `deskops` para que `graph missing` clasifique como `informational`/`planned_target` los destinos inexistentes citados por TaskDocs abiertos, en lugar de listarlos como `missing`. Resultado: salida separada y resumen `N missing, M informational (P planned_target)`, manteniendo visibles los `planned_target`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no cambiar `SOURCE_PATH` ni el extractor, no ocultar rutas, no reescribir evidencia; el estado sale del frontmatter (ausente/desconocido = abierto) y el tipo, del `kind` del nodo.

## AMBIGUEDADES
1. “`tests/test_graph_checks.py`” figura en alcance, pero la validación incluye “`tests/test_graph_cli.py`”. Obliga a inventar si este último debe modificarse o solo ejecutarse.
2. “`planned_target` va en el campo `kind` del hallazgo, con el mismo `reason`”. No explicita el valor de `reason`; obliga a inferir que conserva `missing_declared_target`.
3. “La salida dice cuantos son de cada tipo.” No aclara si “tipo” abarca `missing`/`informational`/`planned_target` o también `source_file`/`test_file`/`doc`.

## DRY-RUN
Lecturas previstas: `deskops/graph/checks.py`, `deskops/cli/commands/graph.py`, `tests/test_graph_checks.py` y, si aplica, `tests/test_graph_cli.py`. Cambios previstos: localizar `MISSING_TARGET_KINDS`/`informational`; clasificar por estado del TaskDoc origen; emitir `planned_target`; ajustar resumen y tests. Dependencias: `kind` del nodo y `status` del frontmatter ya disponibles. Validaciones futuras: los tres `pytest` indicados, `deskops graph missing --root .`, suite completa y comparación de fallas en worktree limpio de `origin/main`. Nada se ejecuta ahora.

## FUTURO
Otro nodo ejecutará la implementación y las pruebas; CI o un revisor verificará el cierre y un humano decidirá la aceptación del informe, incluidas las fallas preexistentes documentadas.
