## REFORMULACION

Encargo ejecutable (nodo `task.code`, no agregado): en el host robocop2, verificar 6 desks —deskops, sldb, spec2viz, scion, pron y graph_ui (este en `UIs/graph_ui`) bajo `/mnt/ssd/proyectos/SLDB_1/<repo>`— ejecutando por desk `deskops desk update` en dry-run, `deskops doctor`, `deskops view board`, `sldb stores check` y `sldb rules check`, registrando rc y resumen. Resultado: tabla en la sección "Verificacion" de `docs/config-vs-code.md` y en el TaskDoc, con esos datos y con los tiempos de `deskops view board --root .` en el desk de deskops (3 corridas frías borrando `.sldb_cache` y `${XDG_CACHE_HOME:-$HOME/.cache}/sldb` antes de cada una, y 3 en caliente; medianas, caliente < 1 s). Además, suites completas de deskops y sldb con `-n 4` sin fallas nuevas contra main. En deskops puede aplicarse `--apply` si el dry-run lo pide y corregir código delatado, cada arreglo en commit con test. En los 5 desks ajenos solo lectura; hallazgos se envían por `deskops message send --to <repo>`. Fuera de alcance: arreglar desks ajenos y la UI en navegador.

## AMBIGUEDADES

1. "sin fallas nuevas contra main": no define baseline ni método de comparación; obligaría a inventar cómo obtener/registrar el estado de main.
2. "3 en caliente": no define si hay corrida de calentamiento previa ni orden exacto; obligaría a inventar el protocolo.
3. "desk update (dry-run, sin --apply en desks ajenos)" vs. "en deskops, desk update --apply si el dry-run lo pide": no aclara si el `--apply` en deskops es obligatorio, opcional o condicionado; obligaría a inventar el criterio.
4. "un resumen": formato y campos del resumen no especificados.
5. "graph_ui en UIs/graph_ui": no fija la ruta absoluta ni el identificador para `message send --to`.
6. "arreglos de codigo que la verificacion delate": alcance abierto; obligaría a decidir qué fallo amerita parche.

## DRY-RUN

Lecturas: TaskDoc, `desk/drawer/plans/deskops-como-config/dag.yaml`, `docs/config-vs-code.md`, `tests/`. Cambios previstos: sección de tabla y tiempos en el doc; actualización del TaskDoc; commits con test por arreglo en deskops; mensajes a inbox de desks ajenos. Dependencias: `../.venv`, binarios `deskops`/`sldb`, `/usr/bin/time`, `TMPDIR=/dev/shm`, cachés borrables. Validaciones futuras: pytest `-n 4` en deskops y sldb, bucle de tiempos con mediana < 1 s, revisión de tabla completa.

## FUTURO

Decisión humana/otro nodo: aceptar o rechazar `--apply` en deskops, definir baseline de main y validar cierre tras recibir respuestas de los desks notificados.
