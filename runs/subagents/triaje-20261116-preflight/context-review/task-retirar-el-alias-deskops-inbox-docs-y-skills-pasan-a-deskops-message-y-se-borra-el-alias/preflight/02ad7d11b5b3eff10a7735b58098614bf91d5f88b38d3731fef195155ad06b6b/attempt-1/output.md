REFORMULACION
El nodo debe retirar el alias `deskops inbox` del repo `/mnt/ssd/proyectos/SLDB_1/deskops`. Resultado esperado: ningún doc ni skill versionado usa ese alias; el alias, sus goldens de ayuda y sus tests desaparecen; `deskops inbox` falla como comando desconocido. Límites: tocar `deskops/cli/registry.py`, `docs/operator-manual.md`, `docs/faq.md`, `deskops/data/faq.md` si corresponde, `.claude/skills/deskops-workflow/**`, goldens de ayuda y los tests indicados. Excluye `.pi/skills`. Es un TaskDoc ejecutable, no un agregado.

AMBIGUEDADES
1. “pasan a `deskops message`” frente a “Reescribir con `deskops message send`”: obliga a inventar si el reemplazo es el comando padre o el subcomando `send`, y cómo mapear argumentos/opciones existentes.
2. “`deskops/data/faq.md` si lo nombra”: obliga a decidir si se modifica solo al aparecer el alias, aunque no figura en `files`.
3. “goldens de ayuda” y “Regenerar goldens”: no se enumeran rutas ni comando de regeneración; obliga a descubrirlos e inventar el procedimiento.
4. “tests/test_message_cli.py y tests/test_message_delivery.py (casos de alias)”: no se identifican los casos exactos; obliga a decidir qué borrar o reescribir.
5. “grep -rn 'deskops inbox ' docs .claude .opencode deskops/data README.md” usa espacio final e incluye `.opencode` y `README.md`, ausentes del Scope/`files`; obliga a fijar superficie y patrón (podría omitir alias al final de línea o con puntuación).
6. “sin fallas nuevas respecto de main”: no define cómo obtener/comparar la línea base; obliga a inventar el mecanismo de comparación.

DRY-RUN
Lecturas: TaskDoc, `registry.py` junto al alias, líneas citadas de docs/skills, tests y goldens localizados por búsqueda. Cambios previstos: reescribir referencias al alias conservando ejemplos; eliminar el registro del alias; ajustar/borrar casos de alias; regenerar goldens. Dependencias: `depends_on` vacío; repo, entorno `.venv` y búsqueda global. Validaciones futuras: los greps y pytest listados, suite completa y comprobación manual del error de comando desconocido. Sin ejecutar nada.

FUTURO
Un nodo ejecutor producirá el diff y la evidencia de tests; un revisor humano decidirá los límites ambiguos y la aceptación final.
